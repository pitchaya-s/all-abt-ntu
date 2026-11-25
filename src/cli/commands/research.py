"""Research service commands."""

from typing import Annotated, Literal, Optional

from functools import partial

import typer

from ..helpers import group, parse_json
from ..execution import application_scope
from ..services import invoke
from ..renderers import research as views

app = typer.Typer(
    no_args_is_help=True, help="Search and browse the DR-NTU research repository."
)
g_browse = group(default=False)
app.add_typer(
    g_browse, name="browse", help="Browse repository communities and collections."
)
g_bundle = group(default=False)
app.add_typer(g_bundle, name="bundle", help="Inspect research file bundles.")
g_item = group(default=True)
app.add_typer(g_item, name="item", help="Read a repository item or its bundles.")
g_oai = group(default=False)
app.add_typer(g_oai, name="oai", help="Use the repository OAI-PMH interface.")


@app.command("search")
def cmd_search(
    query: str = typer.Argument(..., help="Search text or keywords."),
    scope_id: Optional[str] = typer.Option(
        None,
        "--scope",
        help="The scope ID returned by the relevant listing or details command.",
    ),
    entity_type: Annotated[
        Literal["Publication", "Person", "all"],
        typer.Option(
            help="The kind of repository entity to search. Choices: Publication, Person, all. Default: Publication."
        ),
    ] = "Publication",
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON value."),
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 10.")
    ] = 10,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search DR-NTU publications by keywords or Solr query."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.search, application.research),
            {
                "query": query,
                "scope_id": scope_id,
                "entity_type": entity_type,
                "filters": (parse_json(filters) if filters is not None else None),
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
            presenter=views.search,
        )


@g_item.command("__default__", hidden=True)
def cmd_item_default(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.get_item, application.research),
            {"item_id": item_id, "refresh": refresh},
            json_output,
            presenter=views.item_default,
        )


@g_browse.command("communities")
def cmd_browse_communities(
    community_id: Optional[str] = typer.Option(
        None,
        "--community",
        help="The community ID returned by the relevant listing or details command.",
    ),
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 20.")
    ] = 20,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Browse repository communities or collections."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.browse, application.research),
            {
                "community_id": community_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
                "kind": "communities",
            },
            json_output,
            presenter=views.browse_communities,
        )


@g_browse.command("collections")
def cmd_browse_collections(
    community_id: Optional[str] = typer.Option(
        None,
        "--community",
        help="The community ID returned by the relevant listing or details command.",
    ),
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 20.")
    ] = 20,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Browse repository communities or collections."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.browse, application.research),
            {
                "community_id": community_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
                "kind": "collections",
            },
            json_output,
            presenter=views.browse_collections,
        )


@app.command("facets")
def cmd_facets(
    facet: Annotated[
        Optional[str],
        typer.Option(
            help="The facet name to inspect; omit it to discover available facets."
        ),
    ] = None,
    query: Annotated[
        str,
        typer.Option(
            help="The search terms. Quote multiword text so the shell passes it as one argument."
        ),
    ] = "",
    scope_id: Optional[str] = typer.Option(
        None,
        "--scope",
        help="The scope ID returned by the relevant listing or details command.",
    ),
    entity_type: Annotated[
        Literal["Publication", "Person", "all"],
        typer.Option(
            help="The kind of repository entity to search. Choices: Publication, Person, all. Default: Publication."
        ),
    ] = "Publication",
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON value."),
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 10.")
    ] = 10,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.get_facets, application.research),
            {
                "facet": facet,
                "query": query,
                "scope_id": scope_id,
                "entity_type": entity_type,
                "filters": (parse_json(filters) if filters is not None else None),
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
            presenter=views.facets,
        )


@g_item.command("bundles")
def cmd_item_bundles(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 20.")
    ] = 20,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List an item's file groups."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.list_bundles, application.research),
            {
                "item_id": item_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
            presenter=views.item_bundles,
        )


