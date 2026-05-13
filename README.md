# semantic-ambiguity-gate

## Public disclosure boundary

This repository is a public inspection surface, not full architecture disclosure.

It shows a bounded claim, a minimal evidence object, an inspection path, and the claim limit.

See [`PUBLIC_DISCLOSURE_BOUNDARY.md`](PUBLIC_DISCLOSURE_BOUNDARY.md).

## What this repo is

A small deterministic Python proof surface showing one narrow claim:

> Unresolved semantic ambiguity can trigger HOLD / REFUSE rather than silently proceeding.

No external services. No LLM calls. No web calls.

## What it demonstrates

On the demonstrated path:

- an input can be checked for unresolved meaning
- unresolved meaning returns `HOLD` or `REFUSE`
- the action does not proceed
- a structured receipt explains why and what consequence was prevented

## What it does NOT prove

This repo is a narrow, path-local ambiguity gate.

It does not prove:

- production enforcement
- enterprise readiness
- legal compliance
- certification
- full semantic understanding
- complete AI safety
- that ambiguity is solved generally
- the wider execution-boundary governance architecture

## Quick start

```bash
git clone https://github.com/LalaSkye/semantic-ambiguity-gate.git
cd semantic-ambiguity-gate
python -m pip install -e ".[test]"
python -m pytest
```

## Inspection path

Run the tests and inspect the demonstrated HOLD / REFUSE behaviour.

The narrow question this repo answers is:

**Can unresolved meaning prevent the demonstrated action from proceeding?**

Expected answer:

**Yes.**

## Example result shape

```text
decision: REFUSE
allowed: False
reason: high-severity ambiguity present; refusing before consequence
receipt_written: true
```

## Claim boundary

This repo proves only that the demonstrated path refused or held on unresolved semantic ambiguity for the tested inputs.

It does not prove that the gate cannot be bypassed at another layer, nor that the receipt is legally admissible in any jurisdiction.

## Relation to wider work

This is one local proof object.

It should not be treated as proof of the whole system.

## License

MIT. See `LICENSE`.
