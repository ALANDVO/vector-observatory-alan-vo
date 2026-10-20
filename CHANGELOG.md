# Changelog

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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