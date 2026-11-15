"""Onestop service commands."""

from typing import Literal, Optional

import typer

from ..helpers import attachment_target, group, parse_json
from ..output import render
from ..execution import application_scope
from ..services import invoke

app = typer.Typer(no_args_is_help=True)
g_appointments = group(default=True)
app.add_typer(g_appointments, name="appointments")
g_attachments = group(default=False)
app.add_typer(g_attachments, name="attachments")
g_auth = group(default=False)
app.add_typer(g_auth, name="auth")
g_cart = group(default=True)
app.add_typer(g_cart, name="cart")
g_catalog = group(default=False)
app.add_typer(g_catalog, name="catalog")
g_favourites = group(default=True)
app.add_typer(g_favourites, name="favourites")
g_knowledge = group(default=False)
app.add_typer(g_knowledge, name="knowledge")
g_payments = group(default=False)
app.add_typer(g_payments, name="payments")
g_profile = group(default=True)
app.add_typer(g_profile, name="profile")
g_requests = group(default=False)
app.add_typer(g_requests, name="requests")
g_cart_saved = group(default=False)
g_cart.add_typer(g_cart_saved, name="saved")
g_knowledge_comments = group(default=True)
g_knowledge.add_typer(g_knowledge_comments, name="comments")


@g_auth.command("status")
def cmd_auth_status(json_output: bool = typer.Option(False, "--json", "-j")):
    """Report shared keyring availability and the last verified One Stop session without logging in or returning identity or credentials."""
    with application_scope() as application:
        return invoke(application.onestop_session.status, {}, json_output)


@g_catalog.command("categories")
def cmd_catalog_categories(
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List the signed-in student's visible One Stop catalog categories and subcategories, parent IDs and published item counts."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_categories, {"refresh": refresh}, json_output
        )


