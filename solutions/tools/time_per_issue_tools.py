from typing import Annotated

from models.issue_analyzer import Complexity
from pydantic import Field


class TimePerIssueTools:

    def calculate_time_based_on_complexity(
        self,
        complexity: Annotated[Complexity, Field(description="The complexity level of the issue.")],
    ) -> str:
        """Calculate the time required based on issue complexity."""
        match complexity:
            case Complexity.NA:
                return "1 hour"
            case Complexity.LOW:
                return "2 hours"
            case Complexity.MEDIUM:
                return "4 hours"
            case Complexity.HIGH:
                return "8 hours"
            case _:
                return "Unknown complexity level"
