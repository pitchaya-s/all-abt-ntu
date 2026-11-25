import os
import unittest
from unittest.mock import AsyncMock, patch

from services.ntulearn.client.session import Session
from shared.credentials import read_credentials
from services.stars.wish.session import WishSessionManager
from tests.shared.credential_fixtures import MemoryKeyring, stored_credentials


class CredentialTests(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_stars_setting_does_not_disable_unrelated_tools(self):
        from mcp import Client
        from server import create_server

        with patch.dict(os.environ, {"NTU_CACHE_TTL_SECONDS": "invalid"}):
            server = create_server("public")
        self.addAsyncCleanup(server.ntu_application.close)
        async with Client(server) as client:
            tools = {tool.name for tool in (await client.list_tools()).tools}
            self.assertIn("mazemap_search_places", tools)
            result = await client.call_tool(
                "stars_search_courses",
                {"query": "algorithms", "academic_year": 2026, "semester": 1},
            )
            self.assertTrue(result.is_error)
            self.assertIn("NTU_CACHE_TTL_SECONDS", result.content[0].text)

    async def test_profile_boundaries_and_missing_dependency(self):
        from mcp import Client
        from server import create_server

        names = {}
        for profile in ("public", "personal"):
            async with Client(create_server(profile)) as client:
                names[profile] = {
                    tool.name for tool in (await client.list_tools()).tools
                }
        self.assertIn("stars_search_courses", names["public"])
        self.assertNotIn("ntulearn_list_courses", names["public"])
        self.assertIn("ntulearn_list_courses", names["personal"])
        for name in (
            "stars_save_stars_plan",
            "ntulearn_download_file",
            "onestop_upload_attachment",
            "onestop_prepare_request",
        ):
            self.assertNotIn(name, names["public"])
            self.assertIn(name, names["personal"])
        self.assertLess(names["public"], names["personal"])

    def test_network_username_derives_student_email(self):
        with stored_credentials("student001", "shared-test-secret"):
            credentials = read_credentials()
            self.assertEqual(credentials.username, "student001")
            self.assertEqual(credentials.email, "student001@e.ntu.edu.sg")
            self.assertEqual(credentials.password, "shared-test-secret")
            self.assertNotIn(credentials.password, repr(credentials))
            self.assertNotIn(credentials.username, repr(credentials))

    def test_full_email_preserves_domain_and_normalizes_wish_username(self):
        for email in ["student001@e.ntu.edu.sg", "staff001@ntu.edu.sg"]:
            with stored_credentials(email, "shared-test-secret"):
                credentials = read_credentials()
                self.assertEqual(credentials.username, email.split("@")[0])
                self.assertEqual(credentials.email, email)

    def test_plaintext_environment_is_never_a_credential_source(self):
        with (
            patch.dict(
                os.environ,
                {"NTU_USERNAME": "student001", "NTU_PASSWORD": "ignored-secret"},
            ),
            patch("shared.credentials._backend", return_value=MemoryKeyring()),
        ):
            credentials = read_credentials()
            self.assertFalse(
                credentials.username or credentials.email or credentials.password
            )

    async def test_both_services_share_opt_in_keyring_without_login(self):
        with stored_credentials():
            wish, learn = WishSessionManager(), Session()
            try:
                self.assertTrue(wish.status()["credentials_configured"])
                self.assertTrue((await learn.status()).credentials_configured)
                self.assertFalse(wish.status()["session_verified"])
                self.assertFalse((await learn.status()).session_verified)
                self.assertNotIn(
                    "test-secret",
                    str(wish.status()) + (await learn.status()).model_dump_json(),
                )
            finally:
                wish.close()
                await learn.close()

    def test_server_closes_all_sessions_even_if_one_cleanup_fails(self):
        import server
        from application import Application

        application = Application()
        instance = server.create_server("personal", application=application)
        with (
            patch.object(server, "create_server", return_value=instance),
            patch.object(instance, "run_stdio_async", new=AsyncMock()),
            patch.object(
                application.stars_personal,
                "close",
                side_effect=RuntimeError("test cleanup"),
            ) as wish,
            patch.object(
                application.learn_session, "close", new=AsyncMock()
            ) as learn_close,
            patch.object(application.library_session, "close") as library_close,
            patch.object(application.onestop_session, "close") as onestop_close,
            patch.object(application.careeraxis.session, "close") as careeraxis_close,
        ):
            with self.assertRaisesRegex(RuntimeError, "test cleanup"):
                server.main("personal")
            wish.assert_called_once()
            learn_close.assert_awaited_once()
            library_close.assert_called_once()
            onestop_close.assert_called_once()
            careeraxis_close.assert_called_once()
