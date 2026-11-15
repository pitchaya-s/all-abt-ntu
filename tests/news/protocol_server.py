from unittest.mock import patch

from application import Application
from server import main
from tests.news.fixtures import fake_get


if __name__ == "__main__":
    application = Application()
    with patch.object(application.news.http, "get", side_effect=fake_get):
        main(application=application)
