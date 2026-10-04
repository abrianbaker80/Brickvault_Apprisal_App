"""Repository-local Phase 14B CLI; only guarded development catalog reads."""

import argparse
import json
import re
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import psycopg
from brickvault_api.catalog.connection import CatalogDatabase, read_transaction
from brickvault_api.catalog.query_types import CatalogError
from brickvault_api.catalog.repository import PinnedCatalog, open_catalog
from brickvault_api.persistence.database import expected_revisions
from brickvault_api.recognition.comparison import create_comparison, render_note
from brickvault_api.recognition.local import (
    digest,
    private_directory,
    read_bytes,
    write_bytes,
)
from brickvault_api.recognition.retrieval import (
    Comparison,
    Key,
    Query,
    Registry,
    RetrievalError,
    ReviewNote,
    query_from,
    retained_clues,
    retrieve,
    save_note,
)
from database import LOCAL, ROOT, DatabaseError, database_marker, instance, runner_lock

PRIVATE = ROOT / ".local" / "recognition-14b"


@contextmanager
def development_catalog() -> Iterator[PinnedCatalog]:
    """Require existing ownership/service/head; restore its exact initial running state."""
    if not (LOCAL / "development.json").is_file():
        raise RetrievalError("existing_development_receipt_required")
    if expected_revisions() != ("0017_listing_images",):
        raise RetrievalError("approved_0017_schema_required")
    with runner_lock():
        dev = instance("development")
        before = dev.verify()
        if before is None:
            raise RetrievalError("existing_development_service_required")
        running = bool(before["State"]["Running"])
        try:
            if not running:
                dev.up()  # Existing supported no-recreate/no-pull lifecycle; no provisioning.
            database = CatalogDatabase(
                dev.target("brickvault_dev", "runtime"),
                "development",
                database_marker(dev, "development"),
                role="runtime",
            )
            with read_transaction(database, repeatable=True) as connection:
                pointers = connection.execute(
                    """SELECT a.snapshot_id FROM catalog_active_snapshot a
                    JOIN catalog_snapshot s ON s.id=a.snapshot_id
                    JOIN catalog_source_version v ON v.id=s.source_version_id
                    JOIN catalog_provider p ON p.id=v.provider_id
                    WHERE p.code='rebrickable' AND NOT v.synthetic AND s.state='accepted'
                    ORDER BY a.snapshot_id LIMIT 2"""
                ).fetchall()
                if len(pointers) != 1:
                    raise RetrievalError("one_accepted_catalog_required")
                with open_catalog(
                    database,
                    snapshot_id=pointers[0]["snapshot_id"],
                    connection=connection,
                ) as catalog:
                    yield catalog
        finally:
            if not running:
                dev.stop()


def selected_query(args: argparse.Namespace) -> Query:
    if args.query_file:
        return query_from(json.loads(read_bytes(Path(args.query_file))))
    if args.clues_file:
        return retained_clues(
            json.loads(read_bytes(Path(args.clues_file))),
            args.object_index,
            field=args.clue_field,
            indices=args.clue_index,
            candidate_index=args.candidate_index,
        )
    return query_from({"description": input("Visible description (no catalog IDs): ")})


def existing_comparison(root: Path, run: str) -> Comparison:
    if re.fullmatch(r"[a-f0-9]{32}", run) is None:
        raise RetrievalError("invalid_comparison_run")
    return Comparison.model_validate_json(
        read_bytes(root / run / "comparison.json", 4 * 1024 * 1024)
    )


