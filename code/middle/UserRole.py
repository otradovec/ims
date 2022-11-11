from enum import Enum


class UserRole(str, Enum):
    support = "Support"
    netops = "NetOps"
    manager = "Manager"
    superuser = "Superuser"
