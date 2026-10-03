from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List


class State(str, Enum):
    NEW = "NEW"
    READY = "READY"
    REVIEW = "REVIEW"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


ALLOWED = {
    State.NEW: {State.READY, State.REJECTED},
    State.READY: {State.REVIEW, State.PROCESSING},
    State.REVIEW: {State.PROCESSING, State.REJECTED},
    State.PROCESSING: {State.COMPLETED},
    State.COMPLETED: set(),
    State.REJECTED: set(),
}


@dataclass
class AuditEvent:
    at: str
    request_id: str
    from_state: str
    to_state: str
    reason: str


@dataclass
class WorkRequest:
    request_id: str
    amount: float
    source: str
    state: State = State.NEW
    audit: List[AuditEvent] = field(default_factory=list)


def transition(item: WorkRequest, target: State, reason: str) -> None:
    if target not in ALLOWED[item.state]:
        raise ValueError(f"Invalid transition: {item.state} -> {target}")
    previous = item.state
    item.state = target
    item.audit.append(AuditEvent(
        at=datetime.now(timezone.utc).isoformat(),
        request_id=item.request_id,
        from_state=previous.value,
        to_state=target.value,
        reason=reason,
    ))


def validate(item: WorkRequest) -> None:
    if not item.request_id or item.amount <= 0 or not item.source:
        transition(item, State.REJECTED, "Input validation failed")
        return
    transition(item, State.READY, "Input validated")


def route(item: WorkRequest) -> None:
    if item.state != State.READY:
        return
    if item.amount >= 5000:
        transition(item, State.REVIEW, "Risk threshold requires human review")
    else:
        transition(item, State.PROCESSING, "Deterministic rules passed")


def approve_review(item: WorkRequest) -> None:
    transition(item, State.PROCESSING, "Human review approved")


def complete(item: WorkRequest) -> None:
    transition(item, State.COMPLETED, "Downstream action completed")


if __name__ == "__main__":
    request = WorkRequest("REQ-1042", 7200, "web-form")
    validate(request)
    route(request)
    if request.state == State.REVIEW:
        approve_review(request)
    complete(request)

    print(f"{request.request_id}: {request.state.value}")
    for event in request.audit:
        print(event)
