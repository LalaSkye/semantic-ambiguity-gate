"""Tests for receipt construction."""
from datetime import datetime, timezone

from semantic_ambiguity_gate import DecisionInput, Decision, Severity
from semantic_ambiguity_gate.receipts import build_receipt
from semantic_ambiguity_gate.models import AmbiguityFinding


def _d():
    return DecisionInput(
        actor="alice",
        action="grant",
        target="production_db",
        requested_scope="temporary admin access",
        meaning_terms=[],
        context={},
        authority_reference="ticket-002",
    )


def test_receipt_fields_present():
    findings = [
        AmbiguityFinding(
            term="temporary",
            issue="duration is undefined",
            severity=Severity.HIGH,
            required_resolution="specify start, end, and time zone",
        )
    ]
    r = build_receipt(_d(), Decision.REFUSE, "reason here", findings)
    for k in (
        "receipt_id",
        "decision",
        "actor",
        "action",
        "target",
        "reason",
        "findings",
        "timestamp",
        "consequence_prevented",
    ):
        assert k in r, f"missing key: {k}"
    assert r["decision"] == "REFUSE"
    assert r["findings"][0]["term"] == "temporary"
    assert r["findings"][0]["severity"] == "HIGH"


def test_receipt_id_is_deterministic():
    fixed = datetime(2026, 5, 12, 18, 0, 0, tzinfo=timezone.utc)
    r1 = build_receipt(_d(), Decision.REFUSE, "r", [], now=fixed)
    r2 = build_receipt(_d(), Decision.REFUSE, "r", [], now=fixed)
    assert r1["receipt_id"] == r2["receipt_id"]
    assert r1["timestamp"] == "2026-05-12T18:00:00+00:00"
