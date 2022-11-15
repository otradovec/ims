from enum import Enum


class IncidentStatus(str, Enum):
    reported = "Reported"
    confirmed = "Confirmed"
    in_progress = "In progress"
    solved = "Solved"
    cancelled = "Cancelled"

    def __int__(self):
        if self.value == IncidentStatus.reported:
            return 1
        elif self.value == IncidentStatus.confirmed:
            return 2
        elif self.value == IncidentStatus.in_progress:
            return 3
        elif self.value == IncidentStatus.solved:
            return 4
        else:  # self.value == IncidentStatus.cancelled:
            return 5


def is_opened(status: IncidentStatus) -> bool:
    return not is_closed(status)


def is_closed(status: IncidentStatus) -> bool:
    return status == IncidentStatus.solved or status == IncidentStatus.cancelled
