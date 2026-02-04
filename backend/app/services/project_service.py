"""
Project service - Business logic for project management
Integrates Canonical Spec, Question Engine, and AI Service
"""
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import uuid
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

from app.schemas.project import (
    Project,
    ProjectCreateRequest,
    MessageSendRequest,
    OptionSelectRequest,
    CheckpointCreateRequest,
    CheckpointRevertRequest,
    QuestionAnswerRequest,
    Message,
    Checkpoint,
    SpecSection,
    ProjectFile,
    MessageOption,
    Question
)
from app.schemas.canonical_spec import CanonicalProjectSpec, Implementation, TaskStatus
from app.services.spec_utils import create_initial_spec, export_spec_to_json
from app.services.question_engine import get_question_engine, Question as EngineQuestion
from app.services.ai_service import get_ai_service, UserIntent
from app.services.persistence_service import save_project, load_project, list_projects as store_list, delete_project as store_delete
from app.services.doc_generator import generate_project_documentation
from app.services.roadmap_generator import generate_roadmap
from app.services.prompt_generator import generate_prompts

# In-memory storage (Cache)
projects_store: Dict[str, Project] = {}
answered_questions_store: Dict[str, List[str]] = {} # project_id -> list of question IDs
current_questions_store: Dict[str, EngineQuestion] = {} # project_id -> Current Active Question Object


def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())[:8]

async def list_projects() -> List[Project]:
    """List all projects"""
    ids = store_list()
    projects = []
    for pid in ids:
        p = await get_project(pid)
        if p:
            projects.append(p)
    return projects

async def delete_project(project_id: str):
    """Delete a project"""
    if project_id in projects_store:
        del projects_store[project_id]
    store_delete(project_id)

async def get_project(project_id: str) -> Optional[Project]:
    """Get project (memory or disk)"""
    if project_id in projects_store:
        return projects_store[project_id]
    
    # load_project is currently sync, we can keep it for now or wrap in run_in_executor
    project = load_project(project_id)
    if project:
        projects_store[project_id] = project
        return project
    return None

def _update_derived_state(project: Project):
    """Regenerate derived data (Roadmap, Docs, Files)"""
    # 1. Update Implementation Roadmap
    project.spec.implementation = generate_roadmap(project.spec)
    
    # 2. Update Spec Metadata
    project.spec.metadata.lastModified = datetime.utcnow()
    project.spec.metadata.progress = project.progress
    
    # 3. Derive Sections
    project.sections = _derive_sections(project.spec)
    
    # 4. Generate Artifacts
    project.files = _generate_artifacts(project.spec)
    
    # 5. Timestamp
    project.lastSaved = datetime.utcnow().isoformat()

async def create_project(request: ProjectCreateRequest) -> Project:
    """Create a new project from an initial idea."""
    if not request.idea or len(request.idea.strip()) < 5:
        raise ValueError("Project idea must be at least 5 characters long.")

    project_id = generate_id()
    spec = create_initial_spec(project_id, request.idea)
    answered_questions_store[project_id] = []
    
    initial_checkpoint = Checkpoint(
        id=generate_id(),
        timestamp=datetime.utcnow().isoformat(),
        label="Project Created",
        spec=spec.model_copy(deep=True),
        progress=5
    )
    
    engine = get_question_engine()
    next_q = engine.get_next_question(spec.model_dump(), [])
    
    current_question = None
    if next_q:
        current_question = _map_question(next_q)
        current_questions_store[project_id] = next_q
    
    initial_message = Message(
        id=generate_id(),
        role="assistant",
        content="I've analyzed your idea. Let's start building your specification by answering a few key questions.",
        timestamp=datetime.utcnow(),
    )
    
    project = Project(
        id=project_id,
        title=spec.project.name,
        idea=request.idea,
        progress=5,
        lastSaved=datetime.utcnow().isoformat(),
        activePhase="discovery",
        activeChatMode="guided",
        spec=spec,
        sections=[],
        files=[],
        messages=[initial_message],
        checkpoints=[initial_checkpoint],
        currentQuestion=current_question
    )
    
    _update_derived_state(project)
    project.checkpoints[0].spec = project.spec.model_copy(deep=True)
    
    projects_store[project_id] = project
    save_project(project)
    return project

