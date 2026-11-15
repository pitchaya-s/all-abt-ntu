"""Offline faculty directory server for stdio client checks."""

from unittest.mock import patch

from application import Application
from server import main
from tests.faculty.fixtures import fake_get


if __name__ == "__main__":
    application = Application()
    with patch.object(application.faculty.http, "get", side_effect=fake_get):
        main(application=application)
