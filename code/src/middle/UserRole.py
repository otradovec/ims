from enum import Enum


class UserRole(str, Enum):
    support = "Support"
    netops = "NetOps"
    manager = "Manager"
    superuser = "Superuser"

    def __int__(self):
        if self.value == UserRole.support:
            return 1
        elif self.value == UserRole.netops:
            return 2
        elif self.value == UserRole.manager:
            return 3
        elif self.value == UserRole.superuser:
            return 4
        else:
            raise Exception("Unknown incident priority code")
