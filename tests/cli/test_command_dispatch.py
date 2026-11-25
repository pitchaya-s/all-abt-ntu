"""Exercise every service command's argument parsing without network or writes."""

from contextlib import ExitStack, nullcontext
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
import tempfile
from typing import Literal, get_args, get_origin
import unittest
from unittest.mock import Mock, patch

from typer.main import get_command
from typer.testing import CliRunner

from cli.cli import create_app

SERVICES = (
    "stars",
    "learn",
    "career",
    "map",
    "research",
    "library",
    "faculty",
    "news",
    "services",
    "bus",
    "onestop",
)
CONTENT_URL = "https://ntulearn.ntu.edu.sg/ultra/courses/_100_1/document/_200_1"


def command_paths(command, path):
    children = getattr(command, "commands", {})
    if "__default__" in children:
        yield children["__default__"], path
    if not children:
        yield command, path
    for name, child in children.items():
        if not child.hidden:
            yield from command_paths(child, [*path, name])


def example_value(parameter, courses_file):
    annotation = parameter.type_descriptor.annotation
    if get_origin(annotation) is Literal:
        return str(get_args(annotation)[0])
    if annotation is int:
        return "2026" if parameter.name == "academic_year" else "1"
    return {
        "courses": str(courses_file),
        "target": "request:0123456789abcdef0123456789abcdef",
        "date": "2026-11-16",
        "time": "14:00",
        "start_time": "14:00",
        "end_time": "16:00",
        "course_id": "_100_1",
        "course_code": "ZZ0001",
        "url": "https://example.invalid/",
        "persistent_id": "doi:10.1234/example",
    }.get(parameter.name, "sample")


class CommandDispatchTests(unittest.TestCase):
    def test_every_service_command_reaches_its_dispatch_boundary(self):
        app = create_app()
        root = get_command(app)
        runner = CliRunner()
        reached = Mock(side_effect=RuntimeError("synthetic dispatch boundary"))
        paths = [
            entry
            for service in SERVICES
            for entry in command_paths(root.commands[service], [service])
        ]
        self.assertGreater(len(paths), 140)
        with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
            courses_file = Path(directory) / "courses.json"
            courses_file.write_text("[]")
            for service in SERVICES:
                module = import_module(f"cli.commands.{service}")
                child_modules = [
                    import_module(child.name)
                    for child in iter_modules(
                        getattr(module, "__path__", []), module.__name__ + "."
                    )
                ]
                for dispatcher in (module, *child_modules):
                    stack.enter_context(patch.object(dispatcher, "invoke", reached))
                    stack.enter_context(
                        patch.object(
                            dispatcher, "application_scope", lambda: nullcontext(Mock())
                        )
                    )
            stack.enter_context(
                patch("cli.session.session_scope", lambda: nullcontext())
            )
            for command, path in paths:
                with self.subTest(command=" ".join(path)):
                    arguments, options = [], []
                    for parameter in command.params:
                        if not parameter.required:
                            continue
                        sample = example_value(parameter, courses_file)
                        if parameter.param_type_name == "argument":
                            arguments.append(sample)
                        else:
                            options.extend([parameter.opts[0], sample])
                    if path in (
                        ["learn", "attachments"],
                        ["learn", "files", "read"],
                        ["learn", "files", "download"],
                        ["learn", "videos", "download"],
                    ):
                        arguments[0] = CONTENT_URL
                    reached.reset_mock()
                    result = runner.invoke(app, [*path, *arguments, *options])
                    self.assertTrue(reached.called, result.output)
