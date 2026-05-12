"""Structured refusal receipts.

A receipt proves: what was attempted, what was unresolved,
why execution did not proceed, what consequence was prevented.
Deterministic. Receipt IDs are derived from inputs (no randomness).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable, Dict, Any, List

from .models import DecisionInput, AmbiguityFinding, Decision


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    decision: str
    actor: str
    action: str
    target: str
    reason: str
    findings: List[Dict[str, Any]]
    timestamp: str
    consequence_prevented: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _now_iso(now: datetime = None) -> str:
    if now is None:
        now = datetime.now(timezone.utc)
    return now.replace(microsecond=0).isoformat()


def _consequence_phrase(d: DecisionInput, decision: Decision) -> str:
    if decision == Decision.REFUSE:
        verb = "refused"
    else:
        verb = "held"
    return (
        f"{verb} {d.action!r} on target {d.target!r} "
        f"with requested_scope {d.requested_scope!r}"
    )


def _receipt_id(d: DecisionInput, decision: Decision, timestamp: str) -> str:
    payload = json.dumps(
        {
            "actor": d.actor,
            "action": d.action,
            "target": d.target,
            "requested_scope": d.requested_scope,
            "authority": d.authority_reference,
            "decision": decision.value,
            "timestamp": timestamp,
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"rcpt_{digest[:16]}"


def build_receipt(
    decision_input: DecisionInput,
    decision: Decision,
    reason: str,
    findings: Iterable[AmbiguityFinding],
    now: datetime = None,
) -> Dict[str, Any]:
    timestamp = _now_iso(now)
    findings_list = [
        {
            "term": f.term,
            "issue": f.issue,
            "severity": f.severity.value,
            "required_resolution": f.required_resolution,
        }
        for f in findings
    ]
    receipt = Receipt(
        receipt_id=_receipt_id(decision_input, decision, timestamp),
        decision=decision.value,
        actor=decision_input.actor,
        action=decision_input.action,
        target=decision_input.target,
        reason=reason,
        findings=findings_list,
        timestamp=timestamp,
        consequence_prevented=_consequence_phrase(decision_input, decision),
    )
    return receipt.to_dict()
