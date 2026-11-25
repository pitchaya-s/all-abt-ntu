"""Presentations for One Stop services."""

from rich.tree import Tree

from .common import (
    action,
    auth_status as auth_status,
    detail,
    details,
    download,
    listing,
    pagination,
    table,
)

catalog_search = listing(
    "Catalog", "items", ("title", "kind", "form_item_id", "item_id")
)
knowledge_search = listing(
    "Knowledge articles", "articles", ("title", "number", "published", "article_id")
)
knowledge_article = detail(
    "Article", ("number", "title", "updated_on", "text", "links")
)
knowledge_feedback = detail(
    "Feedback options",
    (
        "can_rate",
        "can_mark_helpful",
        "can_comment",
        "can_flag",
        "can_subscribe",
        "subscribed",
        "can_favourite",
        "favourite",
        "send_channels",
        "reasons",
    ),
)
requests_list = listing(
    "Requests", "requests", ("title", "number", "state", "created_on", "request_id")
)
attachments_list = listing(
    "Attachments",
    "attachments",
    ("file_name", "size_label", "attachment_id"),
)
favourites_default = listing("Favourites", "items", ("title", "pinned", "favourite_id"))
payments_services = listing(
    "Payment services", "records", ("title", "record_id", "url")
)
payments_service = detail("Payment service", ("service_id", "title", "fixed_amount"))
payments_checkout_link = detail(
    "Checkout link", ("title", "checkout_url", "requires_browser_completion")
)
attachments_download = download


def catalog_categories(console, data):
    root = Tree("Catalog categories")
    categories = data.get("categories") or []
    branches = {}

    def add(item, visiting):
        ident = item.get("category_id")
        if ident in branches:
            return branches[ident]
        if ident in visiting:
            return root
        parent = next(
            (
                entry
                for entry in categories
                if entry.get("category_id") == item.get("parent_id")
            ),
            None,
        )
        branch = add(parent, visiting | {ident}) if parent else root
        branches[ident] = branch.add(f"{item.get('title', '')} ({ident})")
        return branches[ident]

    for item in categories:
        add(item, set())
    console.print(root)
    pagination(console, data)


def catalog_item(console, data):
    details(
        console,
        "Catalog item",
        data,
        ("item_id", "title", "summary", "description", "mandatory_attachment"),
    )
    fields = []
    for field in data.get("fields") or []:
        choices = ", ".join(
            f"{choice.get('label')} ({choice.get('value')})"
            for choice in field.get("choices") or []
        )
        fields.append({**field, "choices": choices})
    if fields:
        table(
            console,
            "Form fields",
            fields,
            ("name", "label", "type", "mandatory", "read_only", "choices"),
        )


def draft_preview(console, data):
    details(
        console,
        "Form review",
        data,
        (
            "title",
            "state",
            "ready",
            "missing_fields",
            "invalid_fields",
            "available_actions",
        ),
    )
    fields = []
    for field in data.get("fields") or []:
        choices = ", ".join(
            f"{choice.get('label')} ({choice.get('value')})"
            for choice in field.get("choices") or []
        )
        fields.append({**field, "choices": choices})
    if fields:
        table(
            console,
            "Form fields",
            fields,
            (
                "name",
                "label",
                "value",
                "display_value",
                "mandatory",
                "read_only",
                "choices",
            ),
        )


def checkout_preview(console, data):
    table(console, "Checkout", data.get("items"), ("title", "quantity", "price_label"))
    details(
        console,
        "Delivery",
        data,
        ("delivery_address", "special_instructions", "expires_at"),
    )


def appointment_preview(console, data):
    details(
        console,
        "Appointment",
        data,
        (
            "enabled",
            "duration_minutes",
            "future_bookable_days",
            "bookable_weekdays",
            "mandatory",
        ),
    )


def _records(console, title, rows):
    records = []
    for row in rows or []:
        fields = [
            f"{field.get('label') or field.get('name')}: {field['value']}"
            for field in row.get("fields") or []
            if field.get("value") not in (None, "")
        ]
        records.append({**row, "details": "\n".join(fields)})
    table(console, title, records, ("title", "details", "url"))


