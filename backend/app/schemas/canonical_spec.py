"""
Canonical Project Specification Schema and Validation

This module defines the comprehensive project specification structure
that serves as the single source of truth for Alchemy projects.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

class ProjectPhase(str, Enum):
    DISCOVERY = "discovery"
    DEFINITION = "definition"
    SPECIFICATION = "specification"
    COMPLETE = "complete"


class ConstraintType(str, Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    REGULATORY = "regulatory"
    TIMELINE = "timeline"
    BUDGET = "budget"
    OTHER = "other"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Archetype(str, Enum):
    WEB_APP = "web-app"
    MOBILE_APP = "mobile-app"
    DESKTOP_APP = "desktop-app"
    API_SERVICE = "api-service"
    CLI_TOOL = "cli-tool"
    HYBRID = "hybrid"


class DeploymentModel(str, Enum):
    CLOUD = "cloud"
    ON_PREMISE = "on-premise"
    HYBRID = "hybrid"
    LOCAL_ONLY = "local-only"


class LayoutType(str, Enum):
    SINGLE_PAGE = "single-page"
    MULTI_PAGE = "multi-page"
    DASHBOARD = "dashboard"
    SPLIT_VIEW = "split-view"
    CUSTOM = "custom"


class NavigationType(str, Enum):
    SIDEBAR = "sidebar"
    TOPBAR = "topbar"
    TABS = "tabs"
    NONE = "none"


class ComponentType(str, Enum):
    LAYOUT = "layout"
    FEATURE = "feature"
    UI = "ui"
    UTILITY = "utility"


class BackendArchitecture(str, Enum):
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    MODULAR = "modular"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class DatabaseType(str, Enum):
    SQL = "sql"
    NOSQL = "nosql"
    GRAPH = "graph"
    KEY_VALUE = "key-value"
    NONE = "none"


class ApiStyle(str, Enum):
    REST = "REST"
    GRAPHQL = "GraphQL"
    GRPC = "gRPC"
    WEBSOCKET = "WebSocket"


class AuthType(str, Enum):
    NONE = "none"
    JWT = "jwt"
    OAUTH = "oauth"
    SESSION = "session"
    API_KEY = "api-key"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


# ============================================================================
# Schema Models
# ============================================================================

class SpecMetadata(BaseModel):
    """Project metadata"""
    id: str
    created: datetime
    lastModified: datetime
    phase: ProjectPhase = ProjectPhase.DISCOVERY
    progress: int = Field(default=0, ge=0, le=100)


class Constraint(BaseModel):
    """Project constraint"""
    type: ConstraintType
    description: str


class ProjectInfo(BaseModel):
    """Core project information"""
    name: str = Field(..., min_length=1)
    tagline: Optional[str] = None
    purpose: str = Field(..., min_length=1)
    goals: List[str] = []
    targetAudience: List[str] = []
    constraints: List[Constraint] = []
    assumptions: List[str] = []


class FunctionalRequirement(BaseModel):
    """Functional requirement"""
    id: str = Field(..., pattern=r"^FR-\d+$")
    title: str
    description: str
    priority: Priority
    acceptanceCriteria: List[str] = []
    dependencies: List[str] = []  # Other FR IDs


class NonFunctionalRequirements(BaseModel):
    """Non-functional requirements"""
    performance: List[str] = []
    security: List[str] = []
    scalability: List[str] = []
    usability: List[str] = []
    reliability: List[str] = []


class Requirements(BaseModel):
    """All project requirements"""
    functional: List[FunctionalRequirement] = []
    nonFunctional: NonFunctionalRequirements = NonFunctionalRequirements()


class ComponentProp(BaseModel):
    """Component property definition"""
    name: str
    type: str
    required: bool = False


class Component(BaseModel):
    """Frontend component"""
    id: str
    name: str
    type: ComponentType
    description: Optional[str] = None
    props: List[ComponentProp] = []


class Page(BaseModel):
    """Frontend page"""
    id: str
    name: str
    route: str
    description: Optional[str] = None
    components: List[str] = []  # Component IDs
    authentication: bool = False


class Layout(BaseModel):
    """Frontend layout configuration"""
    type: LayoutType
    navigation: NavigationType = NavigationType.NONE
    responsive: bool = True


class FrontendArchitecture(BaseModel):
    """Frontend architecture definition"""
    framework: Optional[str] = None
    stateManagement: Optional[str] = None
    styling: Optional[str] = None
    pages: List[Page] = []
    components: List[Component] = []
    layout: Optional[Layout] = None


class Service(BaseModel):
    """Backend service"""
    id: str
    name: str
    responsibility: str
    dependencies: List[str] = []


class ApiEndpoint(BaseModel):
    """API endpoint definition"""
    id: str
    endpoint: str
    method: HttpMethod
    description: Optional[str] = None
    authentication: bool = False
    requestSchema: Optional[Dict[str, Any]] = None
    responseSchema: Optional[Dict[str, Any]] = None


class DatabaseModel(BaseModel):
    """Database model"""
    name: str
    fields: List[Dict[str, Any]] = []


class Database(BaseModel):
    """Database configuration"""
    type: DatabaseType = DatabaseType.NONE
    technology: Optional[str] = None
    models: List[DatabaseModel] = []


class BackendArchitectureSpec(BaseModel):
    """Backend architecture definition"""
    framework: Optional[str] = None
    language: Optional[str] = None
    architecture: BackendArchitecture = BackendArchitecture.MODULAR
    services: List[Service] = []
    apis: List[ApiEndpoint] = []
    database: Optional[Database] = None


class ExternalService(BaseModel):
    """External service integration"""
    name: str
    purpose: str
    required: bool = False


class Integration(BaseModel):
    """Integration specifications"""
    apiStyle: ApiStyle = ApiStyle.REST
    authentication: AuthType = AuthType.NONE
    externalServices: List[ExternalService] = []


class Architecture(BaseModel):
    """Complete architecture specification"""
    archetype: Archetype
    deploymentModel: DeploymentModel = DeploymentModel.LOCAL_ONLY
    frontend: FrontendArchitecture = FrontendArchitecture()
    backend: BackendArchitectureSpec = BackendArchitectureSpec()
    integration: Integration = Integration()


class Technology(BaseModel):
    """Technology stack"""
    frontend: List[str] = []
    backend: List[str] = []
    database: List[str] = []
    infrastructure: List[str] = []
    devTools: List[str] = []


class Task(BaseModel):
    """Implementation task"""
    id: str
    title: str
    status: TaskStatus = TaskStatus.PENDING


class Phase(BaseModel):
    """Implementation phase"""
    id: str
    name: str
    order: int = Field(..., ge=1)
    description: Optional[str] = None
    tasks: List[Task] = []


class Implementation(BaseModel):
    """Implementation plan"""
    phases: List[Phase] = []
    mvpScope: List[str] = []  # FR IDs included in MVP


class AiModel(BaseModel):
    """AI model usage"""
    purpose: str
    model: str


class AiUsage(BaseModel):
    """AI usage in the project"""
    models: List[AiModel] = []
    features: List[str] = []


class CanonicalProjectSpec(BaseModel):
    """
    Canonical Project Specification - Single Source of Truth
    
    This is the authoritative representation of a project.
    All other artifacts (documentation, roadmaps, prompts) are derived from this.
    """
    version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    metadata: SpecMetadata
    project: ProjectInfo
    requirements: Requirements = Requirements()
    architecture: Architecture
    technology: Technology = Technology()
    implementation: Implementation = Implementation()
    aiUsage: AiUsage = AiUsage()
    
    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0.0",
                "metadata": {
                    "id": "proj-123",
                    "created": "2026-02-04T07:00:00Z",
                    "lastModified": "2026-02-04T07:30:00Z",
                    "phase": "discovery",
                    "progress": 15
                },
                "project": {
                    "name": "Alchemy",
                    "tagline": "Turn ideas into AI-ready specifications",
                    "purpose": "Help developers plan software projects systematically",
                    "goals": ["Reduce planning time", "Improve specification quality"],
                    "targetAudience": ["Solo developers", "Founders"],
                    "constraints": [],
                    "assumptions": []
                },
                "architecture": {
                    "archetype": "web-app",
                    "deploymentModel": "local-only"
                }
            }
        }


# ============================================================================
# Validation and Mutation Rules
# ============================================================================

class SpecValidator:
    """Validates and enforces mutation rules for project specifications"""
    
    @staticmethod
    def validate_spec(spec: CanonicalProjectSpec) -> tuple[bool, List[str]]:
        """
        Validate a complete specification
        Returns (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate FR dependencies exist
        fr_ids = {fr.id for fr in spec.requirements.functional}
        for fr in spec.requirements.functional:
            for dep_id in fr.dependencies:
                if dep_id not in fr_ids:
                    errors.append(f"FR {fr.id} depends on non-existent FR {dep_id}")
        
        # Validate MVP scope references valid FRs
        for fr_id in spec.implementation.mvpScope:
            if fr_id not in fr_ids:
                errors.append(f"MVP scope references non-existent FR {fr_id}")
        
        # Validate component references in pages
        component_ids = {c.id for c in spec.architecture.frontend.components}
        for page in spec.architecture.frontend.pages:
            for comp_id in page.components:
                if comp_id not in component_ids:
                    errors.append(f"Page {page.id} references non-existent component {comp_id}")
        
        # Validate service dependencies
        service_ids = {s.id for s in spec.architecture.backend.services}
        for service in spec.architecture.backend.services:
            for dep_id in service.dependencies:
                if dep_id not in service_ids:
                    errors.append(f"Service {service.id} depends on non-existent service {dep_id}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def safe_merge(base: CanonicalProjectSpec, updates: Dict[str, Any]) -> CanonicalProjectSpec:
        """
        Safely merge updates into base spec
        Enforces mutation rules:
        - Most recent decisions override earlier ones
        - Maintains referential integrity
        - Updates lastModified timestamp
        """
        # Create a copy
        updated_dict = base.model_dump()
        
        # Merge updates (shallow merge for now)
        for key, value in updates.items():
            if key in updated_dict and key != "metadata":
                updated_dict[key] = value
        
        # Update metadata
        updated_dict["metadata"]["lastModified"] = datetime.utcnow()
        
        # Reconstruct and validate
        updated_spec = CanonicalProjectSpec(**updated_dict)
        is_valid, errors = SpecValidator.validate_spec(updated_spec)
        
        if not is_valid:
            raise ValueError(f"Spec validation failed: {errors}")
        
        return updated_spec
