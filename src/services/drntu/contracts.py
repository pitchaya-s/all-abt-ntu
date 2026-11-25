"""Shared input constraints for DR-NTU operations."""

from typing import Annotated, Literal

from pydantic import Field

from .rest.models import SearchFilter


UUID = Annotated[
    str,
    Field(
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    ),
]

Query = Annotated[str, Field(max_length=500)]

Page = Annotated[int, Field(ge=0, le=100000, strict=True)]

Size = Annotated[int, Field(ge=1, le=50, strict=True)]

Filters = Annotated[list[SearchFilter], Field(max_length=10)]

Entity = Literal["Publication", "Person", "all"]

FacetName = Annotated[str, Field(pattern=r"^[A-Za-z][A-Za-z0-9_.-]{0,79}$")]

DOI = Annotated[str, Field(pattern=r"^doi:10\.[0-9]{4,9}/[^\s?#]+$", max_length=250)]

Version = Annotated[str, Field(pattern=r"^[0-9]+\.[0-9]+$", max_length=20)]

OAIIdentifier = Annotated[
    str, Field(pattern=r"^oai:dr\.ntu\.edu\.sg:[^\s\x00-\x1f\x7f]+$", max_length=500)
]

MetadataPrefix = Annotated[str, Field(pattern=r"^[A-Za-z0-9_.-]+$", max_length=100)]

SetSpec = Annotated[str, Field(pattern=r"^[^\s\x00-\x1f\x7f]+$", max_length=500)]

ResumptionToken = Annotated[
    str, Field(min_length=1, max_length=8192, pattern=r"^[^\x00-\x1f\x7f]+$")
]

OAIStamp = Annotated[
    str,
    Field(
        pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        description="Inclusive OAI modification datestamp, in UTC; not a publication date",
    ),
]