@g_bundle.command("files")
def cmd_bundle_files(
    bundle_id: Annotated[
        str,
        typer.Argument(
            help="The bundle ID returned by the relevant listing or details command."
        ),
    ],
    page: int = typer.Option(0, "--page", "-p", help="Result page number."),
    page_size: Annotated[
        int, typer.Option(help="Maximum number of results in a page. Default: 20.")
    ] = 20,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs."""
    with application_scope() as application:
        from services.drntu.rest import repository

        return invoke(
            partial(repository.list_files, application.research),
            {
                "bundle_id": bundle_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
            presenter=views.bundle_files,
        )


@app.command("dataset")
def cmd_dataset(
    persistent_id: Annotated[
        str, typer.Argument(help="The persistent identifier or DOI of the dataset.")
    ],
    version: Annotated[
        Optional[str],
        typer.Option(
            help="The requested dataset version; omit it for the service default."
        ),
    ] = None,
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory."""
    with application_scope() as application:
        from services.drntu.rest import datasets

        return invoke(
            partial(datasets.get_dataset, application.research),
            {
                "persistent_id": persistent_id,
                "version": version,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.dataset,
        )


@g_oai.command("info")
def cmd_oai_info(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp."""
    with application_scope() as application:
        from services.drntu import oai

        return invoke(
            partial(oai.identify, application.research_oai),
            {"refresh": refresh},
            json_output,
            presenter=views.oai_info,
        )


@g_oai.command("formats")
def cmd_oai_formats(
    identifier: Optional[str] = typer.Argument(
        None, help="The OAI identifier for the requested record."
    ),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List OAI metadata prefixes, namespaces and schemas."""
    with application_scope() as application:
        from services.drntu import oai

        return invoke(
            partial(oai.formats, application.research_oai),
            {"identifier": identifier, "refresh": refresh},
            json_output,
            presenter=views.oai_formats,
        )


@g_oai.command("sets")
def cmd_oai_sets(
    resumption_token: Optional[str] = typer.Option(
        None, "--token", help="The continuation token returned by the OAI server."
    ),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """List OAI collection/community sets."""
    with application_scope() as application:
        from services.drntu import oai

        return invoke(
            partial(oai.sets, application.research_oai),
            {
                "resumption_token": resumption_token,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.oai_sets,
        )


@g_oai.command("records")
def cmd_oai_records(
    metadata_prefix: Optional[str] = typer.Option(
        None, "--prefix", help="The OAI metadata format prefix, such as oai_dc."
    ),
    set_spec: Optional[str] = typer.Option(
        None, "--set", help="The OAI set identifier returned by the sets listing."
    ),
    from_date: Annotated[
        Optional[str], typer.Option(help="Start of the date range in ISO format.")
    ] = None,
    until_date: Annotated[
        Optional[str], typer.Option(help="End of the date range in ISO format.")
    ] = None,
    resumption_token: Optional[str] = typer.Option(
        None,
        "--token",
        help="Continue with a token from the previous page. Omit prefix, set, date and offset options.",
    ),
    headers_only: bool = typer.Option(
        False,
        "--headers-only",
        help="List record headers instead of full OAI metadata.",
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read one bounded OAI records page, defaulting to oai_dc."""
    with application_scope() as application:
        from services.drntu import oai

        return invoke(
            partial(oai.records, application.research_oai),
            {
                "metadata_prefix": metadata_prefix,
                "set_spec": set_spec,
                "from_date": from_date,
                "until_date": until_date,
                "resumption_token": resumption_token,
                "headers_only": headers_only,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
            presenter=views.oai_records,
        )


@g_oai.command("record")
def cmd_oai_record(
    identifier: Annotated[
        str, typer.Argument(help="The OAI identifier for the requested record.")
    ],
    metadata_prefix: str = typer.Option(
        "oai_dc",
        "--prefix",
        help="The OAI metadata format prefix, such as oai_dc. Default: oai_dc.",
    ),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Get one record by its OAI identifier, not a REST UUID."""
    with application_scope() as application:
        from services.drntu import oai

        return invoke(
            partial(oai.get_record, application.research_oai),
            {
                "identifier": identifier,
                "metadata_prefix": metadata_prefix,
                "refresh": refresh,
            },
            json_output,
            presenter=views.oai_record,
        )


g_item.command("show")(cmd_item_default)
