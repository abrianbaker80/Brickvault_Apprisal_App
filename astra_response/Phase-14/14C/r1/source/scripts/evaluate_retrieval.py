"""Phase 14C one-run private harness; reuse the accepted guarded catalog lifecycle."""

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


def run(root: Path) -> dict[str, object]:
    private_directory(root)
    frozen = json.loads(read_bytes(root / "frozen.json"))
    queries = QueryFile.model_validate_json(
        frozen_bytes(root / "queries.json", frozen["query_sha256"])
    )
    labels = Labels.model_validate_json(
        frozen_bytes(root / "ground-truth.json", frozen["ground_truth_sha256"])
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
            "version": "14c-evaluation-v1",
            "baseline": frozen["baseline"],
            "catalog_snapshot": snapshot,
            "query_sha256": frozen["query_sha256"],
            "ground_truth_sha256": frozen["ground_truth_sha256"],
            "retrieval_runs": 1,
            "ranked_queries": len(results),
            "aggregate": aggregate(scores),
            "cases": [score.model_dump(mode="json") for score in scores],
            "excluded_groups": labels.excluded_groups,
            "interpretation": "Description-assisted exact-key retrieval only; curated figure reference; RR@8 is zero when absent from the retained shortlist. Unscoreable identities excluded from ranking metrics.",
        }
        write_bytes(root / "results-public.json", json.dumps(summary, indent=2).encode())
        return summary
    except Exception:
        write_bytes(
            root / "run-incomplete.json", b'{"state":"incomplete","rerun_authorized":false}'
        )
        raise


if __name__ == "__main__":
    try:
        summary = run(ROOT / ".local/recognition-14c")
    except Exception:
        # Never emit private labels, queries, credentials, paths or native error text.
        print("Evaluation stopped. Retain local evidence; no automatic rerun.")
        raise SystemExit(1) from None
    print(json.dumps(summary, indent=2))
