"""Published Dataverse citation metadata and file inventories, without login."""

from typing import Annotated
from pydantic import Field
from ..contracts import DOI, Size, Version


from ..models import RepositoryError
from .models import Checksum, Dataset, DatasetFile
from .parser import records


def get_dataset(
    client,
    persistent_id: DOI,
    version: Version | None = None,
    limit: Size = 50,
    offset: Annotated[int, Field(ge=0, strict=True)] = 0,
    refresh: bool = False,
) -> Dataset:
    "Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. Omit version for latest, or use a release such as 1.0. CAPTCHA/access denials are returned as actionable errors without bypass or login."
    path = "/api/datasets/:persistentId"
    if version:
        path += "/versions/" + version
    with client.validated(
        path, {"persistentId": persistent_id}, dataset=True, refresh=refresh
    ) as (data, snapshot):
        if data.get("status") != "OK":
            raise RepositoryError(
                "DR-NTU (Data) did not return a public dataset; check its DOI and access permissions."
            )
        root = data["data"]
        current = root if version else root["latestVersion"]
        actual_version = (
            str(current["versionNumber"]) + "." + str(current["versionMinorNumber"])
        )
        if current["datasetPersistentId"].casefold() != persistent_id.casefold() or (
            version is not None and actual_version != version
        ):
            raise RepositoryError(
                "DR-NTU (Data) returned a different dataset or version."
            )
        if current["versionState"] != "RELEASED":
            raise RepositoryError(
                "Only publicly released dataset versions are supported."
            )
        fields = {
            v["typeName"]: v
            for v in records(current["metadataBlocks"]["citation"]["fields"])
        }
        authors = [
            v["authorName"]["value"]
            for v in records(fields.get("author", {}).get("value", []))
        ]
        descriptions = [
            v["dsDescriptionValue"]["value"]
            for v in records(fields.get("dsDescription", {}).get("value", []))
        ]
        raw_files = records(current["files"])
        files = []
        for value in raw_files[offset : offset + limit]:
            file = value["dataFile"]
            checksum = file.get("checksum")
            files.append(
                DatasetFile(
                    file_id=file["id"],
                    name=file["filename"],
                    directory=value.get("directoryLabel"),
                    media_type=file.get("contentType"),
                    size_bytes=file.get("filesize"),
                    restricted=value.get("restricted"),
                    checksum=Checksum(
                        algorithm=checksum["type"], value=checksum["value"]
                    )
                    if checksum
                    else None,
                )
            )
        license = current.get("license") or {}
        return Dataset(
            persistent_id=current["datasetPersistentId"],
            dataset_id=current["datasetId"],
            version=actual_version,
            version_state=current["versionState"],
            title=fields.get("title", {}).get("value"),
            authors=authors,
            descriptions=descriptions,
            subjects=fields.get("subject", {}).get("value", []),
            publication_date=current.get("publicationDate"),
            license_name=license.get("name"),
            license_url=license.get("uri"),
            url="https://doi.org/" + persistent_id[4:],
            files=files,
            total_files=len(raw_files),
            next_offset=offset + limit if offset + limit < len(raw_files) else None,
            **snapshot,
        )
