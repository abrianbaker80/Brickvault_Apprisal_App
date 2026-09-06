# Originating Chat Summary

## How to read this history

This chronological summary preserves both ideas that now form one product. Historical exploration is not current sequencing authority. [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [DECISIONS.md](DECISIONS.md), and [ROADMAP.md](ROADMAP.md) define the unified valuation-first direction. The starter ZIP is historical material.

## 1. Initial Marketplace-photo idea

The originating discussion concerned Facebook Marketplace LEGO listings whose sellers omit set names/numbers. Brian wanted to inspect photographs, identify likely sets/minifigures, estimate market and realistic resale values, and choose an opening/maximum offer.

The discussion considered training against every LEGO set. The recommendation was instead catalog/reference retrieval plus multimodal verification through server-side OpenAI/Gemini adapters, with evidence, uncertainty, and Brian's corrections; custom training would come only after enough verified examples.

A proposed Android experience used a visible floating control, explicit capture, manual carousel swipes, optional crops, title/asking-price entry, upload, and appraisal handoff. Android Share and ordinary upload were fallbacks. No scraping, interception, unattended navigation, or seller automation was accepted.

Brian wanted original photos, useful crops, model/prompt history, candidate scores, corrections, hard negatives, verified contents, and later resale outcomes preserved for training. Predictions were never confirmed labels, and training exports had to exclude seller/unrelated personal content.

## 2. Private-use and foundation planning decisions

Brian specified one private user, self-hosting, shared server data, no public registration/billing/teams, and no app-store requirement. Personal resale channels, labor, costs, and outcomes could inform later estimates.

The initial repository therefore planned an image-storage slice followed by recognition and Android capture spikes. The documentation checkpoint refined that plan to React/Vite, FastAPI static serving, /api contracts, and robust image semantics: listing_image_id, partial success, immutable originals, derivative lineage, stable upload UUID/position, deterministic persisted ordering, and receipts recovering lost duplicate responses.

That plan was never implemented. The documents and accepted decision history exist; no application, schema, provider integration, or physical-device result is implied. The earlier image contract is now preserved in [IMAGE_INGESTION.md](IMAGE_INGESTION.md).

## 3. Product-scope audit and foundational sourcing definition

Brian then supplied the authoritative set-number/minifigure-value sourcing concept: direct number/name lookup, whole-set new/used market values, each included figure and quantity, individual prices/totals, acquisition/selling costs, profit/ROI/max buy, saved deals/watchlists/settings, and Sets to Hunt.

The read-only product-scope audit found the repository primarily described the photo-recognition app: images in Phase 1, recognition in Phase 2, capture in Phase 3, manual-priced appraisal in Phase 4, catalog in Phase 5, and pricing in Phase 6. It identified missing or late direct search, exhaustive figure relationships/totals, precise ROI, and hunting.

The audit recommended keeping one repository with shared catalog/valuation logic and correcting the sequence before any implementation. Internal documentation agreement was not sufficient evidence of product alignment.

## 4. Approved unified valuation-first correction

Brian directed documentation-only realignment to one unified application. The deterministic set-number/minifigure-value concept is the foundational core. Marketplace image recognition remains a later input method into that same core, not another repository or competing product.

D-018 preserves and annotates D-001 through D-008 history, changes D-008 sequencing, and starts D-003 image retention when that feature exists. D-019 makes Chrome/PWA/Android share the primary React UI and backend, with later native extensions only where needed. D-020 establishes exact financial/evidence rules; D-021 rebases the unexecuted foundation and preserves the later upload contract.

The order is foundation, catalog, market integration, representative feasibility, valuation, search/detail, saved deal workflows, hunting, PWA/Android, local hardening, separately authorized discovery/deployment, then optional images/recognition/capture/datasets. Provider rights, live coverage, and Android behavior remain unverified gates.

## Current workflow and boundaries

Use one repository, durable requirements, one bounded phase per request, and ExecPlans under [.agent/PLANS.md](../.agent/PLANS.md). The next step after review is the Phase 1 plan-only prompt, not implementation. No dependency/service/network/server work or staging/commit is authorized by this documentation correction.
