"""
Guided Roadmap Question Engine

This module implements the static question-driven specification flow.
Questions are loaded from data, not hardcoded logic.
"""
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel
import json
from pathlib import Path


# ============================================================================
# Question Schema Models
# ============================================================================

class Answer(BaseModel):
    """A possible answer to a question"""
    id: str
    label: str
    description: str
    value: Any  # Can be string, list, dict, etc.
    recommended: bool = False
    metadata: Optional[Dict[str, Any]] = None


class SkipCondition(BaseModel):
    """Condition for skipping a question"""
    field: str  # Field path in spec (e.g., "architecture.archetype")
    notEquals: Optional[str] = None
    equals: Optional[str] = None


class Question(BaseModel):
    """A guided roadmap question"""
    id: str
    order: int
    category: str
    question: str
    description: str
    fieldPath: str  # Path in canonical spec to mutate
    answers: List[Answer]
    aiDefault: str  # Answer ID to use if AI picks
    skipCondition: Optional[SkipCondition] = None
    multiSelect: bool = False
    maxSelections: Optional[int] = None


class GuidedRoadmap(BaseModel):
    """Complete guided roadmap definition"""
    version: str
    metadata: Dict[str, Any]
    questions: List[Question]


# ============================================================================
# Question Engine
# ============================================================================

