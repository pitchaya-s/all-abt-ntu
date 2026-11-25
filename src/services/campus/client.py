from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from urllib.parse import urlencode
from uuid import UUID

from public_http_client import PublicHTTPClient
from shared.sitefinity import form_options, query_text

from . import parser
from .models import Filters, SearchResults, ServiceError

DIRECTORY = "https://www.ntu.edu.sg/life-at-ntu/leisure-and-dining/general-directory/"
API = DIRECTORY + "GetLocations/"


from typing import Annotated
from pydantic import Field

Query = Annotated[str, Field(max_length=200)]
FilterID = Annotated[
    str,
    Field(
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    ),
]


class ServiceClient:
    def __init__(self):
        self.http = PublicHTTPClient(
            "NTU campus service directory",
            ["www.ntu.edu.sg"],
            {"application/json", "text/html"},
        )

    def list_filters(self, refresh: bool = False) -> Filters:
        "List official campus service type and category labels with filter IDs. Pass a returned id as service_search.type_id or category_id. Taxonomy assignments may be incomplete; a filtered empty result does not establish no matching service exists."
        with self.http.parsed_response(DIRECTORY, refresh) as (body, snapshot):
            return Filters(
                types=form_options(body, "locationTypes"),
                categories=form_options(body, "locationCategories"),
                **snapshot,
            )

    def _page(self, type_id, category_id, page, refresh):
        params = {
            "locationTypes": type_id or "all",
            "locationCategories": category_id or "all",
            "page": page,
        }
        url = API + "?" + urlencode(params)
        with self.http.parsed_response(url, refresh) as (body, snapshot):
            return (*parser.locations(body, page), snapshot)

    def search(
        self,
        query: Query = "",
        type_id: FilterID | None = None,
        category_id: FilterID | None = None,
        location_contains: Query = "",
        limit: Annotated[int, Field(ge=1, le=100, strict=True)] = 20,
        offset: Annotated[int, Field(ge=0, strict=True)] = 0,
        refresh: bool = False,
    ) -> SearchResults:
        "Find NTU food outlets, shops, clinics and campus services by name/address keyword and optional location substring. Optional type_id/category_id come from service_list_filters. Collects all source pages before local matching and result pagination; returns addresses, published hours, contact details and map links. Source taxonomy filters can omit relevant entries; use an unfiltered keyword search for broader coverage. Hours are not a live open-now check."
        query, location_contains = (
            query_text(query).casefold(),
            query_text(location_contains).casefold(),
        )
        if (
            type(limit) is not int
            or not 1 <= limit <= 100
            or type(offset) is not int
            or offset < 0
        ):
            raise ServiceError("Use limit 1–100 and a non-negative offset.")
        if type_id is not None or category_id is not None:
            filters = self.list_filters(refresh)
            if type_id is not None:
                type_id = str(UUID(type_id))
                if type_id not in {item.id for item in filters.types}:
                    raise ServiceError(
                        "Unknown type_id; use service_list_filters for current IDs."
                    )
            if category_id is not None:
                category_id = str(UUID(category_id))
                if category_id not in {item.id for item in filters.categories}:
                    raise ServiceError(
                        "Unknown category_id; use service_list_filters for current IDs."
                    )
        rows, total, pages, snapshot = self._page(type_id, category_id, 1, refresh)
        snapshots = [snapshot.copy()]
        if pages > 50:
            raise ServiceError(
                "The directory exceeds the 50-page retrieval limit; select a type/category filter."
            )
        if pages > 1:
            with ThreadPoolExecutor(
                max_workers=min(2, pages - 1), thread_name_prefix="ntu-directory"
            ) as pool:
                later_pages = [
                    pool.submit(
                        copy_context().run,
                        self._page,
                        type_id,
                        category_id,
                        page,
                        refresh,
                    )
                    for page in range(2, pages + 1)
                ]
                for future in later_pages:
                    items, count, page_count, current = future.result()
                    snapshots.append(current.copy())
                    if count != total or page_count != pages:
                        for item in snapshots:
                            if item.get("source_url"):
                                self.http.invalidate(
                                    item["source_url"],
                                    retrieved_at=item.get("retrieved_at"),
                                )
                        raise ServiceError(
                            "The directory changed during retrieval; retry with refresh=true."
                        )
                    rows.extend(items)
                    snapshot["retrieved_at"] = min(
                        snapshot["retrieved_at"], current["retrieved_at"]
                    )
                    snapshot["cached"] = snapshot["cached"] and current["cached"]
        if (
            len(rows) != total
            or len({(item.name, item.address) for item in rows}) != total
        ):
            for item in snapshots:
                if item.get("source_url"):
                    self.http.invalidate(
                        item["source_url"], retrieved_at=item.get("retrieved_at")
                    )
            raise ServiceError(
                "NTU returned missing or duplicate directory entries; retry with refresh=true."
            )
        matches = [
            item
            for item in rows
            if query in " ".join([item.name, item.address or ""]).casefold()
            and location_contains in (item.address or "").casefold()
        ]
        end = offset + limit
        return SearchResults(
            locations=matches[offset:end],
            total_count=len(matches),
            directory_count=total,
            pages_checked=max(1, pages),
            next_offset=end if end < len(matches) else None,
            **snapshot,
        )
