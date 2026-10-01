CREATE TABLE public.listing (
    id uuid PRIMARY KEY,
    owner_id uuid NOT NULL REFERENCES public.auth_principal(id),
    source_type varchar(80), source_url varchar(2048), title varchar(512), description varchar(10000),
    asking_price numeric(18,2) CHECK (asking_price>=0),
    currency varchar(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_listing_owner_created ON public.listing(owner_id,created_at DESC,id DESC);
CREATE TABLE public.blob (
    id uuid PRIMARY KEY,
    sha256 varchar(64) NOT NULL UNIQUE CHECK (sha256 ~ '^[a-f0-9]{64}$'),
    storage_key text NOT NULL UNIQUE,
    byte_count bigint NOT NULL CHECK (byte_count>0),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (storage_key='sha256/'||substring(sha256,1,2)||'/'||substring(sha256,3,2)||'/'||sha256)
);
CREATE TABLE public.image_asset (
    id uuid PRIMARY KEY,
    blob_id uuid NOT NULL REFERENCES public.blob(id),
    format varchar(4) NOT NULL CHECK (format IN ('JPEG','PNG','WEBP')),
    width integer NOT NULL CHECK (width BETWEEN 1 AND 16000),
    height integer NOT NULL CHECK (height BETWEEN 1 AND 16000),
    kind text NOT NULL CHECK (kind IN ('original','thumbnail')),
    privacy text NOT NULL CHECK (privacy IN ('private','restricted')),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (blob_id,kind), UNIQUE(id,kind),
    CHECK (width::bigint*height<=40000000)
);
CREATE UNIQUE INDEX ix_image_canonical_original ON public.image_asset(blob_id) WHERE kind='original';
CREATE TABLE public.image_relation (
    id uuid PRIMARY KEY,
    parent_id uuid NOT NULL,
    child_id uuid NOT NULL,
    parent_kind text NOT NULL DEFAULT 'original' CHECK (parent_kind='original'),
    child_kind text NOT NULL DEFAULT 'thumbnail' CHECK (child_kind='thumbnail'),
    transformation_version text NOT NULL CHECK (transformation_version='thumbnail-v1'),
    transformation_metadata jsonb NOT NULL CHECK (jsonb_typeof(transformation_metadata)='object'),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(parent_id,parent_kind) REFERENCES public.image_asset(id,kind),
    FOREIGN KEY(child_id,child_kind) REFERENCES public.image_asset(id,kind),
    UNIQUE(parent_id,transformation_version), CHECK (parent_id<>child_id)
);
CREATE TABLE public.listing_image (
    id uuid PRIMARY KEY,
    listing_id uuid NOT NULL REFERENCES public.listing(id),
    original_asset_id uuid NOT NULL,
    asset_kind text NOT NULL DEFAULT 'original' CHECK (asset_kind='original'),
    display_order integer NOT NULL CHECK (display_order BETWEEN 0 AND 2147483646),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(original_asset_id,asset_kind) REFERENCES public.image_asset(id,kind),
    UNIQUE(listing_id,original_asset_id), UNIQUE(listing_id,display_order), UNIQUE(id,listing_id)
);
CREATE TABLE public.upload_receipt (
    id uuid PRIMARY KEY,
    listing_id uuid NOT NULL REFERENCES public.listing(id),
    client_upload_id uuid NOT NULL,
    filename varchar(255) NOT NULL,
    content_hash varchar(64) NOT NULL REFERENCES public.blob(sha256),
    display_order integer NOT NULL CHECK (display_order BETWEEN 0 AND 2147483646),
    listing_image_id uuid NOT NULL,
    stored_result jsonb NOT NULL CHECK (jsonb_typeof(stored_result)='object'),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_image_id,listing_id) REFERENCES public.listing_image(id,listing_id),
    UNIQUE(listing_id,client_upload_id), UNIQUE(listing_id,display_order),
    CHECK (coalesce(stored_result->>'status' IN ('uploaded','duplicate')
       AND stored_result->>'client_upload_id'=client_upload_id::text
       AND stored_result->>'listing_image_id'=listing_image_id::text
       AND stored_result->>'filename'=filename AND stored_result->'error'='null'::jsonb
       AND stored_result ?& ARRAY['status','client_upload_id','listing_image_id','filename','error'],false))
);
REVOKE ALL ON public.listing,public.blob,public.image_asset,public.image_relation,
    public.listing_image,public.upload_receipt FROM PUBLIC;
-- statement-break
CREATE FUNCTION public.image_record_immutable() RETURNS trigger
LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$
BEGIN
    IF TG_TABLE_NAME='image_asset' AND TG_OP='UPDATE' THEN
        IF (to_jsonb(NEW)-'privacy')=(to_jsonb(OLD)-'privacy')
           AND (NEW.privacy=OLD.privacy OR NEW.privacy='restricted') THEN RETURN NEW; END IF;
    END IF;
    RAISE EXCEPTION 'IMMUTABLE_IMAGE_RECORD' USING ERRCODE='23514';
END $$;
CREATE TRIGGER blob_immutable BEFORE UPDATE OR DELETE ON public.blob
    FOR EACH ROW EXECUTE FUNCTION public.image_record_immutable();
CREATE TRIGGER image_asset_immutable BEFORE UPDATE OR DELETE ON public.image_asset
    FOR EACH ROW EXECUTE FUNCTION public.image_record_immutable();
CREATE TRIGGER image_relation_immutable BEFORE UPDATE OR DELETE ON public.image_relation
    FOR EACH ROW EXECUTE FUNCTION public.image_record_immutable();
CREATE TRIGGER upload_receipt_immutable BEFORE UPDATE OR DELETE ON public.upload_receipt
    FOR EACH ROW EXECUTE FUNCTION public.image_record_immutable();
REVOKE ALL ON FUNCTION public.image_record_immutable() FROM PUBLIC;
-- statement-break
CREATE FUNCTION public.image_receipt_order_check() RETURNS trigger
LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$
DECLARE link_id uuid; link record; minimum_order integer;
BEGIN
    IF TG_TABLE_NAME='upload_receipt' THEN link_id=NEW.listing_image_id; ELSE link_id=NEW.id; END IF;
    SELECT li.display_order,b.sha256 INTO link FROM public.listing_image li
        JOIN public.image_asset a ON a.id=li.original_asset_id
        JOIN public.blob b ON b.id=a.blob_id WHERE li.id=link_id;
    SELECT min(display_order) INTO minimum_order FROM public.upload_receipt WHERE listing_image_id=link_id;
    IF minimum_order IS NULL OR link.display_order<>minimum_order OR EXISTS (
        SELECT 1 FROM public.upload_receipt WHERE listing_image_id=link_id AND content_hash<>link.sha256
    ) THEN RAISE EXCEPTION 'IMAGE_RECEIPT_ORDER_OR_HASH' USING ERRCODE='23514'; END IF;
    RETURN NULL;
END $$;
CREATE CONSTRAINT TRIGGER listing_image_receipt_check AFTER INSERT OR UPDATE ON public.listing_image
    DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.image_receipt_order_check();
CREATE CONSTRAINT TRIGGER upload_receipt_order_check AFTER INSERT ON public.upload_receipt
    DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.image_receipt_order_check();
REVOKE ALL ON FUNCTION public.image_receipt_order_check() FROM PUBLIC;
