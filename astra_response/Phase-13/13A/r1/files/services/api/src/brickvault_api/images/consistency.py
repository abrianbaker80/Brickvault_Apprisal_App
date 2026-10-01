"""Report-only inspection; a definitive orphan report requires uploads stopped."""

from dataclasses import asdict, dataclass, field

from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.images.storage import BlobStore, ImageError, key_for


@dataclass
class ConsistencyReport:
    missing: list[str] = field(default_factory=list)
    corrupt: list[str] = field(default_factory=list)
    unreferenced: list[str] = field(default_factory=list)
    staging: list[str] = field(default_factory=list)
    unexpected: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, list[str]]:
        return asdict(self)


def inspect_storage(database: CatalogDatabase, store: BlobStore) -> ConsistencyReport:
    with database.connect() as c, c.transaction():
        c.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        referenced = c.execute("SELECT sha256,storage_key,byte_count FROM public.blob").fetchall()
    report = ConsistencyReport()
    keys = {row["storage_key"] for row in referenced}
    for row in referenced:
        try:
            blob = store.stat(row["sha256"])
            if blob.key != row["storage_key"] or blob.byte_count != row["byte_count"]:
                report.corrupt.append(row["storage_key"])
        except ImageError as error:
            (report.missing if error.code == "BLOB_MISSING" else report.corrupt).append(
                row["storage_key"]
            )
    for key in store.enumerate():
        if ".stage-" in key.split("/")[-1]:
            report.staging.append(key)
        elif key not in keys:
            try:
                digest = key.split("/")[-1]
                if key != key_for(digest):
                    raise ImageError("INVALID_BLOB_KEY")
                store.stat(digest)
                report.unreferenced.append(key)
            except ImageError:
                report.unexpected.append(key)
    for values in vars(report).values():
        values.sort()
    return report
