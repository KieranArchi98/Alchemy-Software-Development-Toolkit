"""
Utilities for working with canonical project specifications
"""
from typing import Dict, Any
from datetime import datetime
import json

from app.schemas.canonical_spec import (
    CanonicalProjectSpec,
    SpecMetadata,
    ProjectInfo,
    Architecture,
    Archetype,
    SpecValidator
)


def create_initial_spec(project_id: str, idea: str, archetype: Archetype = Archetype.WEB_APP) -> CanonicalProjectSpec:
    """
    Create an initial canonical specification from a project idea
    """
    now = datetime.utcnow()
    
    spec = CanonicalProjectSpec(
        version="1.0.0",
        metadata=SpecMetadata(
            id=project_id,
            created=now,
            lastModified=now,
            phase="discovery",
            progress=5
        ),
        project=ProjectInfo(
            name=_generate_name_from_idea(idea),
            purpose=idea,
            goals=[],
            targetAudience=[],
            constraints=[],
            assumptions=[]
        ),
        architecture=Architecture(
            archetype=archetype
        )
    )
    
    return spec


def validate_and_update_spec(
    current_spec: CanonicalProjectSpec,
    updates: Dict[str, Any]
) -> CanonicalProjectSpec:
    """
    Validate and apply updates to a specification
    Enforces mutation rules and referential integrity
    """
    return SpecValidator.safe_merge(current_spec, updates)


def export_spec_to_json(spec: CanonicalProjectSpec, pretty: bool = True) -> str:
    """
    Export specification to JSON string
    """
    spec_dict = spec.model_dump(mode='json')
    if pretty:
        return json.dumps(spec_dict, indent=2, default=str)
    return json.dumps(spec_dict, default=str)


def import_spec_from_json(json_str: str) -> CanonicalProjectSpec:
    """
    Import specification from JSON string
    Validates against schema
    """
    spec_dict = json.loads(json_str)
    spec = CanonicalProjectSpec(**spec_dict)
    
    # Validate
    is_valid, errors = SpecValidator.validate_spec(spec)
    if not is_valid:
        raise ValueError(f"Invalid specification: {errors}")
    
    return spec


def get_spec_summary(spec: CanonicalProjectSpec) -> Dict[str, Any]:
    """
    Get a summary of the specification for display
    """
    return {
        "id": spec.metadata.id,
        "name": spec.project.name,
        "purpose": spec.project.purpose,
        "phase": spec.metadata.phase,
        "progress": spec.metadata.progress,
        "archetype": spec.architecture.archetype,
        "functional_requirements": len(spec.requirements.functional),
        "pages": len(spec.architecture.frontend.pages),
        "components": len(spec.architecture.frontend.components),
        "services": len(spec.architecture.backend.services),
        "apis": len(spec.architecture.backend.apis),
        "implementation_phases": len(spec.implementation.phases),
        "last_modified": spec.metadata.lastModified.isoformat()
    }


def _generate_name_from_idea(idea: str) -> str:
    """Generate a project name from the idea"""
    words = idea.split()[:4]
    return " ".join(w.capitalize() for w in words)


# ============================================================================
# Mutation Helpers
# ============================================================================

def add_functional_requirement(
    spec: CanonicalProjectSpec,
    title: str,
    description: str,
    priority: str = "medium"
) -> CanonicalProjectSpec:
    """Add a new functional requirement"""
    from app.schemas.canonical_spec import FunctionalRequirement, Priority
    
    # Generate FR ID
    existing_ids = [fr.id for fr in spec.requirements.functional]
    next_num = len(existing_ids) + 1
    fr_id = f"FR-{next_num:03d}"
    
    new_fr = FunctionalRequirement(
        id=fr_id,
        title=title,
        description=description,
        priority=Priority(priority)
    )
    
    spec.requirements.functional.append(new_fr)
    spec.metadata.lastModified = datetime.utcnow()
    
    return spec


def add_page(
    spec: CanonicalProjectSpec,
    name: str,
    route: str,
    description: str = ""
) -> CanonicalProjectSpec:
    """Add a new page to frontend architecture"""
    from app.schemas.canonical_spec import Page
    
    page_id = name.lower().replace(" ", "-")
    
    new_page = Page(
        id=page_id,
        name=name,
        route=route,
        description=description
    )
    
    spec.architecture.frontend.pages.append(new_page)
    spec.metadata.lastModified = datetime.utcnow()
    
    return spec


def add_api_endpoint(
    spec: CanonicalProjectSpec,
    endpoint: str,
    method: str,
    description: str = ""
) -> CanonicalProjectSpec:
    """Add a new API endpoint"""
    from app.schemas.canonical_spec import ApiEndpoint, HttpMethod
    
    api_id = f"{method.lower()}-{endpoint.replace('/', '-').strip('-')}"
    
    new_api = ApiEndpoint(
        id=api_id,
        endpoint=endpoint,
        method=HttpMethod(method),
        description=description
    )
    
    spec.architecture.backend.apis.append(new_api)
    spec.metadata.lastModified = datetime.utcnow()
    
    return spec


def update_progress(spec: CanonicalProjectSpec, progress: int) -> CanonicalProjectSpec:
    """Update project progress"""
    spec.metadata.progress = max(0, min(100, progress))
    spec.metadata.lastModified = datetime.utcnow()
    return spec


def advance_phase(spec: CanonicalProjectSpec) -> CanonicalProjectSpec:
    """Advance to next project phase"""
    from app.schemas.canonical_spec import ProjectPhase
    
    phase_order = [
        ProjectPhase.DISCOVERY,
        ProjectPhase.DEFINITION,
        ProjectPhase.SPECIFICATION,
        ProjectPhase.COMPLETE
    ]
    
    current_index = phase_order.index(spec.metadata.phase)
    if current_index < len(phase_order) - 1:
        spec.metadata.phase = phase_order[current_index + 1]
        spec.metadata.lastModified = datetime.utcnow()
    
    return spec