def review_interactive(root: Path, run: str) -> Path:
    comparison = existing_comparison(root, run)
    decision = input(
        "Decision: provisional / compatible / none / insufficient_evidence / known_identity: "
    )
    selected = []
    identity = None
    needed_view = ""
    if decision in ("provisional", "compatible"):
        ranks = [
            int(v) for v in input("Candidate ranks, separated by commas: ").split(",")
        ]
        if any(not 1 <= rank <= len(comparison.retrieval.matches) for rank in ranks):
            raise RetrievalError("candidate_rank_unavailable")
        selected = [
            comparison.retrieval.matches[rank - 1].candidate.key for rank in ranks
        ]
    if decision == "insufficient_evidence":
        needed_view = input("Needed view: ")
    if decision == "known_identity":
        identity = Key.model_validate(
            {
                "kind": input("Kind: set / minifigure: "),
                "namespace": input("Namespace: "),
                "identifier": input(
                    "Independently known identifier (operator-supplied): "
                ),
            }
        )
    note = ReviewNote.model_validate(
        {
            "run": run,
            "comparison_sha256": digest(
                read_bytes(root / run / "comparison.json", 4 * 1024 * 1024)
            ),
            "decision": decision,
            "candidates": [k.model_dump() for k in selected],
            "needed_view": needed_view,
            "operator_identity": identity.model_dump() if identity else None,
            "comment": input("Optional private review note: "),
        }
    )
    target = save_note(root, comparison, note)
    write_bytes(target.with_suffix(".html"), render_note(note))
    return target.with_suffix(".html")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local description-assisted retrieval; no AI calls."
    )
    parser.add_argument("--private-root", type=Path, default=PRIVATE)
    commands = parser.add_subparsers(dest="command", required=True)
    compare = commands.add_parser("compare")
    compare.add_argument("--image", type=Path, action="append", required=True)
    sources = compare.add_mutually_exclusive_group()
    sources.add_argument("--query-file")
    sources.add_argument("--clues-file")
    compare.add_argument("--object-index", type=int, default=0)
    compare.add_argument("--candidate-index", type=int, default=0)
    compare.add_argument(
        "--clue-field", choices=["visual_clues", "text_clues"], default="visual_clues"
    )
    compare.add_argument("--clue-index", type=int, action="append")
    compare.add_argument(
        "--reference-only",
        action="store_true",
        help="Explicitly omit catalog access; report restricted coverage.",
    )
    compare.add_argument("--limit", type=int, default=8)
    review = commands.add_parser("review")
    review.add_argument("--run", required=True)
    reopen = commands.add_parser("reopen")
    reopen.add_argument("--run", required=True)
    args = parser.parse_args()
    try:
        if args.private_root.resolve() != PRIVATE.resolve():
            raise RetrievalError("repository_private_14b_directory_required")
        private_directory(PRIVATE)
        if args.command == "compare":
            registry = Registry.model_validate_json(
                read_bytes(PRIVATE / "reference-index.json")
            )
            query = selected_query(args)
            if args.reference_only:
                result = retrieve(query, registry, None, limit=args.limit)
            else:
                with development_catalog() as catalog:
                    result = retrieve(query, registry, catalog, limit=args.limit)
            comparison, report = create_comparison(PRIVATE, result, args.image)
            print(f"Local comparison ready. Run: {comparison.run}; report: {report}")
        elif args.command == "review":
            print(f"Separate operator note: {review_interactive(PRIVATE, args.run)}")
        else:
            comparison = existing_comparison(PRIVATE, args.run)
            notes = sorted(
                (PRIVATE / comparison.run).glob("note-*.json"),
                key=lambda p: p.stat().st_mtime_ns,
            )
            if not notes:
                raise RetrievalError("operator_note_unavailable")
            note = ReviewNote.model_validate_json(read_bytes(notes[-1]))
            if note.comparison_sha256 != digest(
                read_bytes(
                    PRIVATE / comparison.run / "comparison.json", 4 * 1024 * 1024
                )
            ):
                raise RetrievalError("note_comparison_mismatch")
            print(
                f"Saved note: {notes[-1].with_suffix('.html')}; decision: {note.decision}"
            )
    except (RetrievalError, CatalogError, DatabaseError) as error:
        print(f"Local candidate workflow stopped: {error}")
        return 1
    except (OSError, ValueError, psycopg.Error):
        # Never emit a traceback, private query, URL, credential or user text.
        print(
            "Local candidate workflow failed. Preserve evidence; inspect the local inputs and owned development prerequisites."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
