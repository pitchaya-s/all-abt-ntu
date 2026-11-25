from typing import Literal
from ..contracts import Entity, FacetName, Filters, Page, Query, Size, UUID

from ..models import RepositoryError
from . import parser
from .models import (
    Bundle,
    Bundles,
    Containers,
    FacetDefinition,
    Facets,
    FacetValue,
    Files,
    Item,
    SearchResults,
)


def search_parameters(query, scope_id, entity_type, filters):
    params = {"query": query.strip()}
    if scope_id:
        params["scope"] = parser.identifier(scope_id)
    if entity_type != "all":
        params["f.entityType"] = [entity_type + ",equals"]
    for filter in filters or []:
        if not filter.value.strip():
            raise RepositoryError("Filter values must contain text.")
        params.setdefault("f." + filter.field, []).append(
            filter.value + "," + filter.operator
        )
    return params


def search(
    client,
    query: Query,
    scope_id: UUID | None = None,
    entity_type: Entity = "Publication",
    filters: Filters | None = None,
    page: Page = 0,
    page_size: Size = 10,
    refresh: bool = False,
) -> SearchResults:
    "Search DR-NTU publications by keywords or Solr query. Returns concise titles, authors, dates, identifiers and rights. Scope to a community/collection UUID, or apply facet filters using field/value/operator. Set entity_type=Person or all explicitly for broader searches."
    if not query.strip():
        raise RepositoryError(
            "query must contain search terms; use drntu_browse to explore repository containers."
        )
    params = search_parameters(query, scope_id, entity_type, filters)
    params.update(dsoType="item", page=page, size=page_size)
    with client.validated("/discover/search/objects", params, refresh=refresh) as (
        data,
        snapshot,
    ):
        result = data["_embedded"]["searchResult"]
        items = [
            parser.summary(v["_embedded"]["indexableObject"])
            for v in parser.embedded(result, "objects")
        ]
        return SearchResults(
            query=query.strip(),
            items=items,
            pagination=parser.pagination(result, len(items), page, page_size),
            **snapshot,
        )


def get_item(client, item_id: UUID, refresh: bool = False) -> Item:
    "Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. Metadata values retain language tags. Public metadata does not establish full-text access."
    item_id = parser.identifier(item_id)
    with client.validated(f"/core/items/{item_id}", refresh=refresh) as (
        data,
        snapshot,
    ):
        summary = parser.summary(data)
        if summary.item_id != item_id:
            raise RepositoryError("DR-NTU returned a different item ID.")
        meta = parser.metadata(data)
        # Keep alternate/multilingual titles; omit the one title already returned above.
        if (
            len(meta.get("dc.title", [])) == 1
            and meta["dc.title"][0].value == summary.title
            and meta["dc.title"][0].language is None
        ):
            del meta["dc.title"]
        return Item(
            item_id=item_id,
            title=summary.title,
            entity_type=summary.entity_type,
            url=summary.url,
            last_modified=data.get("lastModified"),
            withdrawn=data.get("withdrawn"),
            metadata=meta,
            **snapshot,
        )


def browse(
    client,
    kind: Literal["communities", "collections"] = "communities",
    community_id: UUID | None = None,
    page: Page = 0,
    page_size: Size = 20,
    refresh: bool = False,
) -> Containers:
    "Browse repository communities or collections. Omit community_id for all; supply it for subcommunities or collections within that community. Use returned container_id as search scope_id. Negative/unavailable archived item counts become null."
    if community_id:
        relation = "subcommunities" if kind == "communities" else "collections"
        path = f"/core/communities/{parser.identifier(community_id)}/{relation}"
    else:
        path = "/core/" + kind
    with client.validated(path, {"page": page, "size": page_size}, refresh=refresh) as (
        data,
        snapshot,
    ):
        key = "subcommunities" if community_id and kind == "communities" else kind
        containers = [parser.container(v) for v in parser.embedded(data, key)]
        return Containers(
            kind=kind,
            containers=containers,
            pagination=parser.pagination(data, len(containers), page, page_size),
            **snapshot,
        )


def get_facets(
    client,
    facet: FacetName | None = None,
    query: Query = "",
    scope_id: UUID | None = None,
    entity_type: Entity = "Publication",
    filters: Filters | None = None,
    page: Page = 0,
    page_size: Size = 10,
    refresh: bool = False,
) -> Facets:
    "Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. Facet definitions have no counts. Copy each value's filter object into search filters; date range labels can differ from their query values."
    params = search_parameters(query, scope_id, entity_type, filters)
    if facet is None:
        with client.validated("/discover/facets", params, refresh=refresh) as (
            data,
            snapshot,
        ):
            definitions = [
                FacetDefinition(name=v["name"], facet_type=v["facetType"])
                for v in parser.embedded(data, "facets")
            ]
            return Facets(
                facet=None,
                definitions=definitions,
                values=[],
                pagination=None,
                **snapshot,
            )
    params.update(page=page, size=page_size)
    with client.validated("/discover/facets/" + facet, params, refresh=refresh) as (
        data,
        snapshot,
    ):
        if data.get("name") != facet:
            raise RepositoryError("DR-NTU returned a different facet.")
        values = [
            FacetValue(
                label=v["label"],
                count=v["count"],
                authority_key=v.get("authorityKey"),
                filter=parser.facet_filter(v, facet),
            )
            for v in parser.embedded(data, "values")
        ]
        return Facets(
            facet=facet,
            definitions=[],
            values=values,
            pagination=parser.pagination(data, len(values), page, page_size),
            **snapshot,
        )


def list_bundles(
    client, item_id: UUID, page: Page = 0, page_size: Size = 20, refresh: bool = False
) -> Bundles:
    "List an item's file groups. ORIGINAL usually holds deposited papers; TEXT, THUMBNAIL and LICENSE are separate bundles. Pass a returned bundle_id to drntu_list_files."
    item_id = parser.identifier(item_id)
    with client.validated(
        f"/core/items/{item_id}/bundles",
        {"page": page, "size": page_size},
        refresh=refresh,
    ) as (data, snapshot):
        bundles = [
            Bundle(bundle_id=parser.identifier(v["uuid"]), name=v["name"])
            for v in parser.embedded(data, "bundles")
        ]
        return Bundles(
            item_id=item_id,
            bundles=bundles,
            pagination=parser.pagination(data, len(bundles), page, page_size),
            **snapshot,
        )


def list_files(
    client, bundle_id: UUID, page: Page = 0, page_size: Size = 20, refresh: bool = False
) -> Files:
    "List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. Does not fetch file bytes or verify download permission. Restricted content remains restricted even when its metadata is public."
    bundle_id = parser.identifier(bundle_id)
    with client.validated(
        f"/core/bundles/{bundle_id}/bitstreams",
        {"page": page, "size": page_size},
        refresh=refresh,
    ) as (data, snapshot):
        files = [parser.file(v) for v in parser.embedded(data, "bitstreams")]
        return Files(
            bundle_id=bundle_id,
            files=files,
            pagination=parser.pagination(data, len(files), page, page_size),
            **snapshot,
        )
