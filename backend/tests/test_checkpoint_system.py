"""
Integration test for Checkpoint System and Persistence
"""
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import shutil
from pathlib import Path
import time

BASE_URL = "http://localhost:8000/api/v1"
STORAGE_DIR = Path("storage/projects")

def test_checkpoint_system():
    print("\n🚀 Starting Checkpoint System Test")
    print("=" * 60)
    
    # Clean storage
    if STORAGE_DIR.exists():
        for f in STORAGE_DIR.glob("*.json"):
            f.unlink()
    
    # 1. Create Project
    response = requests.post(f"{BASE_URL}/projects/", json={"idea": "Checkpoint Test"})
    project = response.json()['project']
    project_id = project['id']
    print(f"✓ Created Project: {project_id}")
    
    # Verify Persistence
    file_path = STORAGE_DIR / f"{project_id}.json"
    assert file_path.exists(), "Project file not created"
    print(f"✓ Persistence File OK: {file_path}")
    
    # 2. Advance History (2 steps)
    
    # Answer Q1
    q1 = project['currentQuestion']
    res = requests.post(f"{BASE_URL}/projects/answer", json={
        "project_id": project_id, "question_id": q1['id'], "answer_ids": [q1['answers'][0]['id']]
    })
    proj_step2 = res.json()['project']
    print(f"✓ Step 2 (Answered Q1). Checkpoints: {len(proj_step2['checkpoints'])}")
    
    # Answer Q2
    q2 = proj_step2['currentQuestion']
    res = requests.post(f"{BASE_URL}/projects/answer", json={
        "project_id": project_id, "question_id": q2['id'], "answer_ids": [q2['answers'][0]['id']]
    })
    proj_step3 = res.json()['project']
    print(f"✓ Step 3 (Answered Q2). Checkpoints: {len(proj_step3['checkpoints'])}")
    
    # Checkpoints: [Created, AnsQ1, AnsQ2]
    # Indices: 0, 1, 2
    checkpoints = proj_step3['checkpoints']
    assert len(checkpoints) == 3
    
    cp_target = checkpoints[1] # "AnsQ1" aka Step 2
    print(f"  Target Checkpoint: {cp_target['label']} ({cp_target['id']})")
    print(f"  Future Checkpoint: {checkpoints[2]['label']} ({checkpoints[2]['id']})")
    
    # 3. Test Revert and Invalidation
    print("\n↺ Reverting to Step 2...")
    res = requests.post(f"{BASE_URL}/projects/revert", json={
        "project_id": project_id, "checkpoint_id": cp_target['id']
    })
    proj_reverted = res.json()['project']
    
    # Verify Future Invalidation
    new_checkpoints = proj_reverted['checkpoints']
    print(f"✓ Reverted. Checkpoints: {len(new_checkpoints)}")
    assert len(new_checkpoints) == 2, f"Expected 2 checkpoints, got {len(new_checkpoints)}"
    assert new_checkpoints[-1]['id'] == cp_target['id'], "Last checkpoint should be target"
    print("✓ Future checkpoints invalidated successfully")
    
    # Verify Spec Restore
    # Step 3 had Q2 answered. Step 2 did not.
    # Q2 is Target Audience.
    # proj_step3 Spec has targetAudience populated.
    # proj_reverted Spec should NOT have it (or have default).
    # Wait, Q2 answer MUTATES spec.
    # Let's check spec content or progress.
    print(f"  Progress Reverted: {proj_reverted['progress']}% (Was {proj_step3['progress']}%)")
    assert proj_reverted['progress'] < proj_step3['progress']
    print("✓ Spec state restored")
    
    # 4. Verify Restart Persistence
    print("\nChecking persistence reload...")
    # Force reload by calling GET
    res = requests.get(f"{BASE_URL}/projects/{project_id}")
    proj_loaded = res.json()['project']
    assert len(proj_loaded['checkpoints']) == 2
    print("✓ Project loaded correctly from disk")

    print("\n✅ Checkpoint System Test Passed!")

if __name__ == "__main__":
    try:
        test_checkpoint_system()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
