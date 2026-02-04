# Canonical Project Specification Schema

## Overview

The **Canonical Project Specification** is the single source of truth for all Alchemy projects. It is a comprehensive, versioned JSON schema that captures every aspect of a software project from initial idea to implementation plan.

## Design Principles

1. **Single Source of Truth**: All artifacts (documentation, roadmaps, prompts) are derived from this canonical JSON
2. **Versioned Schema**: Schema follows semantic versioning for backward compatibility
3. **Validated Mutations**: All changes are validated to maintain referential integrity
4. **Deterministic**: Same inputs always produce same outputs
5. **Comprehensive**: Captures frontend, backend, requirements, and implementation details

## Schema Structure

### Top-Level Structure

```json
{
  "version": "1.0.0",
  "metadata": { ... },
  "project": { ... },
  "requirements": { ... },
  "architecture": { ... },
  "technology": { ... },
  "implementation": { ... },
  "aiUsage": { ... }
}
```

### 1. Metadata

Tracks project lifecycle and progress.

```json
{
  "metadata": {
    "id": "proj-abc123",
    "created": "2026-02-04T07:00:00Z",
    "lastModified": "2026-02-04T07:30:00Z",
    "phase": "discovery",  // discovery | definition | specification | complete
    "progress": 15
  }
}
```

### 2. Project Information

Core project details and context.

```json
{
  "project": {
    "name": "Alchemy",
    "tagline": "Turn ideas into AI-ready specifications",
    "purpose": "Help developers plan software projects systematically",
    "goals": [
      "Reduce planning time by 80%",
      "Improve specification quality"
    ],
    "targetAudience": ["Solo developers", "Founders", "Small teams"],
    "constraints": [
      {
        "type": "technical",
        "description": "Must work offline"
      }
    ],
    "assumptions": [
      "Users have basic technical knowledge"
    ]
  }
}
```

### 3. Requirements

Functional and non-functional requirements.

```json
{
  "requirements": {
    "functional": [
      {
        "id": "FR-001",
        "title": "User can create a project",
        "description": "Users should be able to initialize a new project from an idea",
        "priority": "critical",  // critical | high | medium | low
        "acceptanceCriteria": [
          "Project is created with unique ID",
          "Initial state is persisted"
        ],
        "dependencies": []
      }
    ],
    "nonFunctional": {
      "performance": ["Page load < 2s"],
      "security": ["No authentication required for MVP"],
      "scalability": ["Support 100 concurrent users"],
      "usability": ["Mobile responsive"],
      "reliability": ["99% uptime"]
    }
  }
}
```

### 4. Architecture

Complete system architecture definition.

#### Frontend Architecture

```json
{
  "architecture": {
    "archetype": "web-app",
    "deploymentModel": "local-only",
    "frontend": {
      "framework": "React + Vite",
      "stateManagement": "React hooks + Context",
      "styling": "Tailwind CSS",
      "pages": [
        {
          "id": "home",
          "name": "Home",
          "route": "/",
          "description": "Landing page",
          "components": ["landing-form", "project-list"],
          "authentication": false
        }
      ],
      "components": [
        {
          "id": "landing-form",
          "name": "LandingForm",
          "type": "feature",
          "description": "Project creation form",
          "props": [
            {
              "name": "onSubmit",
              "type": "function",
              "required": true
            }
          ]
        }
      ],
      "layout": {
        "type": "split-view",
        "navigation": "none",
        "responsive": true
      }
    }
  }
}
```

#### Backend Architecture

```json
{
  "backend": {
    "framework": "FastAPI",
    "language": "Python",
    "architecture": "modular",
    "services": [
      {
        "id": "project-service",
        "name": "ProjectService",
        "responsibility": "Manage project lifecycle",
        "dependencies": []
      }
    ],
    "apis": [
      {
        "id": "create-project",
        "endpoint": "/projects",
        "method": "POST",
        "description": "Create a new project",
        "authentication": false,
        "requestSchema": {
          "idea": "string"
        },
        "responseSchema": {
          "project": "Project"
        }
      }
    ],
    "database": {
      "type": "none",
      "technology": null,
      "models": []
    }
  }
}
```

#### Integration

