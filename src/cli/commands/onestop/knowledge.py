"""One Stop knowledge commands."""

from typing import Annotated, Literal, Optional

import typer

from ...execution import application_scope
from ...helpers import group
from ...renderers import onestop as views
from ...services import invoke

app = group(default=False)
g_knowledge_comments = group(default=True)
app.add_typer(
    g_knowledge_comments, name="comments", help="Read or manage article comments."
)


@app.command("search")
def cmd_knowledge_search(
    query: str = typer.Argument(..., help="Search text or keywords."),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Search the signed-in student's One Stop knowledge base."""
    with application_scope() as application:
        return invoke(
            application.onestop.search_knowledge,
            {"query": query, "limit": limit, "offset": offset, "refresh": refresh},
            json_output,
            presenter=views.knowledge_search,
        )


@app.command("article")
def cmd_knowledge_article(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    offset: int = typer.Option(
        0, "--offset", help="Number of article characters to skip."
    ),
    max_chars: Annotated[
        int,
        typer.Option(
            help="Maximum number of text characters to return. Default: 12000."
        ),
    ] = 12000,
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Fetch fresh data instead of cached results."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.knowledge_article,
        )


@app.command("feedback")
def cmd_knowledge_feedback(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read native knowledge capabilities: ratings, helpfulness, comments, flags/reasons, subscription/inheritance, favourites and self-delivery channels."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.get_feedback,
            {"article_id": article_id},
            json_output,
            presenter=views.knowledge_feedback,
        )


@g_knowledge_comments.command("__default__", hidden=True)
def cmd_knowledge_comments_default(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results."),
    offset: int = typer.Option(0, "--offset", help="Number of results to skip."),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Read visible knowledge comments/replies, author display names, text, dates, reactions, attachment IDs and delete permissions."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.list_comments,
            {"article_id": article_id, "limit": limit, "offset": offset},
            json_output,
            presenter=views.knowledge_comments_default,
        )


@g_knowledge_comments.command("add")
def cmd_knowledge_comments_add(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    text: str = typer.Option(
        ..., "--text", help="The text to send. Quote multiword text in the shell."
    ),
    parent_id: Optional[str] = typer.Option(
        None,
        "--parent",
        help="The ID of a parent folder. Omit it to browse the top level.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Publish plain-text feedback to a knowledge article, or reply to a visible parent comment."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.add_comment,
            {"article_id": article_id, "text": text, "parent_id": parent_id},
            json_output,
            side_effect=True,
            presenter=views.knowledge_comments_add,
        )


@g_knowledge_comments.command("delete")
def cmd_knowledge_comments_delete(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    comment_id: Annotated[
        str,
        typer.Argument(
            help="The comment ID returned by the relevant listing or details command."
        ),
    ],
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Delete a visible article comment only when the native menu permits deletion by the current user."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.delete_comment,
            {"article_id": article_id, "comment_id": comment_id},
            json_output,
            side_effect=True,
            presenter=views.knowledge_comments_delete,
        )


@g_knowledge_comments.command("like")
def cmd_knowledge_comments_like(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    comment_id: Annotated[
        str,
        typer.Argument(
            help="The comment ID returned by the relevant listing or details command."
        ),
    ],
    liked: Literal["on", "off"] = typer.Option(
        ...,
        "--state",
        help="Choose whether the comment should be liked. Choices: on, off.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.knowledge_comments_like,
        )


@app.command("rate")
def cmd_knowledge_rate(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    rating: Annotated[int, typer.Argument(help="The article rating.")],
    reason_id: Annotated[
        Optional[str],
        typer.Option(
            help="The reason ID returned by the relevant listing or details command."
        ),
    ] = None,
    details: Annotated[
        str,
        typer.Option(help="Additional details for the selected feedback or action."),
    ] = "",
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.knowledge_rate,
        )


@app.command("helpful")
def cmd_knowledge_helpful(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    helpful: Annotated[
        Literal["yes", "no"],
        typer.Argument(
            help="Choose whether the article was helpful. Choices: yes, no."
        ),
    ],
    reason_id: Annotated[
        Optional[str],
        typer.Option(
            help="The reason ID returned by the relevant listing or details command."
        ),
    ] = None,
    details: Annotated[
        str,
        typer.Option(help="Additional details for the selected feedback or action."),
    ] = "",
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.knowledge_helpful,
        )


@app.command("flag")
def cmd_knowledge_flag(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    text: str = typer.Option(
        ..., "--text", help="The text to send. Quote multiword text in the shell."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Flag a knowledge article with the user's explanation when the native flag control is available."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.flag,
            {"article_id": article_id, "text": text},
            json_output,
            side_effect=True,
            presenter=views.knowledge_flag,
        )


@app.command("subscribe")
def cmd_knowledge_subscribe(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    subscribed: Literal["on", "off"] = typer.Option(
        ..., "--state", help="The requested subscription state. Choices: on, off."
    ),
    include_knowledge_base: bool = typer.Option(
        False,
        "--include-knowledge-base",
        help="Include the knowledge-base subscription where the native action supports it.",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
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
            presenter=views.knowledge_subscribe,
        )


@app.command("favourite")
def cmd_knowledge_favourite(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    favourite: Literal["on", "off"] = typer.Option(
        ..., "--state", help="The requested favourite state. Choices: on, off."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Set an article's native favourite state when its Favourite control is enabled."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.set_favourite,
            {"article_id": article_id, "favourite": favourite == "on"},
            json_output,
            side_effect=True,
            presenter=views.knowledge_favourite,
        )


@app.command("send-to-self")
def cmd_knowledge_send_to_self(
    article_id: Annotated[
        str,
        typer.Argument(
            help="The article ID returned by the relevant listing or details command."
        ),
    ],
    channel: Annotated[
        Literal["email", "sms"],
        typer.Option(
            help="The delivery channel offered by the service. Choices: email, sms. Default: email."
        ),
    ] = "email",
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Write JSON to stdout."
    ),
):
    """Send this article to your registered email/SMS channel using the native Send to myself action."""
    with application_scope() as application:
        return invoke(
            application.onestop_knowledge.send_to_self,
            {"article_id": article_id, "channel": channel},
            json_output,
            side_effect=True,
            presenter=views.knowledge_send_to_self,
        )
