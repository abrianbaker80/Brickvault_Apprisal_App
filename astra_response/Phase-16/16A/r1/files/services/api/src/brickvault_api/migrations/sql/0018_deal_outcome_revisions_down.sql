DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM public.deal_outcome_revision) THEN
        RAISE EXCEPTION 'outcome_history_prevents_downgrade' USING ERRCODE='23514';
    END IF;
END $$;
-- statement-break
DROP TABLE public.deal_outcome_revision;
-- statement-break
DROP FUNCTION public.deal_outcome_revision_guard();
