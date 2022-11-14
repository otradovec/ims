from enum import Enum


class IncidentStatus(str, Enum):
    reported = "Reported"
    confirmed = "Confirmed"
    in_progress = "In progress"
    solved = "Solved"
    cancelled = "Cancelled"


def is_opened(status: IncidentStatus) -> bool:
    return not is_closed(status)


def is_closed(status: IncidentStatus) -> bool:
    return status == IncidentStatus.solved or status == IncidentStatus.cancelled