def profile_default(console, data):
    table(
        console, "Profile", data.get("fields"), ("name", "label", "value", "read_only")
    )
    table(
        console,
        "Preferences",
        data.get("preferences"),
        ("name", "label", "value", "enabled"),
    )
    if data.get("notifications_enabled") is not None:
        console.print(
            "Notifications: " + ("On" if data["notifications_enabled"] else "Off")
        )


def requests_show(console, data):
    request = data.get("request") or {}
    details(
        console,
        "Request",
        request,
        ("request_id", "number", "title", "state", "created_on", "url"),
    )
    for record in data.get("records") or []:
        identifier = record.get("record_id")
        title = record.get("record_type") or "Record"
        title = f"{title} ({identifier})" if identifier else title
        for key, suffix in (("fields", ""), ("variables", " — form answers")):
            if record.get(key):
                table(console, title + suffix, record[key], ("label", "value"))
    if data.get("requested_items"):
        table(console, "Requested items", data["requested_items"], ("item_id", "stage"))
    pagination(console, data)


def requests_activity(console, data):
    entries = data.get("entries") or []
    if not entries:
        console.print("Activity: No results.")
    for entry in entries:
        heading = entry.get("author") or entry.get("kind") or "Activity"
        console.rule(heading, style="bold")
        details(
            console, "Activity", entry, ("created_on", "kind", "text", "attachment_id")
        )
    if data.get("available_actions"):
        console.print("Available actions: " + ", ".join(data["available_actions"]))


def dashboard(console, data):
    for key, title in (
        ("announcements", "Announcements"),
        ("actions", "Actions"),
        ("appointments", "Appointments"),
        ("popular_links", "Popular links"),
    ):
        _records(console, title, data.get(key))


def announcements(console, data):
    _records(console, "Announcements", data.get("records"))
    pagination(console, data)


def actions(console, data):
    _records(console, "Actions", data.get("records"))
    pagination(console, data)


def links(console, data):
    _records(console, "Links", data.get("records"))
    pagination(console, data)


def appointments_default(console, data):
    _records(console, "Appointments", data.get("records"))
    pagination(console, data)


def cart_default(console, data):
    table(
        console,
        "Cart",
        data.get("items"),
        ("title", "quantity", "price_label", "cart_item_id"),
    )
    table(console, "Saved carts", data.get("saved_carts"), ("name", "cart_id"))
    details(
        console,
        "Delivery",
        data,
        ("delivery_address", "special_instructions", "two_step_checkout"),
    )


def cart_saved_show(console, data):
    _records(console, "Saved cart", data.get("records"))
    pagination(console, data)


def knowledge_comments_default(console, data):
    comments = data.get("comments") or []
    if not comments:
        console.print("Comments: No results.")
    for comment in comments:
        console.rule(comment.get("author") or "Comment", style="bold")
        details(
            console,
            "Comment",
            comment,
            (
                "comment_id",
                "created_on",
                "text",
                "liked",
                "attachment_ids",
            ),
        )
    pagination(console, data)


profile_set = action
profile_picture = action
profile_notifications = action
profile_preference = action
knowledge_comments_add = action
knowledge_comments_delete = action
knowledge_comments_like = action
knowledge_rate = action
knowledge_helpful = action
knowledge_flag = action
knowledge_subscribe = action
knowledge_favourite = action
knowledge_send_to_self = action
requests_reply = action
requests_action = action
attachments_upload = action
attachments_delete = action
attachments_rename = action
cart_quantity = action
cart_remove = action
cart_clear = action
cart_saved_load = action
cart_saved_replace = action
cart_saved_delete = action
cart_saved_create = action
favourites_pin = action
favourites_unpin = action
favourites_remove = action
favourites_clear = action
catalog_favourite = action
requests_apply = action
cart_checkout = action
appointments_book = action
