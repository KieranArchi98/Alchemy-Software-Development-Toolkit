# Dynamic AI Question Layer Implementation

## ✅ Overview

The system now supports intelligent, context-aware question generation that activates after the static roadmap is complete. This allows for deep customization of the specification based on earlier decisions.

## 🧠 AI Service (`backend/app/services/ai_service.py`)

- **Role**: Emulates an intelligent agent analyzing the Canonical Spec.
- **Trigger**: Called automatically when static questions are exhausted.
- **Context Awareness**: Analyzes existing answers (e.g., "Web App" archetype, "Data Management" feature) to generate relevant follow-ups.
- **Output**: Returns a full `Question` object with:
  - Contextual description ("AI Analysis: Based on...")
  - Structured answers with mutation payloads
  - Target field path for spec updates

## 🔄 Dynamic Flow Architecture

1. **Answer Static Questions**
   - User answers standard roadmap questions (Q1-Q12).
   - Engine validates and updates spec.

2. **Transition to Dynamic Mode**
   - `project_service.answer_question` checks for next static question.
   - If `None`, it queries `ai_service.generate_dynamic_question`.

3. **Active Question Context**
   - Since dynamic questions aren't in `guided_roadmap.json`, they are stored in memory (`current_questions_store`).
   - This ensures validation and answer processing works identical to static questions.

4. **Robust Mutation Logic**
   - Updated `QuestionEngine` to intelligently handle list updates:
     - **Extend**: If answer is a list (e.g. `targetAudience`), it extends the existing list.
     - **Append**: If answer is a single item (e.g. `Component`), it appends to the list.

## 🧪 Verification

Integration tests (`backend/test_roadmap_flow.py`) verify the hybrid flow:

```
✓ Created Project
...
✓ Answered 12 Static Questions
🧠 AI Generated Question: Do you need a dashboard? (Q_DYNAMIC_1)
   Description: "AI Analysis: Based on your 'Data Management' feature..."
✓ Answered Dynamic Question (Yes)
✓ Spec updated with Dashboard component
✓ Roadmap Complete
```

## 🚀 Next Steps

- **Connect Real LLM**: Replace the mock logic in `ai_service.py` with OpenAI/Anthropic API calls using the `CanonicalProjectSpec` as context.
- **Persistence**: Store generated questions in the project database/file so they persist across server restarts (currently in-memory).
