"""Bounded OAI-PMH reads without automatic repository-wide harvesting."""

from ..contracts import (
    MetadataPrefix,
    OAIIdentifier,
    OAIStamp,
    Page,
    ResumptionToken,
    SetSpec,
    Size,
)


from ..models import RepositoryError
from .models import (
    OAIFormats,
    OAIIdentify,
    OAIMetadataFormat,
    OAIRecordResult,
    OAIRecords,
    OAISet,
    OAISets,
)
from .parser import NS, datestamp, pagination, record, required, xml


def identify(client, refresh: bool = False) -> OAIIdentify:
    "Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. Public metadata only."
    with client.validated("Identify", refresh=refresh) as (
        data,
        response_date,
        snapshot,
    ):
        return OAIIdentify(
            **snapshot,
            response_date=response_date,
            repository_name=required(data, "repositoryName"),
            base_url=required(data, "baseURL"),
            protocol_version=required(data, "protocolVersion"),
            admin_emails=[
                value.text.strip()
                for value in data.findall(NS + "adminEmail")
                if (value.text or "").strip()
            ],
            earliest_datestamp=datestamp(required(data, "earliestDatestamp")),
            deleted_record=required(data, "deletedRecord"),
            granularity=required(data, "granularity"),
            descriptions_xml=[xml(value) for value in data.findall(NS + "description")],
        )


def formats(
    client, identifier: OAIIdentifier | None = None, refresh: bool = False
) -> OAIFormats:
    "List OAI metadata prefixes, namespaces and schemas. Optionally supply an OAI identifier to discover formats available for one record."
    with client.validated(
        "ListMetadataFormats",
        {"identifier": identifier} if identifier else None,
        refresh,
    ) as (data, response_date, snapshot):
        return OAIFormats(
            **snapshot,
            response_date=response_date,
            formats=[
                OAIMetadataFormat(
                    metadata_prefix=required(value, "metadataPrefix"),
                    schema_url=required(value, "schema"),
                    metadata_namespace=required(value, "metadataNamespace"),
                )
                for value in data.findall(NS + "metadataFormat")
            ],
        )


def selection(metadata_prefix, set_spec, from_date, until_date, resumption_token):
    if resumption_token is not None:
        if any(
            value is not None
            for value in (metadata_prefix, set_spec, from_date, until_date)
        ):
            raise RepositoryError(
                "A resumption_token must be used alone: omit metadata_prefix, set_spec, from_date and until_date."
            )
        return {"resumptionToken": resumption_token}
    for value in (from_date, until_date):
        if value is not None:
            try:
                datestamp(value)
            except ValueError:
                raise RepositoryError(
                    "Invalid OAI date bound. Use a real YYYY-MM-DD date or UTC YYYY-MM-DDTHH:MM:SSZ timestamp."
                ) from None
    if (
        from_date
        and until_date
        and (len(from_date) != len(until_date) or from_date > until_date)
    ):
        raise RepositoryError(
            "OAI date bounds must have the same precision, with from_date no later than until_date."
        )
    return {
        key: value
        for key, value in {
            "metadataPrefix": metadata_prefix or "oai_dc",
            "set": set_spec,
            "from": from_date,
            "until": until_date,
        }.items()
        if value is not None
    }


def sets(
    client,
    resumption_token: ResumptionToken | None = None,
    limit: Size = 20,
    offset: Page = 0,
    refresh: bool = False,
) -> OAISets:
    "List OAI collection/community sets. limit/offset slice one NTU response page. Follow next_offset first, then resumption_token with offset=0. Use returned set_spec to filter OAI records."
    with client.validated(
        "ListSets",
        {"resumptionToken": resumption_token} if resumption_token else None,
        refresh,
    ) as (data, response_date, snapshot):
        values = data.findall(NS + "set")
        page = pagination(data, len(values), limit, offset)
        return OAISets(
            **snapshot,
            response_date=response_date,
            pagination=page,
            sets=[
                OAISet(
                    set_spec=required(value, "setSpec"),
                    name=required(value, "setName"),
                    descriptions_xml=[
                        xml(part) for part in value.findall(NS + "setDescription")
                    ],
                )
                for value in values[offset : offset + limit]
            ],
        )


def records(
    client,
    metadata_prefix: MetadataPrefix | None = None,
    set_spec: SetSpec | None = None,
    from_date: OAIStamp | None = None,
    until_date: OAIStamp | None = None,
    resumption_token: ResumptionToken | None = None,
    headers_only: bool = False,
    limit: Size = 10,
    offset: Page = 0,
    refresh: bool = False,
) -> OAIRecords:
    "Read one bounded OAI records page, defaulting to oai_dc. Set headers_only=true for ListIdentifiers. Dates filter inclusive modification/deletion datestamps, not publication dates; use matching precision. Follow next_offset with unchanged arguments before using the next resumption_token. A token excludes metadata_prefix, set_spec and both dates; reset offset=0 and keep headers_only unchanged. Deleted records have no metadata. No automatic bulk harvest."
    parameters = selection(
        metadata_prefix, set_spec, from_date, until_date, resumption_token
    )
    with client.validated(
        "ListIdentifiers" if headers_only else "ListRecords", parameters, refresh
    ) as (data, response_date, snapshot):
        values = data.findall(NS + ("header" if headers_only else "record"))
        page = pagination(data, len(values), limit, offset)
        return OAIRecords(
            **snapshot,
            response_date=response_date,
            headers_only=headers_only,
            pagination=page,
            records=[
                record(value, headers_only) for value in values[offset : offset + limit]
            ],
        )


def get_record(
    client,
    identifier: OAIIdentifier,
    metadata_prefix: MetadataPrefix = "oai_dc",
    refresh: bool = False,
) -> OAIRecordResult:
    "Get one record by its OAI identifier, not a REST UUID. Dublin Core returns repeated fields and language tags; other advertised formats return metadata_xml. Deleted records preserve their header without inferring metadata or file access."
    with client.validated(
        "GetRecord",
        {"identifier": identifier, "metadataPrefix": metadata_prefix},
        refresh,
    ) as (data, response_date, snapshot):
        values = data.findall(NS + "record")
        if len(values) != 1:
            raise RepositoryError(
                "DR-NTU returned an unexpected number of OAI records."
            )
        result = record(values[0])
        if result.identifier != identifier:
            raise RepositoryError(
                "DR-NTU returned a different OAI identifier; no record was inferred."
            )
        return OAIRecordResult(
            **snapshot,
            response_date=response_date,
            metadata_prefix=metadata_prefix,
            record=result,
        )
