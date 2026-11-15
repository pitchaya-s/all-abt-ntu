"""Research service commands."""

from typing import Literal, Optional

from functools import partial

import typer

from ..helpers import group, parse_json
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_browse = group(default=False)
app.add_typer(g_browse, name="browse")
g_bundle = group(default=False)
app.add_typer(g_bundle, name="bundle")
g_item = group(default=True)
app.add_typer(g_item, name="item")
g_oai = group(default=False)
app.add_typer(g_oai, name="oai")


@app.command("search")
def cmd_search(
    query: str,
    scope_id: Optional[str] = typer.Option(None, "--scope"),
    entity_type: Literal["Publication", "Person", "all"] = "Publication",
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON value."),
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 10,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search DR-NTU publications by keywords or Solr query."""
    with application_scope() as application:
        from drntu.rest import repository

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
        )


@g_item.command("__default__", hidden=True)
def cmd_item_default(
    item_id: str,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied."""
    with application_scope() as application:
        from drntu.rest import repository

        return invoke(
            partial(repository.get_item, application.research),
            {"item_id": item_id, "refresh": refresh},
            json_output,
        )


@g_browse.command("communities")
def cmd_browse_communities(
    community_id: Optional[str] = typer.Option(None, "--community"),
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 20,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Browse repository communities or collections."""
    with application_scope() as application:
        from drntu.rest import repository

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
        )


@g_browse.command("collections")
def cmd_browse_collections(
    community_id: Optional[str] = typer.Option(None, "--community"),
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 20,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Browse repository communities or collections."""
    with application_scope() as application:
        from drntu.rest import repository

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
        )


@app.command("facets")
def cmd_facets(
    facet: Optional[str] = None,
    query: str = "",
    scope_id: Optional[str] = typer.Option(None, "--scope"),
    entity_type: Literal["Publication", "Person", "all"] = "Publication",
    filters: Optional[str] = typer.Option(None, "--filters", help="JSON value."),
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 10,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters."""
    with application_scope() as application:
        from drntu.rest import repository

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
        )


@g_item.command("bundles")
def cmd_item_bundles(
    item_id: str,
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 20,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List an item's file groups."""
    with application_scope() as application:
        from drntu.rest import repository

        return invoke(
            partial(repository.list_bundles, application.research),
            {
                "item_id": item_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
        )


@g_bundle.command("files")
def cmd_bundle_files(
    bundle_id: str,
    page: int = typer.Option(0, "--page", "-p"),
    page_size: int = 20,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs."""
    with application_scope() as application:
        from drntu.rest import repository

        return invoke(
            partial(repository.list_files, application.research),
            {
                "bundle_id": bundle_id,
                "page": page,
                "page_size": page_size,
                "refresh": refresh,
            },
            json_output,
        )


@app.command("dataset")
def cmd_dataset(
    persistent_id: str,
    version: Optional[str] = None,
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory."""
    with application_scope() as application:
        from drntu.rest import datasets

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
        )


@g_oai.command("info")
def cmd_oai_info(
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp."""
    with application_scope() as application:
        from drntu import oai

        return invoke(
            partial(oai.identify, application.research_oai),
            {"refresh": refresh},
            json_output,
        )


@g_oai.command("formats")
def cmd_oai_formats(
    identifier: Optional[str] = typer.Argument(None),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List OAI metadata prefixes, namespaces and schemas."""
    with application_scope() as application:
        from drntu import oai

        return invoke(
            partial(oai.formats, application.research_oai),
            {"identifier": identifier, "refresh": refresh},
            json_output,
        )


@g_oai.command("sets")
def cmd_oai_sets(
    resumption_token: Optional[str] = typer.Option(None, "--token"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List OAI collection/community sets."""
    with application_scope() as application:
        from drntu import oai

        return invoke(
            partial(oai.sets, application.research_oai),
            {
                "resumption_token": resumption_token,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_oai.command("records")
def cmd_oai_records(
    metadata_prefix: Optional[str] = typer.Option(None, "--prefix"),
    set_spec: Optional[str] = typer.Option(None, "--set"),
    from_date: Optional[str] = None,
    until_date: Optional[str] = None,
    resumption_token: Optional[str] = typer.Option(None, "--token"),
    headers_only: bool = typer.Option(False, "--headers-only"),
    limit: int = typer.Option(10, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read one bounded OAI records page, defaulting to oai_dc."""
    with application_scope() as application:
        from drntu import oai

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
        )


@g_oai.command("record")
def cmd_oai_record(
    identifier: str,
    metadata_prefix: str = typer.Option("oai_dc", "--prefix"),
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Get one record by its OAI identifier, not a REST UUID."""
    with application_scope() as application:
        from drntu import oai

        return invoke(
            partial(oai.get_record, application.research_oai),
            {
                "identifier": identifier,
                "metadata_prefix": metadata_prefix,
                "refresh": refresh,
            },
            json_output,
        )


g_item.command("show")(cmd_item_default)
