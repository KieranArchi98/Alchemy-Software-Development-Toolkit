"""
Persistence Service
Handles saving and loading projects from local file system.
"""
import json
import os
import shutil
from typing import Dict, Optional, List
from pathlib import Path

from app.schemas.project import Project
from app.schemas.canonical_spec import CanonicalProjectSpec
from app.services.spec_utils import import_spec_from_json, export_spec_to_json

STORAGE_DIR = Path("storage/projects")

def _ensure_storage():
    """Ensure storage directory exists"""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def save_project(project: Project):
    """Save project to disk"""
    _ensure_storage()
    
    file_path = STORAGE_DIR / f"{project.id}.json"
    
    # Convert to dictionary using Pydantic's model_dump
    # We must handle dates and enums correctly, Pydantic does this with mode='json'
    data = project.model_dump(mode='json')
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_project(project_id: str) -> Optional[Project]:
    """Load project from disk"""
    _ensure_storage()
    
    file_path = STORAGE_DIR / f"{project_id}.json"
    
    if not file_path.exists():
        return None
        
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    try:
        # Pydantic validation handles parsing
        return Project(**data)
    except Exception as e:
        print(f"Error loading project {project_id}: {e}")
        return None

def delete_project(project_id: str):
    """Delete project from disk"""
    file_path = STORAGE_DIR / f"{project_id}.json"
    if file_path.exists():
        os.remove(file_path)

def list_projects() -> List[str]:
    """List all project IDs"""
    _ensure_storage()
    return [f.stem for f in STORAGE_DIR.glob("*.json")]
