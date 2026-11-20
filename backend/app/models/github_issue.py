"""GitHub Issue database model."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class GitHubIssue(Base):
    """GitHub Issue model representing a stored issue from a reference repo."""

    __tablename__ = "github_issues"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, nullable=False, index=True)
    repository = Column(String(255), nullable=False, index=True)
    number = Column(Integer, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    body = Column(Text, nullable=True)
    state = Column(String(50), nullable=False, default="open")  # open, closed
    labels = Column(String(500), nullable=True)  # comma-separated labels
    author_login = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Triage fields
    triaged = Column(Boolean, default=False, nullable=False)
    triage_score = Column(Integer, nullable=True)  # AI quality score
    triage_notes = Column(Text, nullable=True)  # AI advisory notes

    plugin_assignments = relationship("PluginAssignment", back_populates="github_issue", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_githubissues_repo_number", "repository", "number"),
        Index("ix_githubissues_triaged", "triaged"),
    )
