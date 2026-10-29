"""Plugin and Skill API endpoints."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.plugin import Plugin, Skill
from app.schemas.plugin import (
    PluginCreate,
    PluginUpdate,
    PluginRead,
    PluginWithSkills,
    SkillCreate,
    SkillUpdate,
    SkillRead,
    PaginatedResponse,
    SkillPaginatedResponse,
)

router = APIRouter(prefix="/plugins", tags=["plugins"])


# Plugin endpoints

@router.get("", response_model=PaginatedResponse)
def list_plugins(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in name, description, tags"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
) -> PaginatedResponse:
    """List plugins with pagination, search, and filtering."""
    query = select(Plugin)

    # Apply filters
    if is_active is not None:
        query = query.where(Plugin.is_active == is_active)

    if tag:
        query = query.where(Plugin.tags.ilike(f"%{tag}%"))

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Plugin.name.ilike(search_term),
                Plugin.description.ilike(search_term),
                Plugin.tags.ilike(search_term),
            )
        )

    # Count total
    total = db.scalar(select(func.count()).select_from(query.subquery()))

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    plugins = db.scalars(query).all()

    total_pages = (total + page_size - 1) // page_size

    return PaginatedResponse(
        items=[PluginRead.model_validate(p) for p in plugins],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{plugin_id}", response_model=PluginWithSkills)
def get_plugin(plugin_id: int, db: Session = Depends(get_db)) -> PluginWithSkills:
    """Get a plugin by ID with its skills."""
    plugin = db.get(Plugin, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return PluginWithSkills.model_validate(plugin)


@router.get("/slug/{slug}", response_model=PluginWithSkills)
def get_plugin_by_slug(slug: str, db: Session = Depends(get_db)) -> PluginWithSkills:
    """Get a plugin by slug with its skills."""
    plugin = db.scalar(select(Plugin).where(Plugin.slug == slug))
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return PluginWithSkills.model_validate(plugin)


@router.post("", response_model=PluginRead, status_code=201)
def create_plugin(plugin: PluginCreate, db: Session = Depends(get_db)) -> PluginRead:
    """Create a new plugin."""
    # Check slug uniqueness
    existing = db.scalar(select(Plugin).where(Plugin.slug == plugin.slug))
    if existing:
        raise HTTPException(status_code=409, detail="Plugin with this slug already exists")

    db_plugin = Plugin(**plugin.model_dump())
    db.add(db_plugin)
    db.commit()
    db.refresh(db_plugin)
    return PluginRead.model_validate(db_plugin)


@router.patch("/{plugin_id}", response_model=PluginRead)
def update_plugin(plugin_id: int, plugin_update: PluginUpdate, db: Session = Depends(get_db)) -> PluginRead:
    """Update a plugin."""
    plugin = db.get(Plugin, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")

    update_data = plugin_update.model_dump(exclude_unset=True)

    # Check slug uniqueness if being updated
    if "slug" in update_data:
        existing = db.scalar(
            select(Plugin).where(Plugin.slug == update_data["slug"], Plugin.id != plugin_id)
        )
        if existing:
            raise HTTPException(status_code=409, detail="Plugin with this slug already exists")

    for field, value in update_data.items():
        setattr(plugin, field, value)

    db.commit()
    db.refresh(plugin)
    return PluginRead.model_validate(plugin)


@router.delete("/{plugin_id}", status_code=204)
def delete_plugin(plugin_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a plugin."""
    plugin = db.get(Plugin, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")

    db.delete(plugin)
    db.commit()


# Skill endpoints

@router.get("/{plugin_id}/skills", response_model=SkillPaginatedResponse)
def list_skills(
    plugin_id: int,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in name, description"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
) -> SkillPaginatedResponse:
    """List skills for a plugin with pagination and filtering."""
    # Verify plugin exists
    plugin = db.get(Plugin, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")

    query = select(Skill).where(Skill.plugin_id == plugin_id)

    if is_active is not None:
        query = query.where(Skill.is_active == is_active)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Skill.name.ilike(search_term),
                Skill.description.ilike(search_term),
            )
        )

    total = db.scalar(select(func.count()).select_from(query.subquery()))

    query = query.offset((page - 1) * page_size).limit(page_size)
    skills = db.scalars(query).all()

    total_pages = (total + page_size - 1) // page_size

    return SkillPaginatedResponse(
        items=[SkillRead.model_validate(s) for s in skills],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{plugin_id}/skills/{skill_id}", response_model=SkillRead)
def get_skill(plugin_id: int, skill_id: int, db: Session = Depends(get_db)) -> SkillRead:
    """Get a skill by ID."""
    skill = db.get(Skill, skill_id)
    if not skill or skill.plugin_id != plugin_id:
        raise HTTPException(status_code=404, detail="Skill not found")
    return SkillRead.model_validate(skill)


@router.post("/{plugin_id}/skills", response_model=SkillRead, status_code=201)
def create_skill(plugin_id: int, skill: SkillCreate, db: Session = Depends(get_db)) -> SkillRead:
    """Create a new skill for a plugin."""
    plugin = db.get(Plugin, plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")

    if skill.plugin_id != plugin_id:
        raise HTTPException(status_code=400, detail="Plugin ID mismatch")

    # Check slug uniqueness within plugin
    existing = db.scalar(
        select(Skill).where(Skill.plugin_id == plugin_id, Skill.slug == skill.slug)
    )
    if existing:
        raise HTTPException(status_code=409, detail="Skill with this slug already exists in this plugin")

    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return SkillRead.model_validate(db_skill)


@router.patch("/{plugin_id}/skills/{skill_id}", response_model=SkillRead)
def update_skill(
    plugin_id: int, skill_id: int, skill_update: SkillUpdate, db: Session = Depends(get_db)
) -> SkillRead:
    """Update a skill."""
    skill = db.get(Skill, skill_id)
    if not skill or skill.plugin_id != plugin_id:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = skill_update.model_dump(exclude_unset=True)

    # Check slug uniqueness if being updated
    if "slug" in update_data:
        existing = db.scalar(
            select(Skill).where(
                Skill.plugin_id == plugin_id,
                Skill.slug == update_data["slug"],
                Skill.id != skill_id,
            )
        )
        if existing:
            raise HTTPException(status_code=409, detail="Skill with this slug already exists in this plugin")

    for field, value in update_data.items():
        setattr(skill, field, value)

    db.commit()
    db.refresh(skill)
    return SkillRead.model_validate(skill)


@router.delete("/{plugin_id}/skills/{skill_id}", status_code=204)
def delete_skill(plugin_id: int, skill_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a skill."""
    skill = db.get(Skill, skill_id)
    if not skill or skill.plugin_id != plugin_id:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()