async def answer_question(request: QuestionAnswerRequest) -> Project:
    """Answer a roadmap question and update spec."""
    project = await get_project(request.project_id)
    if not project:
        raise ValueError(f"Project {request.project_id} not found")
    
    engine = get_question_engine()
    active_q = current_questions_store.get(request.project_id)
    
    if not active_q:
         active_q = engine.get_question_by_id(request.question_id)
         
    if not active_q:
         raise ValueError(f"Question {request.question_id} definition not found")

    # Apply answer to spec
    current_spec_dict = project.spec.model_dump()
    updated_spec_dict, errors = engine.apply_answer_to_spec(
        current_spec_dict,
        request.question_id,
        request.answer_ids,
        question_obj=active_q
    )
    
    if errors:
        raise ValueError(f"Invalid answer: {errors}")
    
    project.spec = CanonicalProjectSpec(**updated_spec_dict)
    
    # Track answered
    if request.project_id not in answered_questions_store:
        answered_questions_store[request.project_id] = []
    if request.question_id not in answered_questions_store[request.project_id]:
        answered_questions_store[request.project_id].append(request.question_id)
    
    answered_list = answered_questions_store[request.project_id]
    progress = engine.get_progress(answered_list)
    project.progress = max(project.progress, progress)
    
    _update_derived_state(project)
    
    # Get Next Question
    next_q = engine.get_next_question(project.spec.model_dump(), answered_list)
    
    if not next_q:
        ai_service = get_ai_service()
        next_q = await ai_service.generate_dynamic_question(project.spec, answered_list)

    if next_q:
        current_questions_store[request.project_id] = next_q
        project.currentQuestion = _map_question(next_q)
    else:
        if request.project_id in current_questions_store:
            del current_questions_store[request.project_id]
        project.currentQuestion = None
    
    # Checkpoint
    checkpoint = Checkpoint(
        id=generate_id(),
        timestamp=datetime.utcnow().isoformat(),
        label=f"Answered: {request.question_id}",
        spec=project.spec.model_copy(deep=True),
        progress=project.progress
    )
    project.checkpoints.append(checkpoint)
    
    project.messages.append(Message(
        id=generate_id(),
        role="assistant",
        content=f"Updated specification based on your answer.",
        timestamp=datetime.utcnow()
    ))
    
    projects_store[request.project_id] = project
    save_project(project)
    return project

async def send_message(request: MessageSendRequest) -> Tuple[Project, Message]:
    """Process user message with intent classification."""
    project = await get_project(request.project_id)
    if not project:
        raise ValueError(f"Project {request.project_id} not found")
    
    project.messages.append(Message(
        id=generate_id(),
        role="user",
        content=request.content,
        timestamp=datetime.utcnow()
    ))
    
    ai_service = get_ai_service()
    
    try:
        intent_result = await ai_service.classify_intent(request.content, request.mode, project.spec)
        response_text = ""
        updated_spec = None
        
        if intent_result.intent == UserIntent.RESEARCH_QUESTION:
            response_text = await ai_service.process_research_query(request.content, project.spec)
            
        elif intent_result.intent in [UserIntent.DESIGN_DECISION, UserIntent.UPDATE_REQUEST]:
            if request.mode == "research":
                response_text = "I notice you want to make a change, but we are in Research Mode. Switch to Update Mode to mutate the specification."
            else:
                response_text, updated_spec = await ai_service.process_mutation(request.content, intent_result, project.spec)
        else: 
             response_text = "I see. How else can I help with your project specification?"

        if updated_spec:
             project.spec = updated_spec
             _update_derived_state(project)
             
             project.checkpoints.append(Checkpoint(
                id=generate_id(),
                timestamp=datetime.utcnow().isoformat(),
                label=f"Update: {intent_result.intent.value}",
                spec=project.spec.model_copy(deep=True),
                progress=project.progress
            ))

        ai_message = Message(
            id=generate_id(),
            role="assistant",
            content=response_text,
            timestamp=datetime.utcnow()
        )
        project.messages.append(ai_message)
        
    except Exception as e:
        logger.error(f"Error in chat processing: {e}")
        ai_message = Message(
            id=generate_id(),
            role="assistant",
            content=f"I encountered an error: {str(e)}",
            timestamp=datetime.utcnow()
        )
        project.messages.append(ai_message)
    
    save_project(project)
    return project, ai_message

async def select_option(request: OptionSelectRequest) -> Project:
    """Handle chat option selection."""
    project = await get_project(request.project_id)
    if not project:
        raise ValueError("Project not found")
        
    # Find the message and option
    target_msg = next((m for m in project.messages if m.id == request.message_id), None)
    if not target_msg or not target_msg.options:
        raise ValueError("Message or options not found")
    
    option = next((o for o in target_msg.options if o.id == request.option_id), None)
    if not option:
        raise ValueError("Option not found")
        
    # Mark as selected
    target_msg.selectedOption = request.option_id
    
    # If it was a dynamic question, we might want to record it
    if request.message_id == "AI_QUESTION": # Example
         pass
         
    save_project(project)
    return project

