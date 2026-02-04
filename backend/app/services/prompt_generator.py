"""
Prompt Generator Service
Generates sequential AI prompts based on the implementation roadmap.
"""
from typing import List, Dict, Any
import json
from app.schemas.canonical_spec import CanonicalProjectSpec, Phase

class PromptGenerator:
    def __init__(self, spec: CanonicalProjectSpec):
        self.spec = spec

    def generate(self) -> List[Dict[str, str]]:
        """
        Generate a list of prompts, one per phase.
        Returns generic list of dicts: [{ "step": 1, "phase": "...", "prompt": "..." }]
        """
        prompts = []
        phases = self.spec.implementation.phases
        
        for i, phase in enumerate(phases):
            prompt_content = self._create_phase_prompt(phase, i + 1)
            prompts.append({
                "step": i + 1,
                "phase_id": phase.id,
                "phase_name": phase.name,
                "prompt": prompt_content
            })
            
        return prompts

    def _create_phase_prompt(self, phase: Phase, step_num: int) -> str:
        """Create the actual text prompt for a phase"""
        
        # 1. Identity & Context
        prompt = [
            f"# Role: Expert Software Engineer",
            f"You are building '{self.spec.project.name}'.",
            f"Description: {self.spec.project.purpose}",
            "",
            f"## Current Objective: Phase {step_num} - {phase.name}",
            f"{phase.description or ''}",
            "",
            "## Requirements Checklist",
            "Implement the following strictly in order:",
        ]
        
        # 2. Checklist
        for task in phase.tasks:
            prompt.append(f"- [ ] {task.title}")
            
        # 3. Context (JSON Subset)
        context = self._get_context_for_phase(phase)
        context_json = json.dumps(context, indent=2)
        
        prompt.extend([
            "",
            "## Project Context (JSON Source of Truth)",
            "Use this specification to derive technical details (Frameworks, naming, schemas).",
            "```json",
            context_json,
            "```",
            "",
            "## Guidelines",
            "1. Write production-ready code.",
            "2. Create all necessary files and folders.",
            "3. If a file exists, update it safely.",
            "4. Follow the architecture defined in the Context exactly.",
            "5. Do not invent features not listed in the Checklist."
        ])
        
        return "\n".join(prompt)

    def _get_context_for_phase(self, phase: Phase) -> Dict[str, Any]:
        """
        Extract strictly relevant sections of the spec for token efficiency.
        """
        # Helper to remove empty values
        def _clean(d):
            if not isinstance(d, dict):
                return d
            return {k: _clean(v) for k, v in d.items() if v not in [None, [], {}, ""]}

        # Base context
        context = {
            "project": self.spec.project.dict(),
            "technology": self.spec.technology.dict(),
            "constraints": [c.dict() for c in self.spec.project.constraints]
        }
        
        phase_lower = phase.name.lower()
        include_backend = "backend" in phase_lower or "foundation" in phase_lower or "api" in phase_lower
        include_frontend = "frontend" in phase_lower or "ui" in phase_lower or "page" in phase_lower
        include_features = "feature" in phase_lower or "logic" in phase_lower
        
        arch = {}
        if include_backend or include_features:
            arch["backend"] = self.spec.architecture.backend.dict()
            if self.spec.architecture.backend.database:
                arch["database"] = self.spec.architecture.backend.database.dict()
            
        if include_frontend or include_features:
            arch["frontend"] = self.spec.architecture.frontend.dict()
            
        context["architecture"] = arch
        
        if include_features:
            context["requirements"] = self.spec.requirements.dict()
            
        return _clean(context)

def generate_prompts(spec: CanonicalProjectSpec) -> List[Dict[str, str]]:
    generator = PromptGenerator(spec)
    return generator.generate()
