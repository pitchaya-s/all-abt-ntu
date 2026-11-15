"""Course rosters and groups visible to the authenticated user."""

from ..contracts import LearnID, Offset, PageSize


from ..client.client import PREFIX, identifier, mapping, model
from ..models import CourseGroups, CourseUsers, Group, Person
from ..parser.response import required, text


def person(user, user_id=None, role=None):
    name = mapping(user, "name")
    display = (
        user.get("preferredDisplayName")
        or name.get("preferredDisplayName")
        or user.get("displayName")
        or " ".join(
            part
            for part in (
                name.get("given") or user.get("givenName"),
                name.get("family") or user.get("familyName"),
            )
            if part
        )
    )
    return model(
        Person, id=user_id or required(user, "id"), name=display or None, role=role
    )


async def list_course_users(
    client,
    course_id: LearnID,
    limit: PageSize = 50,
    offset: Offset = 0,
    refresh: bool = False,
) -> CourseUsers:
    "List course users visible to your account, with their published names and roles. Includes instructors, TAs and students as NTU permits; does not expose raw profiles."
    course_id = identifier(course_id)
    rows, next_offset, freshness = await client.list_records(
        f"{PREFIX}/courses/{course_id}/users", limit, offset, refresh, expand="user"
    )
    users = [
        person(mapping(row, "user"), required(row, "userId"), row.get("courseRoleId"))
        for row in rows
    ]
    return model(
        CourseUsers,
        course_id=course_id,
        users=users,
        offset=offset,
        next_offset=next_offset,
        **freshness,
    )


async def list_course_groups(
    client,
    course_id: LearnID,
    limit: PageSize = 50,
    offset: Offset = 0,
    refresh: bool = False,
) -> CourseGroups:
    "List groups and group sets defined in a course. Use a group's ID with ntulearn_get_group_members; availability remains unknown when NTU omits it."
    course_id = identifier(course_id)
    rows, next_offset, freshness = await client.list_records(
        f"{PREFIX}/courses/{course_id}/groups", limit, offset, refresh
    )
    groups = [
        model(
            Group,
            id=required(row, "id"),
            name=required(row, "name"),
            description=text(row.get("description")),
            available=mapping(row, "availability").get("available"),
            parent_id=row.get("parentId"),
            is_group_set=row.get("isGroupSet"),
        )
        for row in rows
    ]
    return model(
        CourseGroups,
        course_id=course_id,
        groups=groups,
        offset=offset,
        next_offset=next_offset,
        **freshness,
    )


async def get_group_members(
    client,
    course_id: LearnID,
    group_id: LearnID,
    limit: PageSize = 50,
    offset: Offset = 0,
    refresh: bool = False,
) -> CourseUsers:
    "List visible members of a course group through Blackboard's browser membership API. Use a group ID from ntulearn_list_course_groups; a group set may have no direct members."
    course_id, group_id = identifier(course_id), identifier(group_id)
    rows, next_offset, freshness = await client.list_records(
        f"/learn/api/v1/courses/{course_id}/memberships",
        limit,
        offset,
        refresh,
        groupId=group_id,
        expand="user,courseRole",
        includeCount="true",
    )
    users = [
        person(
            mapping(row, "user"),
            required(row, "userId"),
            mapping(row, "courseRole").get("roleId") or row.get("courseRoleId"),
        )
        for row in rows
    ]
    return model(
        CourseUsers,
        course_id=course_id,
        group_id=group_id,
        users=users,
        offset=offset,
        next_offset=next_offset,
        **freshness,
    )
