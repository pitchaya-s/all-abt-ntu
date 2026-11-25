"""Service authentication checks must verify the endpoint before reporting status."""

import unittest
from unittest.mock import AsyncMock, Mock, patch

from services.careeraxis.browser.session import CareerAxisSession, SEARCH_PATH
from services.ntulearn.client.session import Session
from services.onestop.models import OneStopError
from services.onestop.session import OneStopSession
from services.stars.wish.session import WishSessionManager


class ServiceAuthTests(unittest.TestCase):
    def test_stars_verifies_the_planner_before_reporting_status(self):
        session = WishSessionManager()
        self.addCleanup(session.close)
        with (
            patch.object(session, "get_stars_planner") as planner,
            patch.object(session, "status", return_value={"session_verified": True}),
        ):
            status = session.verify()
        planner.assert_called_once_with(refresh=True)
        self.assertTrue(status["session_verified"])

    def test_career_verifies_the_authenticated_endpoint(self):
        session = CareerAxisSession()
        self.addCleanup(session.close)
        credentials = Mock()
        with (
            patch.object(session, "_credentials", return_value=credentials),
            patch.object(session, "_navigate") as navigate,
            patch.object(session, "_status", return_value={"session_verified": True}),
        ):
            status = session.verify()
        navigate.assert_called_once_with(SEARCH_PATH, credentials)
        self.assertTrue(status["session_verified"])

    def test_onestop_login_failure_is_not_reported_as_authenticated(self):
        session = OneStopSession()
        self.addCleanup(session.close)
        with (
            patch.object(session, "_credentials", return_value=Mock()),
            patch.object(
                session, "_login", side_effect=OneStopError("rejected")
            ) as login,
            patch.object(session, "_status") as status,
        ):
            with self.assertRaisesRegex(OneStopError, "rejected"):
                session.verify()
        login.assert_called_once()
        status.assert_not_called()


class AsyncServiceAuthTests(unittest.IsolatedAsyncioTestCase):
    async def test_ntulearn_authenticates_before_reporting_status(self):
        session = Session()
        self.addAsyncCleanup(session.close)
        with (
            patch.object(
                session, "_ensure_authenticated", new_callable=AsyncMock
            ) as auth,
            patch.object(session, "status", new_callable=AsyncMock) as status,
        ):
            await session.verify()
        auth.assert_awaited_once()
        status.assert_awaited_once()
