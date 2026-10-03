"""Protected local files, anonymous derivatives and durable attempt admission."""

import hashlib
import io
import json
import os
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path

from PIL import Image, ImageOps

from brickvault_api.images.processing import MAX_FILE_BYTES, process_image
from brickvault_api.providers.bricklink.configuration import ordinary
from brickvault_api.recognition.contracts import (
    MAX_ATTEMPTS,
    Approval,
    Attempt,
    Ledger,
    PilotError,
    Prepared,
    PreparedGroup,
    PreparedImage,
    Selection,
    StrictModel,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def private_directory(path: Path, *, create: bool = False) -> None:
    ordinary(path)
    if create:
        path.mkdir(mode=0o700)  # Deliberately fail on an existing pilot directory.
    if not path.is_dir():
        raise PilotError("private_directory_required")
    if os.name == "nt":
        # Fixed script; no command interpolation and no private data on stdout.
        script = """
$ErrorActionPreference = 'Stop'
$p = $env:BVA_PILOT_DIRECTORY
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User
if ($env:BVA_PILOT_CREATE -eq '1') {
  $acl = [System.IO.Directory]::GetAccessControl($p,
    [System.Security.AccessControl.AccessControlSections]::Access)
  $acl.SetAccessRuleProtection($true, $false)
  foreach ($existing in @($acl.Access)) { $acl.RemoveAccessRuleSpecific($existing) }
  $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
  $acl.AddAccessRule($rule)
  [System.IO.Directory]::SetAccessControl($p, $acl)
}
$acl = Get-Acl -LiteralPath $p
if (-not $acl.AreAccessRulesProtected) { exit 1 }
foreach ($entry in @((Get-Item -LiteralPath $p)) + @(Get-ChildItem -LiteralPath $p -Force)) {
  $a = Get-Acl -LiteralPath $entry.FullName
  foreach ($r in $a.Access) {
    $s = $r.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value
    if ($r.AccessControlType -eq 'Allow' -and
        $s -notin @($sid.Value, 'S-1-5-18', 'S-1-5-32-544')) { exit 1 }
  }
}
"""
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
            env={
                # Windows PowerShell must build its own module path; a parent
                # PowerShell 7 path can break its built-in Security module.
                **{k: v for k, v in os.environ.items() if k.upper() != "PSMODULEPATH"},
                "BVA_PILOT_DIRECTORY": str(path),
                "BVA_PILOT_CREATE": "1" if create else "0",
            },
            capture_output=True,
            timeout=15,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode:
            raise PilotError("private_acl_required")
    elif any(p.stat().st_mode & 0o077 for p in (path, *path.iterdir())):
        raise PilotError("private_permissions_required")


def read_bytes(path: Path, limit: int = 256 * 1024) -> bytes:
    ordinary(path)
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise PilotError("input_size_limit")
    return data


def read_model[T: StrictModel](path: Path, model: type[T]) -> T:
    return model.model_validate_json(read_bytes(path))


def write_bytes(path: Path, data: bytes, *, replace: bool = False) -> None:
    ordinary(path)
    if not replace:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    else:
        descriptor, name = tempfile.mkstemp(dir=path.parent, prefix=".pending-")
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, path)
        finally:
            Path(name).unlink(missing_ok=True)
    if os.name == "posix":
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)


def write_model(path: Path, model: StrictModel, *, replace: bool = False) -> None:
    write_bytes(path, model.model_dump_json(indent=2).encode(), replace=replace)


@contextmanager
def locked(root: Path) -> Iterator[None]:
    lock = root / "operation.lock"
    try:
        write_bytes(lock, b"Exclusive operation; stale lock requires manual reconciliation.\n")
    except FileExistsError:
        raise PilotError("pilot_busy_or_interrupted") from None
    try:
        yield
    finally:
        lock.unlink()


def sanitized_image(data: bytes) -> bytes:
    # Reuse accepted format, dimension, animation and decompression validation.
    process_image(data)
    with Image.open(io.BytesIO(data)) as source:
        source.load()
        oriented = ImageOps.exif_transpose(source)
        oriented.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        rgba = oriented.convert("RGBA")
        clean = Image.new("RGB", rgba.size, "white")
        clean.paste(rgba, mask=rgba.getchannel("A"))
        output = io.BytesIO()
        clean.save(output, format="JPEG", quality=85)
    result = output.getvalue()
    if len(result) > 1024 * 1024:
        raise PilotError("transmitted_image_size_limit")
    return result


