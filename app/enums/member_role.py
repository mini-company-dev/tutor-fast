from enum import Enum


class MEMBER_ROLE(str, Enum):
    USER = "User"
    TUTOR = "Tutor"
    ADMIN = "Admin"
