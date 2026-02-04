"""
API v1 Projects Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectListResponse,
    ProjectListItem,
    MessageSendRequest,
    MessageResponse,
    OptionSelectRequest,
    CheckpointCreateRequest,
    CheckpointRevertRequest,
    ArtifactsResponse,
    CheckpointsResponse,
    QuestionAnswerRequest,
    Project,
    Checkpoint
)
from app.services import project_service

router = APIRouter()


@router.get("/", response_model=ProjectListResponse)
async def list_projects():
    """List all projects."""
    projects = await project_service.list_projects()
    items = [
        ProjectListItem(
            id=p.id,
            title=p.title,
            idea=p.idea,
            progress=p.progress,
            lastSaved=p.lastSaved or ""
        ) for p in projects
    ]
    return ProjectListResponse(projects=items)


@router.post("/", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest):
    """Create a new project."""
    try:
        project = await project_service.create_project(request)
        return ProjectResponse(project=project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Retrieve a project by ID."""
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(project=project)


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project."""
    await project_service.delete_project(project_id)
    return {"status": "success"}


@router.post("/answer", response_model=ProjectResponse)
async def answer_question(request: QuestionAnswerRequest):
    """
    Answer a roadmap question.
    """
    try:
        project = await project_service.answer_question(request)
        return ProjectResponse(project=project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageSendRequest):
    """Send a message (Chat Mode)."""
    try:
        project, message = await project_service.send_message(request)
        return MessageResponse(project=project, message=message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/option", response_model=ProjectResponse)
async def select_option(request: OptionSelectRequest):
    """Select option (Chat Mode)."""
    try:
        project = await project_service.select_option(request)
        return ProjectResponse(project=project)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/checkpoint", response_model=Checkpoint)
async def create_checkpoint(request: CheckpointCreateRequest):
    """Create a manual checkpoint."""
    try:
        checkpoint = await project_service.create_checkpoint(request)
        return checkpoint
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/revert", response_model=ProjectResponse)
async def revert_checkpoint(request: CheckpointRevertRequest):
    """Revert to a checkpoint."""
    try:
        project = await project_service.revert_checkpoint(request)
        return ProjectResponse(project=project)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{project_id}/artifacts", response_model=ArtifactsResponse)
async def get_artifacts(project_id: str):
    """Get project artifacts."""
    try:
        files = await project_service.get_artifacts(project_id)
        return ArtifactsResponse(files=files)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{project_id}/checkpoints", response_model=CheckpointsResponse)
async def get_checkpoints(project_id: str):
    """Get project checkpoints."""
    try:
        checkpoints = await project_service.get_checkpoints(project_id)
        return CheckpointsResponse(checkpoints=checkpoints)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
