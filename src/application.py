"""Owned, lazy NTU service resources for one CLI or MCP application."""

from contextlib import AsyncExitStack
from threading import RLock
from contextlib import contextmanager

from shared.settings import resolved_settings, settings_scope


class Application:
    """Create service resources on first use and close only those created here."""

    def __init__(self):
        self._settings = resolved_settings()
        self._resources = {}
        self._lock = RLock()
        self._exit = AsyncExitStack()
        self._closed = False

    def _get(self, name, factory, close=None, *, asynchronous=False):
        with self._lock:
            if self._closed:
                raise RuntimeError("This application has already been closed.")
            if name not in self._resources:
                with settings_scope(self._settings):
                    resource = factory()
                if close is not None:
                    callback = lambda: close(resource)
                    if asynchronous:
                        self._exit.push_async_callback(callback)
                    else:
                        self._exit.callback(callback)
                self._resources[name] = resource
            return self._resources[name]

    @contextmanager
    def operation(self):
        from services.stars.runtime import stars_scope

        with settings_scope(self._settings), stars_scope(lambda: self.stars_public):
            yield

    @property
    def stars_public(self):
        from services.stars.client.http import create_public_client
        from services.stars.runtime import StarsResources

        return self._get(
            "stars_public",
            lambda: StarsResources(create_public_client()),
            StarsResources.close,
        )

    @property
    def mazemap(self):
        from services.mazemap.client import MapClient

        return self._get("mazemap", MapClient, lambda client: client.http.close())

    @property
    def faculty(self):
        from services.faculty.client import FacultyClient

        return self._get("faculty", FacultyClient, lambda client: client.http.close())

    @property
    def news(self):
        from services.news.client import NewsClient

        return self._get("news", NewsClient, lambda client: client.http.close())

    @property
    def campus_services(self):
        from services.campus.client import ServiceClient

        return self._get(
            "campus_services", ServiceClient, lambda client: client.http.close()
        )

    @property
    def library(self):
        from services.library.client import LibraryClient

        return self._get("library", LibraryClient, lambda client: client.http.close())

    @property
    def library_facilities(self):
        from services.library.facilities import FacilitiesClient

        return self._get(
            "library_facilities", FacilitiesClient, lambda client: client.http.close()
        )

    @property
    def library_session(self):
        from services.library.facilities.session import FacilitySession

        return self._get(
            "library_session", FacilitySession, lambda session: session.close()
        )

    @property
    def research(self):
        from services.drntu.rest.client import RepositoryClient

        return self._get(
            "research", RepositoryClient, lambda client: client.http.close()
        )

    @property
    def research_oai(self):
        from services.drntu.oai import OAIClient

        return self._get("research_oai", OAIClient, lambda client: client.close())

    @property
    def omnibus(self):
        from services.omnibus.client import OmnibusClient

        return self._get("omnibus", OmnibusClient, lambda client: client.close())

    @property
    def careeraxis(self):
        from services.careeraxis.client import CareerAxisClient

        return self._get(
            "careeraxis", CareerAxisClient, lambda client: client.session.close()
        )

    @property
    def careeraxis_session(self):
        return self.careeraxis.session

    @property
    def learn_session(self):
        from services.ntulearn.client import Session

        return self._get(
            "learn_session", Session, lambda session: session.close(), asynchronous=True
        )

    @property
    def learn(self):
        from services.ntulearn.client import LearnClient

        return self._get("learn", lambda: LearnClient(self.learn_session))

    @property
    def onestop_session(self):
        from services.onestop.session import OneStopSession

        return self._get(
            "onestop_session", OneStopSession, lambda session: session.close()
        )

    @property
    def onestop(self):
        from services.onestop.client import OneStopClient

        return self._get("onestop", lambda: OneStopClient(self.onestop_session))

    @property
    def onestop_forms(self):
        from services.onestop.services.forms import FormService

        return self._get("onestop_forms", lambda: FormService(self.onestop_session))

    @property
    def onestop_knowledge(self):
        from services.onestop.services.knowledge import KnowledgeService

        return self._get(
            "onestop_knowledge", lambda: KnowledgeService(self.onestop_session)
        )

    @property
    def onestop_tickets(self):
        from services.onestop.services.tickets import TicketService

        return self._get(
            "onestop_tickets", lambda: TicketService(self.onestop_session, self.onestop)
        )

    @property
    def onestop_files(self):
        from services.onestop.attachments import AttachmentService

        return self._get(
            "onestop_files",
            lambda: AttachmentService(
                self.onestop_session, self.onestop_tickets, self.onestop_knowledge
            ),
        )

    @property
    def onestop_portal(self):
        from services.onestop.services.portal import PortalService

        return self._get("onestop_portal", lambda: PortalService(self.onestop_session))

    @property
    def onestop_cart(self):
        from services.onestop.services.cart import CartService

        return self._get("onestop_cart", lambda: CartService(self.onestop_session))

    @property
    def onestop_favourites(self):
        from services.onestop.services.cart import FavouriteService

        return self._get(
            "onestop_favourites", lambda: FavouriteService(self.onestop_session)
        )

    @property
    def onestop_appointments(self):
        from services.onestop.services.appointments import AppointmentService

        return self._get(
            "onestop_appointments",
            lambda: AppointmentService(self.onestop_session, self.onestop_forms),
        )

    @property
    def stars_personal(self):
        from services.stars.wish.session import WishSessionManager

        return self._get(
            "stars_personal", WishSessionManager, lambda session: session.close()
        )

    async def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True
        await self._exit.aclose()
