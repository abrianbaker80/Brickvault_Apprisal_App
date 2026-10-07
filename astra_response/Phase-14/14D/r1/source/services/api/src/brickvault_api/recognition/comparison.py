"""Private self-contained HTML and append-only human review; no remote image requests."""

import base64
import html
import io
import json
from pathlib import Path
from uuid import uuid4

from PIL import Image

from brickvault_api.recognition.local import digest, private_directory, read_bytes, write_bytes
from brickvault_api.recognition.retrieval import (
    Comparison,
    Retrieval,
    RetrievalError,
    ReviewNote,
    SelectedImage,
)

STYLE = """
body{font:16px system-ui;margin:24px auto;max-width:1200px;padding:0 16px;color:#172130}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
article{border:1px solid #a9b6c5;border-radius:8px;padding:16px;overflow-wrap:anywhere}
img{width:100%;height:auto;max-height:650px;object-fit:contain}
.limit{background:#fff2cc;padding:12px}small{display:block;margin:8px 0}h2{margin-top:32px}
"""


def escaped(value: object) -> str:
    return html.escape(str(value), quote=True)


def page(title: str, content: str) -> bytes:
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        "img-src data:; style-src &apos;unsafe-inline&apos;; script-src &apos;none&apos;; "
        'connect-src &apos;none&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        f"<title>{escaped(title)}</title><style>{STYLE}</style><body>"
        f"<h1>{escaped(title)}</h1>{content}</body></html>"
    ).encode()


def inline_image(path: Path, expected: str, caption: str) -> str:
    raw = read_bytes(path, 25 * 1024 * 1024)
    if digest(raw) != expected:
        raise RetrievalError("selected_image_changed")
    with Image.open(io.BytesIO(raw)) as image:
        if image.format not in ("JPEG", "PNG", "WEBP") or image.width * image.height > 20_000_000:
            raise RetrievalError("unsupported_comparison_image")
        image.verify()
        mime = {"JPEG": "jpeg", "PNG": "png", "WEBP": "webp"}[image.format]
    return (
        f'<img alt="{escaped(caption)}" src="data:image/{mime};base64,'
        f'{base64.b64encode(raw).decode()}">'
    )


