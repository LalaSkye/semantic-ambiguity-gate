"""Data models for the semantic ambiguity gate.

Deterministic. No external services. No LLM calls.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class Decision(str, Enum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"
    REFUSE = "REFUSE"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class DecisionInput:
    actor: str
    action: str
    target: str
    requested_scope: str
    meaning_terms: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    authority_reference: Optional[str] = None


@dataclass(frozen=True)
class AmbiguityFinding:
    term: str
    issue: str
    severity: Severity
    required_resolution: str


@dataclass
class GateResult:
    decision: Decision
    allowed: bool
    reason: str
    findings: List[AmbiguityFinding] = field(default_factory=list)
    receipt: Optional[Dict[str, Any]] = None
