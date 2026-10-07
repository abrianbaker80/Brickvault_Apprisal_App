# Plan 107 — Phase 14D kind-partitioned retrieval

## Goal and user-visible outcome

Rank and return up to eight sets and eight minifigures independently, with explicit
no-match per kind and separate comparison sections. Test the starvation hypothesis.

## Why now

Accepted 14C was NOT USEFUL: all three set shortlists contained only minifigures.
This correction follows those observations; its evaluation is a before/after
structural diagnostic, not an independent benchmark.

## In scope

One partition after the existing scoring/sort; rendering and bucket-aware local
review/scoring. Reuse the exact four frozen 14C queries, seventeen labels, snapshot
and references, reading the original files directly. One evaluation; three fixtures.

## Explicit non-goals

No tokenization/weight/bonus/tie/term-cap changes, synonyms, new cases/references,
corpus or resolution changes, provider calls, embeddings, production, migrations,
old-suite reruns or iterative optimization.

## Current repository state

14C's exact six accepted files were committed locally as
7d664487ab436547dfa8293f4359ea4e38e59523, after staged-diff/link/hash checks only.
Use this as the 14D baseline. Main unpushed; 14D uncommitted/index empty; three
protected files remain unstaged/intact. 14A/14B closed; 14C closed/NOT USEFUL.

## Decisions and assumptions

- Produce both kinds for every query without a ground-truth kind input. A label
  selects a bucket only in the scorer after retrieval.
- Preserve all weights, query terms, names, source features and deterministic ties.
- New versioned results expose sets/minifigures. A flat projection contains both
  buckets for note-key compatibility; it is not an overall rank. Legacy saved
  combined results remain readable without rewriting their bytes.
- Keep overall pool/truncation evidence and exact per-kind pool counts. Reported
  truncation remains overall term/type saturation, not inferred per-kind completeness.
- Preserve thirteen unscoreable corpus/mapping identities and original 14C results.

## Data model and interface changes

Local KindBucket result; per-kind report and operator rank selection; bucket-aware
score fields and a separate 14D harness output folder using frozen 14C inputs.
No HTTP/database/14A provider contract changes.

## Implementation sequence

1. Checkpoint exact accepted 14C inventory without requalification.
2. Partition existing scored candidates; update local report/note/scorer.
3. Three targeted fixtures and changed-file Ruff/mypy.
4. Verify original query/truth hashes and run one diagnostic, restoring development.
5. Preserve before/after evidence and publish r1; stop.

## Validation and acceptance

Fixtures: buckets cannot starve; within-kind score/tie order stays unchanged; query
leakage/exact canonical boundaries stay intact. Inspect generated HTML in a fixture;
no browser smoke required. One guarded read-only development evaluation.

## Security, privacy and integrity

Existing private ACL/exclusive writes and hash guards; original 14C inputs/results
read directly, never edited or regenerated. No private queries, figure IDs, photos,
credentials or asset paths published. Ledger/reservations remain closed and intact.

## Failure modes, rollback and recovery

Bad hashes/snapshot/config stop; interrupted run retained without retry. Empty bucket
does not borrow another kind's candidates. Poor results do not authorize tuning.
Removing local changes requires Brian's instruction; no unrelated cleanup/reset.

## Progress log

- [x] 2026-10-06: Accepted 14C checkpoint; 14D structural changes prepared.
- [x] Three focused fixtures passed; one bonus expectation corrected and that fixture
  rerun alone (0.33 seconds). Changed-file Ruff and strict mypy passed on six files.
- [x] Original query/truth/registry hashes and unchanged scoring/search AST verified.
  One diagnostic completed; owned development stopped before/after.
- [x] Before/after result and disposition prepared for 14D/r1 publication.

## Open questions and manual checks

Single curated figure evidence cannot establish production accuracy or hidden-part
uniqueness. If set top-eight recovery remains poor, image-driven retrieval is the
next separate decision; no further text-ranking optimization follows here.

## Outcome and follow-up

**READY FOR PHASE 14D STRUCTURAL RETRIEVAL REVIEW.** Disposition: **STILL NOT USEFUL**.
Every query now returns eight sets plus eight minifigures, but all three known sets
remain outside the set top-eight. Old/new top-1/3/8 on the four scoreable cases:
0/4, 0/4, 1/4 in both. G05 remains rank 7 in the minifigure bucket; thirteen corpus
identities stay unscoreable. All four searches are saturated/truncated.

Original 14C evidence remains unchanged. This is a diagnostic designed after its
results, not independent accuracy evidence. Kind capacity is corrected; deterministic
description retrieval is not worth further optimization on this evidence. Recommend
image-driven retrieval as the next separate decision, without starting it here.

The one curated figure result supports no production-quality or hidden-part identity
claim. Wider Phase 14 stays IN PROGRESS. No new provider calls/spend; stop for review.
