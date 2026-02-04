# Artifact Generators Status

**Date**: 2026-02-04
**Status**: Operational

## 1. Documentation Generator
- **Service**: `app/services/doc_generator.py`
- **Output**: `Project Documentation.md`
- **Content**: Executive summary, Architecture, Requirements.
- **Trigger**: auto-regenerates on spec update.

## 2. Roadmap Generator
- **Service**: `app/services/roadmap_generator.py`
- **Output**: `project.spec.implementation` (Structured) & `Implementation Roadmap.md` (Markdown).
- **Logic**: 5-Phase standard flow (Foundation -> Backend -> Frontend -> Features -> Polish).
- **Adaptability**: Reacts to chosen Tech Stack (e.g. "Setup FastAPI" vs "Setup Django").

## 3. Prompt Generator
- **Service**: `app/services/prompt_generator.py`
- **Output**: `AI Prompt Sequence.json`
- **Structure**: List of objects `{ step: 1, prompt: "..." }`.
- **Context**: Injects filtered JSON context (e.g. Backend Arch for Backend Phase) to ensure AI compliance.

## Integration
All generators are wired into `project_service.py` via `_update_derived_state()`.
Any change to the project via Chat or Question Answering triggers a full regeneration of these artifacts.
