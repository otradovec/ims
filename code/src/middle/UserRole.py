from enum import Enum


class UserRole(int, Enum):
    support = 1  # "Support"
    netops = 2  # "NetOps"
    manager = 3  # "Manager"
    superuser = 4  # "Superuser"
