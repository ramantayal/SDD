# Project Constitution — v0.1.0

This document defines non-negotiable rules for the Customer Orders Service.
It is read by humans and AI agents at every session.

## Article I — Tech Stack [CRITICAL]

ALLOWED: Python 3.12, FastAPI ≥0.110, SQLite for local development, PostgreSQL ≥15 for production environments.

FORBIDDEN: Direct SQL queries without parameterization.
FORBIDDEN: Use of unmaintained or deprecated libraries for core functionality.

The service SHALL run locally via:
- uvicorn src.main:app --reload
using the configured database (SQLite or PostgreSQL).

## Article II — Architectural Patterns [CRITICAL]

The system SHALL access the database only through repository modules under src/repositories/.
Controllers/route handlers SHALL NOT contain direct SQL or ORM calls.

Business logic SHALL reside in service modules under src/services/, not inside API route handlers.
Global mutable state SHALL NOT be used for request-scoped data.

Configuration values (e.g., DB connection strings, API keys) SHALL be loaded from environment variables or configuration files, not hard-coded into business logic.

## Article III — Security [CRITICAL]

The system SHALL parameterize all database queries (CWE-89 – SQL Injection).
User-provided input SHALL be validated and/or sanitized before use in queries or outbound calls.

All protected endpoints SHALL verify authentication before accessing customer data.
Authorization checks SHALL be enforced in service or middleware layers, not only in the UI.

Secrets (e.g., API keys, database passwords) SHALL NOT be hard-coded; they SHALL be stored in environment variables or secure configuration mechanisms.

## Article IV — Testing Gates [SHOULD]

All new features SHALL include at least one automated test before merge.
Code coverage on changed files SHOULD be ≥ 80%.

Unit tests SHOULD cover core service logic under src/services/.
Integration tests SHOULD exist for key endpoints (for example, GET /orders) and their database interactions.

The full test suite (e.g., pytest) SHALL pass before any merge into the main branch.

## Article V — Code Style [MAY]

API route handlers SHOULD be placed under src/api/.
Repository modules SHOULD be placed under src/repositories/.

Python modules SHOULD use snake_case file names.
Class names SHOULD use PascalCase; function names SHOULD use snake_case.

Code SHOULD be formatted consistently with an agreed formatter (for example, black), where available.
Directory and module naming conventions SHOULD remain stable to help AI agents and humans navigate the codebase.