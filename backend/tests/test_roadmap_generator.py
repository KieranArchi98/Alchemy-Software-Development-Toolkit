"""
Test Roadmap Generator
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from app.services.spec_utils import create_initial_spec
from app.services.roadmap_generator import generate_roadmap
from app.schemas.canonical_spec import BackendArchitecture, Database, DatabaseType

def test_roadmap_generator():
    print("\n🚀 Starting Roadmap Generator Test")
    print("=" * 60)
    
    # 1. Create a spec
    spec = create_initial_spec("test-roadmap", "A Todo App")
    
    # 2. Set Architecture (Mocking choices)
    spec.architecture.frontend.framework = "React"
    spec.architecture.backend.framework = "FastAPI"
    
    # Initialize Database object
    spec.architecture.backend.database = Database(
        type=DatabaseType.SQL,
        technology="PostgreSQL"
    )
    
    print("✓ Created Spec with Architecture")
    
    # 3. Generate Roadmap
    roadmap = generate_roadmap(spec)
    print(f"✓ Generated Roadmap with {len(roadmap.phases)} phases")
    
    # 4. Verify Content
    phase_names = [p.name for p in roadmap.phases]
    print(f"  Phases: {phase_names}")
    
    assert "Project Foundation" in phase_names
    assert "Backend Core" in phase_names
    assert "Frontend Skeleton" in phase_names
    
    # Verify specific tasks
    all_tasks = [t.title for p in roadmap.phases for t in p.tasks]
    
    assert "Setup React project structure" in all_tasks
    assert "Setup FastAPI project structure" in all_tasks
    assert "Initialize PostgreSQL and migration system" in all_tasks
    
    print("✅ Roadmap Generator Test Passed!")

if __name__ == "__main__":
    try:
        test_roadmap_generator()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
