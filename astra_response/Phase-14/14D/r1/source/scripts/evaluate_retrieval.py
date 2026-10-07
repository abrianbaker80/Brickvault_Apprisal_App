"""One-run 14C/14D private harness; reuse the accepted guarded catalog lifecycle."""

import argparse
import json
from pathlib import Path

from brickvault_api.recognition.evaluation import (
    Labels,
    QueryFile,
    aggregate,
    evaluate,
    frozen_bytes,
)
from brickvault_api.recognition.local import private_directory, read_bytes, write_bytes
from brickvault_api.recognition.retrieval import Registry
from database import ROOT
from reference_candidates import development_catalog


def run(root: Path, *, input_root: Path | None = None) -> dict[str, object]:
    private_directory(root)
    inputs = input_root if input_root is not None else root
    frozen = json.loads(read_bytes(root / "frozen.json"))
    queries = QueryFile.model_validate_json(
        frozen_bytes(inputs / "queries.json", frozen["query_sha256"])
    )
    labels = Labels.model_validate_json(
        frozen_bytes(inputs / "ground-truth.json", frozen["ground_truth_sha256"])
    )
    registry = Registry.model_validate_json(
        frozen_bytes(
            ROOT / ".local/recognition-14b/reference-index.json", frozen["registry_sha256"]
        )
    )
    # Exclusive durable admission prevents a second evaluation, including after interruption.
    write_bytes(root / "run-started.json", json.dumps({"frozen": frozen, "runs": 1}).encode())
    try:
        with development_catalog() as catalog:
            if str(catalog.snapshot.id) != frozen["catalog_snapshot"]:
                raise ValueError("accepted_snapshot_changed")
            scores, results = evaluate(queries, labels, registry, catalog)
            snapshot = str(catalog.snapshot.id)
        private_results = {code: result.model_dump(mode="json") for code, result in results.items()}
        write_bytes(
            root / "ranked-results-private.json", json.dumps(private_results, indent=2).encode()
        )
        summary: dict[str, object] = {
            "version": "14d-structural-diagnostic-v1" if input_root else "14c-evaluation-v1",
            "baseline": frozen["baseline"],
            "catalog_snapshot": snapshot,
            "query_sha256": frozen["query_sha256"],
            "ground_truth_sha256": frozen["ground_truth_sha256"],
            "retrieval_runs": 1,
            "ranked_queries": len(results),
            "aggregate": aggregate(scores),
            "cases": [score.model_dump(mode="json") for score in scores],
            "excluded_groups": labels.excluded_groups,
            "kind_buckets": {
                code: {
                    "overall_pool": result.pool_count,
                    "overall_truncated": result.catalog_truncated,
                    "sets": result.sets.model_dump(exclude={"matches"}) if result.sets else None,
                    "minifigures": result.minifigures.model_dump(exclude={"matches"})
                    if result.minifigures
                    else None,
                    "set_shortlist_count": len(result.sets.matches) if result.sets else None,
                    "minifigure_shortlist_count": len(result.minifigures.matches)
                    if result.minifigures
                    else None,
                }
                for code, result in results.items()
            },
            "interpretation": "Before/after structural diagnostic when using kind buckets; designed after 14C, not an independent benchmark. Description-assisted exact-key retrieval; curated figure reference; RR@8 zero outside the relevant shortlist. Unscoreable identities excluded; truncation is overall term-result saturation.",
        }
        write_bytes(root / "results-public.json", json.dumps(summary, indent=2).encode())
        return summary
    except Exception:
        write_bytes(
            root / "run-incomplete.json", b'{"state":"incomplete","rerun_authorized":false}'
        )
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="One admitted frozen evaluation; no provider calls."
    )
    parser.add_argument("--phase", choices=["14c", "14d"], default="14c")
    args = parser.parse_args()
    try:
        summary = run(
            ROOT / f".local/recognition-{args.phase}",
            input_root=ROOT / ".local/recognition-14c" if args.phase == "14d" else None,
        )
    except Exception:
        # Never emit private labels, queries, credentials, paths or native error text.
        print("Evaluation stopped. Retain local evidence; no automatic rerun.")
        raise SystemExit(1) from None
    print(json.dumps(summary, indent=2))
