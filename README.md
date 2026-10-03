# Operational Workflow Engine

A small, production-minded reference implementation for turning a fragile manual process into an observable operational workflow.

The project models a common business pattern: **intake → validation → rules → state transition → exception handling → action → audit trail**.

It is intentionally domain-neutral and uses synthetic data. The goal is to demonstrate system design, not a client implementation.

## Why this exists

Operational problems are rarely solved by adding one more automation. Reliable systems need explicit states, business rules, exception paths and traceability.

This repository demonstrates the **Workflow → System → Automation → AI** approach I use when designing internal tools.

## Architecture

```text
Request / Intake
      ↓
Validation
      ↓
Workflow Engine ─────→ Exception Queue
      ↓                     ↓
Business Rules         Human Resolution
      ↓                     ↓
State Transition ←──────────┘
      ↓
Action Dispatcher
      ↓
Audit Log
```

## What it demonstrates

- explicit workflow states and allowed transitions
- deterministic business rules separated from orchestration
- validation before execution
- exceptions routed instead of silently failing
- append-only audit events
- synthetic examples that are safe to publish

## Quick start

Requires Python 3.10+.

```bash
python src/workflow_engine.py
```

## Example

A request starts as `NEW`. Valid input moves to `READY`; a high-risk request is routed to `REVIEW`; approved work moves through `PROCESSING` to `COMPLETED`. Invalid transitions are rejected and recorded.

## Design principle

> I don't start with the tool. I start with the workflow.

## Related

- [Portfolio](https://mariacastano.co/)
- [Internal Tools & Operational Systems](https://mariacastano.co/internal-tools/)
- [When Should a Spreadsheet Become a Custom Web App?](https://mariacastano.co/insights/spreadsheet-to-custom-web-app/)

Built by **María Isabel Castaño — AI Systems Developer | Web Apps, APIs & Automation**.
