"""The deterministic ambiguity gate.

Core rule: if required meaning is unresolved at the point of consequence,
return HOLD or REFUSE. Do not allow execution.

No external services. No LLM calls. No web calls. Deterministic.
"""
from __future__ import annotations

from typing import List, Iterable, Optional

from .models import (
    DecisionInput,
    AmbiguityFinding,
    GateResult,
    Decision,
    Severity,
)
from .receipts import build_receipt


# Terms whose meaning is typically unresolved at the point of consequence.
# Presence alone is a flag; severity is assigned per term.
AMBIGUOUS_TERMS = {
    "temporary": Severity.HIGH,
    "contractor": Severity.MEDIUM,
    "admin access": Severity.HIGH,
    "admin": Severity.HIGH,
    "urgent": Severity.MEDIUM,
    "limited access": Severity.MEDIUM,
    "manager approval": Severity.MEDIUM,
    "safe": Severity.MEDIUM,
    "appropriate": Severity.MEDIUM,
    "normal access": Severity.MEDIUM,
    "soon": Severity.LOW,
    "privileged": Severity.HIGH,
    "exception": Severity.MEDIUM,
}

_TERM_ISSUE = {
    "temporary": "duration is undefined",
    "contractor": "contractor identity and scope are not bound",
    "admin access": "admin rights set is not enumerated",
    "admin": "admin rights set is not enumerated",
    "urgent": "urgency is undefined and may bypass review",
    "limited access": "limit boundary is not enumerated",
    "manager approval": "approving manager identity is not bound",
    "safe": "safety criterion is undefined",
    "appropriate": "appropriateness criterion is undefined",
    "normal access": "normal access set is not enumerated",
    "soon": "timeline is undefined",
    "privileged": "privileged rights set is not enumerated",
    "exception": "exception scope is undefined",
}

_TERM_RESOLUTION = {
    "temporary": "specify start, end, and time zone",
    "contractor": "specify contractor identity, employer, contract reference",
    "admin access": "enumerate exact permissions or role binding",
    "admin": "enumerate exact permissions or role binding",
    "urgent": "state deadline and reason; do not bypass review",
    "limited access": "enumerate the limit set",
    "manager approval": "name approving manager and authority reference",
    "safe": "state safety criterion and check",
    "appropriate": "state appropriateness criterion",
    "normal access": "enumerate the normal access set",
    "soon": "specify a date/time",
    "privileged": "enumerate the privileged rights set",
    "exception": "specify scope and authority of the exception",
}


def _scan_terms(text: str) -> List[AmbiguityFinding]:
    findings: List[AmbiguityFinding] = []
    lowered = text.lower()
    seen = set()
    # Check multi-word terms first to avoid double-counting components.
    for term in sorted(AMBIGUOUS_TERMS.keys(), key=len, reverse=True):
        if term in lowered and term not in seen:
            seen.add(term)
            findings.append(
                AmbiguityFinding(
                    term=term,
                    issue=_TERM_ISSUE[term],
                    severity=AMBIGUOUS_TERMS[term],
                    required_resolution=_TERM_RESOLUTION[term],
                )
            )
    return findings


def _surface(d: DecisionInput) -> str:
    parts = [d.action, d.target, d.requested_scope]
    parts.extend(d.meaning_terms or [])
    return " ".join(p for p in parts if p)


class AmbiguityGate:
    """Deterministic gate. Evaluates a DecisionInput and returns a GateResult."""

    def evaluate(self, decision_input: DecisionInput) -> GateResult:
        findings = _scan_terms(_surface(decision_input))

        # Missing authority on any non-trivial action is a REFUSE.
        if not decision_input.authority_reference:
            return self._refuse(
                decision_input,
                findings,
                reason="authority_reference is missing; refusing before consequence",
            )

        if not findings:
            return GateResult(
                decision=Decision.ALLOW,
                allowed=True,
                reason="no ambiguity terms detected; authority present",
                findings=[],
                receipt=None,
            )

        if any(f.severity == Severity.HIGH for f in findings):
            return self._refuse(
                decision_input,
                findings,
                reason="high-severity ambiguity present; refusing before consequence",
            )
        return self._hold(
            decision_input,
            findings,
            reason="ambiguity present; holding pending resolution",
        )

    def _hold(self, d: DecisionInput, findings, reason: str) -> GateResult:
        receipt = build_receipt(d, Decision.HOLD, reason, findings)
        return GateResult(
            decision=Decision.HOLD,
            allowed=False,
            reason=reason,
            findings=findings,
            receipt=receipt,
        )

    def _refuse(self, d: DecisionInput, findings, reason: str) -> GateResult:
        receipt = build_receipt(d, Decision.REFUSE, reason, findings)
        return GateResult(
            decision=Decision.REFUSE,
            allowed=False,
            reason=reason,
            findings=findings,
            receipt=receipt,
        )


def evaluate(decision_input: DecisionInput) -> GateResult:
    """Module-level convenience."""
    return AmbiguityGate().evaluate(decision_input)
