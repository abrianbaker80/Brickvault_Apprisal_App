"""Fixed PostgreSQL search predicates shared by queries and planner tests."""

import unicodedata

from brickvault_api.catalog.query_types import CatalogError

NORMALIZED_NAME = (
    "(lower(btrim(regexp_replace(f.display_name, '[[:space:]]+', ' ', 'g'))) COLLATE \"C\")"
)
NORMALIZED_INPUT = (
    "(lower(btrim(regexp_replace(%(query)s::text, '[[:space:]]+', ' ', 'g'))) COLLATE \"C\")"
)
TEXT_NAME = "to_tsvector('simple'::regconfig, f.display_name)"
TEXT_INPUT = "plainto_tsquery('simple'::regconfig, %(query)s)"
EXACT = f"{NORMALIZED_NAME} = {NORMALIZED_INPUT}"
# Escape LIKE metacharacters as data; backslash is also escaped first.
PREFIX_INPUT = f"replace(replace(replace({NORMALIZED_INPUT}, chr(92), chr(92)||chr(92)), '%%', chr(92)||'%%'), '_', chr(92)||'_') || '%%'"
PREFIX = f"{NORMALIZED_NAME} LIKE ({PREFIX_INPUT})"
TEXT_MATCH = f"{TEXT_NAME} @@ {TEXT_INPUT}"
MATCH_COLUMNS = "f.set_id,c.namespace,c.identifier,f.source_identifier,f.display_name,f.snapshot_id,f.source_version_id,f.evidence_id"
SEARCH_SQL = f"""SELECT {MATCH_COLUMNS},
    CASE WHEN {EXACT} THEN 0 WHEN {PREFIX} THEN 1 ELSE 2 END AS rank
    FROM catalog_set_fact f JOIN catalog_set c ON c.id=f.set_id
    WHERE f.snapshot_id=%(snapshot)s AND ({EXACT} OR {PREFIX} OR {TEXT_MATCH})
    ORDER BY rank, f.display_name COLLATE "C", c.identifier COLLATE "C", c.id
    LIMIT %(limit)s"""

FIGURE_SEARCH_SQL = f"""SELECT c.id,c.namespace,c.identifier,f.display_name,
    f.source_type,f.classification,f.snapshot_id,f.source_version_id,f.evidence_id
    FROM catalog_minifigure_fact f JOIN catalog_minifigure c ON c.id=f.minifigure_id
    WHERE f.snapshot_id=%(snapshot)s AND ({EXACT} OR {PREFIX} OR {TEXT_MATCH})
    ORDER BY f.display_name COLLATE "C",c.namespace COLLATE "C",c.identifier COLLATE "C",c.id
    LIMIT %(limit)s"""


def search_input(value: str, limit: int) -> str:
    if (
        not isinstance(value, str)
        or len(value) > 256
        or not value.strip()
        or any(unicodedata.category(c).startswith("C") for c in value)
        or type(limit) is not int
        or not 1 <= limit <= 100
    ):
        raise CatalogError("invalid_input")
    return value.strip()
