"""Synthetic NTULearn stdio server; no network or account credentials."""

from unittest.mock import PropertyMock, patch

from fixtures import COURSE, PREFIX, RESPONSES, FixtureSession

from application import Application
from server import main

if __name__ == "__main__":
    RESPONSES[f"{PREFIX}/courses/{COURSE}/contents/_202_1/attachments"]["results"][
        0
    ].update(fileName="example.txt", mimeType="text/plain")
    application = Application()
    with patch.object(
        Application,
        "learn_session",
        new_callable=PropertyMock,
        return_value=FixtureSession(),
    ):
        main("personal", check_dependencies=False, application=application)
