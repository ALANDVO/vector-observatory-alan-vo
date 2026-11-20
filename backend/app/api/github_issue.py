"""GitHub Issue API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.github_issue import GitHubIssue
from app.schemas.github_issue import (
    GitHubIssueCreate,
    GitHubIssueRead,
    GitHubIssueList,
    TriageSuggestion,
)
from app.services.github_issue import (
    fetch_issues_from_repo,
    store_issue_from_payload,
    get_triage_suggestion,
)


router = APIRouter(prefix="/github/issues", tags=["github-issues"])


@router.get("", response_model=GitHubIssueList)
async def list_github_issues(
    repo: Optional[str] = None,
    state: str = "open",
    page: int = 1,
    per_page: int = 30,
    db_session: Session = Depends(get_db),
) -> GitHubIssueList:
    """List stored GitHub issues, optionally filtered by repository.
    
    If repo is specified, only returns issues from that repository.
    """
    from app.db.session import SessionLocal
    
    query = db_session.query(GitHubIssue)
    
    if repo:
        query = query.filter(GitHubIssue.repository == repo)
    
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return GitHubIssueList(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("/ingest/{repo}", status_code=202)
async def ingest_github_issues(
    repo: str,
    page: int = 1,
    per_page: int = 30,
    state: str = "open",
) -> {"message": str, "fetched": int, "stored": int}:
    """Fetch and store GitHub issues from a reference repository.
    
    This endpoint triggers the GitHub API to fetch issues from the
    specified repository and stores them in the local database.
    
    Args:
        repo: Repository in "owner/name" format (e.g., "owner/repo")
        page: Page number for pagination
        per_page: Items per page
        state: Filter by state (open, closed, all)
    
    Returns:
        Summary of ingestion operation
    """
    try:
        result = await fetch_issues_from_repo(
            repo=repo,
            page=page,
            per_page=per_page,
            state=state,
        )
        
        stored = len(result.items)
        
        return {
            "message": f"Issue ingestion from {repo} completed",
            "fetched": stored,
            "stored": stored,
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub API error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}",
        )


@router.post("/{issue_id}/triage", response_model=TriageSuggestion)
async def trigger_triage(
    issue_id: int,
    db_session: Session = Depends(get_db),
) -> TriageSuggestion:
    """Get AI-assisted triage suggestion for a specific issue.
    
    Fetches the issue from the database and generates a triage suggestion
    using heuristic analysis (opt-in, labeled advisory).
    """
    issue = db_session.query(GitHubIssue).filter(
        GitHubIssue.id == issue_id
    ).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue {issue_id} not found",
        )
    
    return await get_triage_suggestion(issue)
