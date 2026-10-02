"""Bounded fixture tests. These establish no live recognition quality."""

import http.client
import io
import json
import socket
import threading
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
from PIL import Image
from pydantic import ValidationError

from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.catalog.query_types import Identity, SnapshotRef
from brickvault_api.recognition import __main__ as cli
from brickvault_api.recognition import pilot
from brickvault_api.recognition.contracts import (
    MODEL,
    Approval,
    Attempt,
    CatalogRequest,
    Ledger,
    PilotError,
    Prepared,
    PreparedGroup,
    PreparedImage,
    Proposal,
    Recognition,
    ReferenceSubset,
)
from brickvault_api.recognition.local import (
    approved,
    digest,
    input_digest,
    locked,
    prepare,
    private_directory,
    read_model,
    reserve,
    sanitized_image,
    write_bytes,
    write_model,
)


@pytest.fixture(autouse=True)
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("Fixture tests prohibit network access")

    monkeypatch.setattr(socket.socket, "connect", refuse)


def candidate(identifier: str = "100-1", rank: int = 1) -> dict[str, Any]:
    return dict(
        kind="set",
        namespace="rebrickable",
        identifier=identifier,
        rank=rank,
        confidence_uncalibrated=0.9,
        supporting_visual_clues=["red roof"],
        supporting_text_clues=[],
        contradictions=["rear view unavailable"],
    )


def recognition(
    outcome: str = "unknown", candidates: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    return {
        "objects": [
            {
                "object_description": "central object",
                "outcome": outcome,
                "candidates": candidates or [],
                "additional_view_requested": "rear view",
            }
        ]
    }


def response(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": MODEL,
        "status": "completed",
        "service_tier": "default",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps(result)}],
            }
        ],
        "usage": {
            "input_tokens": 1000,
            "output_tokens": 100,
            "input_tokens_details": {"cached_tokens": 200, "cache_write_tokens": 100},
            "output_tokens_details": {"reasoning_tokens": 50},
        },
    }


def image_bytes(color: str = "red") -> bytes:
    out = io.BytesIO()
    exif = Image.Exif()
    exif[270] = "PRIVATE OWNER ADDRESS"
    Image.new("RGB", (1200, 800), color).save(out, format="JPEG", exif=exif)
    return out.getvalue()


def setup_pilot(root: Path) -> Approval:
    groups = []
    for index, color in enumerate(("red", "blue", "green", "yellow", "black", "white"), 1):
        original = image_bytes(color)
        clean = sanitized_image(original)
        hashed = digest(clean)
        write_bytes(root / f"{hashed}.jpg", clean)
        groups.append(
            PreparedGroup(
                group=f"G0{index}",
                images=[PreparedImage(original_sha256=digest(original), transmitted_sha256=hashed)],
                listing_text="untrusted evidence only",
                independently_confirmed=True,
                labels_exhaustive=True,
                expected=[Proposal(kind="set", namespace="rebrickable", identifier="100-1")],
                expected_outcome="candidates",
            )
        )
    write_model(
        root / "prepared.json", Prepared(recipe="recognition-rgb-1024-jpeg85-v1", groups=groups)
    )
    subset = ReferenceSubset(
        snapshot=SnapshotRef(UUID(int=1), UUID(int=2), UUID(int=3), "catalog", False),
        identities=[Identity(UUID(int=i), "set", "rebrickable", f"{i}-1") for i in range(100, 125)],
    )
    write_model(root / "subset.json", subset)
    approval = Approval(
        approved=True,
        approved_by="Brian",
        provider="openai",
        model=MODEL,
        project_id="proj_fixture",
        prepared_sha256=digest((root / "prepared.json").read_bytes()),
        subset_sha256=digest((root / "subset.json").read_bytes()),
        protocol_sha256=pilot.protocol_digest(),
        dollar_cap=Decimal("10.00"),
        max_attempts=10,
        standard_api_retention_accepted=True,
        account_data_sharing_disabled_confirmed=True,
        selected_photos_and_text_approved=True,
        prices_verified_on="2026-10-02",
        expires_on=(date.today() + timedelta(days=1)).isoformat(),
    )
    write_model(root / "approval.json", approval)
    write_model(
        root / "ledger.json",
        Ledger(approval_sha256=digest((root / "approval.json").read_bytes()), attempts=[]),
    )
    write_bytes(root / "api-key.txt", b"sk-fixture-never-a-real-key")
    write_bytes(
        root / "model-access.json",
        json.dumps(
            {
                "model": MODEL,
                "project_id": approval.project_id,
                "key_sha256": digest(b"sk-fixture-never-a-real-key"),
                "approval_sha256": digest((root / "approval.json").read_bytes()),
            }
        ).encode(),
    )
    return approval