def prepare(root: Path) -> Prepared:
    if (root / "prepared.json").exists() or (root / "ledger.json").exists():
        raise PilotError("sample_already_prepared")
    selection = read_model(root / "selection.json", Selection)
    groups: list[PreparedGroup] = []
    seen: set[str] = set()
    copies: dict[str, bytes] = {}
    for group in selection.groups:
        if not group.submission_rights_confirmed or not group.personal_content_removed:
            raise PilotError("photo_rights_and_visible_privacy_review_required")
        if len(group.listing_text.encode()) > 1000:
            raise PilotError("listing_text_size_limit")
        if group.independently_confirmed and not (group.expected or group.expected_outcome):
            raise PilotError("independent_label_required")
        images: list[PreparedImage] = []
        for filename in group.files:
            path = Path(filename)
            # Explicit local paths only: reject network shares, URLs and alternate streams.
            if not path.is_absolute() or str(path).startswith(("\\\\", "//")):
                raise PilotError("explicit_local_file_required")
            if ":" in str(path)[2:]:
                raise PilotError("explicit_local_file_required")
            original = read_bytes(path, MAX_FILE_BYTES)
            clean = sanitized_image(original)
            hashed = digest(clean)
            if hashed in seen:
                raise PilotError("duplicate_photo_in_sample")
            seen.add(hashed)
            copies[hashed] = clean
            images.append(
                PreparedImage(original_sha256=digest(original), transmitted_sha256=hashed)
            )
        groups.append(
            PreparedGroup(
                group=group.group,
                images=images,
                listing_text=group.listing_text,
                independently_confirmed=group.independently_confirmed,
                labels_exhaustive=group.labels_exhaustive,
                expected=group.expected,
                expected_outcome=group.expected_outcome,
            )
        )
    prepared = Prepared(recipe="recognition-rgb-1024-jpeg85-v1", groups=groups)
    for hashed, clean in copies.items():
        write_bytes(root / f"{hashed}.jpg", clean)
    write_model(root / "prepared.json", prepared)
    return prepared


def approved(root: Path) -> Approval:
    from brickvault_api.recognition.pilot import protocol_digest

    value = read_model(root / "approval.json", Approval)
    if not all(
        (
            value.approved,
            value.standard_api_retention_accepted,
            value.account_data_sharing_disabled_confirmed,
            value.selected_photos_and_text_approved,
        )
    ):
        raise PilotError("live_approval_required")
    if date.today() > date.fromisoformat(value.expires_on):
        raise PilotError("approval_expired")
    if value.protocol_sha256 != protocol_digest():
        raise PilotError("approved_protocol_changed")
    if value.prepared_sha256 != digest(
        read_bytes(root / "prepared.json")
    ) or value.subset_sha256 != digest(read_bytes(root / "subset.json")):
        raise PilotError("approved_inputs_changed")
    return value


def reserve(
    root: Path, approval: Approval, group: str, input_digest: str, input_token_bound: int
) -> Ledger:
    from brickvault_api.recognition.pilot import maximum_cost

    reservation = maximum_cost(input_token_bound)
    ledger_path = root / "ledger.json"
    # Initialization is a separate explicit seal command, never an implicit run reset.
    ledger = read_model(ledger_path, Ledger)
    if ledger.approval_sha256 != digest(read_bytes(root / "approval.json")):
        raise PilotError("approval_changed_after_seal")
    if ledger.stopped or any(a.state != "complete" for a in ledger.attempts):
        raise PilotError("prior_attempt_requires_reconciliation")
    if any(a.group == group or a.input_sha256 == input_digest for a in ledger.attempts):
        raise PilotError("replay_refused")
    if len(ledger.attempts) >= min(MAX_ATTEMPTS, approval.max_attempts):
        raise PilotError("attempt_cap")
    if (
        sum((a.reserved_usd for a in ledger.attempts), Decimal(0)) + reservation
        > approval.dollar_cap
    ):
        raise PilotError("dollar_cap")
    ledger.attempts.append(
        Attempt(
            group=group,
            input_sha256=input_digest,
            state="reserved",
            reserved_usd=reservation,
            input_token_bound=input_token_bound,
        )
    )
    write_model(ledger_path, ledger, replace=True)
    return ledger


def input_digest(group: PreparedGroup, protocol: str, subset: str) -> str:
    return digest(
        json.dumps(
            {
                "images": [i.transmitted_sha256 for i in group.images],
                "text": group.listing_text,
                "protocol_sha256": protocol,
                "catalog_reference_sha256": subset,
            },
            sort_keys=True,
        ).encode()
    )
