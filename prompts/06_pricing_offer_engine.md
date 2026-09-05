# Prompt 06 — Pricing and offer engine

**Use in:** a new Codex chat after set identity and catalog retrieval are stable  
**Model:** GPT-6 Astra  
**Reasoning:** High  
**Mode:** Plan first  
**Expected result:** transparent, testable values and offer recommendations

---

Plan and implement the pricing, resale, and offer engine.

The engine must keep sourced market data separate from calculated estimates. Use official APIs or explicitly approved sources and record provenance, query parameters, sample windows, currency, region, condition, and fetch time.

For each confirmed or assumed set identity, calculate and display:

- current/fair market estimate,
- quick-sale estimate,
- expected gross resale,
- channel-specific fees,
- shipping/packing allowance,
- missing-parts/minifigure allowance,
- cleaning/sorting labor allowance,
- uncertainty/risk reserve,
- expected net proceeds,
- suggested opening offer,
- maximum offer,
- confidence and every assumption used.

Requirements:

- Keep formulas deterministic, versioned, configurable, and covered by a table-driven unit-test matrix.
- Support at least local sale, eBay-like shipped resale, BrickLink-like resale, and personal-collection profiles without hard-coding provider fees as eternal facts.
- Cache external price calls and handle missing/thin/old samples honestly.
- Never sum theoretical part-out prices and present them as readily realizable cash without a configurable liquidity/labor adjustment.
- Allow manual override with an audit trail.
- Compare appraisal to seller asking price and show margin in dollars and percent.
- Persist the appraisal snapshot so later source updates do not rewrite what Brian saw when he made the decision.

Do not implement custom training or automatic purchasing. Run tests and stop after the valuation workflow is complete.
