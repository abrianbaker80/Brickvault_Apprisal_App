# Plan 106 — Phase 14C small retrieval quality gate

## Goal and user-visible outcome

One frozen sample measures exact top-1/3/8 retrieval, reciprocal rank within the
eight-candidate shortlist, coverage and truncation for the accepted 14B baseline.

## Why now

Brian accepted 14B r1. Its ten files are checkpointed locally as
44a1e15bc0d45f996d3eb6898534cd2f202ca275 without rerunning foundation checks.
Qualitative usefulness precedes any new verification or embedding infrastructure.

## In scope

Fresh visible descriptions from the approved G01/G02/G03/G05 photos; separate
corpus-availability audit of all 17 confirmed 14A identities. No extra examples are
manufactured to reach the suggested 6–10 scoreable cases. Four frozen queries and
one existing guarded development read-only lifecycle; three scoring/integrity fixtures.

## Explicit non-goals

No provider calls, paid inference, embeddings, tuning, new images/references,
crosswalks, migrations, production, browser smoke, broad tests or 14A/14B reruns.

## Current repository state

14C baseline: 44a1e15bc0d45f996d3eb6898534cd2f202ca275. Main remains unpushed;
14C changes remain uncommitted with empty index. Three protected files stay intact.
Phase 14A CLOSED; 14B ACCEPTED / CLOSED; wider Phase 14 IN PROGRESS.

## Decisions and assumptions

- Freeze private query bytes/hash before ranked results; separately retain confirmed
  label bytes/hash and their prepared-source hash. Ground truth is never a query input.
- Exclude listing/placard text, IDs, names, filenames, earlier predictions and reviewer
  conclusions. Describe visible colors, object type and construction only.
- Score exact kind/namespace/identifier when present in the native snapshot or the
  three-reference corpus. Missing corpus/mapping is unscoreable, never a retrieval miss.
- G05 is curated-reference evidence, not independent image/reference coverage.
- RR@8 is zero if absent from the retained top eight; full-corpus rank is unknown.
- Use Brian's predeclared qualitative USEFUL / PARTIAL / NOT USEFUL rule; no new
  numerical pass threshold. Preserve all 14A scores and unresolved mappings.

## Data model and interface changes

Small evaluation-only models/helpers and scripts/evaluate_retrieval.py reuse the
unchanged 14B retriever/lifecycle. Private hash-bound inputs, admission marker and
ranked outputs stay local; public results contain case codes/metrics only.

## Implementation sequence

1. Commit exact accepted 14B inventory after closeout-only checks.
2. Freeze descriptions; separately bind confirmed labels, corpus and baseline.
3. Validate the harness with three fixtures and affected lint/types.
4. Admit one evaluation; retain per-case ranks and coverage, then stop.
5. Publish sanitized r1 evidence; leave application changes uncommitted.

## Validation and acceptance

Three fixtures check exact-key/rank boundaries, absent-corpus denominator separation,
and independent query/truth integrity. No repeat of the six 14B cases. One guarded
read-only evaluation returns development to its initial stopped state.

## Security, privacy and integrity

Use existing protected-folder/read/write helpers. An exclusive run-started marker
refuses repeats, including interrupted runs. No private query, figure ID, photo,
credential or asset path enters the public review. No ledger/reservation changes.

## Failure modes, rollback and recovery

Changed frozen bytes, unexpected scoreable identity without a query, or snapshot
drift stops before ranking. Retain incomplete evidence; no automatic rerun. Weak
results do not authorize a ranking change. No cleanup/reset of unrelated work.

## Progress log

- [x] 2026-10-06: 14B checkpoint and separate four-query freeze completed.
- [x] Three fixtures passed (0.39 seconds); affected Ruff and strict mypy passed.
  A test import-order correction needed no foundation-test rerun.
- [x] One four-query evaluation; development verified stopped before and after.
- [x] Sanitized result and disposition prepared for astra-response 14C/r1.

## Open questions and manual checks

The scored sample may be below six because reusable independently confirmed,
visible examples are limited. Further independent examples require a separate slice.

## Outcome and follow-up

**READY FOR PHASE 14C RETRIEVAL QUALITY REVIEW.** Four identities scoreable, thirteen
unscoreable because corpus/mapping is absent. Exact top-1/3: 0/4; top-8: 1/4, the
curated G05 reference at rank 7. All four searches truncated. Disposition:
**NOT USEFUL** for this sample; no source defect or ranking optimization pursued.

The three set shortlists contained only minifigures. The sole external-ID hit remains
canonically unresolved and does not prove hidden-part uniqueness. The sample is
smaller than suggested; there are no added independent catalog examples. Detailed
sanitized ranks/coverage and the checkpoint receipt are in the 14C/r1 review package.

This is description-assisted feasibility evidence only; image-only/general
recognition, production minifigure accuracy, canonical crosswalk completeness and
AI-verification accuracy remain unestablished. Phase 14A scores/ledger and 14B
retrieval source remain unchanged. Stop for review; no next slice is authorized.
