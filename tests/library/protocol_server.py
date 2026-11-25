from unittest.mock import patch

from application import Application
from tests.library.fixtures import fake_get
from tests.library.facility_fixtures import fake_facility_get, fake_schedule
from server import main


if __name__ == "__main__":
    application = Application()
    with (
        patch.object(application.library.http, "get", side_effect=fake_get),
        patch.object(
            application.library_facilities.http, "get", side_effect=fake_facility_get
        ),
        patch.object(
            application.library_session,
            "_get_schedule",
            side_effect=lambda path, date, refresh: fake_schedule(date, space_id=100),
        ),
    ):
        main("personal", application=application)
