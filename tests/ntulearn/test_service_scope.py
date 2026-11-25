import unittest
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import patch

from services.ntulearn.services import content


class ServiceScopeTests(unittest.IsolatedAsyncioTestCase):
    async def test_content_tree_keeps_one_scope_across_requests_and_closes_it(self):
        events = []

        class Session:
            @asynccontextmanager
            async def operation(self):
                events.append("enter")
                try:
                    yield
                finally:
                    events.append("exit")

        client = SimpleNamespace(session=Session())

        async def tree(actual_client, *args):
            self.assertIs(actual_client, client)
            events.extend(["request 1", "request 2"])
            return []

        with patch("services.ntulearn.services.content.tree", tree):
            result = await content.get_content_tree(client, "course", 5, 10, 10, False)
        self.assertEqual(result.contents, [])
        self.assertEqual(events, ["enter", "request 1", "request 2", "exit"])

    async def test_scope_exits_when_workflow_fails(self):
        events = []

        class Session:
            @asynccontextmanager
            async def operation(self):
                try:
                    yield
                finally:
                    events.append("exit")

        async def tree(*args):
            raise RuntimeError("failure")

        client = SimpleNamespace(session=Session())
        with patch("services.ntulearn.services.content.tree", tree):
            with self.assertRaises(RuntimeError):
                await content.get_content_tree(client, "course", 5, 10, 10, False)
        self.assertEqual(events, ["exit"])
