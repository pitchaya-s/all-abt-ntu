"""Offline public HTTP app; the same ASGI entrypoint as Vercel with synthetic data."""

from contextlib import nullcontext
from unittest.mock import patch

from application import Application
from public_http_server import create_app
from tests.faculty.fixtures import fake_get as faculty_get
from tests.library.fixtures import fake_get as library_get
from tests.mazemap.fixtures import fake_get as map_get
from tests.news.fixtures import fake_get as news_get
from tests.repository.fixtures import fake_get as repository_get
from tests.repository.oai_fixtures import fake_get as oai_get
from tests.service.fixtures import fake_get as service_get
from tests.stars.mcp_fixtures import COURSE


application = Application()
PATCHES = [
    patch("stars.tools.academic.fetch_course", return_value=COURSE),
    patch.object(application.faculty.http, "get", side_effect=faculty_get),
    patch.object(application.library.http, "get", side_effect=library_get),
    patch.object(
        application.mazemap,
        "_get",
        side_effect=lambda *args, **kwargs: nullcontext(map_get(*args, **kwargs)),
    ),
    patch.object(application.news.http, "get", side_effect=news_get),
    patch.object(application.research, "get", side_effect=repository_get),
    patch.object(application.research_oai, "get", side_effect=oai_get),
    patch.object(application.campus_services.http, "get", side_effect=service_get),
]
for replacement in PATCHES:
    replacement.start()
app = create_app(application)
