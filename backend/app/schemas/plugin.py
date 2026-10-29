"""Pydantic schemas for Plugin and Skill API."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class PluginBase(BaseModel):
    """Base plugin schema."""

    name: str = Field(..., min_length=1, max_length=255, description="Plugin name")
    slug: str = Field(..., min_length=1, max_length=255, description="URL-friendly identifier")
    description: Optional[str] = Field(None, description="Plugin description")
    version: Optional[str] = Field(None, max_length=50, description="Plugin version")
    author: Optional[str] = Field(None, max_length=255, description="Plugin author")
    repository_url: Optional[HttpUrl] = Field(None, description="Repository URL")
    homepage_url: Optional[HttpUrl] = Field(None, description="Homepage URL")
    license: Optional[str] = Field(None, max_length=100, description="License identifier")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    is_active: bool = Field(True, description="Whether plugin is active")


class PluginCreate(PluginBase):
    """Schema for creating a plugin."""

    pass


class PluginUpdate(BaseModel):
    """Schema for updating a plugin (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    version: Optional[str] = Field(None, max_length=50)
    author: Optional[str] = Field(None, max_length=255)
    repository_url: Optional[HttpUrl] = None
    homepage_url: Optional[HttpUrl] = None
    license: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None
    is_active: Optional[bool] = None


class PluginRead(PluginBase):
    """Schema for reading a plugin."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SkillBase(BaseModel):
    """Base skill schema."""

    name: str = Field(..., min_length=1, max_length=255, description="Skill name")
    slug: str = Field(..., min_length=1, max_length=255, description="URL-friendly identifier")
    description: Optional[str] = Field(None, description="Skill description")
    input_schema: Optional[str] = Field(None, description="JSON schema for inputs")
    output_schema: Optional[str] = Field(None, description="JSON schema for outputs")
    is_active: bool = Field(True, description="Whether skill is active")


class SkillCreate(SkillBase):
    """Schema for creating a skill."""

    plugin_id: int = Field(..., description="Parent plugin ID")


class SkillUpdate(BaseModel):
    """Schema for updating a skill (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    input_schema: Optional[str] = None
    output_schema: Optional[str] = None
    is_active: Optional[bool] = None


class SkillRead(SkillBase):
    """Schema for reading a skill."""

    id: int
    plugin_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PluginWithSkills(PluginRead):
    """Plugin with nested skills."""

    skills: List[SkillRead] = []


class PaginatedResponse(BaseModel):
    """Generic paginated response."""

    items: List[PluginRead]
    total: int
    page: int
    page_size: int
    total_pages: int


class SkillPaginatedResponse(BaseModel):
    """Generic paginated response for skills."""

    items: List[SkillRead]
    total: int
    page: int
    page_size: int
    total_pages: int