def test_structured_parsing_malformed_and_refusal() -> None:
    assert pilot.parse_response(response(recognition())).objects[0].outcome == "unknown"
    for result in (
        recognition("candidates", [candidate(rank=2)]),
        recognition("unknown", [candidate()]),
        recognition("candidates", [candidate(), candidate()]),
        {**recognition(), "price": 10},
    ):
        with pytest.raises(PilotError, match="malformed"):
            pilot.parse_response(response(result))
    refused = response(recognition())
    refused["output"][0]["content"] = [{"type": "refusal", "refusal": "private refusal text"}]
    with pytest.raises(PilotError, match="provider_refusal") as error:
        pilot.parse_response(refused)
    assert "private" not in str(error.value)
    malformed = response(recognition())
    malformed["output"][0]["content"][0]["text"] = "not JSON PRIVATE"
    with pytest.raises(PilotError, match="malformed"):
        pilot.parse_response(malformed)
    malformed["status"] = "incomplete"
    with pytest.raises(PilotError, match="incomplete"):
        pilot.parse_response(malformed)
    with pytest.raises(PilotError, match="unexpected_provider_model"):
        pilot.parse_response({**response(recognition()), "model": "fallback-model"})


def test_exact_canonical_resolution_and_no_production() -> None:
    ref = Identity(UUID(int=1), "set", "rebrickable", "100-2")
    proposal = Proposal(kind="set", namespace="rebrickable", identifier="100-2")
    assert pilot.resolve(proposal, [ref])["canonical"]["id"] == ref.id
    for identifier, state in (
        ("100", "unresolved"),
        ("100-1", "unresolved"),
        ("../100-2", "invalid_identifier"),
    ):
        assert (
            pilot.resolve(proposal.model_copy(update={"identifier": identifier}), [ref])["state"]
            == state
        )
    assert pilot.resolve(proposal, [ref, replace(ref, id=UUID(int=2))])["state"] == "ambiguous"
    assert (
        pilot.resolve(proposal.model_copy(update={"namespace": "bricklink"}), [ref])["canonical"]
        is None
    )
    figure = Proposal(kind="minifigure", namespace="bricklink", identifier="sw0001")
    assert (
        pilot.resolve(figure, [Identity(UUID(int=3), "minifigure", "bricklink", "sw0001")])["state"]
        == "resolved"
    )
    request = CatalogRequest(snapshot_id=str(UUID(int=1)), identities=[proposal] * 25)
    with pytest.raises(PilotError, match="development_read_only"):
        pilot.export_subset(CatalogDatabase("never-connect", "production", "marker"), request)


