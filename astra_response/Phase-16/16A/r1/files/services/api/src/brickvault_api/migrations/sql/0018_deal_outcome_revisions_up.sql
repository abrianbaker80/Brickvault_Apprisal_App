CREATE TABLE public.deal_outcome_revision (
    id uuid PRIMARY KEY,
    owner_id uuid NOT NULL REFERENCES public.auth_principal(id) ON DELETE RESTRICT,
    root_forecast_id uuid NOT NULL,
    revision integer NOT NULL CHECK (revision>=1),
    recorded_at timestamptz NOT NULL DEFAULT public.forecast_clock(),
    correction_reason text,
    actuals jsonb NOT NULL,
    results jsonb NOT NULL,
    UNIQUE (owner_id,root_forecast_id,revision),
    FOREIGN KEY (root_forecast_id,owner_id)
        REFERENCES public.deal_forecast(id,owner_id) ON DELETE RESTRICT,
    CHECK (correction_reason IS NULL OR char_length(btrim(correction_reason)) BETWEEN 1 AND 500),
    CHECK (revision=1 OR correction_reason IS NOT NULL),
    CHECK (jsonb_typeof(actuals)='object' AND octet_length(actuals::text)<=16384),
    CHECK (jsonb_typeof(results)='object' AND octet_length(results::text)<=16384)
);
-- statement-break
REVOKE ALL ON public.deal_outcome_revision FROM PUBLIC;
-- statement-break
CREATE FUNCTION public.deal_outcome_revision_guard() RETURNS trigger LANGUAGE plpgsql
SET search_path=pg_catalog,public AS $$
DECLARE n timestamptz; session_token text; auth_until timestamptz;
        previous_revision integer; previous_at timestamptz; valid_session boolean;
BEGIN
    IF TG_OP<>'INSERT' THEN
        RAISE EXCEPTION 'OUTCOME_IMMUTABLE' USING ERRCODE='23514';
    END IF;
    PERFORM pg_advisory_xact_lock(hashtextextended(NEW.owner_id::text,16));
    n=public.forecast_clock();
    session_token=NULLIF(current_setting('brickvault.outcome_session',true),'');
    auth_until=NULLIF(current_setting('brickvault.outcome_auth_until',true),'')::timestamptz;
    SELECT EXISTS (
        SELECT 1 FROM public.auth_session s
        WHERE s.token_hash=session_token AND s.principal_id=NEW.owner_id
          AND s.revoked_at IS NULL AND n>=s.last_activity_at AND n<s.expires_at
          AND n<auth_until
    ) INTO valid_session;
    IF NOT valid_session THEN
        RAISE EXCEPTION 'OUTCOME_UNAUTHORIZED' USING ERRCODE='23514';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM public.deal_forecast f
        WHERE f.id=NEW.root_forecast_id AND f.owner_id=NEW.owner_id
          AND f.saved_at IS NOT NULL AND f.root_id IS NULL AND f.parent_id IS NULL
    ) THEN
        RAISE EXCEPTION 'OUTCOME_ROOT_INVALID' USING ERRCODE='23514';
    END IF;
    SELECT revision,recorded_at INTO previous_revision,previous_at
        FROM public.deal_outcome_revision
        WHERE owner_id=NEW.owner_id AND root_forecast_id=NEW.root_forecast_id
        ORDER BY revision DESC LIMIT 1;
    IF NEW.revision<>COALESCE(previous_revision,0)+1 THEN
        RAISE EXCEPTION 'OUTCOME_CONFLICT' USING ERRCODE='23514';
    END IF;
    NEW.recorded_at=GREATEST(n,previous_at+interval '1 microsecond');
    RETURN NEW;
END $$;
-- statement-break
REVOKE ALL ON FUNCTION public.deal_outcome_revision_guard() FROM PUBLIC;
-- statement-break
CREATE TRIGGER deal_outcome_revision_guard
BEFORE INSERT OR UPDATE OR DELETE ON public.deal_outcome_revision
FOR EACH ROW EXECUTE FUNCTION public.deal_outcome_revision_guard();
