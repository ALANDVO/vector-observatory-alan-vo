"""GitHub Issue service - fetch and store issues from GitHub API."""

import os
import httpx
from typing import List, Optional

from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.models.github_issue import GitHubIssue
from app.schemas.github_issue import (
    GitHubIssueCreate,
    GitHubIssueRead,
    GitHubIssueList,
    TriageSuggestion,
)


GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def fetch_issues_from_repo(
    repo: str,
    page: int = 1,
    per_page: int = 30,
    state: str = "open",
) -> GitHubIssueList:
    """Fetch issues from a GitHub repository.
    
    Args:
        repo: Repository in "owner/name" format
        page: Page number for pagination
        per_page: Items per page (max 100)
        state: Filter by state (open, closed, all)
    
    Returns:
        GitHubIssueList with fetched issues
    """
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    async with httpx.AsyncClient(headers=headers) as client:
        url = f"{GITHUB_API_BASE}/repos/{repo}/issues"
        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
        }
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    
    items = []
    for issue_data in data:
        # Check if issue already stored
        async with SessionLocal() as db:
            existing = db.query(GitHubIssue).filter(
                GitHubIssue.github_id == issue_data["id"]
            ).first()
            
            if not existing:
                # Create new issue
                from datetime import datetime, timezone
                github_issue = GitHubIssue(
                    github_id=issue_data["id"],
                    repository=repo,
                    number=issue_data["number"],
                    title=issue_data["title"],
                    body=issue_data.get("body"),
                    state=issue_data.get("state", "open"),
                    labels=",".join([label["name"] for label in issue_data.get("labels", [])]) 
                    if issue_data.get("labels") else None,
                    author_login=issue_data.get("author", {}).get("login"),
                )
                db.add(github_issue)
                db.commit()
                db.refresh(github_issue)
            
            items.append(GitHubIssueRead.model_validate(existing or github_issue))
    
    # Get total count from Link header or first page
    total = len(data)
    
    return GitHubIssueList(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


async def store_issue_from_payload(
    payload: dict,
    repo: str,
) -> GitHubIssue:
    """Store a single GitHub issue from API payload.
    
    Args:
        payload: Raw GitHub API issue payload
        repo: Repository in "owner/name" format
    
    Returns:
        GitHubIssue model instance
    """
    from datetime import datetime, timezone
    
    github_id = payload["id"]
    
    async with SessionLocal() as db:
        existing = db.query(GitHubIssue).filter(
            GitHubIssue.github_id == github_id
        ).first()
        
        if existing:
            # Update existing
            for key, value in {
                "repository": repo,
                "number": payload["number"],
                "title": payload["title"],
                "body": payload.get("body"),
                "state": payload.get("state", "open"),
                "labels": ",".join([label["name"] for label in payload.get("labels", [])]) 
                if payload.get("labels") else None,
                "author_login": payload.get("author", {}).get("login"),
            }.items():
                setattr(existing, key, value)
            db.commit()
            db.refresh(existing)
            return existing
        
        # Create new
        github_issue = GitHubIssue(
            github_id=github_id,
            repository=repo,
            number=payload["number"],
            title=payload["title"],
            body=payload.get("body"),
            state=payload.get("state", "open"),
            labels=",".join([label["name"] for label in payload.get("labels", [])]) 
            if payload.get("labels") else None,
            author_login=payload.get("author", {}).get("login"),
        )
        db.add(github_issue)
        db.commit()
        db.refresh(github_issue)
        return github_issue


async def get_triage_suggestion(
    issue: GitHubIssue,
    db_session: Session,
) -> TriageSuggestion:
    """Get AI-assisted triage suggestion for an issue (opt-in).
    
    Uses LLM to analyze the issue and suggest a label and priority.
    Only runs if issue is not already triaged.
    """
    from app.db.session import SessionLocal
    
    if issue.triaged:
        return TriageSuggestion(
            issue_id=issue.id,
            suggested_label=None,
            priority="medium",
            confidence=1.0,
            reasoning="Already triaged",
        )
    
    # Basic heuristic-based triage without LLM for now
    # In production, this would call an LLM
    title_lower = issue.title.lower()
    body_lower = (issue.body or "").lower()
    combined = f"{title_lower} {body_lower}"
    
    # Simple keyword-based labeling
    suggested_label = None
    priority = "medium"
    confidence = 0.5
    reasoning = "Basic keyword analysis"
    
    # Check for bug-related keywords
    bug_keywords = ["bug", "issue", "fix", "problem", "error", "crash", "broken"]
    # Check for enhancement-related keywords
    enhancement_keywords = ["feature", "enhancement", "improve", "add", "support"]
    # Check for documentation-related keywords
    doc_keywords = ["doc", "readme", "website", "manual"]
    
    if any(kw in combined for kw in bug_keywords):
        suggested_label = "bug"
        priority = "high"
        confidence = 0.7
        reasoning = "Contains bug-related keywords"
    elif any(kw in combined for kw in enhancement_keywords):
        suggested_label = "enhancement"
        priority = "medium"
        confidence = 0.6
        reasoning = "Contains enhancement-related keywords"
    elif any(kw in combined for kw in doc_keywords):
        suggested_label = "documentation"
        priority = "low"
        confidence = 0.5
        reasoning = "Contains documentation-related keywords"
    
    # Mark as triaged after suggestion
    issue.triaged = True
    issue.triage_score = int(confidence * 10)
    issue.triage_notes = reasoning
    db_session.commit()
    
    return TriageSuggestion(
        issue_id=issue.id,
        suggested_label=suggested_label,
        priority=priority,
        confidence=confidence,
        reasoning=reasoning,
    )