def test_unknown_mixed_evaluation_and_no_silent_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    setup_pilot(tmp_path)
    monkeypatch.setattr(pilot, "input_token_bound", lambda body: 20000)
    answers = [
        recognition("candidates", [candidate()]),
        recognition("mixed_sets", [candidate("101-1"), candidate(rank=2)]),
        recognition(),
        recognition("insufficient_evidence"),
        recognition("custom_build"),
        recognition("non_lego"),
    ]
    calls: list[bytes] = []

    def fake_call(body: bytes, key: str, project: str) -> dict[str, Any]:
        assert key == "sk-fixture-never-a-real-key"
        assert project == "proj_fixture"
        calls.append(body)
        return response(answers[len(calls) - 1])

    monkeypatch.setattr(pilot, "call_openai", fake_call)
    pilot.execute(tmp_path)
    pilot.execute(tmp_path)
    assert len(calls) == 6
    stats = pilot.evaluate(tmp_path)
    assert (stats["labeled_identities"], stats["top1"], stats["top3"]) == (6, 1, 2)
    assert stats["abstention_objects"] == 4
    assert stats["incorrect_confident_suggestions"] == 1
    assert stats["reserved_usd"] == "0.021144"
    assert stats["result_reuses"] == 6
    assert stats["reported_billing_usd"] is None
    assert stats["estimated_usd_available_sum"] == "0.0008070"
    assert stats["unresolved_candidates"] == 0
    assert "red roof" not in json.dumps(stats)
    request = json.loads(calls[0])
    assert request["store"] is False and "tools" not in request
    assert "100-1" not in calls[0].decode()  # Answer labels are withheld.
    assert "PRIVATE OWNER" not in calls[0].decode()
    assert request["model"] == "gpt-6-luna" and request["service_tier"] == "default"
    assert request["max_output_tokens"] == 2048 and request["reasoning"] == {"effort": "medium"}
    assert "temperature" not in request
    assert request["prompt_cache_options"] == {"mode": "explicit", "ttl": "30m"}
    assert request["input"][0]["content"][0]["prompt_cache_breakpoint"] == {"mode": "explicit"}
    assert "prompt_cache_breakpoint" not in json.dumps(request["input"][1])
    (tmp_path / "api-key.txt").unlink()  # Reuse needs no credentials or network.
    pilot.execute(tmp_path)
    assert len(calls) == 6 and pilot.evaluate(tmp_path)["result_reuses"] == 12
    (tmp_path / "G01-result.json").write_text("{}")
    with pytest.raises(PilotError, match="saved_result_integrity"):
        pilot.execute(tmp_path)
    assert len(calls) == 6


def test_budget_caps_interruptions_and_exclusive_reservation(tmp_path: Path) -> None:
    approval = setup_pilot(tmp_path)
    with pytest.raises(PilotError, match="dollar_cap"):
        reserve(
            tmp_path,
            approval.model_copy(update={"dollar_cap": Decimal("0.001")}),
            "G01",
            "a" * 64,
            20000,
        )
    with pytest.raises(PilotError, match="attempt_cap"):
        reserve(tmp_path, approval.model_copy(update={"max_attempts": 0}), "G01", "a" * 64, 20000)
    with locked(tmp_path):
        with pytest.raises(PilotError, match="busy_or_interrupted"):
            with locked(tmp_path):
                pytest.fail("second process admitted")
        ledger = reserve(tmp_path, approval, "G01", "a" * 64, 922000)
    assert ledger.attempts[0].state == "reserved"
    with pytest.raises(PilotError, match="reconciliation"):
        reserve(tmp_path, approval, "G02", "b" * 64, 20000)
    ledger.attempts[0].state = "complete"
    write_model(tmp_path / "ledger.json", ledger, replace=True)
    with pytest.raises(PilotError, match="replay"):
        reserve(tmp_path, approval, "G01", "c" * 64, 20000)
    with pytest.raises(PilotError, match="replay"):
        reserve(tmp_path, approval, "G02", "a" * 64, 20000)
    for index in range(1, 10):
        ledger = reserve(tmp_path, approval, f"extra-{index}", digest(str(index).encode()), 922000)
        ledger.attempts[-1].state = "complete"
        write_model(tmp_path / "ledger.json", ledger, replace=True)
    with pytest.raises(PilotError, match="attempt_cap"):
        reserve(tmp_path, approval, "eleventh", "d" * 64, 20000)
    assert sum(a.reserved_usd for a in ledger.attempts) == Decimal("2.320360")
    (tmp_path / "ledger.json").unlink()
    with pytest.raises(FileNotFoundError):
        reserve(tmp_path, approval, "G08", "e" * 64, 20000)


