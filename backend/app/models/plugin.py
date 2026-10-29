"""Plugin and Skill database models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Plugin(Base):
    """Plugin model representing an AI/ML plugin or extension."""

    __tablename__ = "plugins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    version = Column(String(50), nullable=True)
    author = Column(String(255), nullable=True)
    repository_url = Column(String(500), nullable=True)
    homepage_url = Column(String(500), nullable=True)
    license = Column(String(100), nullable=True)
    tags = Column(String(500), nullable=True)  # comma-separated tags
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    skills = relationship("Skill", back_populates="plugin", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_plugins_name_search", "name"),
        Index("ix_plugins_tags_search", "tags"),
    )


class Skill(Base):
    """Skill model representing a capability provided by a plugin."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    plugin_id = Column(Integer, ForeignKey("plugins.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    input_schema = Column(Text, nullable=True)  # JSON schema for inputs
    output_schema = Column(Text, nullable=True)  # JSON schema for outputs
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    plugin = relationship("Plugin", back_populates="skills")

    __table_args__ = (
        Index("ix_skills_name_search", "name"),
        Index("ix_skills_plugin_slug", "plugin_id", "slug"),
    )

