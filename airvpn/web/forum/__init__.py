"""For now this will be read-only."""

from airvpn.web.network import WebSession
from .models import *

from bs4 import BeautifulSoup

class ForumManager:
    """Entry point for browsing the forum's categories.

    Attributes:
        session (WebSession): The session used to fetch related resources.
        categories (list[Category]): The forum's top-level categories, fetched and cached lazily on first access.
    """

    __URL__ = "https://airvpn.org/forums/"

    def __init__(self, session: WebSession):
        self.session = session
        self._categories: list[Category] = []

    @property
    def categories(self) -> list[Category]:
        """The forum's top-level categories, fetching them on first access if not already loaded."""
        if len(self._categories) == 0:
            self.update()

        return self._categories

    def update(self):
        """Fetch the forum index page and (re)populate self.categories, each with its forums pre-loaded."""
        response = self.session.request("get", ForumManager.__URL__)
        soup = BeautifulSoup(response.text, "html.parser")

        for forum_container in soup.find_all("li", {"class": "cForumRow", "data-categoryid": True}):
            category_title_h2 = forum_container.find("h2", {"class": "cForumTitle"})
            title_a = category_title_h2.find_all("a")[1]

            url = title_a.get("href")
            title = title_a.text

            category = Category(self.session, title, url)
            category.update(forum_container.find_all("li", {"class": "cForumRow", "data-forumid": True}))

            self._categories.append(category)