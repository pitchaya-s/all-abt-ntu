"""Terminal and machine-readable rendering of service results."""

import json
from dataclasses import asdict, is_dataclass

from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.tree import Tree


def plain(value):
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def render(value, json_output: bool = False) -> None:
    value = plain(value)
    if json_output:
        print(json.dumps(value, default=str, ensure_ascii=False))
        return
    console = Console(markup=False)
    if isinstance(value, dict):
        lists = [
            (key, items)
            for key, items in value.items()
            if isinstance(items, list)
            and items
            and all(isinstance(item, dict) for item in items)
        ]
        if lists:
            key, items = max(lists, key=lambda entry: len(entry[1]))
            columns = list(
                dict.fromkeys(
                    k
                    for item in items
                    for k in item
                    if not isinstance(item[k], (dict, list))
                )
            )[:8]
            table = Table(title=key.replace("_", " ").title())
            for column in columns:
                table.add_column(column.replace("_", " ").title())
            for item in items:
                table.add_row(*(str(item.get(column, "")) for column in columns))
            console.print(table)
            for index, item in enumerate(items, 1):
                nested = {
                    name: value
                    for name, value in item.items()
                    if (isinstance(value, (dict, list)) and value)
                    or name not in columns
                }
                if nested:
                    console.print(
                        f"{key} {index}: {json.dumps(nested, default=str, ensure_ascii=False)}"
                    )
            for name, item in value.items():
                if name != key and not isinstance(item, (dict, list)):
                    console.print(f"{name}: {item}")
            for name, item in value.items():
                if name != key and isinstance(item, (dict, list)):
                    console.print(
                        f"{name}: {json.dumps(item, default=str, ensure_ascii=False)}"
                    )
            return
        tree = Tree("Result")

        def add(branch, data):
            if isinstance(data, dict):
                for key, item in data.items():
                    if isinstance(item, (dict, list)):
                        add(branch.add(str(key)), item)
                    else:
                        branch.add(f"{key}: {item}")
            elif isinstance(data, list):
                for item in data:
                    add(branch.add("•"), item)
            else:
                branch.add(str(data))

        add(tree, value)
        console.print(tree)
        return
    console.print(value)
