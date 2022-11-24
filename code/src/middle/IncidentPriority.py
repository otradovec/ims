from enum import Enum


class IncidentPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

    def __int__(self):
        if self.value == IncidentPriority.low:
            return -2
        elif self.value == IncidentPriority.medium:
            return 0
        elif self.value == IncidentPriority.high:
            return 2
        else:
            raise Exception("Unknown incident priority code")

