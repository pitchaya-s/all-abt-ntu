"""Terminal and machine-readable rendering of service results."""

import json
from dataclasses import asdict, is_dataclass

from pydantic import BaseModel
from rich.console import Console
from rich.tree import Tree

from .renderers.common import add_tree


def plain(value):
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def render(value, json_output: bool = False, *, presenter=None) -> None:
    data = plain(value)
    if json_output:
        print(json.dumps(data, default=str, ensure_ascii=False))
        return
    console = Console(markup=False)
    if presenter is not None:
        presenter(console, data)
    elif isinstance(data, (dict, list)):
        # Workflow previews must retain all form fields and choices for review.
        tree = Tree("Review")
        add_tree(tree, data)
        console.print(tree)
    else:
        console.print(data)
