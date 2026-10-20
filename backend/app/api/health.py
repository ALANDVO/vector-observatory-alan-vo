"""Health check API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Basic health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


@router.get("/health/db")
def health_check_db(db: Session = Depends(get_db)) -> dict:
    """Database connectivity health check."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}