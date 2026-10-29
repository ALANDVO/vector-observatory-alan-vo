# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-29

### Added
- Plugin and Skill database models with SQLAlchemy
- REST API for plugin/skill catalog (`/api/v1/plugins/*`)
  - List plugins with pagination, search, tag filtering
  - Get plugin by ID or slug with nested skills
  - Create, update, delete plugins
  - List skills for a plugin with pagination and search
  - Get, create, update, delete skills
- Seed data: 4 plugins (Claude Code, LangChain, LlamaIndex, AutoGPT) with 9 skills
- Backend tests for all plugin/skill endpoints (14 tests passing)

## [1.0.0] - 2026-10-20

### Added
- FastAPI backend with health check endpoints (`/api/v1/health`, `/api/v1/health/db`)
- React + TypeScript + Vite frontend with dashboard and health check views
- Docker Compose configuration with backend, frontend, and Keycloak services
- Keycloak realm export with viewer, analyst, and admin roles
- SQLite database with SQLAlchemy ORM
- Pytest backend tests and Vitest frontend tests
- CI/CD workflow configuration
- Project documentation (README, LICENSE, CHANGELOG)
- Portfolio metadata (portfolio.json)

### Security
- Non-root Docker users
- Health checks on all services
- CORS configuration for development origins
- Keycloak OIDC configuration with PKCE support

