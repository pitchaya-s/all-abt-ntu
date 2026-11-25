"""One Stop cart commands."""

from typing import Annotated, Optional

import typer

from ...execution import application_scope
from ...helpers import group, parse_json
from ...renderers import onestop as views
from ...services import invoke
from .workflows import _show_workflow

app = group(default=True)
g_cart_saved = group(default=False)
app.add_typer(g_cart_saved, name="saved", help="View or manage saved carts.")


@app.command("__default__", hidden=True)
def cmd_cart_default(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.get, {}, json_output, presenter=views.cart_default
        )


@g_cart_saved.command("show")
def cmd_cart_saved_show(
    saved_cart_id: Annotated[
        str,
        typer.Argument(
            help="The saved cart ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Inspect items in a verified own saved cart before loading it."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.get_saved,
            {"saved_cart_id": saved_cart_id},
            json_output,
            presenter=views.cart_saved_show,
        )


@app.command("quantity")
def cmd_cart_quantity(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    quantity: Annotated[int, typer.Argument(help="The desired item quantity.")],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Set the quantity of an item in your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"item_id": item_id, "quantity": quantity, "action": "set_quantity"},
            json_output,
            side_effect=True,
            presenter=views.cart_quantity,
        )


@app.command("remove")
def cmd_cart_remove(
    item_id: Annotated[
        str,
        typer.Argument(
            help="The item ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Remove an item from your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"item_id": item_id, "action": "remove"},
            json_output,
            side_effect=True,
            presenter=views.cart_remove,
        )


@app.command("clear")
def cmd_cart_clear(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Remove all items from your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"action": "clear"},
            json_output,
            side_effect=True,
            presenter=views.cart_clear,
        )


@g_cart_saved.command("load")
def cmd_cart_saved_load(
    saved_cart_id: Annotated[
        str,
        typer.Argument(
            help="The saved cart ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Append items from a saved cart to your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "load_saved"},
            json_output,
            side_effect=True,
            presenter=views.cart_saved_load,
        )


@g_cart_saved.command("replace")
def cmd_cart_saved_replace(
    saved_cart_id: Annotated[
        str,
        typer.Argument(
            help="The saved cart ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Replace your active cart with items from a saved cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "replace_with_saved"},
            json_output,
            side_effect=True,
            presenter=views.cart_saved_replace,
        )


@g_cart_saved.command("delete")
def cmd_cart_saved_delete(
    saved_cart_id: Annotated[
        str,
        typer.Argument(
            help="The saved cart ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Delete a saved cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "delete_saved"},
            json_output,
            side_effect=True,
            presenter=views.cart_saved_delete,
        )


@g_cart_saved.command("create")
def cmd_cart_saved_create(
    name: Annotated[
        str, typer.Argument(help="The name of the item, setting or field to use.")
    ],
    item_ids: Optional[str] = typer.Option(None, "--item-ids", help="JSON value."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.save,
            {
                "name": name,
                "item_ids": (parse_json(item_ids) if item_ids is not None else None),
            },
            json_output,
            side_effect=True,
            presenter=views.cart_saved_create,
        )


@app.command("checkout")
def cmd_cart_checkout():
    """Review and submit a cart checkout in one session."""
    with application_scope() as application:
        from ...session import session_scope

        with session_scope():
            preview = invoke(
                application.onestop_cart.prepare_checkout,
                {},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(preview, views.checkout_preview)
            return invoke(
                application.onestop_cart.submit_checkout,
                {"checkout_id": preview.checkout_id},
                False,
                side_effect=True,
                presenter=views.cart_checkout,
            )
