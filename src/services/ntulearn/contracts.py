"""Shared NTULearn input constraints for clients and workflows."""

from typing import Annotated

from pydantic import Field

ID = r"[A-Za-z0-9_-]{1,80}"
PageSize = Annotated[int, Field(ge=1, le=100, strict=True)]
Offset = Annotated[int, Field(ge=0, strict=True)]
LearnID = Annotated[
    str, Field(pattern=f"^{ID}$", description="NTULearn ID returned by another tool")
]
CourseReference = Annotated[
    str,
    Field(
        pattern=f"^{ID}$", description="Blackboard course ID or enrolled course code"
    ),
]
CourseIDs = Annotated[list[CourseReference], Field(min_length=1, max_length=100)]
RequestBudget = Annotated[int, Field(ge=1, le=200, strict=True)]
Depth = Annotated[int, Field(ge=1, le=10, strict=True)]
Nodes = Annotated[int, Field(ge=1, le=5000, strict=True)]
Results = Annotated[int, Field(ge=1, le=200, strict=True)]
Query = Annotated[str, Field(min_length=1, max_length=200)]