async def create_checkpoint(request: CheckpointCreateRequest) -> Checkpoint:
    project = await get_project(request.project_id)
    if not project:
        raise ValueError(f"Project {request.project_id} not found")
    
    checkpoint = Checkpoint(
        id=generate_id(),
        timestamp=datetime.utcnow().isoformat(),
        label=request.label,
        spec=project.spec.model_copy(deep=True),
        progress=project.progress
    )
    
    project.checkpoints.append(checkpoint)
    save_project(project)
    return checkpoint

async def revert_checkpoint(request: CheckpointRevertRequest) -> Project:
    project = await get_project(request.project_id)
    if not project:
        raise ValueError(f"Project {request.project_id} not found")
    
    target_index = -1
    target_checkpoint = None
    for i, cp in enumerate(project.checkpoints):
        if cp.id == request.checkpoint_id:
            target_index = i
            target_checkpoint = cp
            break
            
    if target_index == -1:
        raise ValueError("Checkpoint not found")
    
    project.checkpoints = project.checkpoints[:target_index + 1]
    project.spec = target_checkpoint.spec.model_copy(deep=True)
    project.progress = target_checkpoint.progress
    
    _update_derived_state(project)
    save_project(project)
    return project

async def get_artifacts(project_id: str) -> list[ProjectFile]:
    project = await get_project(project_id)
    if not project:
        raise ValueError("Project not found")
    return project.files

async def get_checkpoints(project_id: str) -> list[Checkpoint]:
    project = await get_project(project_id)
    if not project:
        raise ValueError("Project not found")
    return project.checkpoints

# ============================================================================
# Helpers
# ============================================================================

def _map_question(q: EngineQuestion) -> Question:
    return Question(
        id=q.id,
        order=q.order,
        category=q.category,
        question=q.question,
        description=q.description,
        answers=[a.dict() for a in q.answers],
        multiSelect=q.multiSelect,
        aiDefault=q.aiDefault
    )

def _derive_sections(spec: CanonicalProjectSpec) -> list[SpecSection]:
    return [
        SpecSection(id="overview", title="Overview", content=spec.project.purpose),
        SpecSection(id="requirements", title="Requirements", content=_format_requirements(spec)),
        SpecSection(id="architecture", title="Architecture", content=_format_architecture(spec)),
        SpecSection(id="constraints", title="Constraints", content=_format_constraints(spec)),
    ]

def _format_requirements(spec: CanonicalProjectSpec) -> str:
    reqs = [f"- {fr.title}: {fr.description}" for fr in spec.requirements.functional]
    return "\n".join(reqs) if reqs else "No requirements defined."

def _format_architecture(spec: CanonicalProjectSpec) -> str:
    lines = [f"Archetype: {spec.architecture.archetype.value}"]
    if spec.architecture.frontend.framework:
        lines.append(f"Frontend: {spec.architecture.frontend.framework}")
    if spec.architecture.backend.framework:
        lines.append(f"Backend: {spec.architecture.backend.framework}")
    return "\n".join(lines)

def _format_constraints(spec: CanonicalProjectSpec) -> str:
    cons = [f"- {c.type}: {c.description}" for c in spec.project.constraints]
    return "\n".join(cons) if cons else "No constraints defined."

def _format_roadmap_markdown(impl: Implementation) -> str:
    md = ["# Implementation Roadmap", ""]
    for phase in impl.phases:
        md.append(f"## Phase {phase.order}: {phase.name}")
        if phase.description:
            md.append(f"_{phase.description}_")
        md.append("")
        for task in phase.tasks:
            status = "[x]" if task.status == TaskStatus.COMPLETED else "[ ]"
            md.append(f"- {status} {task.title}")
        md.append("")
    return "\n".join(md)

def _generate_artifacts(spec: CanonicalProjectSpec) -> list[ProjectFile]:
    doc = generate_project_documentation(spec)
    json_content = export_spec_to_json(spec)
    roadmap = _format_roadmap_markdown(spec.implementation)
    prompts_list = generate_prompts(spec)
    
    # Format prompts as Markdown
    prompts_md = ["# AI Implementation Prompt Sequence", ""]
    for p in prompts_list:
        prompts_md.append(f"## Step {p['step']}: {p['phase_name']}")
        prompts_md.append(p["prompt"])
        prompts_md.append("\n---\n")
    prompts_content = "\n".join(prompts_md)
    
    return [
        ProjectFile(id="documentation", name="Documentation", type="design", content=doc),
        ProjectFile(id="spec-json", name="Spec (JSON)", type="context", content=json_content),
        ProjectFile(id="roadmap", name="Roadmap", type="roadmap", content=roadmap),
        ProjectFile(id="prompts", name="AI Prompts", type="prompts", content=prompts_content)
    ]
