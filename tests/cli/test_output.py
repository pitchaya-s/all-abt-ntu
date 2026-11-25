"""Human and JSON presentations of representative service results."""

from contextlib import redirect_stdout
from io import StringIO
import json
import unittest
from unittest.mock import patch

from cli.cli import create_app
from cli.output import render
from cli.renderers import bus, learn, onestop, research, stars
from omnibus.models import Stop, Stops
from datetime import datetime, timezone
from typer.testing import CliRunner


class OutputTests(unittest.TestCase):
    def output(self, value, presenter, *, json_output=False):
        stream = StringIO()
        with redirect_stdout(stream):
            render(value, json_output=json_output, presenter=presenter)
        return stream.getvalue()

    def test_courses_only_show_selected_fields(self):
        data = {
            "courses": [
                {
                    "id": "_100_1",
                    "course_code": "ZZ0001",
                    "name": "Example",
                    "available": "Yes",
                    "role": "Student",
                    "organization": False,
                }
            ],
            "next_offset": None,
            "cached": True,
        }
        output = self.output(data, learn.courses_default)
        for expected in ("_100_1", "ZZ0001", "Example"):
            self.assertIn(expected, output)
        for unwanted in ("Courses 1", "Role", "Organization", "Cached"):
            self.assertNotIn(unwanted, output)
        self.assertEqual(
            json.loads(self.output(data, learn.courses_default, json_output=True)), data
        )

    def test_announcements_show_full_body_under_actual_title(self):
        body = "A full announcement. " * 25 + "THE END"
        data = {
            "announcements": [
                {"id": "a", "title": "Welcome", "body": body, "created": "2026-01-01"}
            ],
            "next_offset": None,
        }
        output = self.output(data, learn.announcements)
        self.assertIn("Welcome", output)
        self.assertIn("THE END", output)
        self.assertNotIn("Announcements 1", output)
        self.assertNotIn("use --json", output)
        self.assertEqual(
            json.loads(self.output(data, learn.announcements, json_output=True)), data
        )

    def test_routes_and_stops_hide_transport_metadata(self):
        data = {
            "routes": [{"route_code": "Blue", "is_lta_service": False}],
            "colors": [{"color_code": "0054A6"}],
            "source_urls": ["private-source"],
        }
        output = self.output(data, bus.routes)
        self.assertIn("Blue", output)
        self.assertNotIn("0054A6", output)
        self.assertNotIn("private-source", output)
        self.assertEqual(
            json.loads(self.output(data, bus.routes, json_output=True)), data
        )
        stops = {
            "stops": [
                {"name": "Hall 1", "stop_code": "Hall 1", "route_code": "Blue"},
                {"name": "Hall 1", "stop_code": "Hall 1", "route_code": "Red"},
            ],
            "total_count": 2,
            "next_offset": None,
        }
        self.assertIn("Blue, Red", self.output(stops, bus.stops))

    def test_stops_collect_other_pages_without_changing_json(self):
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
        with patch("cli.commands.bus.invoke", side_effect=[page, all_stops]):
            result = runner.invoke(create_app(), ["bus", "stops", "--limit", "1"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Blue, Red", result.output)
        with patch("cli.commands.bus.invoke", return_value=page):
            result = runner.invoke(
                create_app(), ["bus", "stops", "--limit", "1", "--json"]
            )
        self.assertEqual(len(json.loads(result.output)["stops"]), 1)

    def test_actual_plan_numbers_and_nested_schedule_remain_visible(self):
        value = {
            "saved_plans": [
                {
                    "plan_number": 1,
                    "status": "saved",
                    "sessions": [
                        {
                            "course_code": "ZZ0001",
                            "day": "MON",
                            "start_time": "09:30",
                            "end_time": "10:30",
                            "venue": "LT1",
                        }
                    ],
                }
            ]
        }
        output = self.output(value, stars.planner_show)
        for expected in ("Plan 1", "ZZ0001", "MON", "09:30", "LT1"):
            self.assertIn(expected, output)

    def test_registered_courses_include_published_column_names(self):
        value = {
            "registered_courses": [
                {
                    "course_code": "ZZ0001",
                    "Course Title": "Example",
                    "Index No": "10001",
                    "Course AU": "3",
                }
            ]
        }
        output = self.output(value, stars.planner_show)
        for expected in ("ZZ0001", "Example", "10001", "3"):
            self.assertIn(expected, output)

    def test_grades_include_feedback_and_unmatched_grade_pages(self):
        value = {
            "columns": [{"id": "a", "name": "Assignment", "possible_score": 10}],
            "grades": [
                {"column_id": "a", "score": 8, "feedback": "Well done"},
                {"column_id": "b", "score": 7},
            ],
        }
        output = self.output(value, learn.grades)
        for expected in ("Assignment", "Well done", "b", "7"):
            self.assertIn(expected, output)

    def test_degree_audit_displays_published_table_without_duplicate_metadata(self):
        value = {
            "requirements": [
                {
                    "section": "Core",
                    "headers": ["Name", "Balance AU"],
                    "records": [{"Name": "Example", "Balance AU": "3"}],
                }
            ]
        }
        output = self.output(value, stars.audit)
        self.assertIn("Core", output)
        self.assertIn("Balance AU", output)
        self.assertIn("Example", output)
        self.assertNotIn("Headers", output)
        self.assertNotIn("Records 1", output)

    def test_checkout_preview_selects_review_details(self):
        value = {
            "checkout_id": "temporary-secret-id",
            "source_url": "private-source",
            "items": [{"title": "Example", "quantity": 2, "price_label": "$10"}],
            "delivery_address": "Example address",
        }
        output = self.output(value, onestop.checkout_preview)
        for expected in ("Example", "$10", "Example address"):
            self.assertIn(expected, output)
        self.assertNotIn("temporary-secret-id", output)
        self.assertNotIn("private-source", output)

    def test_checkout_link_does_not_claim_payment_completed(self):
        value = {
            "title": "Fee",
            "checkout_url": "https://example.invalid",
            "requires_browser_completion": True,
        }
        output = self.output(value, onestop.payments_checkout_link)
        self.assertIn("https://example.invalid", output)
        self.assertIn("Requires browser completion: Yes", output)

    def test_saved_cart_shows_portal_records(self):
        data = {
            "records": [
                {
                    "record_id": "cart-item",
                    "title": "Example request",
                    "fields": [{"label": "Quantity", "value": "2"}],
                }
            ]
        }
        output = self.output(data, onestop.cart_saved_show)
        self.assertIn("Example request", output)
        self.assertIn("Quantity", output)
        self.assertNotIn("Records 1", output)

    def test_oai_metadata_uses_identifiers_and_continuation(self):
        data = {
            "records": [
                {
                    "identifier": "oai:example:1",
                    "metadata": {
                        "dc.title": [{"value": "Example paper", "language": None}]
                    },
                }
            ],
            "pagination": {"next_offset": 10},
        }
        output = self.output(data, research.oai_records)
        self.assertIn("oai:example:1", output)
        self.assertIn("Example paper", output)
        self.assertIn("--offset 10", output)
        self.assertNotIn("Records 1", output)


if __name__ == "__main__":
    unittest.main()
