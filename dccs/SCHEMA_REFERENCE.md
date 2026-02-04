# Canonical Specification Schema - Visual Reference

## Schema Hierarchy

```
CanonicalProjectSpec (v1.0.0)
│
├─── 📋 metadata
│    ├─ id: string
│    ├─ created: datetime
│    ├─ lastModified: datetime
│    ├─ phase: discovery | definition | specification | complete
│    └─ progress: 0-100
│
├─── 🎯 project
│    ├─ name: string
│    ├─ tagline: string?
│    ├─ purpose: string (required)
│    ├─ goals: string[]
│    ├─ targetAudience: string[]
│    ├─ constraints: Constraint[]
│    │   ├─ type: technical | business | regulatory | timeline | budget | other
│    │   └─ description: string
│    └─ assumptions: string[]
│
├─── ✅ requirements
│    ├─ functional: FunctionalRequirement[]
│    │   ├─ id: "FR-001" (pattern: FR-\d+)
│    │   ├─ title: string
│    │   ├─ description: string
│    │   ├─ priority: critical | high | medium | low
│    │   ├─ acceptanceCriteria: string[]
│    │   └─ dependencies: string[] (other FR IDs)
│    └─ nonFunctional
│        ├─ performance: string[]
│        ├─ security: string[]
│        ├─ scalability: string[]
│        ├─ usability: string[]
│        └─ reliability: string[]
│
├─── 🏗️ architecture
│    ├─ archetype: web-app | mobile-app | desktop-app | api-service | cli-tool | hybrid
│    ├─ deploymentModel: cloud | on-premise | hybrid | local-only
│    │
│    ├─ frontend
│    │   ├─ framework: string?
│    │   ├─ stateManagement: string?
│    │   ├─ styling: string?
│    │   ├─ pages: Page[]
│    │   │   ├─ id: string
│    │   │   ├─ name: string
│    │   │   ├─ route: string
│    │   │   ├─ description: string?
│    │   │   ├─ components: string[] (component IDs)
│    │   │   └─ authentication: boolean
│    │   ├─ components: Component[]
│    │   │   ├─ id: string
│    │   │   ├─ name: string
│    │   │   ├─ type: layout | feature | ui | utility
│    │   │   ├─ description: string?
│    │   │   └─ props: ComponentProp[]
│    │   │       ├─ name: string
│    │   │       ├─ type: string
│    │   │       └─ required: boolean
│    │   └─ layout
│    │       ├─ type: single-page | multi-page | dashboard | split-view | custom
│    │       ├─ navigation: sidebar | topbar | tabs | none
│    │       └─ responsive: boolean
│    │
│    ├─ backend
│    │   ├─ framework: string?
│    │   ├─ language: string?
│    │   ├─ architecture: monolith | microservices | serverless | modular
│    │   ├─ services: Service[]
│    │   │   ├─ id: string
│    │   │   ├─ name: string
│    │   │   ├─ responsibility: string
│    │   │   └─ dependencies: string[] (other service IDs)
│    │   ├─ apis: ApiEndpoint[]
│    │   │   ├─ id: string
│    │   │   ├─ endpoint: string
│    │   │   ├─ method: GET | POST | PUT | PATCH | DELETE
│    │   │   ├─ description: string?
│    │   │   ├─ authentication: boolean
│    │   │   ├─ requestSchema: object?
│    │   │   └─ responseSchema: object?
│    │   └─ database
│    │       ├─ type: sql | nosql | graph | key-value | none
│    │       ├─ technology: string?
│    │       └─ models: DatabaseModel[]
│    │           ├─ name: string
│    │           └─ fields: object[]
│    │
│    └─ integration
│        ├─ apiStyle: REST | GraphQL | gRPC | WebSocket
│        ├─ authentication: none | jwt | oauth | session | api-key
│        └─ externalServices: ExternalService[]
│            ├─ name: string
│            ├─ purpose: string
│            └─ required: boolean
│
├─── 💻 technology
│    ├─ frontend: string[]
│    ├─ backend: string[]
│    ├─ database: string[]
│    ├─ infrastructure: string[]
│    └─ devTools: string[]
│
├─── 🚀 implementation
│    ├─ phases: Phase[]
│    │   ├─ id: string
│    │   ├─ name: string
│    │   ├─ order: integer (≥1)
│    │   ├─ description: string?
│    │   └─ tasks: Task[]
│    │       ├─ id: string
│    │       ├─ title: string
│    │       └─ status: pending | in-progress | completed | blocked
│    └─ mvpScope: string[] (FR IDs)
│
└─── 🤖 aiUsage
     ├─ models: AiModel[]
     │   ├─ purpose: string
     │   └─ model: string
     └─ features: string[]
```

