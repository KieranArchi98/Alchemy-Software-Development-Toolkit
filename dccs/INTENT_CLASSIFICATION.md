# Intent Classification & Chat Modes

## ✅ Implementation Complete

The system now intelligently classifies user messages and strictly enforces chat modes.

## 🧠 Intent Classification

Messages are classified into three types:

1.  **Thinking / Research** (`RESEARCH_QUESTION`)
    - Read-only queries interactions
    - Example: "What is the best database for high scale?"
    - Result: AI provides information, no state change.

2.  **Design Decision** (`DESIGN_DECISION`)
    - Declarative choices about the product
    - Example: "I want to use Tailwind CSS"
    - Result: Updates Canonical Spec, triggers checkpoint.

3.  **Update Request** (`UPDATE_REQUEST`)
    - Explicit commands to change existing spec
    - Example: "Change the database to PostgreSQL"
    - Result: Updates Canonical Spec, triggers checkpoint.

## 🛡️ Chat Modes

The system enforces rules based on the active mode:

| Mode | Allowed Intents | Behavior |
|------|----------------|----------|
| **Research** | Research Only | Block mutations with helpful message. |
| **Guided** | All | Standard guided flow (Questions + Chat). |
| **Update** | All | Allows direct manipulation of the spec. |

## 🧪 Verification

`backend/test_chat_intents.py` verifies:

1.  **Research Query**: Returns info, no mutation.
2.  **Blocked Mutation**: "Change styling" in Research Mode -> **BLOCKED**.
3.  **Allowed Mutation**: "I want Tailwind" in Update Mode -> **SUCCESS**.
    - Spec updated to `styling: "Tailwind CSS"`
    - Checkpoint created: `Update: design_decision`

## 📂 Key Files

- `backend/app/services/ai_service.py`: Classification logic & Mock LLM
- `backend/app/services/project_service.py`: Routing & Mode Enforcement
- `backend/test_chat_intents.py`: Integration Tests