```json
{
  "integration": {
    "apiStyle": "REST",
    "authentication": "none",
    "externalServices": [
      {
        "name": "OpenAI",
        "purpose": "AI orchestration",
        "required": false
      }
    ]
  }
}
```

### 5. Technology Stack

```json
{
  "technology": {
    "frontend": ["React", "TypeScript", "Vite", "Tailwind CSS"],
    "backend": ["Python", "FastAPI", "Pydantic"],
    "database": [],
    "infrastructure": [],
    "devTools": ["Git", "npm", "pip"]
  }
}
```

### 6. Implementation Plan

```json
{
  "implementation": {
    "phases": [
      {
        "id": "phase-1",
        "name": "Foundation",
        "order": 1,
        "description": "Set up project structure",
        "tasks": [
          {
            "id": "task-1",
            "title": "Initialize repository",
            "status": "completed"
          }
        ]
      }
    ],
    "mvpScope": ["FR-001", "FR-002", "FR-003"]
  }
}
```

### 7. AI Usage

```json
{
  "aiUsage": {
    "models": [
      {
        "purpose": "Intent classification",
        "model": "gpt-4"
      }
    ],
    "features": [
      "Dynamic question generation",
      "State extraction",
      "Documentation generation"
    ]
  }
}
```

## Validation Rules

The schema enforces the following validation rules:

1. **Referential Integrity**:
   - FR dependencies must reference existing FRs
   - MVP scope must reference existing FRs
   - Page components must reference existing components
   - Service dependencies must reference existing services

2. **Version Format**: Must follow semver (e.g., "1.0.0")

3. **ID Patterns**:
   - Functional requirements: `FR-\d+` (e.g., "FR-001")
   - Other IDs: kebab-case strings

4. **Enums**: Strict validation for all enum fields (phase, priority, archetype, etc.)

## Mutation Rules

All mutations must follow these rules:

1. **Explicit Only**: No implicit state changes
2. **Most Recent Wins**: Later decisions override earlier ones
3. **Timestamp Updates**: `lastModified` updated on every change
4. **Validation Required**: All mutations validated before applying
5. **Atomic**: Changes either fully succeed or fully fail

## Usage Examples

### Creating a New Specification

```python
from app.services.spec_utils import create_initial_spec
from app.schemas.canonical_spec import Archetype

spec = create_initial_spec(
    project_id="proj-123",
    idea="A tool to help developers plan projects",
    archetype=Archetype.WEB_APP
)
```

### Adding Requirements

```python
from app.services.spec_utils import add_functional_requirement

spec = add_functional_requirement(
    spec,
    title="User can create a project",
    description="Initialize new project from idea",
    priority="critical"
)
```

### Validating a Specification

```python
from app.schemas.canonical_spec import SpecValidator

is_valid, errors = SpecValidator.validate_spec(spec)
if not is_valid:
    print(f"Validation errors: {errors}")
```

### Exporting to JSON

```python
from app.services.spec_utils import export_spec_to_json

json_str = export_spec_to_json(spec, pretty=True)
with open("project_spec.json", "w") as f:
    f.write(json_str)
```

### Importing from JSON

```python
from app.services.spec_utils import import_spec_from_json

with open("project_spec.json", "r") as f:
    json_str = f.read()

spec = import_spec_from_json(json_str)
```

## Schema Files

- **JSON Schema**: `backend/app/schemas/project_spec_schema.json`
- **Pydantic Models**: `backend/app/schemas/canonical_spec.py`
- **Utilities**: `backend/app/services/spec_utils.py`
- **Tests**: `backend/test_canonical_spec.py`

## Testing

Run the test suite:

```bash
cd backend
python test_canonical_spec.py
```

This will test:
- Specification creation
- Requirement addition
- Architecture definition
- Validation (both valid and invalid specs)
- Export/import cycle
- Summary generation

## Versioning

The schema follows semantic versioning:

- **Major**: Breaking changes to schema structure
- **Minor**: Backward-compatible additions
- **Patch**: Bug fixes and clarifications

Current version: **1.0.0**

## Future Enhancements

Planned for future versions:

- [ ] Schema migration utilities
- [ ] Diff/merge capabilities
- [ ] Version history tracking
- [ ] Advanced validation rules
- [ ] Custom constraint definitions
- [ ] Template system for common patterns
