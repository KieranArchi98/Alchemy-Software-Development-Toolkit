# Guided Roadmap Question Engine Implementation

## ✅ Overview

The Guided Roadmap Engine is a data-driven system that orchestrates the project specification process through a linear series of intelligent questions.

## 🔑 Key Components

### 1. **Question Data Store** (`backend/app/data/guided_roadmap.json`)
- **Structure**: JSON-based definition of all questions
- **Content**: 12 core questions covering Foundation, Requirements, Architecture, UI, and AI
- **Features**:
  - `fieldPath`: Maps answer directly to Canonical Spec field
  - `skipCondition`: Logic to skip non-relevant questions (e.g., skip UI questions for API service)
  - `aiDefault`: Fallback answer identification
  - `multiSelect`: Support for multiple choices

### 2. **Question Engine** (`backend/app/services/question_engine.py`)
- **Logic**:
  - Load and parse roadmap JSON
  - `get_next_question()`: Determines next step based on current progress & skip conditions
  - `apply_answer_to_spec()`: Mutates the Canonical Spec based on selected answer(s)
  - `get_progress()`: Calculates completion percentage
- **Singleton Pattern**: Efficient resource usage via `get_question_engine()`

### 3. **Service Integration** (`backend/app/services/project_service.py`)
- **Initialization**: Automatically starts roadmap when creating project
- **Answering**: `answer_question()` function:
  1. Validates input
  2. Applies mutation via Engine
  3. Updates progress
  4. Regenerates artifacts (Docs, JSON, Roadmap)
  5. **Creates Checkpoint** (Time travel support)
  6. Returns next question

### 4. **API Endpoints** (`backend/app/api/v1/endpoints/projects.py`)
- `POST /projects/answer`: Handle user answers
- `GET /projects/{id}`: Returns `currentQuestion` in response

## 🧪 Verification

Integration tests (`backend/test_roadmap_flow.py`) verify the complete lifecycle:

1. **Create Project** -> Initial Spec created, Q1 offered
2. **Answer Q1 (Archetype)** -> Spec updated, Artifacts regenerated, Checkpoint created
3. **Answer Q2 (Audience)** -> Spec updated, Progress advances
4. **Revert** -> Rollback to previous state works correctly

```
✅ Integration Test Passed!
✓ Created Project
✓ Answered Q001 (Archetype updated)
✓ Answered Q002 (Audience updated, Progress 16%)
✓ Checkpoints created: 3
✓ Artifacts Generated: 4 (Content verified)
✓ Revert complete (Progress reset)
```

## 📋 Question List (v1.0.0)

1. **Archetype**: Web App / Mobile App / API Service
2. **Target Audience**: Solo / Team / Enterprise
3. **Critical Features (MVP)**: Auth / Data / Real-time (Multi-select)
4. **Frontend Framework**: React / Vue / Svelte (Skip if not Web App)
5. **Backend Framework**: FastAPI / Express / Django
6. **Database**: PostgreSQL / MongoDB / None
7. **Authentication**: JWT / OAuth / None
8. **Non-Functional Reqs**: Performance / Security / Scalability
9. **Constraints**: Timeline / Budget / Technical
10. **Deployment**: Cloud / Local / Hybrid
11. **UI Style**: Tailwind / Material / Custom (Skip if not Web App)
12. **AI Features**: None / Text / Chat

## 🛠 Usage Example

```python
# Answer a question
response = requests.post(
    f"{BASE_URL}/projects/answer",
    json={
        "project_id": "proj-123",
        "question_id": "Q001",
        "answer_ids": ["web-app"]
    }
)

# Get next question from response
next_q = response.json()['project']['currentQuestion']
print(next_q['question'])
```
