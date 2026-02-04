# Alchemy Backend API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check
```
GET /health
```
Returns server health status.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Create Project
```
POST /projects/
```
Initialize a new project from an idea.

**Request Body:**
```json
{
  "idea": "A tool to help developers plan software projects"
}
```

**Response:**
```json
{
  "project": {
    "id": "abc123",
    "title": "A Tool To Help",
    "idea": "A tool to help developers plan software projects",
    "progress": 5,
    "lastSaved": "2026-02-04T07:20:00.000Z",
    "activePhase": "discovery",
    "activeChatMode": "guided",
    "state": {
      "purpose": "...",
      "constraints": [],
      "app_archetype": "",
      "features": [],
      ...
    },
    "sections": [...],
    "files": [...],
    "messages": [...],
    "checkpoints": [...]
  }
}
```

---

### Get Project
```
GET /projects/{project_id}
```
Retrieve a project by ID.

**Response:** Same as Create Project

---

### Send Message
```
POST /projects/message
```
Send a user message and receive AI response.

**Request Body:**
```json
{
  "project_id": "abc123",
  "content": "I want to build a web application",
  "mode": "guided"  // "guided" | "research" | "update"
}
```

**Response:**
```json
{
  "project": { ... },
  "message": {
    "id": "msg123",
    "role": "assistant",
    "content": "...",
    "timestamp": "2026-02-04T07:20:00.000Z",
    "options": [...]
  }
}
```

---

### Select Option
```
POST /projects/option
```
Select an option from an AI message (triggers state update).

**Request Body:**
```json
{
  "project_id": "abc123",
  "message_id": "msg123",
  "option_id": "solopreneur"
}
```

**Response:**
```json
{
  "project": { ... }
}
```

---

### Create Checkpoint
```
POST /projects/checkpoint
```
Create a manual checkpoint.

**Request Body:**
```json
{
  "project_id": "abc123",
  "label": "Before major refactor"
}
```

**Response:**
```json
{
  "id": "cp123",
  "timestamp": "2026-02-04T07:20:00.000Z",
  "label": "Before major refactor",
  "state": { ... },
  "progress": 45
}
```

---

### Revert Checkpoint
```
POST /projects/revert
```
Revert project to a previous checkpoint.

**Request Body:**
```json
{
  "project_id": "abc123",
  "checkpoint_id": "cp123"
}
```

**Response:**
```json
{
  "project": { ... }
}
```

---

### Get Artifacts
```
GET /projects/{project_id}/artifacts
```
Get all generated artifacts.

**Response:**
```json
{
  "files": [
    {
      "id": "documentation",
      "name": "Project Documentation",
      "type": "design",
      "content": "# Project Documentation\n..."
    },
    {
      "id": "spec-json",
      "name": "Canonical Spec (JSON)",
      "type": "context",
      "content": "{...}"
    },
    {
      "id": "roadmap",
      "name": "Implementation Roadmap",
      "type": "roadmap",
      "content": "# Roadmap\n..."
    },
    {
      "id": "prompts",
      "name": "AI Prompt Sequence",
      "type": "prompts",
      "content": "[...]"
    }
  ]
}
```

---

### Get Checkpoints
```
GET /projects/{project_id}/checkpoints
```
Get all checkpoints for a project.

**Response:**
```json
{
  "checkpoints": [
    {
      "id": "cp1",
      "timestamp": "2026-02-04T07:20:00.000Z",
      "label": "Project Created",
      "state": { ... },
      "progress": 5
    },
    ...
  ]
}
```

---

## Error Responses

All endpoints may return error responses:

**404 Not Found:**
```json
{
  "detail": "Project not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error message"
}
```

---

## Testing

Run the test suite:
```bash
cd backend
python test_api.py
```

## CORS

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative dev port)

Configure in `backend/.env`:
```
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```
