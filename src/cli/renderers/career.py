"""Terminal views for CareerAxis commands."""

from .common import auth_status as auth_status
from .common import detail, listing

opportunities_search = listing("Opportunities", "opportunities", ("title", "url"))
opportunities_show = detail(
    "Opportunity", ("title", "text", "application_links", "url")
)
record = detail("CareerAxis record", ("title", "text", "links", "url"))
events_search = listing("Events", "items", ("title", "summary", "url"))
resources_search = listing("Resources", "items", ("title", "summary", "url"))
employers_search = listing("Employers", "items", ("title", "summary", "url"))
appointments_topics = listing("Coaching topics", "items", ("title", "summary", "url"))
internships_search = listing("Internships", "items", ("title", "summary", "url"))