@g_catalog.command("search")
def cmd_catalog_search(
    query: str = typer.Argument(""),
    category_id: Optional[str] = typer.Option(None, "--category"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search the student's One Stop service catalog with query, or browse one category_id."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_catalog_items,
            {
                "query": query,
                "category_id": category_id,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_catalog.command("item")
def cmd_catalog_item(
    item_id: str,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a native One Stop form's description, current visible field labels/types, mandatory flags and choices."""
    with application_scope() as application:
        return invoke(
            application.onestop.get_catalog_item,
            {"item_id": item_id, "refresh": refresh},
            json_output,
        )


@g_knowledge.command("search")
def cmd_knowledge_search(
    query: str,
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search the signed-in student's One Stop knowledge base."""
    with application_scope() as application:
        return invoke(
            application.onestop.search_knowledge,
            {"query": query, "limit": limit, "offset": offset, "refresh": refresh},
            json_output,
        )


@g_knowledge.command("article")
def cmd_knowledge_article(
    article_id: str,
    offset: int = 0,
    max_chars: int = 12000,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a knowledge article's text, text-template sections or wiki body by article_id from search_knowledge, with text pagination and source links."""
    with application_scope() as application:
        return invoke(
            application.onestop.get_knowledge_article,
            {
                "article_id": article_id,
                "offset": offset,
                "max_chars": max_chars,
                "refresh": refresh,
            },
            json_output,
        )


@g_requests.command("list")
def cmd_requests_list(
    status: Literal["all", "open", "closed"] = "all",
    kind: Literal["all", "case", "request"] = "all",
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read your own open/closed One Stop cases and service requests, expanding native lists up to 500 records."""
    with application_scope() as application:
        return invoke(
            application.onestop.list_my_requests,
            {
                "status": status,
                "kind": kind,
                "limit": limit,
                "offset": offset,
                "refresh": refresh,
            },
            json_output,
        )


@g_requests.command("show")
def cmd_requests_show(
    request_id: str,
    refresh: bool = typer.Option(False, "--refresh", "-r"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read one of your requests after checking request_id against your retrieved personal lists."""
    with application_scope() as application:
        return invoke(
            application.onestop.get_my_request,
            {"request_id": request_id, "refresh": refresh},
            json_output,
        )


@app.command("dashboard")
def cmd_dashboard(json_output: bool = typer.Option(False, "--json", "-j")):
    """Read your One Stop homepage announcements, actions/payment links, upcoming appointments and popular links."""
    with application_scope() as application:
        return invoke(application.onestop_portal.dashboard, {}, json_output)


@app.command("announcements")
def cmd_announcements(
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read One Stop announcements, summaries and links from the native announcements collection with local pagination."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_announcements,
            {"limit": limit, "offset": offset},
            json_output,
        )


@app.command("actions")
def cmd_actions(
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read your One Stop to-do/billing actions and their published due dates and payment links."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_actions,
            {"limit": limit, "offset": offset},
            json_output,
        )


@app.command("links")
def cmd_links(
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List links on One Stop's Popular Sites page, preserving native catalog, knowledge and external destinations."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_popular_links,
            {"limit": limit, "offset": offset},
            json_output,
        )


@g_profile.command("__default__", hidden=True)
def cmd_profile_default(json_output: bool = typer.Option(False, "--json", "-j")):
    """Read your own displayed profile fields, editable flags, preferences/choices, notification setting and picture-upload capability."""
    with application_scope() as application:
        return invoke(application.onestop_portal.get_profile, {}, json_output)


@g_payments.command("services")
def cmd_payments_services(
    query: str = typer.Argument(""),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Search/browse services in the student's native payment directory, preserving its active/category/access filter."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.list_payment_services,
            {"query": query, "limit": limit, "offset": offset},
            json_output,
        )


@g_payments.command("service")
def cmd_payments_service(
    service_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read a visible payment service's native fixed-amount information."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.get_payment_service,
            {"service_id": service_id},
            json_output,
        )


@g_knowledge.command("feedback")
def cmd_knowledge_feedback(
    article_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.get_feedback,
            {"article_id": article_id},
            json_output,
        )


@g_knowledge_comments.command("__default__", hidden=True)
def cmd_knowledge_comments_default(
    article_id: str,
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.list_comments,
            {"article_id": article_id, "limit": limit, "offset": offset},
            json_output,
        )


@g_requests.command("activity")
def cmd_requests_activity(
    request_id: str,
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read visible comments and attachment events on a verified own request/item, plus current reply/upload/state-action permissions."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.activity,
            {"request_id": request_id, "record_id": record_id},
            json_output,
        )


@g_attachments.command("list")
def cmd_attachments_list(
    target: str,
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """List attachments on a verified own request/item, a readable knowledge article/comment, or an active local draft."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(application.onestop_files.list, {"target": target}, json_output)


@g_cart.command("__default__", hidden=True)
def cmd_cart_default(json_output: bool = typer.Option(False, "--json", "-j")):
    """Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults."""
    with application_scope() as application:
        return invoke(application.onestop_cart.get, {}, json_output)


@g_cart_saved.command("show")
def cmd_cart_saved_show(
    saved_cart_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Inspect items in a verified own saved cart before loading it."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.get_saved,
            {"saved_cart_id": saved_cart_id},
            json_output,
        )


@g_favourites.command("__default__", hidden=True)
def cmd_favourites_default(json_output: bool = typer.Option(False, "--json", "-j")):
    """Read your saved catalog favourites and which are pinned to the homepage."""
    with application_scope() as application:
        return invoke(application.onestop_favourites.list, {}, json_output)


@g_appointments.command("__default__", hidden=True)
def cmd_appointments_default(
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = 0,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Read your native upcoming appointment list with appointment numbers, published dates/times and locations."""
    with application_scope() as application:
        return invoke(
            application.onestop_appointments.list,
            {"limit": limit, "offset": offset},
            json_output,
        )


@g_profile.command("set")
def cmd_profile_set(
    field_name: str,
    value: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Update one displayed editable own-profile field through its native inline editor."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.update_profile,
            {"field_name": field_name, "value": value},
            json_output,
            side_effect=True,
        )


@g_profile.command("picture")
def cmd_profile_picture(
    file_path: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Upload the explicitly selected local image as your own ServiceNow profile picture using the native file input."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.update_picture,
            {"file_path": file_path},
            json_output,
            side_effect=True,
        )


@g_profile.command("notifications")
def cmd_profile_notifications(
    enabled: Literal["on", "off"],
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Enable or disable your ServiceNow notification preference."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.set_notifications,
            {"enabled": enabled == "on"},
            json_output,
            side_effect=True,
        )


@g_profile.command("preference")
def cmd_profile_preference(
    name: Literal[
        "accessibility",
        "voice_input",
        "analytics",
        "timezone",
        "language",
        "communication_channels",
    ],
    value: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Set an enabled own preference returned by get_profile."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.set_preference,
            {"name": name, "value": value},
            json_output,
            side_effect=True,
        )


@g_payments.command("checkout-link")
def cmd_payments_checkout_link(
    service_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Ask One Stop to prepare a checkout link for a visible payment service."""
    with application_scope() as application:
        return invoke(
            application.onestop_portal.prepare_payment,
            {"service_id": service_id},
            json_output,
            side_effect=True,
        )


@g_knowledge_comments.command("add")
def cmd_knowledge_comments_add(
    article_id: str,
    text: str = typer.Option(..., "--text"),
    parent_id: Optional[str] = typer.Option(None, "--parent"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Publish plain-text feedback to a knowledge article, or reply to a visible parent comment."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.add_comment,
            {"article_id": article_id, "text": text, "parent_id": parent_id},
            json_output,
            side_effect=True,
        )


@g_knowledge_comments.command("delete")
def cmd_knowledge_comments_delete(
    article_id: str,
    comment_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Delete a visible article comment only when the native menu permits deletion by the current user."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.delete_comment,
            {"article_id": article_id, "comment_id": comment_id},
            json_output,
            side_effect=True,
        )


@g_knowledge_comments.command("like")
def cmd_knowledge_comments_like(
    article_id: str,
    comment_id: str,
    liked: Literal["on", "off"] = typer.Option(..., "--state"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Like or unlike a visible knowledge comment using a desired state."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.set_comment_like,
            {
                "article_id": article_id,
                "comment_id": comment_id,
                "liked": liked == "on",
            },
            json_output,
            side_effect=True,
        )


@g_knowledge.command("rate")
def cmd_knowledge_rate(
    article_id: str,
    rating: int,
    reason_id: Optional[str] = None,
    details: str = "",
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Submit a 1–5 star knowledge rating when the native control is enabled."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.rate,
            {
                "article_id": article_id,
                "rating": rating,
                "reason_id": reason_id,
                "details": details,
            },
            json_output,
            side_effect=True,
        )


@g_knowledge.command("helpful")
def cmd_knowledge_helpful(
    article_id: str,
    helpful: Literal["yes", "no"],
    reason_id: Optional[str] = None,
    details: str = "",
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Submit helpful/not-helpful feedback only when the article offers that native control."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.set_helpful,
            {
                "article_id": article_id,
                "helpful": helpful == "yes",
                "reason_id": reason_id,
                "details": details,
            },
            json_output,
            side_effect=True,
        )


@g_knowledge.command("flag")
def cmd_knowledge_flag(
    article_id: str,
    text: str = typer.Option(..., "--text"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Flag a knowledge article with the user's explanation when the native flag control is available."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.flag,
            {"article_id": article_id, "text": text},
            json_output,
            side_effect=True,
        )


@g_knowledge.command("subscribe")
def cmd_knowledge_subscribe(
    article_id: str,
    subscribed: Literal["on", "off"] = typer.Option(..., "--state"),
    include_knowledge_base: bool = typer.Option(False, "--include-knowledge-base"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Subscribe/unsubscribe to article updates."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.set_subscription,
            {
                "article_id": article_id,
                "subscribed": subscribed == "on",
                "include_knowledge_base": include_knowledge_base,
            },
            json_output,
            side_effect=True,
        )


@g_knowledge.command("favourite")
def cmd_knowledge_favourite(
    article_id: str,
    favourite: Literal["on", "off"] = typer.Option(..., "--state"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Set an article's native favourite state when its Favourite control is enabled."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.set_favourite,
            {"article_id": article_id, "favourite": favourite == "on"},
            json_output,
            side_effect=True,
        )


@g_knowledge.command("send-to-self")
def cmd_knowledge_send_to_self(
    article_id: str,
    channel: Literal["email", "sms"] = "email",
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Send this article to your registered email/SMS channel using the native Send to myself action."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.send_to_self,
            {"article_id": article_id, "channel": channel},
            json_output,
            side_effect=True,
        )


@g_requests.command("reply")
def cmd_requests_reply(
    request_id: str,
    text: str = typer.Option(..., "--text"),
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Post a real additional comment to a verified own ticket/item when its current native state permits replying."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.reply,
            {"request_id": request_id, "text": text, "record_id": record_id},
            json_output,
            side_effect=True,
        )


@g_requests.command("action")
def cmd_requests_action(
    request_id: str,
    action: Literal["close", "reopen", "accept-solution", "reject-solution"],
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Execute a state action currently offered by the native own-ticket page."""
    with application_scope() as application:
        return invoke(
            application.onestop_tickets.take_action,
            {
                "request_id": request_id,
                "action": action.replace("-", "_"),
                "record_id": record_id,
            },
            json_output,
            side_effect=True,
        )


@g_attachments.command("upload")
def cmd_attachments_upload(
    target: str,
    file_path: str,
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Upload an explicitly selected file from the configured One Stop upload directory to the verified target."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.upload,
            {"target": target, "file_path": file_path},
            json_output,
            side_effect=True,
        )


@g_attachments.command("download")
def cmd_attachments_download(
    target: str,
    attachment_id: str,
    destination: str = typer.Option(..., "--output", "-o"),
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Download a listed attachment of the verified target to a new explicit absolute file path, up to 20 MB."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.download,
            {
                "target": target,
                "attachment_id": attachment_id,
                "destination": destination,
            },
            json_output,
            side_effect=True,
        )


@g_attachments.command("delete")
def cmd_attachments_delete(
    target: str,
    attachment_id: str,
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Delete an attachment only when it is listed on the verified target and native editing is allowed."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.delete,
            {"target": target, "attachment_id": attachment_id},
            json_output,
            side_effect=True,
        )


@g_attachments.command("rename")
def cmd_attachments_rename(
    target: str,
    attachment_id: str,
    file_name: str,
    record_id: Optional[str] = None,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Rename a listed editable attachment using the native attachment service."""
    with application_scope() as application:
        target = attachment_target(target, record_id)
        return invoke(
            application.onestop_files.rename,
            {"target": target, "attachment_id": attachment_id, "file_name": file_name},
            json_output,
            side_effect=True,
        )


@g_cart.command("quantity")
def cmd_cart_quantity(
    item_id: str,
    quantity: int,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Set the quantity of an item in your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"item_id": item_id, "quantity": quantity, "action": "set_quantity"},
            json_output,
            side_effect=True,
        )


@g_cart.command("remove")
def cmd_cart_remove(
    item_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Remove an item from your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"item_id": item_id, "action": "remove"},
            json_output,
            side_effect=True,
        )


@g_cart.command("clear")
def cmd_cart_clear(json_output: bool = typer.Option(False, "--json", "-j")):
    """Remove all items from your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"action": "clear"},
            json_output,
            side_effect=True,
        )


@g_cart_saved.command("load")
def cmd_cart_saved_load(
    saved_cart_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Append items from a saved cart to your active cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "load_saved"},
            json_output,
            side_effect=True,
        )


@g_cart_saved.command("replace")
def cmd_cart_saved_replace(
    saved_cart_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Replace your active cart with items from a saved cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "replace_with_saved"},
            json_output,
            side_effect=True,
        )


@g_cart_saved.command("delete")
def cmd_cart_saved_delete(
    saved_cart_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Delete a saved cart."""
    with application_scope() as application:
        return invoke(
            application.onestop_cart.update,
            {"saved_cart_id": saved_cart_id, "action": "delete_saved"},
            json_output,
            side_effect=True,
        )


@g_cart_saved.command("create")
def cmd_cart_saved_create(
    name: str,
    item_ids: Optional[str] = typer.Option(None, "--item-ids", help="JSON value."),
    json_output: bool = typer.Option(False, "--json", "-j"),
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
        )


@g_favourites.command("pin")
def cmd_favourites_pin(
    favourite_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Pin a saved favourite to the homepage."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "pin"},
            json_output,
            side_effect=True,
        )


@g_favourites.command("unpin")
def cmd_favourites_unpin(
    favourite_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Unpin a favourite from the homepage."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "unpin"},
            json_output,
            side_effect=True,
        )


@g_favourites.command("remove")
def cmd_favourites_remove(
    favourite_id: str,
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Remove a saved favourite."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"favourite_id": favourite_id, "action": "remove"},
            json_output,
            side_effect=True,
        )


@g_favourites.command("clear")
def cmd_favourites_clear(json_output: bool = typer.Option(False, "--json", "-j")):
    """Remove eligible saved favourites."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.update,
            {"action": "clear"},
            json_output,
            side_effect=True,
        )


@g_catalog.command("favourite")
def cmd_catalog_favourite(
    item_id: str,
    category_id: str = typer.Option(..., "--category"),
    favourite: Literal["on", "off"] = typer.Option(..., "--state"),
    json_output: bool = typer.Option(False, "--json", "-j"),
):
    """Set a catalog item's favourite state through its category's native control."""
    with application_scope() as application:
        return invoke(
            application.onestop_favourites.set_catalog_favourite,
            {
                "category_id": category_id,
                "item_id": item_id,
                "favourite": favourite == "on",
            },
            json_output,
            side_effect=True,
        )


def _show_workflow(value):
    """Display a review without exposing temporary workflow identifiers."""
    if hasattr(value, "model_dump"):
        value = value.model_dump(
            mode="json", exclude={"draft_id", "checkout_id", "item_id"}
        )
    render(value)


def _choose(choices, label):
    for index, choice in enumerate(choices, 1):
        typer.echo(f"{index}. {choice.label}", err=True)
    number = typer.prompt(label, type=int, err=True)
    if not 1 <= number <= len(choices):
        raise typer.BadParameter("Choose a number from the displayed list.")
    return choices[number - 1]


def _fill_draft(draft, *, allow_appointment=False):
    """Fill required fields, optionally edit others, and show each native preview."""
    with application_scope() as application:
        for _ in range(10):
            missing = set(draft.missing_fields) | set(draft.invalid_fields)
            if allow_appointment:
                missing.discard("appointment")
            if not missing:
                editable = [field for field in draft.fields if not field.read_only]
                if not editable or not typer.confirm(
                    "Edit another field?", default=False, err=True
                ):
                    return draft
                typer.echo(
                    "Editable fields: "
                    + ", ".join(f"{field.name} ({field.label})" for field in editable),
                    err=True,
                )
                name = typer.prompt("Field name", err=True)
                if name not in {field.name for field in editable}:
                    raise typer.BadParameter(
                        "Choose a currently visible editable field."
                    )
                missing.add(name)
            values = {}
            for field in draft.fields:
                if field.name not in missing or field.read_only:
                    continue
                if getattr(field, "reference", False):
                    query = typer.prompt(f"Search {field.label}", err=True)
                    matches = invoke(
                        application.onestop_forms.search_references,
                        {
                            "draft_id": draft.draft_id,
                            "field_name": field.name,
                            "query": query,
                        },
                        False,
                        show_result=False,
                    )
                    if not matches.choices:
                        raise typer.BadParameter(
                            f"No choices were returned for {field.label}."
                        )
                    values[field.name] = _choose(
                        matches.choices, f"Choose {field.label}"
                    ).value
                    continue
                if field.choices:
                    values[field.name] = _choose(
                        field.choices, f"Choose {field.label}"
                    ).value
                else:
                    values[field.name] = typer.prompt(field.label, err=True)
            if not values:
                raise typer.BadParameter(
                    "The form needs a field that cannot be filled here; use the One Stop portal."
                )
            draft = invoke(
                application.onestop_forms.update,
                {"draft_id": draft.draft_id, "values": values},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(draft)
        raise typer.BadParameter(
            "The form still has missing or invalid fields after ten updates."
        )


def _add_draft_attachments(draft):
    """Upload only files explicitly selected during this workflow."""
    with application_scope() as application:
        for _ in range(20):
            if not typer.confirm(
                "Add an attachment to this draft?", default=False, err=True
            ):
                return draft
            path = typer.prompt(
                "Absolute path in the configured One Stop upload directory", err=True
            )
            invoke(
                application.onestop_files.upload,
                {
                    "target": {"kind": "draft", "draft_id": draft.draft_id},
                    "file_path": path,
                },
                False,
                side_effect=True,
            )
            draft = invoke(
                application.onestop_forms.get,
                {"draft_id": draft.draft_id},
                False,
                show_result=False,
            )
            _show_workflow(draft)
        typer.echo("Reached the limit of 20 attachments for this workflow.", err=True)
        return draft


@g_requests.command("apply")
def cmd_requests_apply(item_id: str):
    """Prepare, fill, review and submit a native request in one session."""
    with application_scope() as application:
        from ..session import session_scope

        with session_scope():
            draft = invoke(
                application.onestop_forms.prepare,
                {"item_id": item_id},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(draft)
            draft = _fill_draft(draft)
            draft = _add_draft_attachments(draft)
            if not draft.ready:
                raise typer.BadParameter("The native form is not ready for submission.")
            return invoke(
                application.onestop_forms.submit,
                {"draft_id": draft.draft_id, "action": "submit"},
                False,
                side_effect=True,
            )


@g_cart.command("checkout")
def cmd_cart_checkout():
    """Review and submit a cart checkout in one session."""
    with application_scope() as application:
        from ..session import session_scope

        with session_scope():
            preview = invoke(
                application.onestop_cart.prepare_checkout,
                {},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(preview)
            return invoke(
                application.onestop_cart.submit_checkout,
                {"checkout_id": preview.checkout_id},
                False,
                side_effect=True,
            )


@g_appointments.command("book")
def cmd_appointments_book(item_id: str):
    """Prepare an appointment form, choose a slot and book it in one session."""
    with application_scope() as application:
        from ..session import session_scope

        with session_scope():
            draft = invoke(
                application.onestop_forms.prepare,
                {"item_id": item_id},
                False,
                show_result=False,
                side_effect=True,
            )
            _show_workflow(draft)
            draft = _fill_draft(draft, allow_appointment=True)
            draft = _add_draft_attachments(draft)
            configuration = invoke(
                application.onestop_appointments.configuration,
                {"draft_id": draft.draft_id},
                False,
                show_result=False,
            )
            _show_workflow(configuration)
            if not configuration.enabled:
                raise typer.BadParameter(
                    "The native form does not offer appointment booking."
                )
            date = typer.prompt("Appointment date (YYYY-MM-DD)", err=True)
            slots = invoke(
                application.onestop_appointments.slots,
                {"draft_id": draft.draft_id, "date": date},
                False,
                show_result=False,
            )
            if not slots.slots:
                raise typer.BadParameter(
                    "No appointment slots were returned for that date."
                )
            slot = _choose(slots.slots, "Choose a time").slot_id
            return invoke(
                application.onestop_appointments.book,
                {"draft_id": draft.draft_id, "slot_id": slot},
                False,
                side_effect=True,
            )


g_profile.command("show")(cmd_profile_default)
g_knowledge_comments.command("list")(cmd_knowledge_comments_default)
g_cart.command("show")(cmd_cart_default)
g_favourites.command("list")(cmd_favourites_default)
g_appointments.command("list")(cmd_appointments_default)
