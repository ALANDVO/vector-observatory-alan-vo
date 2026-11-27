# Changelog

## 1.6.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.5.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.1 — GitHub issue ingestion and triage workflow (in progress)

### Added
- Backend: GitHubIssue database model with fields for issue metadata, state, labels, and triage tracking
- Backend: Pydantic schemas (GitHubIssueCreate, GitHubIssueRead, GitHubIssueList, TriageSuggestion)
- Backend: Service to fetch and store issues from GitHub API with deduplication by GitHub ID
- Backend: Heuristic-based triage suggestion generation (opt-in, labeled advisory)
- Backend: FastAPI endpoints for issue ingestion and triage:
  - `POST /api/v1/github/issues/ingest/{repo}` — Fetch and store issues from reference repository
  - `GET /api/v1/github/issues` — List stored issues with filtering by repo/state/pagination
  - `POST /api/v1/github/issues/{issue_id}/triage` — Get AI-assisted triage suggestion
- App: Router registration for github-issues prefix under `/api/v1`

### Changed
- Version bump to 1.3.1

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
CHANGELOG: version 1.3.1
CHANGELOG: last_feature: issue-tracker
CHANGELOG: current_feature: issue-tracker
CHANGELOG: plan_complete: false
CHANGELOG: sha: will be updated on publish
