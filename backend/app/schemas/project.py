from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from app.schemas.canonical_spec import CanonicalProjectSpec

# ============================================================================
# Request Schemas
# ============================================================================

class ProjectCreateRequest(BaseModel):
    """Request to create a new project"""
    idea: str = Field(..., min_length=1, description="Initial project idea")

class MessageSendRequest(BaseModel):
    """Request to send a message"""
    project_id: str
    content: str
    mode: str  # "guided" | "research" | "update"

class OptionSelectRequest(BaseModel):
    """Request to select an option"""
    project_id: str
    message_id: str
    option_id: str

class CheckpointCreateRequest(BaseModel):
    """Request to create a checkpoint"""
    project_id: str
    label: str

class CheckpointRevertRequest(BaseModel):
    """Request to revert to a checkpoint"""
    project_id: str
    checkpoint_id: str

class QuestionAnswerRequest(BaseModel):
    """Request to answer a roadmap question"""
    project_id: str
    question_id: str
    answer_ids: List[str]

# ============================================================================
# Response Schemas
# ============================================================================

class Checkpoint(BaseModel):
    """Timestamped snapshot of project state"""
    id: str
    timestamp: str
    label: str
    spec: CanonicalProjectSpec
    progress: int

class ProjectFile(BaseModel):
    """Generated artifact file"""
    id: str
    name: str
    type: str  # "design" | "context" | "roadmap" | "prompts"
    content: str

class SpecSection(BaseModel):
    """UI section for specification view"""
    id: str
    title: str
    content: str

class MessageOption(BaseModel):
    """Option for user selection in AI messages"""
    id: str
    label: str
    description: str

class Message(BaseModel):
    """Chat message"""
    id: str
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime
    context: Optional[str] = None
    options: Optional[List[MessageOption]] = None
    selectedOption: Optional[str] = None

class Question(BaseModel):
    """Roadmap question for UI"""
    id: str
    order: int
    category: str
    question: str
    description: str
    answers: List[Any]
    multiSelect: bool
    aiDefault: Optional[str] = None

class Project(BaseModel):
    """Complete project representation"""
    id: str
    title: str
    idea: str
    progress: int
    lastSaved: Optional[str] = None
    activePhase: str
    activeChatMode: str
    spec: CanonicalProjectSpec
    sections: List[SpecSection]
    files: List[ProjectFile]
    messages: List[Message]
    checkpoints: List[Checkpoint]
    currentQuestion: Optional[Question] = None

class ProjectResponse(BaseModel):
    """Response containing project data"""
    project: Project

class ProjectListItem(BaseModel):
    """Simplified project for listing"""
    id: str
    title: str
    idea: str
    progress: int
    lastSaved: str

class ProjectListResponse(BaseModel):
    """Response containing list of projects"""
    projects: List[ProjectListItem]

class ArtifactsResponse(BaseModel):
    """Response containing project artifacts"""
    files: List[ProjectFile]

class CheckpointsResponse(BaseModel):
    """Response containing checkpoints"""
    checkpoints: List[Checkpoint]

class MessageResponse(BaseModel):
    """Response after sending a message"""
    project: Project
    message: Message

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
