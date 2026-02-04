"""
Final MVP Validation Script
Synthesizes end-to-end tests for Alchemy MVP completeness.
"""
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000/api/v1"

def validate_mvp():
    print("\n🧪 Alchemy MVP Validation Phase")
    print("=" * 60)
    
    # 1. Project Initialization
    print("1. Initializing Discovery...")
    res = requests.post(f"{BASE_URL}/projects/", json={"idea": "A personal finance tracker for freelancers"})
    if res.status_code != 200:
        print(f"❌ Error creating project: {res.status_code} - {res.text}")
        return
    project = res.json()["project"]
    project_id = project["id"]
    print(f"   ✓ Project '{project['title']}' created ({project_id}).")
    assert project["spec"]["project"]["purpose"] == "A personal finance tracker for freelancers"
    assert project["progress"] == 5

    # 2. Roadmap Progress & JSON Source of Truth
    print("\n2. Advancing Guided Roadmap...")
    # Answer first question (Archetype)
    q = project["currentQuestion"]
    res = requests.post(f"{BASE_URL}/projects/answer", json={
        "project_id": project_id,
        "question_id": q["id"],
        "answer_ids": ["web-app"]
    })
    project = res.json()["project"]
    print(f"   ✓ Answered: {q['id']} -> web-app")
    assert project["spec"]["architecture"]["archetype"] == "web-app"
    assert project["progress"] > 5

    # 3. Artifact Completeness
    print("\n3. Verifying Artifacts...")
    files = project["files"]
    file_types = [f["type"] for f in files]
    print(f"   Found files: {file_types}")
    
    assert "design" in file_types, "Missing Documentation"
    assert "context" in file_types, "Missing JSON Spec"
    assert "roadmap" in file_types, "Missing Roadmap"
    assert "prompts" in file_types, "Missing Prompt Sequence"
    
    # Check Roadmap Detail
    roadmap_file = next(f for f in files if f["type"] == "roadmap")
    assert "Phase 1: Project Foundation" in roadmap_file["content"]
    assert "- [ ] Setup" in roadmap_file["content"]
    print("   ✓ Roadmap artifact is structured with phases and tasks.")
    
    # Check JSON Authoratative State
    spec_file = next(f for f in files if f["type"] == "context")
    spec_json = json.loads(spec_file["content"])
    assert spec_json["project"]["name"] == project["title"]
    print("   ✓ JSON Spec is authoritative and matches live state.")

    # 4. Prompt List Validity
    print("\n4. Validating AI Prompt Sequence...")
    prompt_file = next(f for f in files if f["type"] == "prompts")
    prompt_content = prompt_file["content"]
    
    assert "# AI Implementation Prompt Sequence" in prompt_content
    assert "## Step 1:" in prompt_content
    assert "# Role: Expert Software Engineer" in prompt_content
    assert "## Project Context" in prompt_content
    assert "A personal finance tracker" in prompt_content
    print("   ✓ Prompt Sequence contains valid markdown steps.")
    print("   ✓ First prompt initialized with correct context and role.")

    # 5. Checkpoint Replay
    print("\n5. Verifying Checkpoint System...")
    checkpoints = project["checkpoints"]
    assert len(checkpoints) >= 2, "Checkpoints not captured automatically"
    print(f"   ✓ {len(checkpoints)} checkpoints recorded.")
    
    # 6. Final MVP Summary
    print("\n" + "=" * 60)
    print("🏆 Alchemy MVP Validation: SUCCESS")
    print("=" * 60)
    print("Project Identity: Verified")
    print("Guided discovery: Functional")
    print("Single Source of Truth: Absolute (JSON)")
    print("External ready: Prompts and Spec available for AI IDEs")

if __name__ == "__main__":
    try:
        validate_mvp()
    except Exception as e:
        print(f"\n❌ Validation ERROR: {e}")
        import traceback
        traceback.print_exc()
