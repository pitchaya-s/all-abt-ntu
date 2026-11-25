"""Terminal views for faculty commands."""

from .common import listing

search = listing("Faculty", "profiles", ("name", "school", "email", "profile_url"))
interests = listing("Research interests", "interests", ("name", "interest_id"))
