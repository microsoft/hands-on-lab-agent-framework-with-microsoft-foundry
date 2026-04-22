from enum import Enum

from pydantic import BaseModel


class Complexity(str, Enum):
    NA = "NA"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class IssueAnalyzer(BaseModel):
    """Information about an issue."""
    title: str | None
    description: str | None
    reason: str | None
    complexity: Complexity | None
    time_estimate_hours: str | None
