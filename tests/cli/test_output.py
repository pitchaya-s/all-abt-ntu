"""Human-readable results hide transport metadata without changing JSON."""

from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
import json
import unittest
from unittest.mock import patch

from cli.output import render
from cli.cli import create_app
from omnibus.models import Route, RouteColor, Routes, Stop, Stops
from typer.testing import CliRunner


class OutputTests(unittest.TestCase):
    def output(self, value, *, json_output=False):
        stream = StringIO()
        with redirect_stdout(stream):
            render(value, json_output=json_output)
        return stream.getvalue()

    def test_bus_routes_show_routes_instead_of_color_metadata(self):
        result = Routes(
            retrieved_at=datetime.now(timezone.utc),
            source_urls=["https://example.invalid/source"],
            routes=[Route(route_code="Blue", is_lta_service=False)],
            colors=[RouteColor(route_code="Blue", color_code="0054A6")],
        )
        output = self.output(result)
        self.assertIn("Blue", output)
        self.assertNotIn("0054A6", output)
        self.assertNotIn("example.invalid", output)
        self.assertNotIn("Is lta service", output)
        data = json.loads(self.output(result, json_output=True))
        self.assertEqual(data["colors"][0]["color_code"], "0054A6")
        self.assertEqual(data["source_urls"], ["https://example.invalid/source"])

    def test_bus_stops_combine_routes_without_conflating_distinct_stops(self):
        def stop(name, code, route):
            return Stop(
                name=name,
                stop_code=code,
                route_code=route,
                service_id="NTU",
                is_lta_service=False,
            )

        result = Stops(
            retrieved_at=datetime.now(timezone.utc),
            source_urls=["https://example.invalid/source"],
            stops=[
                stop("Hall 1", "Hall 1", "Blue"),
                stop("Hall 1", "Hall 1", "Red"),
                stop("Hall 1", "27281", "179"),
            ],
            total_count=5,
            next_offset=3,
        )
        output = self.output(result)
        self.assertIn("Blue, Red", output)
        self.assertIn("27281", output)
        self.assertIn("179", output)
        self.assertIn("Total stop route entries: 5", output)
        self.assertIn("more routes may appear on later pages", output)
        self.assertNotIn("Service id", output)
        self.assertNotIn("Is lta service", output)
        self.assertNotIn("Next offset", output)
        data = json.loads(self.output(result, json_output=True))
        self.assertEqual(len(data["stops"]), 3)
        self.assertEqual(data["next_offset"], 3)

    def test_bus_stops_include_routes_from_other_pages_in_terminal_output(self):
        def stop(route):
            return Stop(
                name="Hall 1",
                stop_code="Hall 1",
                route_code=route,
                is_lta_service=False,
            )

        common = {"retrieved_at": datetime.now(timezone.utc), "source_urls": []}
        page = Stops(**common, stops=[stop("Blue")], total_count=2, next_offset=1)
        all_stops = Stops(**common, stops=[stop("Blue"), stop("Red")], total_count=2)
        runner = CliRunner()
        with patch("cli.commands.bus.invoke", side_effect=[page, all_stops]) as invoke:
            result = runner.invoke(create_app(), ["bus", "stops", "--limit", "1"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Blue, Red", result.output)
        self.assertNotIn("more routes may appear", result.output)
        self.assertEqual(invoke.call_count, 2)
        with patch("cli.commands.bus.invoke", return_value=page) as invoke:
            result = runner.invoke(
                create_app(), ["bus", "stops", "--limit", "1", "--json"]
            )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(len(json.loads(result.output)["stops"]), 1)
        self.assertEqual(invoke.call_count, 1)

    def test_multiple_result_lists_and_incomplete_warnings_remain_visible(self):
        output = self.output(
            {
                "shuttle_arrivals": [{"route": "Blue", "eta": "2 min"}],
                "lta_arrivals": [{"route": "179", "eta": "5 min"}],
                "complete": False,
                "issues": ["Some results could not be retrieved."],
                "cached": True,
                "source_urls": ["https://example.invalid/source"],
            }
        )
        for expected in ("Blue", "179", "Complete: False", "Some results"):
            self.assertIn(expected, output)
        self.assertNotIn("example.invalid", output)
        self.assertNotIn("Cached", output)

    def test_top_level_lists_are_readable_and_json_stays_complete(self):
        value = [{"name": "Example", "cached": True}]
        output = self.output(value)
        self.assertIn("Example", output)
        self.assertNotIn("Cached", output)
        self.assertEqual(json.loads(self.output(value, json_output=True)), value)

    def test_search_results_keep_identifiers_and_shorten_long_summaries(self):
        item_id = "12345678-1234-1234-1234-123456789abc"
        output = self.output(
            {
                "items": [
                    {
                        "item_id": item_id,
                        "title": "A useful research result",
                        "summary": "Long description " * 40,
                        "details": "Further information " * 40,
                        "url": "https://example.invalid/item",
                    }
                ],
                "total_count": 1,
            }
        )
        self.assertIn(item_id, output)
        self.assertIn("https://example.invalid/item", output)
        self.assertIn("Long descriptions are shortened", output)
        self.assertLess(len(output), 2000)

    def test_nested_timetable_sessions_are_compact_and_keep_schedule_details(self):
        value = {
            "saved_plans": [
                {
                    "plan_number": 1,
                    "sessions": [
                        {
                            "course_code": "ZZ0001",
                            "day": "MON",
                            "start_time": "09:30",
                            "end_time": "10:30",
                            "lesson_type": "LEC",
                            "venue": "LT1",
                            "teaching_weeks": [1, 2, 3],
                            "remarks": "Wk1-3",
                        }
                    ],
                }
            ]
        }
        output = self.output(value)
        for expected in ("ZZ0001", "MON", "09:30", "10:30", "LT1", "1–3"):
            self.assertIn(expected, output)
        self.assertNotIn("Remarks", output)
        self.assertLess(len(output.splitlines()), 20)
