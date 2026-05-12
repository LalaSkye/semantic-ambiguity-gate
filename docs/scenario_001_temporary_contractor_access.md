# Scenario 001 — Temporary contractor admin access

## Request
A manager asks an AI workflow to:

> "Give the temporary contractor admin access."

## Why the gate must not execute

The sentence contains terms whose meaning is unresolved at the point
of consequence. Each must be resolved before any access mutation:

| Term | Question that must be answered |
|------|-------------------------------|
| `temporary` | What does temporary mean? Start, end, time zone? |
| `contractor` | Who is the contractor? Identity, employer, contract reference? |
| `admin access` | What admin rights are included? Enumerate the permission set. |
| (authority) | Who authorised this? Reference a ticket, policy, or signed approval. |
| (expiry) | When does access expire and how is revocation enforced? |
| (target system) | Which system is affected? Production, staging, sandbox? |
| (receipt) | What receipt is written if the gate refuses? |

## Expected outcome

- The gate returns `REFUSE` (high-severity ambiguity in `admin access`).
- If authority is also missing, the gate returns `REFUSE` for authority.
- A structured receipt is written, naming the unresolved terms and
  the consequence that was prevented.
- No access change occurs.

## Example

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

assert result.decision.value == "REFUSE"
assert result.receipt is not None
```

## Claim limit

This scenario demonstrates only that the gate refuses or holds
when meaning is unresolved. It does not demonstrate enterprise
integration, runtime enforcement at the OS or IAM layer, or
legal sufficiency of the receipt as evidence.
