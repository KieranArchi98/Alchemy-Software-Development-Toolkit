# Alchemy Backend

## Overview
This is the Python/FastAPI backend for **Alchemy**, an AI-assisted specification compiler.
It implements the architecture defined in `ChatGPTspec.md` and `projectspec.json`.

## Key Capabilities
- **Question Engine**: Static and dynamic guided roadmap.
- **Canonical State**: JSON-based single source of truth (`CanonicalProjectSpec`).
- **AI Orchestration**: Intent classification and content generation.
- **Persistence**: Local-first storage with checkpointing.
- **Artifacts**: Automatic generation of Documentation, Roadmap, and Prompts.

## Development
Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## Structure
- `app/services`: Business logic (Project, Question Engine, AI, Persistence).
- `app/schemas`: Pydantic models (Project, Canonical Spec).
- `app/api`: FastAPI endpoints.
- `storage/projects`: Local project data (JSON).
