"""Bounded content traversal and substring search; attachment bytes are not searched."""

from ..contracts import CourseIDs, Depth, LearnID, Nodes, Query, RequestBudget, Results


from ..client.client import identifier, model
from ..models import ContentMatch, ContentNode, ContentSearch, ContentTree, LearnError
from .scan import LimitReached, Scan, resolve_course_ids, pages


def bounds(max_depth, max_nodes):
    if type(max_depth) is not int or not 1 <= max_depth <= 10:
        raise LearnError("max_depth must be between 1 and 10; root items are depth 1.")
    if type(max_nodes) is not int or not 1 <= max_nodes <= 5000:
        raise LearnError("max_nodes must be between 1 and 5000.")


async def walk(client, scan, course_id, max_depth, max_nodes, refresh, roots=None):
    course_id = identifier(course_id)
    bounds(max_depth, max_nodes)
    seen: set[str] = set()

    async def visit(parent_id, depth, breadcrumb, nodes):
        try:
            async for item in pages(
                scan,
                client.get_course_contents,
                "contents",
                course_id,
                parent_id,
                refresh=refresh,
            ):
                if len(seen) >= max_nodes:
                    raise LimitReached(
                        "Content node limit reached; increase max_nodes or browse individual folders."
                    )
                if item.id in seen:
                    scan.issue(
                        "content",
                        "Repeated or cyclic content ID was not followed again.",
                        course_id,
                        item.id,
                    )
                    continue
                seen.add(item.id)
                node = model(ContentNode, **item.model_dump())
                nodes.append(node)
                path = [*breadcrumb, node.title]
                yield node, path
                if item.has_children:
                    if depth >= max_depth:
                        node.children_complete = False
                        scan.issue(
                            "content",
                            "Folder not opened because max_depth was reached.",
                            course_id,
                            item.id,
                        )
                    else:
                        issue_count = len(scan.issues)
                        async for child in visit(
                            item.id, depth + 1, path, node.children
                        ):
                            yield child
                        node.children_complete = len(scan.issues) == issue_count
        except LearnError as error:
            scan.issue("content", error, course_id, parent_id)

    async for node in visit(None, 1, [], roots if roots is not None else []):
        yield node


async def tree(client, scan, course_id, max_depth, max_nodes, refresh):
    roots: list[ContentNode] = []
    async for _ in walk(client, scan, course_id, max_depth, max_nodes, refresh, roots):
        pass
    return roots


async def get_content_tree(
    client,
    course_id: LearnID,
    max_depth: Depth = 5,
    max_nodes: Nodes = 1000,
    max_requests: RequestBudget = 100,
    refresh: bool = False,
) -> ContentTree:
    "Read a course's nested content tree. Root items are depth 1; max_depth is at most 10. Unopened, denied or cyclic branches are explicit; complete=false means the tree is partial."
    async with client.session.operation():
        scan = Scan(max_requests)
        contents = await tree(client, scan, course_id, max_depth, max_nodes, refresh)
        return model(
            ContentTree,
            course_id=identifier(course_id),
            contents=contents,
            max_depth=max_depth,
            **scan.metadata(),
        )


async def search_all_courses(
    client,
    query: Query,
    course_ids: CourseIDs | None = None,
    max_depth: Depth = 5,
    max_nodes: Nodes = 1000,
    max_results: Results = 50,
    max_requests: RequestBudget = 100,
    refresh: bool = False,
) -> ContentSearch:
    """Recursively search content across available enrolled courses, or selected course_ids. Each result carries course_id and breadcrumb. max_nodes and max_requests apply to the whole search. Check complete/issues for coverage."""
    async with client.session.operation():
        if not isinstance(query, str) or not 1 <= len(query.strip()) <= 200:
            raise LearnError("query must contain 1–200 non-whitespace characters.")
        if type(max_results) is not int or not 1 <= max_results <= 200:
            raise LearnError("max_results must be between 1 and 200.")
        bounds(max_depth, max_nodes)
        query = query.strip()
        scan = Scan(max_requests)
        matches, searched = [], []
        try:
            courses = await resolve_course_ids(client, scan, course_ids, refresh)
        except LearnError as error:
            scan.issue("courses", error)
            courses = []
        remaining_nodes = max_nodes
        for course in courses:
            if scan.requests >= scan.limit or remaining_nodes <= 0:
                scan.issue(
                    "search",
                    "Search limit reached before all selected courses were visited.",
                )
                break
            searched.append(course)
            async for node, breadcrumb in walk(
                client, scan, course, max_depth, remaining_nodes, refresh
            ):
                remaining_nodes -= 1
                source = "\n".join(
                    value
                    for value in (node.title, node.body, node.description)
                    if value
                )
                position = source.casefold().find(query.casefold())
                if position < 0:
                    continue
                matches.append(
                    ContentMatch(
                        course_id=course,
                        content_id=node.id,
                        title=node.title,
                        breadcrumb=breadcrumb,
                        excerpt=source[
                            max(0, position - 80) : position + len(query) + 200
                        ],
                    )
                )
                if len(matches) >= max_results:
                    scan.issue(
                        "search",
                        "max_results reached; narrow the query to inspect additional matches.",
                    )
                    return model(
                        ContentSearch,
                        query=query,
                        courses_searched=searched,
                        matches=matches,
                        **scan.metadata(),
                    )
        return model(
            ContentSearch,
            query=query,
            courses_searched=searched,
            matches=matches,
            **scan.metadata(),
        )


async def search_course_content(
    client,
    course_id: LearnID,
    query: Query,
    max_depth: Depth = 5,
    max_nodes: Nodes = 1000,
    max_results: Results = 50,
    max_requests: RequestBudget = 100,
    refresh: bool = False,
) -> ContentSearch:
    """Recursively search one course's content titles, body and description for a case-insensitive substring. Results include course_id and breadcrumbs. Does not search inside attachment bytes. Bounded or denied folders are reported in issues."""
    return await search_all_courses(
        client,
        query,
        [course_id],
        max_depth,
        max_nodes,
        max_results,
        max_requests,
        refresh,
    )