class QuestionEngine:
    """Manages guided roadmap question flow"""
    
    def __init__(self, roadmap_path: Optional[str] = None):
        """Initialize with roadmap data"""
        if roadmap_path is None:
            # Default to bundled roadmap
            roadmap_path = Path(__file__).parent.parent / "data" / "guided_roadmap.json"
        
        with open(roadmap_path, 'r') as f:
            data = json.load(f)
        
        self.roadmap = GuidedRoadmap(**data)
        self.questions_by_id = {q.id: q for q in self.roadmap.questions}
        self.questions_by_order = sorted(self.roadmap.questions, key=lambda q: q.order)
    
    def get_total_questions(self) -> int:
        """Get total number of questions"""
        return len(self.roadmap.questions)
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get a specific question by ID"""
        return self.questions_by_id.get(question_id)
    
    def get_question_by_order(self, order: int) -> Optional[Question]:
        """Get question by order number (1-indexed)"""
        if 1 <= order <= len(self.questions_by_order):
            return self.questions_by_order[order - 1]
        return None
    
    def get_next_question(
        self,
        current_spec: Dict[str, Any],
        answered_questions: List[str]
    ) -> Optional[Question]:
        """
        Get the next unanswered question based on current spec state.
        Respects skip conditions.
        """
        for question in self.questions_by_order:
            # Skip if already answered
            if question.id in answered_questions:
                continue
            
            # Check skip condition
            if question.skipCondition:
                if self._should_skip(question.skipCondition, current_spec):
                    continue
            
            return question
        
        return None  # All questions answered
    
    def _should_skip(self, condition: SkipCondition, spec: Dict[str, Any]) -> bool:
        """Check if question should be skipped based on spec state"""
        # Get field value from spec using dot notation
        value = self._get_nested_value(spec, condition.field)
        
        if condition.notEquals is not None:
            # Skip if value is NOT equal to the specified value
            return value != condition.notEquals
        
        if condition.equals is not None:
            # Skip if value IS equal to the specified value
            return value == condition.equals
        
        return False
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get value from nested dict using dot notation (e.g., 'architecture.archetype')"""
        keys = path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        
        return value
    
    def get_answer(self, question_id: str, answer_id: str) -> Optional[Answer]:
        """Get a specific answer from a question"""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
        
        for answer in question.answers:
            if answer.id == answer_id:
                return answer
        
        return None
    
    def get_ai_default_answer(self, question_id: str) -> Optional[Answer]:
        """Get the AI default answer for a question"""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
        
        return self.get_answer(question_id, question.aiDefault)
    
    def apply_answer_to_spec(
        self,
        spec: Dict[str, Any],
        question_id: str,
        answer_ids: List[str],
        question_obj: Optional[Question] = None
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Apply answer(s) to specification.
        Returns (updated_spec, list_of_errors)
        """
        question = question_obj if question_obj else self.get_question_by_id(question_id)
        
        if not question:
            return spec, [f"Question {question_id} not found"]
        
        # Validate answer count
        if question.multiSelect:
            max_sel = question.maxSelections or len(question.answers)
            if len(answer_ids) > max_sel:
                return spec, [f"Too many answers selected (max: {max_sel})"]
        else:
            if len(answer_ids) != 1:
                return spec, ["Single answer required"]
        
        # Get answers
        answers = []
        for answer_id in answer_ids:
            # Find answer in the provided question object
            answer = next((a for a in question.answers if a.id == answer_id), None)
            
            if not answer:
                return spec, [f"Answer {answer_id} not found"]
            answers.append(answer)
        
        # Apply to spec
        try:
            updated_spec = self._apply_values(spec, question.fieldPath, answers, question.multiSelect)
            return updated_spec, []
        except Exception as e:
            return spec, [f"Failed to apply answer: {str(e)}"]
    
    def _apply_values(
        self,
        spec: Dict[str, Any],
        field_path: str,
        answers: List[Answer],
        multi_select: bool
    ) -> Dict[str, Any]:
        """Apply answer values to spec at field path"""
        import copy
        spec = copy.deepcopy(spec)
        
        # Handle special cases for different field types
        if multi_select:
            # For multi-select, we need to merge values
            if field_path == "requirements.functional":
                # Append functional requirements
                if "requirements" not in spec:
                    spec["requirements"] = {"functional": [], "nonFunctional": {}}
                if "functional" not in spec["requirements"]:
                    spec["requirements"]["functional"] = []
                
                for answer in answers:
                    spec["requirements"]["functional"].append(answer.value)
            
            elif field_path == "requirements.nonFunctional":
                # Merge non-functional requirements
                if "requirements" not in spec:
                    spec["requirements"] = {"functional": [], "nonFunctional": {}}
                if "nonFunctional" not in spec["requirements"]:
                    spec["requirements"]["nonFunctional"] = {}
                
                for answer in answers:
                    category = answer.value["category"]
                    items = answer.value["items"]
                    if category not in spec["requirements"]["nonFunctional"]:
                        spec["requirements"]["nonFunctional"][category] = []
                    spec["requirements"]["nonFunctional"][category].extend(items)
            
            elif field_path == "project.constraints":
                # Append constraints
                if "project" not in spec:
                    spec["project"] = {}
                if "constraints" not in spec["project"]:
                    spec["project"]["constraints"] = []
                
                for answer in answers:
                    spec["project"]["constraints"].append(answer.value)
            
            elif field_path == "aiUsage.features":
                # Set AI features (flatten lists)
                if "aiUsage" not in spec:
                    spec["aiUsage"] = {"models": [], "features": []}
                
                features = []
                for answer in answers:
                    if isinstance(answer.value, list):
                        features.extend(answer.value)
                    else:
                        features.append(answer.value)
                
                spec["aiUsage"]["features"] = features
            
            else:
                # Generic multi-select: collect values into array
                values = [answer.value for answer in answers]
                self._set_nested_value(spec, field_path, values)
        
        else:
            # Single select
            answer = answers[0]
            
            # Handle special metadata cases
            if answer.metadata and field_path == "architecture.backend.database.type":
                # Set both type and technology
                if "architecture" not in spec:
                    spec["architecture"] = {}
                if "backend" not in spec["architecture"]:
                    spec["architecture"]["backend"] = {}
                    
                # Check if database entry is missing OR None
                if "database" not in spec["architecture"]["backend"] or spec["architecture"]["backend"]["database"] is None:
                    spec["architecture"]["backend"]["database"] = {}
                
                spec["architecture"]["backend"]["database"]["type"] = answer.value
                spec["architecture"]["backend"]["database"]["technology"] = answer.metadata.get("technology")
            else:
                # Standard single value
                existing_val = self._get_nested_value(spec, field_path)
                
                if isinstance(existing_val, list):
                    # Append/Extend mode for list fields
                    if answer.value is not None:
                        if isinstance(answer.value, list):
                            existing_val.extend(answer.value)
                        else:
                            existing_val.append(answer.value)
                else:
                    # Overwrite mode for scalar fields
                    self._set_nested_value(spec, field_path, answer.value)
        
        return spec
    
    def _set_nested_value(self, data: Dict[str, Any], path: str, value: Any):
        """Set value in nested dict using dot notation"""
        keys = path.split('.')
        current = data
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set final value
        current[keys[-1]] = value
    
    def get_progress(self, answered_questions: List[str]) -> int:
        """Calculate progress percentage based on answered questions"""
        total = self.get_total_questions()
        answered = len(answered_questions)
        return int((answered / total) * 100) if total > 0 else 0


# ============================================================================
# Singleton Instance
# ============================================================================

_engine_instance: Optional[QuestionEngine] = None

def get_question_engine() -> QuestionEngine:
    """Get singleton question engine instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = QuestionEngine()
    return _engine_instance
