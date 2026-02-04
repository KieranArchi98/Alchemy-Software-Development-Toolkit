"""
Roadmap Generator Service
Generates a structured implementation roadmap from the detailed project specification.
"""
from typing import List, Dict, Any
from app.schemas.canonical_spec import (
    CanonicalProjectSpec, 
    Implementation, 
    Phase, 
    Task, 
    TaskStatus,
    Archetype,
    BackendArchitecture
)
import uuid

class RoadmapGenerator:
    def __init__(self, spec: CanonicalProjectSpec):
        self.spec = spec
        self.phases: List[Phase] = []
        self.task_counter = 0

    def generate(self) -> Implementation:
        """Generate a complete implementation plan"""
        self.phases = []
        
        # 1. Setup & Foundation
        self._add_phase_1_foundation()
        
        # 2. Core Backend / Infrastructure
        self._add_phase_2_backend()
        
        # 3. Core Frontend / UI
        self._add_phase_3_frontend()
        
        # 4. Features & Logic (MVP Scope)
        self._add_phase_4_features()
        
        # 5. Polish & Verification
        self._add_phase_5_polish()
        
        # Identify MVP Scope (All tasks in generated phases for now)
        mvp_scope = [fr.id for fr in self.spec.requirements.functional if fr.priority in ['critical', 'high']]
        
        return Implementation(phases=self.phases, mvpScope=mvp_scope)

    def _create_task(self, title: str) -> Task:
        self.task_counter += 1
        return Task(
            id=f"TASK-{self.task_counter:03d}",
            title=title,
            status=TaskStatus.PENDING
        )

    def _add_phase_1_foundation(self):
        tasks = []
        tasks.append(self._create_task("Initialize version control (Git)"))
        
        # Tech Stack Specifics
        fe_tech = self.spec.architecture.frontend.framework or "Frontend Framework"
        be_tech = self.spec.architecture.backend.framework or "Backend Framework"
        
        tasks.append(self._create_task(f"Setup {fe_tech} project structure"))
        tasks.append(self._create_task(f"Setup {be_tech} project structure"))
        tasks.append(self._create_task("Configure linting and formatting"))
        
        # Database
        if self.spec.architecture.backend.database:
            db_tech = self.spec.architecture.backend.database.technology or "Database"
            tasks.append(self._create_task(f"Initialize {db_tech} and migration system"))

        self.phases.append(Phase(
            id="PHASE-1",
            name="Project Foundation",
            order=1,
            description="Setup project structure, tooling, and core infrastructure.",
            tasks=tasks
        ))

    def _add_phase_2_backend(self):
        tasks = []
        
        # API Structure
        tasks.append(self._create_task("Define API standard / request-response format"))
        
        # Auth
        if self.spec.architecture.integration.authentication.value != "none":
            auth_type = self.spec.architecture.integration.authentication.value
            tasks.append(self._create_task(f"Implement {auth_type} authentication system"))
            
        # Database Models
        if self.spec.architecture.backend.database and self.spec.architecture.backend.database.models:
            for model in self.spec.architecture.backend.database.models:
                tasks.append(self._create_task(f"Implement database model: {model.name}"))
        
        # Core Services
        if self.spec.architecture.backend.services:
            for svc in self.spec.architecture.backend.services:
                tasks.append(self._create_task(f"Create service scaffold: {svc.name}"))

        self.phases.append(Phase(
            id="PHASE-2",
            name="Backend Core",
            order=2,
            description="Implement core backend services, database schema, and authentication.",
            tasks=tasks
        ))

    def _add_phase_3_frontend(self):
        tasks = []
        
        # Styling / UI Lib
        styling = self.spec.architecture.frontend.styling or "CSS"
        tasks.append(self._create_task(f"Setup styling system ({styling})"))
        
        # Layouts
        if self.spec.architecture.frontend.layout:
            tasks.append(self._create_task(f"Implement {self.spec.architecture.frontend.layout.type.value} layout wrapper"))
            
        # Core Components
        if self.spec.architecture.frontend.components:
             # Just key ones to avoid clutter
             layout_comps = [c for c in self.spec.architecture.frontend.components if c.type == 'layout']
             for comp in layout_comps:
                 tasks.append(self._create_task(f"Build component: {comp.name}"))
        
        # Navigation
        tasks.append(self._create_task("Implement client-side routing and navigation"))

        self.phases.append(Phase(
            id="PHASE-3",
            name="Frontend Skeleton",
            order=3,
            description="Build the frontend shell, navigation, and reusable UI components.",
            tasks=tasks
        ))

    def _add_phase_4_features(self):
        tasks = []
        
        # Pages
        if self.spec.architecture.frontend.pages:
            for page in self.spec.architecture.frontend.pages:
                tasks.append(self._create_task(f"Implement Page: {page.name} ({page.route})"))
                
        # Connect API
        tasks.append(self._create_task("Integrate Frontend with Backend APIs"))
        
        # Functional Requirements (MVP)
        for req in self.spec.requirements.functional:
            if req.priority in ['critical', 'high']:
                 tasks.append(self._create_task(f"Implement Feature: {req.title}"))

        self.phases.append(Phase(
            id="PHASE-4",
            name="Core Features (MVP)",
            order=4,
            description="Implement primary pages and business logic features.",
            tasks=tasks
        ))

    def _add_phase_5_polish(self):
        tasks = []
        tasks.append(self._create_task("Perform end-to-end testing"))
        tasks.append(self._create_task("Optimize performance and bundle size"))
        tasks.append(self._create_task("Write deployment documentation"))
        
        self.phases.append(Phase(
            id="PHASE-5",
            name="Polish & Launch",
            order=5,
            description="Final testing, optimization, and documentation.",
            tasks=tasks
        ))

def generate_roadmap(spec: CanonicalProjectSpec) -> Implementation:
    generator = RoadmapGenerator(spec)
    return generator.generate()
