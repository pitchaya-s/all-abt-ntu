"""Local authenticated library tools; never registered by the hosted server."""

from mcp_adapters.tools import ToolRegistrar
from mcp_adapters.tools import ToolPolicy


INSTRUCTIONS = (
    "library_get_facility_schedule requires the shared local keyring credentials and Chromium. "
    "It reads daily available/unavailable time grids and preserves source status classes. Missing slots are unknown. "
    "Booking identities and checksums are omitted. MFA or CAPTCHA stops login; no bookings are submitted. "
)


def register_tools(registrar: ToolRegistrar) -> None:
    registrar.tool(
        name="library_get_facility_schedule",
        annotations=ToolPolicy(
            read_only_hint=True,
            idempotent_hint=True,
            open_world_hint=True,
            failure_message="NTU Library returned an unexpected response format; no availability or record data was inferred.",
        ),
    )(registrar.app.library_session.get_schedule)
