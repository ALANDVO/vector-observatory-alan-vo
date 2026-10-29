"""Backend API package."""

from app.api.health import router as health_router
from app.api.plugins import router as plugins_router

__all__ = ["health_router", "plugins_router"]