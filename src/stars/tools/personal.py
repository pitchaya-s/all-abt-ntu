"""Local authenticated STARS tools; never registered by the hosted server."""

from typing import Annotated, Literal, cast

from shared.operation import OperationError
from pydantic import BaseModel, Field

from ..compact import personal_fields, saved_plan_fields
from ..client import NTURequestError
from ..wish import DegreeAuditResult, SavePlanResult, StarsPlannerResult
from ..wish.models import SavedPlan


class PlannedIndex(BaseModel):
    course_code: str = Field(description="NTU undergraduate course code")
    index: str = Field(pattern=r"^[0-9]{1,12}$", description="Index number as a string")


def get_stars_planner(application, refresh: bool = False) -> StarsPlannerResult:
    """Get registered courses, the published term, and saved Plans 1–3 with indexes and timetables. Use refresh after editing a plan."""
    try:
        return cast(
            StarsPlannerResult,
            personal_fields(
                application.stars_personal.get_stars_planner(refresh=refresh)
            ),
        )
    except (NTURequestError, ValueError) as error:
        raise OperationError(str(error)) from error


def save_stars_plan(
    application,
    plan_number: Literal[1, 2, 3],
    courses: Annotated[list[PlannedIndex], Field(min_length=1, max_length=13)],
    academic_year: int,
    semester: Literal[1, 2],
) -> SavePlanResult:
    """Replace saved Plan 1, 2, or 3 with the complete supplied course/index list for the current Planner term. Omitted courses are removed from that plan. Verifies persistence by loading the saved plan. Does not perform course registration, dropping, or index swapping."""
    try:
        result = application.stars_personal.save_stars_plan(
            plan_number,
            [course.model_dump() for course in courses],
            academic_year,
            semester,
        )
        return cast(
            SavePlanResult,
            {
                **result,
                "saved_plan": cast(SavedPlan, saved_plan_fields(result["saved_plan"])),
            },
        )
    except (NTURequestError, ValueError) as error:
        raise OperationError(str(error)) from error


def get_degree_audit(application) -> DegreeAuditResult:
    """Get your degree requirements, examination results, and registered courses from Degree Audit."""
    try:
        return cast(
            DegreeAuditResult,
            personal_fields(application.stars_personal.get_degree_audit()),
        )
    except (NTURequestError, ValueError) as error:
        raise OperationError(str(error)) from error
