"""
Documentation Generator Service
Converts Canonical Project Specification into human-readable Markdown documentation.
"""
from typing import List
from datetime import datetime
from app.schemas.canonical_spec import CanonicalProjectSpec

class DocGenerator:
    def __init__(self, spec: CanonicalProjectSpec):
        self.spec = spec
        self.md = []

    def generate(self) -> str:
        """Generate complete project specification markdown"""
        self.md = []
        
        self._add_header()
        self._add_executive_summary()
        self._add_requirements()
        self._add_architecture()
        self._add_tech_stack()
        self._add_roadmap()
        self._add_footer()
        
        return "\n".join(self.md)

    def _add_header(self):
        self.md.append(f"# {self.spec.project.name or 'Untitled Project'}")
        self.md.append(f"**Version**: {self.spec.version} | **Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        self.md.append("")

    def _add_executive_summary(self):
        self.md.append("## 1. Executive Summary")
        self.md.append(self.spec.project.purpose or "No purpose defined.")
        
        if self.spec.project.targetAudience:
            self.md.append("\n**Target Audience:**")
            for audience in self.spec.project.targetAudience:
                self.md.append(f"- {audience}")
        self.md.append("")

    def _add_requirements(self):
        self.md.append("## 2. Requirements")
        
        self.md.append("### 2.1 Functional Requirements")
        if self.spec.requirements.functional:
            for req in self.spec.requirements.functional:
                self.md.append(f"#### {req.title}")
                self.md.append(f"{req.description}")
                if req.priority:
                    self.md.append(f"*Priority: {req.priority}*")
                self.md.append("")
        else:
            self.md.append("_No functional requirements defined._\n")

        self.md.append("### 2.2 Non-Functional Requirements")
        nfr = self.spec.requirements.nonFunctional
        has_nfr = False
        
        if nfr:
            # Iterate through model fields (categories)
            # Pydantic models support .dict() or model_dump()
            nfr_dict = nfr.dict() if hasattr(nfr, 'dict') else nfr.model_dump()
            
            for category, items in nfr_dict.items():
                if items:
                    has_nfr = True
                    self.md.append(f"#### {category.capitalize()}")
                    for item in items:
                        self.md.append(f"- {item}")
                    self.md.append("")
                    
        if not has_nfr:
            self.md.append("_No non-functional requirements defined._")
        self.md.append("")

    def _add_architecture(self):
        self.md.append("## 3. Architecture")
        self.md.append(f"**System Archetype**: {self.spec.architecture.archetype.value}")
        
        # Frontend
        fe = self.spec.architecture.frontend
        self.md.append("\n### 3.1 Frontend")
        if fe.framework:
            self.md.append(f"- **Framework**: {fe.framework}")
        if fe.styling:
            self.md.append(f"- **Styling**: {fe.styling}")
        if fe.components:
            self.md.append("\n**Key Components:**")
            for comp in fe.components:
                self.md.append(f"- `{comp.name}` ({comp.type}): {comp.description}")
        
        # Backend
        be = self.spec.architecture.backend
        self.md.append("\n### 3.2 Backend")
        if be.framework:
            self.md.append(f"- **Framework**: {be.framework}")
        
        if be.database:
            db = be.database
            self.md.append(f"- **Database**: {db.type or 'None'} ({db.technology or 'N/A'})")
            if db.schema:
                self.md.append("  - Schema defined")

        self.md.append("")

    def _add_tech_stack(self):
        self.md.append("## 4. Technology Stack")
        # Just a summary table
        self.md.append("| Category | Technology |")
        self.md.append("|----------|------------|")
        
        arch = self.spec.architecture
        if arch.frontend.framework:
            self.md.append(f"| Frontend | {arch.frontend.framework} |")
        if arch.backend.framework:
            self.md.append(f"| Backend | {arch.backend.framework} |")
        if arch.backend.database and arch.backend.database.technology:
            self.md.append(f"| Database | {arch.backend.database.technology} |")
        
        self.md.append("")

    def _add_roadmap(self):
        self.md.append("## 5. Implementation Roadmap")
        if self.spec.implementation.phases:
            for phase in self.spec.implementation.phases:
                self.md.append(f"### Phase {phase.order}: {phase.name}")
                if phase.description:
                    self.md.append(f"_{phase.description}_")
                for task in phase.tasks:
                    self.md.append(f"- [ ] {task.title}")
                self.md.append("")
        else:
             self.md.append("_Roadmap not yet generated._")

    def _add_footer(self):
        self.md.append("\n---\n*Generated by Alchemy*")

def generate_project_documentation(spec: CanonicalProjectSpec) -> str:
    generator = DocGenerator(spec)
    return generator.generate()
