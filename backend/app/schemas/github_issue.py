"""GitHub Issue schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class GitHubIssueCreate(BaseModel):
    """Create a GitHubIssue from GitHub API payload."""
    github_id: int = Field(..., description="GitHub issue unique ID")
    repository: str = Field(..., description="Repository name (owner/name)")
    number: int = Field(..., description="Issue number")
    title: str = Field(..., description="Issue title")
    body: Optional[str] = Field(None, description="Issue body/description")
    state: str = Field("open", description="Issue state: open or closed")
    labels: Optional[List[str]] = Field(None, description="Issue labels")
    author_login: Optional[str] = Field(None, description="Issue author username")


class GitHubIssueRead(GitHubIssueCreate):
    """Read model for stored GitHub issue."""
    id: int
    triaged: bool
    triage_score: Optional[int] = None
    triage_notes: Optional[str] = None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class GitHubIssueList(BaseModel):
    """Paginated list of GitHub issues."""
    items: List[GitHubIssueRead]
    total: int
    page: int
    per_page: int


class TriageSuggestion(BaseModel):
    """AI-assisted triage suggestion for an issue (opt-in, labeled advisory)."""
    issue_id: int
    suggested_label: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    confidence: float = 0.5
    reasoning: str = ""
