"""Own cart, saved carts and catalog favourites using native widget actions."""

from typing import Annotated
from typing import Literal
from pydantic import Field
from ..models import ActionResult, ID, Token

from datetime import datetime, timedelta, timezone
import hashlib
import json
import secrets
import time

from shared.action_review import ActionReview

from ..browser import action_result, commit, evaluate
from ..models import (
    CartCheckout,
    CartItem,
    CartState,
    Favourite,
    Favourites,
    NamedValue,
    OneStopError,
    PortalRecords,
    SavedCart,
)
from ..parser import pagination, sys_id
from .portal import record


class CartService:
    def __init__(self, session):
        self.session = session

    def get(self) -> CartState:
        "Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. Does not order, load or alter any cart."
        return self.session.workflow(self._get)

    def _get(self, session, revision):
        snapshot = session.read("sc_cart", refresh=True)
        raw = evaluate(
            session._page,
            r"""
          const s=scope('sc-shopping-cart-v2'), saved=scope('sc-saved-carts');
          return {items:(s.data.cartItems||[]).map(i=>({cart_item_id:i.sys_id,
              item_id:i.item_id||i.catalog_item_id||i.sysparm_id||null,title:i.name,
              quantity:Number(i.quantity||1),quantity_editable:s.c.showQuantity(i)===true,
              price_label:i.price_display||i.price||null})),
            saved_carts:(saved.data.savedCarts||[]).map(c=>({cart_id:c.sys_id,name:c.name})),
            delivery_address:s.data.cart?.delivery_address??null,
            special_instructions:s.data.cart?.special_instructions??null,
            two_step_checkout:s.data.sys_properties.twostep===true};
        """,
        )
        for item in raw["items"]:
            item["cart_item_id"] = sys_id(item["cart_item_id"])
            if item["price_label"] is not None:
                item["price_label"] = str(item["price_label"])
        return CartState(
            **snapshot.metadata(),
            items=[CartItem(**i) for i in raw["items"]],
            saved_carts=[SavedCart(**s) for s in raw["saved_carts"]],
            delivery_address=raw["delivery_address"],
            special_instructions=raw["special_instructions"],
            two_step_checkout=raw["two_step_checkout"],
        )

    def update(
        self,
        action: Literal[
            "set_quantity",
            "remove",
            "clear",
            "load_saved",
            "replace_with_saved",
            "delete_saved",
        ],
        item_id: ID | None = None,
        quantity: Annotated[int, Field(ge=1, le=100, strict=True)] | None = None,
        saved_cart_id: ID | None = None,
    ) -> ActionResult:
        "Change your native cart: set a permitted quantity, remove/clear items, append a saved cart, replace with a saved cart, or delete a saved cart. IDs must appear in get_cart. replace_with_saved replaces current contents; load_saved appends. Does not checkout."
        if action not in {
            "set_quantity",
            "remove",
            "clear",
            "load_saved",
            "replace_with_saved",
            "delete_saved",
        }:
            raise OneStopError("Unsupported cart action.")
        return self.session.workflow(
            self._update,
            action,
            sys_id(item_id) if item_id else None,
            quantity,
            sys_id(saved_cart_id) if saved_cart_id else None,
        )

    def _update(self, session, revision, action, item_id, quantity, saved_cart_id):
        state = self._get(session, revision)
        if action in {"set_quantity", "remove"}:
            item = next((i for i in state.items if i.cart_item_id == item_id), None)
            if item is None:
                raise OneStopError("This item is not in your current cart.")
            if action == "set_quantity" and (
                not item.quantity_editable
                or type(quantity) is not int
                or not 1 <= quantity <= 100
            ):
                raise OneStopError(
                    "This item must offer quantity editing; use a quantity from 1 to 100."
                )
            payload = (
                {"action": "update_quantity", "itemID": item_id, "quantity": quantity}
                if action == "set_quantity"
                else {
                    "action": "remove_item",
                    "cartName": "DEFAULT",
                    "removeItemID": item_id,
                }
            )
            widget = "sc-shopping-cart-v2"
        elif action == "clear":
            if not state.items:
                return action_result(
                    "clear_cart", state.source_url, verified=True, outcome="unchanged"
                )
            payload, widget = {"action": "clear_cart"}, "sc-shopping-cart-v2"
        else:
            if saved_cart_id not in {s.cart_id for s in state.saved_carts}:
                raise OneStopError(
                    "This saved cart does not belong to your current saved-cart list."
                )
            payload = {
                "action": {
                    "load_saved": "load_cart",
                    "replace_with_saved": "replace_cart",
                    "delete_saved": "remove_bundle",
                }[action],
                "cartID": saved_cart_id,
            }
            widget = "sc-saved-carts"
        commit(
            session,
            revision,
            lambda: evaluate(
                session._page,
                "await scope(args.widget).server.get(args.payload);return true;",
                {"widget": widget, "payload": payload},
                asynchronous=True,
            ),
        )
        try:
            after = self._get(session, revision)
        except Exception:
            return action_result(
                action + "_cart",
                state.source_url,
                item_id or saved_cart_id,
                outcome="uncertain",
                message="The native action returned, but the cart could not be refreshed. Check it before repeating the action.",
            )
        verified = False
        if action == "clear":
            verified = not after.items
        elif action == "remove":
            verified = all(i.cart_item_id != item_id for i in after.items)
        elif action == "set_quantity":
            verified = any(
                i.cart_item_id == item_id and i.quantity == quantity
                for i in after.items
            )
        elif action == "delete_saved":
            verified = all(s.cart_id != saved_cart_id for s in after.saved_carts)
        return action_result(
            action + "_cart",
            state.source_url,
            item_id or saved_cart_id,
            outcome="completed" if verified else "uncertain",
            verified=verified,
            message=None
            if verified
            else "The native action returned; inspect the refreshed cart contents.",
        )

    def get_saved(self, saved_cart_id: ID) -> PortalRecords:
        "Inspect items in a verified own saved cart before loading it. Does not merge or replace the active cart."
        return self.session.workflow(self._get_saved, sys_id(saved_cart_id))

    def _get_saved(self, session, revision, saved_cart_id):
        state = self._get(session, revision)
        saved = next((s for s in state.saved_carts if s.cart_id == saved_cart_id), None)
        if not saved:
            raise OneStopError("This saved cart is not in your saved-cart list.")
        raw = evaluate(
            session._page,
            "const r=await scope('sc-saved-carts').server.get({action:'retrieve_bundle_items',cartName:args});return (r.data.bundleItems||[]).map(i=>pick(i,['sys_id','name','short_description','quantity','price']));",
            saved.name,
            asynchronous=True,
        )
        records = [
            record(
                i.get("sys_id"),
                i.get("name") or i.get("short_description") or "Saved cart item",
                quantity=i.get("quantity"),
                price=i.get("price"),
            )
            for i in raw
        ]
        return PortalRecords(
            retrieved_at=datetime.now(timezone.utc),
            source_url=state.source_url,
            cached=False,
            **pagination(len(records), None, False, 0, 100),
            records=records[:100],
        )

    def save(
        self,
        name: Annotated[str, Field(min_length=1, max_length=100)],
        item_ids: list[ID] | None = None,
    ) -> ActionResult:
        "Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. Existing saved names are not overwritten. Does not submit an order."
        if (
            not isinstance(name, str)
            or not name.strip()
            or len(name) > 100
            or "\0" in name
        ):
            raise OneStopError("Provide a saved-cart name of 1–100 characters.")
        if item_ids is not None and (
            not isinstance(item_ids, list) or not item_ids or len(item_ids) > 100
        ):
            raise OneStopError(
                "Choose up to 100 own cart item IDs, or omit item_ids to save the whole cart."
            )
        return self.session.workflow(
            self._save,
            name.strip(),
            [sys_id(i) for i in item_ids] if item_ids is not None else None,
        )

    def _save(self, session, revision, name, item_ids):
        cart = self._get(session, revision)
        selected = (
            item_ids if item_ids is not None else [i.cart_item_id for i in cart.items]
        )
        if not selected or not set(selected).issubset(
            {i.cart_item_id for i in cart.items}
        ):
            raise OneStopError("Select items that are in your current cart.")
        if name.casefold() in {s.name.casefold() for s in cart.saved_carts}:
            raise OneStopError(
                "A saved cart already uses that name. Choose a new name."
            )
        evaluate(
            session._page, "scope('sc-shopping-cart-v2').c.saveBundle();return true;"
        )
        session._page.wait_for_function(
            "[...document.querySelectorAll('div[widget][data]')].some(e=>angular.element(e).scope()?.widget?.id==='sc_save_bundle')",
            timeout=15000,
        )
        valid = evaluate(
            session._page,
            r"""
          const s=scope('sc_save_bundle');s.data.newCartName=args.name;
          for(const item of s.data.cartItems)item.selected=args.ids.includes(item.sys_id);
          if(!s.c.enableSave())return false;
          const r=await s.server.get({cart_name:args.name,action:'validate_cart_name'});
          return !r.data.error;
        """,
            {"name": name, "ids": selected},
            asynchronous=True,
        )
        if not valid:
            raise OneStopError(
                "The native portal rejected the saved-cart name or selection."
            )
        accepted = commit(
            session,
            revision,
            lambda: evaluate(
                session._page,
                "const r=await scope('sc_save_bundle').server.update();return !r.error;",
                asynchronous=True,
            ),
        )
        if not accepted:
            raise OneStopError(
                "The portal did not acknowledge saving the cart. Check saved carts before retrying."
            )
        try:
            after = self._get(session, revision)
        except Exception:
            return action_result(
                "save_cart",
                cart.source_url,
                outcome="uncertain",
                message="Saving returned, but saved carts could not be refreshed. Check them before saving again.",
            )
        saved = next((s for s in after.saved_carts if s.name == name), None)
        return action_result(
            "save_cart",
            cart.source_url,
            saved.cart_id if saved else None,
            verified=saved is not None,
            outcome="completed" if saved else "uncertain",
        )

    @staticmethod
    def _fingerprint(cart):
        content = dict(
            items=[i.model_dump() for i in cart.items],
            delivery_address=cart.delivery_address,
            special_instructions=cart.special_instructions,
        )
        return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

    def prepare_checkout(
        self,
        delivery_address: Annotated[str, Field(max_length=10000)] | None = None,
        special_instructions: Annotated[str, Field(max_length=10000)] | None = None,
    ) -> CartCheckout:
        "Create a 15-minute local checkout preview with the current own cart, delivery address and instructions. Does not order anything. submit_cart_checkout rechecks that cart contents have not changed."
        return self.session.workflow(
            self._prepare_checkout, delivery_address, special_instructions
        )

    def _prepare_checkout(
        self, session, revision, delivery_address, special_instructions
    ):
        cart = self._get(session, revision)
        if not cart.items:
            raise OneStopError("Your cart is empty.")
        for value in (delivery_address, special_instructions):
            if value is not None and (
                not isinstance(value, str) or len(value) > 10000 or "\0" in value
            ):
                raise OneStopError(
                    "Checkout address and instructions must be strings of at most 10,000 characters."
                )
        for key, entry in list(session._checkouts.items()):
            if time.monotonic() > entry["deadline"]:
                session._checkouts.pop(key)
        if len(session._checkouts) >= 4:
            raise OneStopError(
                "Four cart checkout previews are already open; wait for one to expire."
            )
        token = secrets.token_urlsafe(24)
        preview = CartCheckout(
            checkout_id=token,
            source_url=cart.source_url,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
            items=cart.items,
            delivery_address=delivery_address
            if delivery_address is not None
            else cart.delivery_address or "",
            special_instructions=special_instructions
            if special_instructions is not None
            else cart.special_instructions or "",
        )
        session._checkouts[token] = {
            "revision": revision,
            "deadline": time.monotonic() + 900,
            "fingerprint": self._fingerprint(cart),
            "preview": preview,
            "state": "prepared",
            "receipt": None,
        }
        return preview

    def submit_checkout(self, checkout_id: Token) -> ActionResult:
        "Submit a reviewed cart checkout exactly once after checking account identity, expiry and unchanged cart contents. Returns the native request receipt. Accounts requiring an additional two-step form receive a portal handoff. Uncertain submissions must be inspected before another checkout."
        return self.session.workflow(self._submit_checkout, checkout_id)

    def review_checkout(self, checkout_id):
        return self.session.inspect_workflow(self._review_checkout, checkout_id)

    def _review_checkout(self, session, revision, checkout_id):
        entry = self._checkout(session, revision, checkout_id)
        cart = entry["preview"]
        items = ", ".join(
            f"{item.quantity} × {item.title[:80]}" for item in cart.items[:3]
        )
        extra = f", and {len(cart.items) - 3} more" if len(cart.items) > 3 else ""
        return ActionReview(
            f"Submit the One Stop cart with {items}{extra}.",
            [revision, entry["state"], cart.model_dump(mode="json")],
        )

    def _checkout(self, session, revision, checkout_id):
        entry = session._checkouts.get(checkout_id)
        if (
            not entry
            or entry["revision"] != revision
            or time.monotonic() > entry["deadline"]
        ):
            raise OneStopError(
                "This checkout preview expired or belongs to a different account."
            )
        return entry

    def _submit_checkout(self, session, revision, checkout_id):
        entry = self._checkout(session, revision, checkout_id)
        if entry["receipt"]:
            return entry["receipt"].model_copy(update={"outcome": "unchanged"})
        if entry["state"] != "prepared":
            raise OneStopError(
                "This checkout has an uncertain outcome. Check your requests before submitting again."
            )
        cart = self._get(session, revision)
        if self._fingerprint(cart) != entry["fingerprint"]:
            raise OneStopError(
                "Your cart changed after the preview. Prepare checkout again."
            )
        if cart.two_step_checkout:
            return action_result(
                "checkout_cart",
                cart.source_url,
                checkout_id,
                outcome="requires_user_action",
                message="This account requires an additional native checkout form; finish checkout in the portal.",
            )

        def perform():
            entry["state"] = "submitting"
            try:
                result = evaluate(
                    session._page,
                    r"""
                  const s=scope('sc-shopping-cart-v2');
                  s.data.cart.delivery_address=args.address;
                  s.data.cart.special_instructions=args.instructions;
                  s.data.action='checkout'; const r=await s.server.update();
                  return r.result?pick(r.result,['sys_id','number','table']):null;
                """,
                    {
                        "address": entry["preview"].delivery_address,
                        "instructions": entry["preview"].special_instructions,
                    },
                    asynchronous=True,
                )
                if not result or not result.get("sys_id"):
                    entry["state"] = "uncertain"
                    return action_result(
                        "checkout_cart",
                        cart.source_url,
                        checkout_id,
                        outcome="uncertain",
                        message="Checkout returned no record receipt. Check your requests before repeating it.",
                    )
                receipt_id = sys_id(result["sys_id"])
                receipt = action_result(
                    "checkout_cart",
                    cart.source_url,
                    receipt_id,
                    outcome="completed",
                    verified=True,
                    references=[
                        NamedValue(
                            name="number",
                            label="Reference number",
                            value=result.get("number"),
                        )
                    ],
                )
                entry["state"], entry["receipt"] = "submitted", receipt
                return receipt
            except Exception:
                entry["state"] = "uncertain"
                raise

        return commit(session, revision, perform)


