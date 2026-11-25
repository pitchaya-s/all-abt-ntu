import re
from urllib.parse import urlencode
from uuid import UUID

from public_http_client import PublicHTTPClient
from shared.sitefinity import form_options, query_text

from . import parser
from .models import Categories, NewsError

DIRECTORY = "https://www.ntu.edu.sg/news/"
API = DIRECTORY + "GetStories/"
ARTICLE_URL = (
    r"https://www\.ntu\.edu\.sg/news/detail/[A-Za-z0-9][A-Za-z0-9_.-]{0,499}/?"
)


from typing import Annotated
from typing import Literal
from pydantic import Field
from .models import Article, SearchResults


class NewsClient:
    def __init__(self):
        self.http = PublicHTTPClient(
            "NTU news", ["www.ntu.edu.sg"], {"application/json", "text/html"}
        )

    def list_categories(self, refresh: bool = False) -> Categories:
        "List current news category labels and filter IDs from NTU's official news form. Pass a returned id as news_search.category_id; display labels are not filter values."
        with self.http.parsed_response(DIRECTORY, refresh) as (body, snapshot):
            return Categories(categories=form_options(body, "categories"), **snapshot)

    def _page(self, query, category_id, sort, page, refresh):
        params = {
            "categories": category_id or "all",
            "page": page,
            "listingKeyword": query,
            "sort": sort,
        }
        url = API + "?" + urlencode(params)
        with self.http.parsed_response(url, refresh) as (body, snapshot):
            return parser.search_results(body, snapshot, page)

    def search(
        self,
        query: Annotated[str, Field(max_length=200)] = "",
        category_id: Annotated[
            str,
            Field(
                pattern="^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
            ),
        ]
        | None = None,
        sort: Literal["latest", "oldest"] = "latest",
        page: Annotated[int, Field(ge=1, le=10000, strict=True)] = 1,
        refresh: bool = False,
    ) -> SearchResults:
        "Search public NTU news by keyword and optional category, sorted latest or oldest. Omit query to browse. Copy category_id from news_list_categories. Returns titles, dates, URLs and summaries where supplied; pages start at 1 with up to ten stories. Follow next_page, then pass a story URL to news_get_article."
        query = query_text(query)
        if (
            type(page) is not int
            or not 1 <= page <= 10000
            or sort not in ("latest", "oldest")
        ):
            raise NewsError("Use page 1–10000 and sort latest or oldest.")
        if category_id is not None:
            category_id = str(UUID(category_id))
            if category_id not in {
                item.id for item in self.list_categories(refresh).categories
            }:
                raise NewsError(
                    "Unknown category_id; use news_list_categories for current IDs."
                )
        result = self._page(query, category_id, sort, page, refresh)
        if page > max(1, result.total_pages):
            raise NewsError(
                f"This search has {result.total_pages} pages; start at page 1 and follow next_page."
            )
        return result

    def get_article(
        self,
        url: Annotated[str, Field(pattern="^" + ARTICLE_URL + "$", max_length=600)],
        offset: Annotated[int, Field(ge=0, strict=True)] = 0,
        max_chars: Annotated[int, Field(ge=1, le=50000, strict=True)] = 12000,
        refresh: bool = False,
    ) -> Article:
        "Read the published text of an NTU /news/detail/ article URL returned by news_search. Returns its title, display date and bounded text, excluding navigation, related stories and scripts. Follow next_offset to continue reading. Does not download linked documents or fetch external articles."
        if not isinstance(url, str) or re.fullmatch(ARTICLE_URL, url) is None:
            raise NewsError(
                "Use an https://www.ntu.edu.sg/news/detail/ article URL returned by news_search."
            )
        if (
            type(offset) is not int
            or offset < 0
            or type(max_chars) is not int
            or not 1 <= max_chars <= 50000
        ):
            raise NewsError("Use a non-negative offset and max_chars 1–50000.")
        with self.http.parsed_response(url, refresh) as (body, snapshot):
            return parser.article(body, snapshot, offset, max_chars)
