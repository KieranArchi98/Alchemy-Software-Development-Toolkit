"""
Test Prompt Generator
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from app.services.spec_utils import create_initial_spec
from app.services.roadmap_generator import generate_roadmap
from app.services.prompt_generator import generate_prompts
from app.schemas.canonical_spec import Database, DatabaseType

def test_prompt_generator():
    print("\n🚀 Starting Prompt Generator Test")
    print("=" * 60)
    
    # 1. Create a spec
    spec = create_initial_spec("test-prompts", "A Chat App")
    
    # 2. Set Architecture (Required for valid roadmap)
    spec.architecture.frontend.framework = "Next.js"
    spec.architecture.backend.framework = "FastAPI"
    spec.architecture.backend.database = Database(type=DatabaseType.NOSQL, technology="MongoDB")
    
    # 3. Generate Roadmap (Prerequisite)
    spec.implementation = generate_roadmap(spec)
    print(f"✓ Generated Roadmap with {len(spec.implementation.phases)} phases")
    
    # 4. Generate Prompts
    prompts = generate_prompts(spec)
    print(f"✓ Generated {len(prompts)} prompts")
    
    # 5. Verify Content
    assert len(prompts) == len(spec.implementation.phases)
    
    # Inspect Prompt 1 (Foundation)
    p1 = prompts[0]
    print(f"\n--- Prompt 1: {p1['phase_name']} ---")
    print(f"Step: {p1['step']}")
    
    content = p1['prompt']
    
    # Check Structure
    assert "# Role: Expert Software Engineer" in content
    assert "## Current Objective: Phase 1" in content
    assert "## Requirements Checklist" in content
    assert "- [ ] Setup Next.js" in content
    assert "## Project Context" in content
    
    # Check Context Isolation (Backend Arch should be present in Phase 2, maybe not Phase 3 if logic separates, but here likely present in many)
    # Check that Context IS valid JSON
    # Find JSON block
    start = content.find("```json")
    end = content.find("```", start + 7)
    json_str = content[start+7:end]
    context = json.loads(json_str)
    
    assert "project" in context
    assert "architecture" in context
    print("✓ Context JSON is valid")
    
    print("✅ Prompt Generator Test Passed!")

if __name__ == "__main__":
    try:
        test_prompt_generator()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
