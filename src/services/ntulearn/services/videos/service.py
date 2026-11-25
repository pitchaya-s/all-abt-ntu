"""Resolve a course video item and save its Kaltura source."""

from typing import Annotated
from pydantic import Field
from ...contracts import CourseReference, LearnID


from pathlib import Path

from ...client.client import identifier
from ...models import Download, LearnError
from .kaltura import (
    _browseandembed_link,
    _capture_viewer_manifest,
    _download_manifest_url,
    _player,
    _player_from_browseandembed,
    _webdav_link,
)


async def download_video(
    client,
    course_id: CourseReference,
    content_id: LearnID,
    destination: str,
    max_mb: Annotated[int, Field(ge=1, le=2000, strict=True)] = 1000,
) -> Download:
    "Download a Kaltura video embedded in an NTULearn content item to a new local file. Uses your normal course access and a short-lived viewer session; max_mb is 1–2000, existing files are never overwritten, and NTULearn is not modified."
    async with client.session.operation():
        content_id = identifier(content_id)
        if type(max_mb) is not int or not 1 <= max_mb <= 2000:
            raise LearnError("max_mb must be an integer from 1 to 2000.")
        target = Path(destination).expanduser().absolute()
        if any(part.is_symlink() for part in (target.parent, *target.parent.parents)):
            raise LearnError(
                "Video download directories must not contain symbolic links."
            )
        if target.exists() or not target.parent.is_dir():
            raise LearnError(
                "Choose a new video file path in an existing directory; existing files are never overwritten."
            )

        course_id = await client.resolve_course_id(course_id)
        record = await client.get_content_record(course_id, content_id)
        fragments = [
            value
            for value in (record.get("body"), record.get("description"))
            if isinstance(value, str)
        ]
        if not fragments:
            raise LearnError("This NTULearn item has no readable video content body.")

        player = None
        for fragment in fragments:
            player = _player(fragment)
            if player:
                break
        if player is None:
            webdav = next(
                (link for fragment in fragments if (link := _webdav_link(fragment))),
                None,
            )
            if webdav is not None:
                wrapper = await client.session.get_webdav_wrapper(webdav)
                player = _player(wrapper)
            else:
                browseandembed = next(
                    (
                        item
                        for fragment in fragments
                        if (item := _browseandembed_link(fragment))
                    ),
                    None,
                )
                if browseandembed is None:
                    raise LearnError(
                        "No supported Kaltura player or NTULearn video wrapper was found on this content item."
                    )
                wrapper = await client.session.get_browseandembed_page(
                    browseandembed[0]
                )
                player = _player(wrapper) or _player_from_browseandembed(
                    wrapper, browseandembed[1]
                )
        if player is None:
            raise LearnError(
                "This NTULearn content item does not contain a supported Kaltura player."
            )

        player_url, entry_id = player
        manifest_url = await _capture_viewer_manifest(player_url, entry_id)
        download_url = _download_manifest_url(manifest_url, entry_id)
        return await client.session.download_kaltura_video(
            download_url,
            destination,
            max_mb * 1_000_000,
            player_url,
        )
