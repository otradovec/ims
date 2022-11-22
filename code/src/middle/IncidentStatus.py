from enum import Enum


class IncidentStatus(str, Enum):
    reported = "Reported"
    confirmed = "Confirmed"
    in_progress = "In progress"
    for_review = "For review"
    solved = "Solved"
    cancelled = "Cancelled"

    def __int__(self):
        if self.value == IncidentStatus.reported:
            return 1
        elif self.value == IncidentStatus.confirmed:
            return 2
        elif self.value == IncidentStatus.in_progress:
            return 3
        elif self.value == IncidentStatus.for_review:
            return 4
        elif self.value == IncidentStatus.solved:
            return 5
        elif self.value == IncidentStatus.cancelled:
            return 6
        else:
            raise Exception("Unknown incident code")


def is_opened(status: IncidentStatus) -> bool:
    return not is_closed(status)


def is_closed(status: IncidentStatus) -> bool:
    return status == IncidentStatus.solved or status == IncidentStatus.cancelled
