# Phase 14 — recognition quality spike closeout

## Accepted disposition — 2026-10-06

**Phase 14: COMPLETED / ACCEPTED AS QUALITY-SPIKE EVIDENCE.**
**PRODUCTION RECOGNITION: NOT QUALIFIED.** Phases 14A–14D and Plans 104–107 are
accepted and closed. The spike produced decision evidence; production recognition
success was not a condition for completing it. No evidence is rescored or reinterpreted.

## Accepted findings and evidence

### 14A — direct multimodal and reference comparison

Luna matched **3/3 selected set labels and 0/14 exact minifigure labels** on the tiny
approved sample. Listing text was included: these are neither visual-only results nor
general accuracy estimates. The original direct scores and denominators remain intact.
G06 Luna and Sol each scored **0/8 exact**; that single comparison demonstrated no
benefit from Sol. Closed-set G05 reference comparison selected the confirmed candidate
but did not visually establish unique A/B whole-figure identity. Their concealed-head
distinction remains unresolved; darkness is not proof of a different variant. No
additional view was requested. Closed-set verification is not full-catalog retrieval.

**Ten lifetime provider attempts consumed.** Estimated provider spend:
**USD 0.0497493**; actual billed dollars unavailable. **USD 7.616340 retained
reservations are accounting holds, not spending or a new allowance.** No further
Phase 14A calls are authorized. All fourteen BrickLink minifigure mappings remain
unresolved; no new catalog, alias, mapping or automatic confirmation follows.

Accepted evidence: [14A r6](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/2c71ad336424c8d4e7af6e8ed15279371afab578/astra_response/Phase-14/14A/r6/REVIEW.md),
with detailed findings in the existing [accepted pilot closeout](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/2c71ad336424c8d4e7af6e8ed15279371afab578/astra_response/Phase-14/14A/r6/REVIEW.md).

### 14B — local foundation

Description-assisted candidate retrieval/comparison and separate private operator
review work technically. Candidate proposals, visual compatibility, operator assertions
and canonical resolution remain distinct. The working foundation establishes no
retrieval-quality or production-recognition claim.

Accepted evidence: [14B r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/d9d77b0c7b4491cc3edf4374ba71e0cc15c16752/astra_response/Phase-14/14B/r1/REVIEW.md).

### 14C — frozen quality gate

Four scoreable cases; thirteen exact figure identities unscoreable because the
required corpus/mapping was unavailable. **Top-1: 0/4; top-3: 0/4; top-8: 1/4.**
All three known sets were absent from top-eight; all searches were truncated.
Disposition: **NOT USEFUL**. The one scoreable figure came from curated references,
not independently measured reference coverage. Unavailable identities were excluded
from ranking metrics, preserving their distinction from retrieval misses.

Accepted evidence: [14C r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/21cb0224372fa4161bfac4206a115a3f376b5215/astra_response/Phase-14/14C/r1/REVIEW.md).

### 14D — structural diagnostic

Sets and minifigures received independent top-eight buckets, removing set starvation.
None of the three known sets recovered. **Top-1/top-3/top-8 remained 0/4, 0/4, 1/4.**
Disposition: **STILL NOT USEFUL**. This was a before/after diagnostic designed after
14C results, not an independent benchmark. Further deterministic description-ranking
optimization is **STOPPED**; current evidence does not justify it.

Accepted evidence: [14D r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/640d83f72d727c2145635751c4d1642c48b0fd97/astra_response/Phase-14/14D/r1/REVIEW.md).
Its exact nine-file local checkpoint is `9dfe8868b9271eeed84831ce60f71a8df2b6d7dd`.

## Product and architecture disposition

- Normal direct catalog/set search continues independently of recognition.
- No automatic photo-based catalog confirmation, automatic exact-minifigure-ID
  confirmation or valuation triggered by a model prediction is approved.
- No production provider recognition endpoint is enabled by Phase 14. Candidate
  and operator-review code remains local/non-production evidence until separately
  promoted by an authorized future phase.
- **Sets:** direct multimodal results are promising but insufficiently sampled and
  not production-qualified.
- **Minifigures:** exact unaided recognition is not viable on current evidence.
  Reference-assisted comparison may help with valid candidates/views; ambiguity
  must remain explicit.
- **Description retrieval:** not useful enough to pursue on current evidence.

## Image-driven retrieval — DEFERRED / UNRESOLVED

This option is not failed or qualified. A meaningful benchmark requires additional
rights-cleared reference-image coverage and/or new image-embedding/provider
infrastructure. Current evidence does not justify full-catalog/vector infrastructure
and establishes no conclusion about whether image embeddings would work.

Revisit only after a larger independently confirmed, rights-cleared corpus exists,
including data from later reviewed capture/outcome workflows. Provider/model,
image-use, retention, cost and feasibility approvals remain separate future decisions.
The fourteen missing mappings stay unresolved in the existing catalog model.

## Roadmap transition and preservation

**Phase 15: NEXT / NOT STARTED / NOT AUTHORIZED.** Any later capture work must retain
a supported workflow when recognition is disabled or unavailable. Phase 16 remains
later and unchanged. Neither phase starts in this closeout.

Plans [104](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/2c71ad336424c8d4e7af6e8ed15279371afab578/astra_response/Phase-14/14A/r6/plan-104.md),
[105](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/d9d77b0c7b4491cc3edf4374ba71e0cc15c16752/astra_response/Phase-14/14B/r1/source/docs/plans/105-reference-candidate-retrieval.md),
[106](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/21cb0224372fa4161bfac4206a115a3f376b5215/astra_response/Phase-14/14C/r1/source/docs/plans/106-retrieval-quality-gate.md) and
[107](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/640d83f72d727c2145635751c4d1642c48b0fd97/astra_response/Phase-14/14D/r1/source/docs/plans/107-kind-partitioned-retrieval.md) are closed with their dated histories intact.
Approved inputs/labels, responses, accounting, reference/license evidence, frozen
queries/results and private notes remain local. Main remains unpushed. This closeout
runs documentation/Git checks only: no tests, evaluation, lint/types, database,
browser/device, build, provider, image sourcing, model research or production work.

Published links point to accepted execution records. The current closed-plan headers
and final status edits are preserved in the [committed documentation patch](documentation-closeout.patch).
