# semantic-ambiguity-gate

A small Python proof surface showing that unresolved semantic ambiguity
should refuse before consequence.

> Semantic ambiguity is not permission.
>
> If meaning is unresolved at the point of consequence, the gate refuses
> or holds before execution.

## What this repo is

A deterministic, dependency-free Python module. Given a structured
`DecisionInput`, it returns one of `ALLOW`, `HOLD`, or `REFUSE`, and
writes a structured receipt when execution does not proceed.

No external services. No LLM calls. No web calls. No hidden state.

## What it demonstrates

- An input can be checked for unresolved meaning.
- Unresolved meaning returns `HOLD` or `REFUSE`.
- The action does not proceed.
- A structured receipt explains why and what consequence was prevented.

## What it does NOT prove

This repo is a narrow, path-local ambiguity gate. It does not prove:

- production enforcement
- enterprise readiness
- legal compliance
- certification
- full semantic understanding
- complete AI safety
- that ambiguity is solved generally

## Quick start

```bash
git clone https://github.com/LalaSkye/semantic-ambiguity-gate.git
cd semantic-ambiguity-gate
python -m pip install -e ".[test]"
python -m pytest
```

## Example input

```python
from semantic_ambiguity_gate import evaluate, DecisionInput

result = evaluate(
    DecisionInput(
        actor="manager_x",
        action="grant",
        target="production_db",
        requested_scope="temporary contractor admin access",
        authority_reference="ticket-123",
    )
)

print(result.decision.value)   # REFUSE
print(result.reason)
print(result.receipt)
```

## Example HOLD / REFUSE output

```text
decision: REFUSE
allowed: False
reason: high-severity ambiguity present; refusing before consequence
findings:
  - term: admin access
    severity: HIGH
    issue: admin rights set is not enumerated
    required_resolution: enumerate exact permissions or role binding
  - term: temporary
    severity: HIGH
    issue: duration is undefined
    required_resolution: specify start, end, and time zone
  - term: contractor
    severity: MEDIUM
    issue: contractor identity and scope are not bound
    required_resolution: specify contractor identity, employer, contract reference
receipt:
  receipt_id: rcpt_<sha256-prefix>
  decision: REFUSE
  timestamp: 2026-05-12T18:00:00+00:00
  consequence_prevented: refused 'grant' on target 'production_db' ...
```

## Claim boundary

This repo demonstrates a narrow, path-local ambiguity gate. The receipt
proves only that the gate refused at this path on this input. It does
not prove that the gate cannot be bypassed at a different layer, nor
that the receipt is legally admissible in any jurisdiction.

## Relation to execution-boundary governance

This module is intended as one path-local check that can sit in front
of a consequence-producing action. It complements (but does not replace)
identity, authority, and runtime-enforcement layers further down the
stack. The principle: unresolved meaning at the point of consequence
should fail closed, not proceed.

## License

MIT. See `LICENSE`.
