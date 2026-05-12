"""Semantic ambiguity gate: unresolved meaning refuses or holds before consequence."""
from .gate import evaluate, AmbiguityGate
from .models import (
    DecisionInput,
    AmbiguityFinding,
    GateResult,
    Decision,
    Severity,
)
from .receipts import build_receipt, Receipt

__all__ = [
    "evaluate",
    "AmbiguityGate",
    "DecisionInput",
    "AmbiguityFinding",
    "GateResult",
    "Decision",
    "Severity",
    "Receipt",
    "build_receipt",
]

__version__ = "0.1.0"