def test_provider_failure_timeout_and_redaction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    setup_pilot(tmp_path)
    monkeypatch.setattr(pilot, "input_token_bound", lambda body: 20000)

    class RejectedResponse:
        status = 429

        def read(self, limit: int) -> bytes:
            return b'{"error":{"code":"rate_limit_exceeded","message":"PRIVATE AUTHORIZATION"}}'

    class FakeConnection:
        sock = None
        calls = 0

        def __init__(self, host: str, **kwargs: Any) -> None:
            assert host == "api.openai.com"

        def connect(self) -> None:
            pass

        def request(self, method: str, path: str, **kwargs: Any) -> None:
            assert (method, path) == ("POST", "/v1/responses")
            FakeConnection.calls += 1

        def getresponse(self) -> RejectedResponse:
            return RejectedResponse()

        def close(self) -> None:
            pass

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(
        PilotError, match="provider_request_failed_http_429_code_rate_limit_exceeded"
    ):
        pilot._https_request(b"{}", "PRIVATE_AUTHORIZATION", "proj_fixture")
    assert FakeConnection.calls == 1

    def fail(body: bytes, key: str, project: str, **kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("PRIVATE secret key/photo/seller")

    monkeypatch.setattr(pilot, "_https_request", fail)
    with pytest.raises(PilotError) as error:
        pilot.execute(tmp_path)
    assert "PRIVATE" not in str(error.value)
    ledger = read_model(tmp_path / "ledger.json", Ledger)
    assert ledger.stopped and ledger.attempts[0].state == "failed"
    assert ledger.attempts[0].reserved_usd == Decimal("0.003524")
    with pytest.raises(PilotError, match="reconciliation"):
        pilot.execute(tmp_path)
    event = threading.Event()

    def stall(body: bytes, key: str, project: str, **kwargs: Any) -> dict[str, Any]:
        event.wait(2)
        return {}

    monkeypatch.setattr(pilot, "_https_request", stall)
    monkeypatch.setattr(pilot, "TIMEOUT", 0.01)
    try:
        with pytest.raises(PilotError, match="uncertain"):
            pilot.call_openai(b"{}", "private", "proj_fixture")
    finally:
        event.set()
    assert cli.main(["PRIVATE_ARG_VALUE"]) == 1
    assert "PRIVATE_ARG_VALUE" not in capsys.readouterr().err


def test_photo_privacy_approval_and_size_boundaries(tmp_path: Path) -> None:
    private = tmp_path / "private"
    private_directory(private, create=True)
    private_directory(private)
    approval = setup_pilot(private)
    assert approved(private).model == MODEL
    clean = sanitized_image(image_bytes())
    with Image.open(io.BytesIO(clean)) as image:
        assert max(image.size) == 1024 and not image.getexif()
    assert b"PRIVATE OWNER ADDRESS" not in clean
    changed = approval.model_copy(update={"approved": False})
    write_model(private / "approval.json", changed, replace=True)
    with pytest.raises(PilotError, match="live_approval"):
        approved(private)
    write_model(private / "approval.json", approval, replace=True)
    prepared = read_model(private / "prepared.json", Prepared)
    group = prepared.groups[0]
    clean_path = private / f"{group.images[0].transmitted_sha256}.jpg"
    with pytest.raises(PilotError, match="image_changed"):
        pilot.request_body(group, [b"changed"])
    with pytest.raises(PilotError, match="text_input_limit"):
        pilot.request_body(
            group.model_copy(update={"listing_text": "é" * 1000}), [clean_path.read_bytes()]
        )
    with pytest.raises(ValidationError):
        Recognition.model_validate({"objects": []})
    original_path = tmp_path / "revealing-answer-100-1.jpg"
    original = image_bytes()
    original_path.write_bytes(original)
    selection = {
        "groups": [
            {
                "group": f"G0{i}",
                "files": [str(original_path)],
                "listing_text": "",
                "independently_confirmed": False,
                "labels_exhaustive": False,
                "expected": [],
                "expected_outcome": None,
                "submission_rights_confirmed": False,
                "personal_content_removed": False,
            }
            for i in range(1, 7)
        ]
    }
    other = tmp_path / "other"
    other.mkdir()
    write_bytes(other / "selection.json", json.dumps(selection).encode())
    with pytest.raises(PilotError, match="privacy_review"):
        prepare(other)
    assert original_path.read_bytes() == original
    for index, color in enumerate(("red", "blue", "green", "yellow", "black", "white")):
        selected = tmp_path / f"revealing-{index}.jpg"
        selected.write_bytes(image_bytes(color))
        selection["groups"][index].update(
            files=[str(selected)], submission_rights_confirmed=True, personal_content_removed=True
        )
    write_bytes(other / "selection.json", json.dumps(selection).encode(), replace=True)
    created = prepare(other)
    assert len(created.groups) == 6
    assert "revealing-" not in (other / "prepared.json").read_text()
    with pytest.raises(PilotError, match="already_prepared"):
        prepare(other)
    prepared.groups[0].listing_text = "changed approved text"
    write_model(private / "prepared.json", prepared, replace=True)
    with pytest.raises(PilotError, match="approved_inputs_changed"):
        approved(private)


def test_cost_bound_usage_and_ordered_reuse_identity(tmp_path: Path) -> None:
    approval = setup_pilot(tmp_path)
    group = read_model(tmp_path / "prepared.json", Prepared).groups[0]
    body = pilot.request_body(
        group, [(tmp_path / f"{group.images[0].transmitted_sha256}.jpg").read_bytes()]
    )
    assert pilot.input_token_bound(body) == 922000
    changed_request = json.loads(body)
    changed_request["max_output_tokens"] = 2049
    with pytest.raises(PilotError, match="reservation_parameters_changed"):
        pilot.input_token_bound(json.dumps(changed_request).encode())
    assert read_model(tmp_path / "ledger.json", Ledger).attempts == []
    assert pilot.maximum_cost(922000) == Decimal("0.232036")
    assert pilot.maximum_cost(272000) == Decimal("0.035024")
    assert pilot.maximum_cost(272001) == Decimal("0.06953625")
    for bad in (0, 922001, True):
        with pytest.raises(PilotError, match="input_token_bound_invalid"):
            pilot.maximum_cost(bad)
    attempt = Attempt(
        group="G01",
        input_sha256="a" * 64,
        state="reserved",
        reserved_usd=pilot.maximum_cost(20000),
        input_token_bound=20000,
    )
    data = response(recognition())
    pilot.record_usage(data, attempt)
    assert attempt.estimated_usd == Decimal("0.0001345")
    assert attempt.reasoning_tokens == 50  # Already part of 100 output tokens.
    del data["usage"]["input_tokens_details"]
    pilot.record_usage(data, attempt)
    assert attempt.cached_input_tokens is None and attempt.cache_write_tokens is None
    assert attempt.estimated_usd == Decimal("0.000175")
    assert attempt.cost_basis == "upper_bound_missing_details"
    data["usage"]["output_tokens_details"]["reasoning_tokens"] = 101
    with pytest.raises(PilotError, match="usage_inconsistent"):
        pilot.record_usage(data, attempt)
    data["usage"]["output_tokens_details"]["reasoning_tokens"] = 50
    data["usage"]["input_tokens"] = 20001
    with pytest.raises(PilotError, match="exceeded_reservation"):
        pilot.record_usage(data, attempt)
    groups = read_model(tmp_path / "prepared.json", Prepared).groups
    group = groups[0].model_copy(update={"images": groups[0].images + groups[1].images})
    key = input_digest(group, pilot.protocol_digest(), approval.subset_sha256)
    for changed in [
        group.model_copy(update={"images": list(reversed(group.images))}),
        group.model_copy(update={"listing_text": "different"}),
    ]:
        assert input_digest(changed, pilot.protocol_digest(), approval.subset_sha256) != key
    assert input_digest(group, "b" * 64, approval.subset_sha256) != key
    assert input_digest(group, pilot.protocol_digest(), "c" * 64) != key


def test_raw_recognition_credits_unmapped_identity_and_reports_cost(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    approval = setup_pilot(tmp_path)
    prepared = read_model(tmp_path / "prepared.json", Prepared)
    prepared.groups[0].expected = [
        Proposal(kind="minifigure", namespace="bricklink", identifier="sw_fixture_only")
    ]
    write_model(tmp_path / "prepared.json", prepared, replace=True)
    approval.prepared_sha256 = digest((tmp_path / "prepared.json").read_bytes())
    write_model(tmp_path / "approval.json", approval, replace=True)
    approval_hash = digest((tmp_path / "approval.json").read_bytes())
    write_model(
        tmp_path / "ledger.json", Ledger(approval_sha256=approval_hash, attempts=[]), replace=True
    )
    access = json.loads((tmp_path / "model-access.json").read_bytes())
    access["approval_sha256"] = approval_hash
    write_bytes(tmp_path / "model-access.json", json.dumps(access).encode(), replace=True)
    proposed = candidate("sw_fixture_only")
    proposed.update(kind="minifigure", namespace="bricklink")
    calls = 0

    def fake(body: bytes, key: str, project: str) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return response(recognition("candidates", [proposed]) if calls == 1 else recognition())

    monkeypatch.setattr(pilot, "call_openai", fake)
    pilot.execute(tmp_path)
    stats = pilot.evaluate(tmp_path)
    assert stats["top1"] == stats["top3"] == 1
    assert stats["canonical_top1"] == stats["canonical_top3"] == 0
    assert stats["canonical_expected_resolved"] == 5 and stats["canonical_expected_unresolved"] == 1
    assert stats["responses_received"] == calls == 6
    assert stats["full_sample_completed"] is True and stats["attempted_images"] == 6
    assert Decimal(stats["average_estimated_cost_per_request_usd"]) == Decimal("0.0001345")
    assert stats["reported_billing_usd"] is None
    assert stats["reserved_usd"] == "1.392216"


def test_model_metadata_probe_is_not_inference(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    setup_pilot(tmp_path)
    (tmp_path / "model-access.json").unlink()
    seen = []

    def fake(body: bytes, key: str, project: str, *, model_check: bool = False) -> dict[str, Any]:
        seen.append((body, project, model_check))
        return {"id": MODEL, "object": "model"}

    monkeypatch.setattr(pilot, "call_openai", fake)
    pilot.check_model_access(tmp_path)
    assert seen == [(b"", "proj_fixture", True)]
    assert read_model(tmp_path / "ledger.json", Ledger).attempts == []
    assert "sk-fixture" not in (tmp_path / "model-access.json").read_text()


def test_large_mixed_lot_preserves_eight_labels_and_unscored_objects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    approval = setup_pilot(tmp_path)
    prepared = read_model(tmp_path / "prepared.json", Prepared)
    prepared.groups[0].expected = [
        Proposal(kind="set", namespace="rebrickable", identifier=f"{i}-1") for i in range(100, 108)
    ]
    prepared.groups[0].labels_exhaustive = False
    write_model(tmp_path / "prepared.json", prepared, replace=True)
    approval.prepared_sha256 = digest((tmp_path / "prepared.json").read_bytes())
    write_model(tmp_path / "approval.json", approval, replace=True)
    approval_hash = digest((tmp_path / "approval.json").read_bytes())
    write_model(
        tmp_path / "ledger.json", Ledger(approval_sha256=approval_hash, attempts=[]), replace=True
    )
    access_path = tmp_path / "model-access.json"
    access = json.loads(access_path.read_bytes())
    access["approval_sha256"] = approval_hash
    write_bytes(access_path, json.dumps(access).encode(), replace=True)
    objects = [
        recognition("candidates", [candidate(f"{i}-1")])["objects"][0] for i in range(100, 108)
    ]
    objects += [recognition()["objects"][0] for _ in range(3)]
    calls = 0

    def fake(body: bytes, key: str, project: str) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return response({"objects": objects} if calls == 1 else recognition())

    monkeypatch.setattr(pilot, "input_token_bound", lambda body: 20000)
    monkeypatch.setattr(pilot, "call_openai", fake)
    pilot.execute(tmp_path)
    stats = pilot.evaluate(tmp_path)
    assert stats["labeled_identities"] == 13
    assert stats["top1"] == stats["top3"] == 8
    assert stats["abstention_objects"] == 8
    assert stats["incorrect_confident_suggestions"] == 0
    assert len(json.loads((tmp_path / "G01-result.json").read_bytes())["objects"]) == 11
    with pytest.raises(PilotError, match="malformed"):
        pilot.parse_response(response({"objects": objects + objects[:2]}))
    truncated = response({"objects": objects})
    truncated["status"] = "incomplete"
    with pytest.raises(PilotError, match="incomplete"):
        pilot.parse_response(truncated)