## Validation Rules

### ✅ Referential Integrity

```
FR Dependencies
  FR-002 depends on FR-001 ──→ FR-001 must exist

MVP Scope
  mvpScope: ["FR-001", "FR-003"] ──→ Both FRs must exist

Page Components
  Page.components: ["header", "footer"] ──→ Both components must exist

Service Dependencies
  Service.dependencies: ["auth-service"] ──→ Service must exist
```

### ✅ ID Patterns

```
Functional Requirements:  FR-001, FR-002, FR-003, ...
Other IDs:                kebab-case (e.g., "home-page", "user-service")
```

### ✅ Enums

```
Phase:           discovery → definition → specification → complete
Priority:        critical > high > medium > low
Archetype:       web-app | mobile-app | desktop-app | api-service | cli-tool | hybrid
HTTP Method:     GET | POST | PUT | PATCH | DELETE
Database Type:   sql | nosql | graph | key-value | none
API Style:       REST | GraphQL | gRPC | WebSocket
Auth Type:       none | jwt | oauth | session | api-key
Task Status:     pending → in-progress → completed | blocked
```

## Mutation Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Receive Update Request                                   │
│    { "project": { "name": "New Name" } }                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Load Current Spec                                        │
│    current_spec = get_spec(project_id)                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Apply Updates (Most Recent Wins)                        │
│    updated_spec = safe_merge(current_spec, updates)        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Update Timestamp                                         │
│    updated_spec.metadata.lastModified = now()               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Validate Spec                                            │
│    is_valid, errors = SpecValidator.validate_spec(spec)     │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    ┌─────────┐
                    │ Valid?  │
                    └─────────┘
                    ↙         ↘
               YES ↙           ↘ NO
                  ↓             ↓
    ┌──────────────────┐   ┌──────────────────┐
    │ 6. Save Spec     │   │ 6. Raise Error   │
    │    persist(spec) │   │    return errors │
    └──────────────────┘   └──────────────────┘
              ↓
    ┌──────────────────┐
    │ 7. Return Spec   │
    │    return spec   │
    └──────────────────┘
```

## Example Spec (Minimal)

```json
{
  "version": "1.0.0",
  "metadata": {
    "id": "proj-123",
    "created": "2026-02-04T07:00:00Z",
    "lastModified": "2026-02-04T07:30:00Z",
    "phase": "discovery",
    "progress": 15
  },
  "project": {
    "name": "Alchemy",
    "purpose": "Help developers plan software projects",
    "goals": ["Reduce planning time"],
    "targetAudience": ["Solo developers"],
    "constraints": [],
    "assumptions": []
  },
  "requirements": {
    "functional": [
      {
        "id": "FR-001",
        "title": "User can create a project",
        "description": "Initialize new project from idea",
        "priority": "critical",
        "acceptanceCriteria": [],
        "dependencies": []
      }
    ],
    "nonFunctional": {
      "performance": [],
      "security": [],
      "scalability": [],
      "usability": [],
      "reliability": []
    }
  },
  "architecture": {
    "archetype": "web-app",
    "deploymentModel": "local-only",
    "frontend": {
      "pages": [],
      "components": []
    },
    "backend": {
      "architecture": "modular",
      "services": [],
      "apis": []
    },
    "integration": {
      "apiStyle": "REST",
      "authentication": "none"
    }
  },
  "technology": {
    "frontend": ["React", "TypeScript"],
    "backend": ["Python", "FastAPI"]
  },
  "implementation": {
    "phases": [],
    "mvpScope": ["FR-001"]
  },
  "aiUsage": {
    "models": [],
    "features": []
  }
}
```

## Quick Reference

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `version` | string | ✅ | Semver pattern |
| `metadata.id` | string | ✅ | Unique |
| `metadata.phase` | enum | ✅ | 4 values |
| `metadata.progress` | int | ✅ | 0-100 |
| `project.name` | string | ✅ | Min length 1 |
| `project.purpose` | string | ✅ | Min length 1 |
| `requirements.functional[].id` | string | ✅ | Pattern: FR-\d+ |
| `architecture.archetype` | enum | ✅ | 6 values |
| `implementation.mvpScope[]` | string | ❌ | Must reference valid FR |

---

**Legend:**
- ✅ Required field
- ❌ Optional field
- `?` Nullable field
- `[]` Array
