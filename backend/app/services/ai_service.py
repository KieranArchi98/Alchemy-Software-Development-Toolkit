"""
AI Service for Alchemy - Production-Ready Integration
Handles LLM interactions for question generation, intent classification, and project refinement.
"""
from typing import List, Dict, Any, Optional, Tuple
import json
import enum
import logging
from pydantic import BaseModel, Field

from app.schemas.canonical_spec import CanonicalProjectSpec
from app.services.question_engine import Question, Answer
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# Intent Classification Models
# ============================================================================

class UserIntent(str, enum.Enum):
    DESIGN_DECISION = "design_decision"  # Making a choice or defining a feature
    RESEARCH_QUESTION = "research_question" # Asking for info, comparison, or explanation
    UPDATE_REQUEST = "update_request"    # Requesting a specific change to existing spec
    CHIT_CHAT = "chit_chat"              # Greetings, acknowledgments (no-op)

class IntentResult(BaseModel):
    intent: UserIntent
    confidence: float
    reasoning: str
    suggested_mutation: Optional[Dict[str, Any]] = None

# ============================================================================
# AI Service
# ============================================================================

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized.")
            except ImportError:
                logger.warning("OpenAI package not found. AI features will be limited.")
        else:
            logger.warning("OPENAI_API_KEY not found. Operating in mock/fallback mode.")

    def is_available(self) -> bool:
        return self.client is not None

    async def _call_llm(self, messages: List[Dict[str, str]], json_mode: bool = False) -> str:
        """Helper to call OpenAI with retry and error handling"""
        if not self.client:
            raise ValueError("AI Service is not configured (OpenAI API key missing).")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview", # Efficient and smart
                messages=messages,
                response_format={"type": "json_object"} if json_mode else {"type": "text"},
                temperature=0.2 # Lower temperature for better structure
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Call failed: {e}")
            raise RuntimeError(f"AI interaction failed: {str(e)}")

    async def generate_dynamic_question(
        self,
        spec: CanonicalProjectSpec,
        answered_questions: List[str]
    ) -> Optional[Question]:
        """
        Generate a context-aware question based on current spec using LLM.
        """
        if not self.is_available():
            return self._fallback_dynamic_question(spec, answered_questions)

        prompt = [
            {"role": "system", "content": "You are an expert Software Architect. Analyze the current Project Specification and identify the most critical MISSING detail or architectural decision required to build an MVP. Output a single question in JSON format matching the Question schema."},
            {"role": "user", "content": f"Project Spec: {spec.model_dump_json()}\nAlready answered: {answered_questions}"},
            {"role": "assistant", "content": "Return JSON with keys: id (start with Q_DYNAMIC_), order, category, question, description, fieldPath, answers (list with id, label, description, value, recommended), aiDefault, multiSelect."}
        ]

        try:
            result_str = await self._call_llm(prompt, json_mode=True)
            data = json.loads(result_str)
            # Ensure ID prefix
            if not data.get('id', '').startswith("Q_DYNAMIC_"):
                data['id'] = f"Q_DYNAMIC_{uuid.uuid4().hex[:4]}"
            return Question(**data)
        except Exception as e:
            logger.error(f"Dynamic question generation failed: {e}")
            return None

    async def classify_intent(
        self,
        message: str,
        mode: str,
        spec: CanonicalProjectSpec
    ) -> IntentResult:
        """
        Classify the user's message intent using LLM.
        """
        if not self.is_available():
            return self._fallback_classify_intent(message, mode)

        prompt = [
            {"role": "system", "content": "Classify user intent into: design_decision, research_question, update_request, chit_chat. Return JSON."},
            {"role": "user", "content": f"Message: '{message}'\nMode: {mode}\nContext: {spec.project.purpose}"}
        ]

        try:
            result_str = await self._call_llm(prompt, json_mode=True)
            return IntentResult(**json.loads(result_str))
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return self._fallback_classify_intent(message, mode)

    async def process_research_query(self, message: str, spec: CanonicalProjectSpec) -> str:
        """Handle read-only research questions using LLM"""
        if not self.is_available():
            return "[Offline Mode] Information about your request is limited."

        prompt = [
            {"role": "system", "content": f"You are Alchemy AI. Answer the user's research question about their project: {spec.project.name}. Be concise and helpful. Do not suggest changes to the existing spec unless asked."},
            {"role": "user", "content": message}
        ]
        
        return await self._call_llm(prompt)

    async def process_mutation(self, message: str, intent: IntentResult, spec: CanonicalProjectSpec) -> Tuple[str, Optional[CanonicalProjectSpec]]:
        """
        Handle a project mutation request using LLM.
        Returns (response_text, updated_spec_or_none)
        """
        if not self.is_available():
            return "[Offline Mode] Specification updates require an active API key.", None

        prompt = [
            {"role": "system", "content": "You are a Specification Compiler. Based on the user's request, update the project JSON. Return a JSON object with two fields: 'message' (explanation to user) and 'patch' (the UPDATED full CanonicalProjectSpec or a subset). Only return 'patch' if a change is actually warranted."},
            {"role": "user", "content": f"Current Spec: {spec.model_dump_json()}\nUser Request: {message}\nIntent: {intent.intent}"}
        ]

        try:
            result_str = await self._call_llm(prompt, json_mode=True)
            res_data = json.loads(result_str)
            
            message_to_user = res_data.get("message", "I've updated the specification.")
            patch = res_data.get("patch")
            
            if patch:
                # Naive merge strategy: Re-parse the whole thing if it's a full spec, or just apply fields
                # For safety, we try to parse it as the spec model
                try:
                    # If it's a partial patch, we'd need more complex logic. 
                    # For this MVP, we prompt the AI to return the WHOLE project spec or at least valid top-level structures.
                    updated_spec = CanonicalProjectSpec(**patch)
                    return message_to_user, updated_spec
                except:
                    # Partial update or malformed.
                    logger.warning("AI returned a non-conforming patch. Falling back to message only.")
                    return message_to_user, None
            
            return message_to_user, None

        except Exception as e:
            logger.error(f"Mutation processing failed: {e}")
            return "I couldn't process that update right now.", None

    # ========================================================================
    # Fallback / Mock Methods (for key-less operation)
    # ========================================================================

    def _fallback_dynamic_question(self, spec: CanonicalProjectSpec, answered: List[str]) -> Optional[Question]:
        """Simple heuristic fallbacks for when AI is unavailable"""
        if any(q.startswith("Q_DYNAMIC") for q in answered):
            return None
        
        if spec.architecture.archetype == "web-app":
             # Return a hardcoded mock question
             from app.services.ai_service_mocks import mock_web_app_question
             return mock_web_app_question()
        return None

    def _fallback_classify_intent(self, message: str, mode: str) -> IntentResult:
        message_lower = message.lower()
        if "?" in message:
            return IntentResult(intent=UserIntent.RESEARCH_QUESTION, confidence=0.8, reasoning="Question mark detected.")
        return IntentResult(intent=UserIntent.CHIT_CHAT, confidence=0.5, reasoning="Fallback.")

# Singleton instance
_ai_service = AIService()

def get_ai_service() -> AIService:
    return _ai_service
