"""Terminal views for news commands."""

from .common import detail, listing

search = listing("News", "stories", ("title", "published_date", "url"))
categories = listing("Categories", "categories", ("name", "id"))
article = detail("Article", ("title", "published_date", "text"))
