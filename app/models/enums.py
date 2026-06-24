from enum import StrEnum


class UserRole(StrEnum):
    OWNER = "owner"
    MANAGER = "manager"
    RECEPTIONIST = "receptionist"


class DocumentStatus(StrEnum):
    UPLOADED = "uploaded"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"