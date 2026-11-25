"""Terminal views for DR-NTU commands."""

from .common import detail, details, listing, pagination, table

search = listing(
    "Research", "items", ("item_id", "title", "authors", "dates_issued", "url")
)
item_default = detail(
    "Research item",
    (
        "item_id",
        "title",
        "entity_type",
        "url",
        "last_modified",
        "withdrawn",
        "metadata",
    ),
)
browse_communities = listing(
    "Communities", "containers", ("container_id", "name", "archived_items_count", "url")
)
browse_collections = listing(
    "Collections", "containers", ("container_id", "name", "archived_items_count", "url")
)
item_bundles = listing("Bundles", "bundles", ("bundle_id", "name"))
bundle_files = listing(
    "Files", "files", ("file_id", "name", "size_bytes", "rights", "content_url")
)
oai_info = detail(
    "OAI repository",
    (
        "repository_name",
        "base_url",
        "protocol_version",
        "admin_emails",
        "earliest_datestamp",
        "deleted_record",
        "granularity",
        "descriptions_xml",
    ),
)
oai_formats = listing(
    "Metadata formats",
    "formats",
    ("metadata_prefix", "schema_url", "metadata_namespace"),
)
oai_sets = listing("Repository sets", "sets", ("set_spec", "name"))
oai_record = detail(
    "Record",
    (
        "identifier",
        "datestamp",
        "deleted",
        "set_specs",
        "metadata",
        "metadata_xml",
        "about_xml",
    ),
    nested="record",
)


def oai_records(console, data):
    records = data.get("records") or []
    if data.get("headers_only"):
        table(
            console,
            "Records",
            records,
            ("identifier", "datestamp", "deleted", "set_specs"),
        )
    elif not records:
        console.print("Records: No results.")
    else:
        for record in records:
            details(
                console,
                record.get("identifier") or "Record",
                record,
                (
                    "datestamp",
                    "deleted",
                    "set_specs",
                    "metadata",
                    "metadata_xml",
                    "about_xml",
                ),
            )
    pagination(console, data)


def facets(console, data):
    if data.get("definitions"):
        table(console, "Facets", data["definitions"], ("name", "facet_type"))
    if data.get("values"):
        table(
            console, "Facet values", data["values"], ("label", "count", "authority_key")
        )
    if not data.get("definitions") and not data.get("values"):
        console.print("Facets: No results.")
    pagination(console, data)


def dataset(console, data):
    details(
        console,
        "Dataset",
        data,
        (
            "persistent_id",
            "title",
            "version",
            "version_state",
            "authors",
            "descriptions",
            "subjects",
            "publication_date",
            "license_name",
            "license_url",
            "url",
        ),
    )
    table(
        console,
        "Files",
        data.get("files"),
        ("file_id", "name", "directory", "media_type", "size_bytes", "restricted"),
    )
    pagination(console, data)
