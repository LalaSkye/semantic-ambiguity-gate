"""Proof tests for the ambiguity gate.

Run with:
    python -m pytest
"""
from semantic_ambiguity_gate import (
    evaluate,
    DecisionInput,
    Decision,
    Severity,
)


def _mk(action="read", target="public_doc", scope="read-only",
        authority="ticket-001", terms=None):
    return DecisionInput(
        actor="alice",
        action=action,
        target=target,
        requested_scope=scope,
        meaning_terms=terms or [],
        context={},
        authority_reference=authority,
    )


def test_clear_low_risk_allows():
    result = evaluate(_mk())
    assert result.decision == Decision.ALLOW
    assert result.allowed is True
    assert result.receipt is None


def test_temporary_contractor_admin_access_refuses():
    d = _mk(
        action="grant",
        target="production_db",
        scope="temporary contractor admin access",
    )
    result = evaluate(d)
    assert result.decision == Decision.REFUSE
    assert result.allowed is False
    assert any(f.term == "admin access" for f in result.findings)
    assert result.receipt is not None


def test_missing_authority_refuses():
    d = _mk(authority=None)
    result = evaluate(d)
    assert result.decision == Decision.REFUSE
    assert result.allowed is False
    assert "authority" in result.reason.lower()


def test_ambiguous_duration_holds():
    d = _mk(
        action="send",
        target="weekly_report",
        scope="send report soon",
    )
    result = evaluate(d)
    assert result.decision == Decision.HOLD
    assert result.allowed is False
    assert any(f.term == "soon" for f in result.findings)


def test_receipt_created_on_hold():
    d = _mk(
        action="send",
        target="weekly_report",
        scope="send report soon",
    )
    result = evaluate(d)
    assert result.decision == Decision.HOLD
    assert result.receipt is not None
    assert result.receipt["decision"] == "HOLD"
    assert result.receipt["receipt_id"].startswith("rcpt_")


def test_receipt_created_on_refuse():
    d = _mk(
        action="grant",
        target="production_db",
        scope="temporary admin access",
    )
    result = evaluate(d)
    assert result.decision == Decision.REFUSE
    assert result.receipt is not None
    assert result.receipt["decision"] == "REFUSE"
    assert "consequence_prevented" in result.receipt


def test_no_allow_when_high_severity_ambiguity_exists():
    d = _mk(
        action="grant",
        target="prod",
        scope="privileged admin access",
    )
    result = evaluate(d)
    assert result.decision != Decision.ALLOW
    assert result.allowed is False