def render(comparison: Comparison) -> bytes:
    result = comparison.retrieval
    parts = [
        f"<p>{escaped(result.claim)}</p>",
        '<p class="limit">Candidate, not confirmed. No image-only recognition or AI verification '
        "was performed. Retrieval, visual compatibility, unique identity, operator assertion "
        "and canonical mapping are separate. Photo darkness is not proof of different printing; "
        "concealed components need another view.</p>",
        f"<p>Query: {escaped(result.query.text)}</p>",
        f"<p>Catalog: {escaped(result.catalog_status)}. Pool: {result.pool_count}; "
        f"approved references: {result.reference_count}. "
        f"Catalog term-result limits reached: {result.catalog_truncated}.</p>",
        "<h2>Explicitly selected evaluation images</h2><div class=grid>",
    ]
    for i, image in enumerate(comparison.images, 1):
        parts.append(
            f"<article>{inline_image(Path(image.path), image.sha256, f'Selected view {i}')}</article>"
        )
    parts.append("</div>")
    sections = [("Ranked candidates", result.matches, result.state, result.pool_count)]
    if result.sets is not None and result.minifigures is not None:
        sections = [
            ("Set candidates", result.sets.matches, result.sets.state, result.sets.pool_count),
            (
                "Minifigure candidates",
                result.minifigures.matches,
                result.minifigures.state,
                result.minifigures.pool_count,
            ),
        ]
    for title, matches, state, pool in sections:
        parts.append(f"<h2>{escaped(title)}</h2><p>Kind pool: {pool}; state: {escaped(state)}.</p>")
        if state == "no_match":
            parts.append("<p>No matching candidate of this kind in the queried coverage.</p>")
        parts.append("<div class=grid>")
        for rank, match in enumerate(matches, 1):
            c = match.candidate
            parts.extend(
                [
                    f"<article><h3>{rank}. {escaped(c.name)}</h3>",
                    f"<p>{escaped(c.key.token)} — candidate, not confirmed</p>",
                    f"<p>Retrieval score {match.score}; {escaped(match.ranking_basis)}.</p>",
                    f"<p>Matched terms: {escaped(json.dumps(match.matched_terms))}</p>",
                    f"<p>Source-supported features: {escaped(c.features or 'No feature description available')}</p>",
                    f"<p>Canonical resolution: {escaped(c.resolution)}; "
                    f"{escaped(json.dumps(c.canonical) if c.canonical else 'No verified canonical identity')}</p>",
                    f"<small>Catalog/name provenance: {escaped(json.dumps(c.provenance))}</small>",
                ]
            )
            if c.reference:
                ref = c.reference
                parts.extend(
                    [
                        inline_image(Path(ref.image_path), ref.image_sha256, "Approved reference"),
                        f"<p>Photo association: {escaped(ref.identity_status)}. "
                        f"{escaped(ref.association_basis)}</p>",
                        f"<p>Available views: {escaped(', '.join(ref.views))}. Missing/unverified: "
                        f"{escaped(', '.join(ref.missing_views))}.</p>",
                        f"<small>Identity sources: {escaped(' ; '.join(ref.source_urls))}</small>",
                        f"<small>Attribution: {escaped(json.dumps(ref.attribution))}</small>",
                        f"<small>Permission evidence: {escaped(ref.permission)} "
                        f"Retained evidence hash: {escaped(ref.license_evidence['sha256'])}</small>",
                    ]
                )
            else:
                parts.append(
                    "<p>Reference image unavailable. Visual compatibility and hidden components "
                    "cannot be assessed from this catalog record alone.</p>"
                )
            parts.append(
                "<p>Visual compatibility: not assessed; unique identity: not established.</p></article>"
            )
        parts.append("</div>")
    parts.append(
        "<h2>Private operator review</h2><p>For partitioned results, ranks restart per kind. "
        "Select that kind in the local review CLI to record one "
        "provisional candidate, several compatible candidates, none, insufficient evidence "
        "with a needed view, or an independently known operator-supplied identity. Notes "
        "are separate append-only files; no catalog or valuation follows.</p>"
    )
    return page("BrickVault — description-assisted candidate comparison", "".join(parts))


def create_comparison(root: Path, result: Retrieval, images: list[Path]) -> tuple[Comparison, Path]:
    if not 1 <= len(images) <= 2:
        raise RetrievalError("select_one_or_two_images")
    selected = [
        SelectedImage(path=str(p.resolve()), sha256=digest(read_bytes(p, 25 * 1024 * 1024)))
        for p in images
    ]
    comparison = Comparison(run=uuid4().hex, retrieval=result, images=selected)
    rendered = render(comparison)  # Validate all bytes before publishing a report directory.
    target = root / comparison.run
    private_directory(target, create=True)
    write_bytes(target / "comparison.json", comparison.model_dump_json(indent=2).encode())
    write_bytes(target / "comparison.html", rendered)
    return comparison, target / "comparison.html"


def render_note(note: ReviewNote) -> bytes:
    content = (
        f"<p>{escaped(note.assertion)}</p><p>Decision: {escaped(note.decision)}</p>"
        f"<p>Compatible/provisional candidates: {escaped(', '.join(k.token for k in note.candidates))}</p>"
        f"<p>Needed view: {escaped(note.needed_view)}</p><p>Note: {escaped(note.comment)}</p>"
        f"<p>Independently known identity — operator-supplied assertion: "
        f"{escaped(note.operator_identity.token if note.operator_identity else 'None')}</p>"
        "<p>Visual uniqueness and canonical mapping are not established by this note.</p>"
    )
    return page("BrickVault — private operator review note", content)