class FavouriteService:
    def __init__(self, session):
        self.session = session

    def list(self) -> Favourites:
        "Read your saved catalog favourites and which are pinned to the homepage. The native portal permits up to four pins."
        return self.session.workflow(self._list)

    def _list(self, session, revision):
        snapshot = session.read("sc_favourite", refresh=True)
        data = evaluate(
            session._page,
            r"""
          const s=scope('sc-favourite-list');
          return {pinned:s.data.pinItemCount,items:(s.data.cartItems||[]).map(i=>({
            favourite_id:i.sys_id,item_id:i.item_id,title:i.name,pinned:String(i.pin_to_home)==='1'}))};
        """,
        )
        return Favourites(
            **snapshot.metadata(),
            items=[Favourite(**i) for i in data["items"]],
            pinned_count=int(data["pinned"]),
        )

    def update(
        self,
        action: Literal["pin", "unpin", "remove", "clear"],
        favourite_id: ID | None = None,
    ) -> ActionResult:
        "Pin/unpin/remove one own saved favourite or clear all favourites. The native four-pin limit and unpin-before-removal rules apply. clear affects every unpinned favourite; it does not clear the shopping cart."
        if action not in {"pin", "unpin", "remove", "clear"}:
            raise OneStopError("Unsupported favourite action.")
        return self.session.workflow(
            self._update, action, sys_id(favourite_id) if favourite_id else None
        )

    def _update(self, session, revision, action, favourite_id):
        current = self._list(session, revision)
        item = next((i for i in current.items if i.favourite_id == favourite_id), None)
        if action != "clear" and item is None:
            raise OneStopError("This saved favourite does not belong to your list.")
        if action in {"pin", "unpin"}:
            desired = action == "pin"
            if item.pinned == desired:
                return action_result(
                    action + "_favourite",
                    current.source_url,
                    favourite_id,
                    verified=True,
                    outcome="unchanged",
                )
            if desired and current.pinned_count >= 4:
                raise OneStopError(
                    "The portal permits four home pins. Unpin an item before pinning another."
                )
            payload = {
                "action": "toggle_pin",
                "cartName": "saved_items",
                "catItemID": item.item_id,
                "itemName": item.title,
                "itemID": item.favourite_id,
            }
        elif action == "remove":
            if item.pinned:
                raise OneStopError(
                    "The native portal requires unpinning this favourite before removal."
                )
            payload = {
                "action": "remove_item",
                "cartName": "saved_items",
                "removeItemID": favourite_id,
            }
        else:
            if current.pinned_count:
                raise OneStopError(
                    "The native portal requires unpinning all favourites before clearing them."
                )
            if not current.items:
                return action_result(
                    "clear_favourites",
                    current.source_url,
                    verified=True,
                    outcome="unchanged",
                )
            payload = {"action": "clear_cart"}
        commit(
            session,
            revision,
            lambda: evaluate(
                session._page,
                "await scope('sc-favourite-list').server.get(args);return true;",
                payload,
                asynchronous=True,
            ),
        )
        try:
            after = self._list(session, revision)
        except Exception:
            return action_result(
                action + "_favourite",
                current.source_url,
                favourite_id,
                outcome="uncertain",
                message="The native action returned, but favourites could not be refreshed. Check them before repeating it.",
            )
        verified = (
            not after.items
            if action == "clear"
            else all(i.favourite_id != favourite_id for i in after.items)
            if action == "remove"
            else any(
                i.favourite_id == favourite_id and i.pinned == (action == "pin")
                for i in after.items
            )
        )
        return action_result(
            action + "_favourite",
            current.source_url,
            favourite_id,
            verified=verified,
            outcome="completed" if verified else "uncertain",
        )

    def set_catalog_favourite(
        self, category_id: ID, item_id: ID, favourite: bool
    ) -> ActionResult:
        "Set a catalog item's favourite state through its category's native control. Both IDs must match a visible category item. Uses the desired state and verifies it against your favourites list."
        if type(favourite) is not bool:
            raise OneStopError("favourite must be a boolean.")
        return self.session.workflow(
            self._set_catalog_favourite, sys_id(category_id), sys_id(item_id), favourite
        )

    def _set_catalog_favourite(
        self, session, revision, category_id, item_id, favourite
    ):
        snapshot = session.read("sc_category", {"sys_id": category_id}, refresh=True)
        state = evaluate(
            session._page,
            r"""
          const s=scope('ntu_sc_category_page'), item=s.data.items.find(i=>i.sys_id===args);
          if(!item||typeof item.favorite!=='boolean'||typeof s.toggleFavorite!=='function')return null;
          return item.favorite;
        """,
            item_id,
        )
        if state is None:
            raise OneStopError(
                "This category does not expose a favourite control for the item."
            )
        if state == favourite:
            return action_result(
                "set_catalog_favourite",
                snapshot.source_url,
                item_id,
                verified=True,
                outcome="unchanged",
            )
        commit(
            session,
            revision,
            lambda: evaluate(
                session._page,
                "await scope('ntu_sc_category_page').server.get({action:'toggleFavorite',sys_id:args.id,addFav:args.favourite});return true;",
                {"id": item_id, "favourite": favourite},
                asynchronous=True,
            ),
        )
        try:
            after = self._list(session, revision)
        except Exception:
            return action_result(
                "set_catalog_favourite",
                snapshot.source_url,
                item_id,
                outcome="uncertain",
                message="The native action returned, but favourites could not be refreshed. Check them before repeating it.",
            )
        verified = any(i.item_id == item_id for i in after.items) == favourite
        return action_result(
            "set_catalog_favourite",
            snapshot.source_url,
            item_id,
            verified=verified,
            outcome="completed" if verified else "uncertain",
        )
