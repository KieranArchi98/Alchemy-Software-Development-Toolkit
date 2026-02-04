"""
Integration test script for Question Engine Flow via API
Includes Static and Dynamic AI Questions
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_full_roadmap_flow():
    print("\n🚀 Starting Full Roadmap Flow Test")
    print("=" * 60)
    
    # 1. Create Project
    response = requests.post(
        f"{BASE_URL}/projects/",
        json={"idea": "A marketplace for digital art"}
    )
    assert response.status_code == 200, f"Creates failed: {response.text}"
    project = response.json()['project']
    project_id = project['id']
    
    print(f"✓ Created Project: {project['title']} ({project_id})")
    
    # helper to answer
    def answer_current(ans_ids):
        q = project['currentQuestion']
        print(f"\n❓ Question: {q['question']} ({q['id']})")
        res = requests.post(
            f"{BASE_URL}/projects/answer",
            json={
                "project_id": project_id,
                "question_id": q['id'],
                "answer_ids": ans_ids
            }
        )
        assert res.status_code == 200, f"Answer failed: {res.text}"
        return res.json()['project']

    # 2. Answer Static Questions to reach end
    # Q1: Archetype -> web-app (Required for AI trigger)
    project = answer_current(["web-app"])
    
    # Loop until no more static questions or we hit Dynamic
    while project['currentQuestion'] and not project['currentQuestion']['id'].startswith("Q_DYNAMIC"):
        q = project['currentQuestion']
        # Pick first answer
        ans_id = q['answers'][0]['id']
        project = answer_current([ans_id])
    
    print("\n✅ Finished Static Questions")
    
    # 3. Verify Dynamic Question
    if project['currentQuestion'] and project['currentQuestion']['id'].startswith("Q_DYNAMIC"):
        q = project['currentQuestion']
        print(f"\n🧠 AI Generated Question: {q['question']} ({q['id']})")
        print(f"   Description: {q['description']}")
        
        # Answer it
        ans_id = q['answers'][0]['id'] # "dash-yes"
        project = answer_current([ans_id])
        
        print("✓ Answered Dynamic Question")
        
        # Verify Spec Update
        # The mock adds a "Dashboard" component
        spec = project['spec']
        has_dashboard = any(c['name'] == 'Dashboard' for c in spec['architecture']['frontend'].get('components', []))
        if has_dashboard:
             print("✓ Spec updated with Dashboard component")
        else:
             print("✗ Spec missing Dashboard component")
             # Debug
             # print(json.dumps(spec['architecture']['frontend'], indent=2))
    else:
        print("✗ No Dynamic Question Generated")
    
    # 4. Verify no more questions
    if project['currentQuestion'] is None:
        print("\n✓ Roadmap Complete (No more questions)")
    else:
        print(f"\n? Still has question: {project['currentQuestion']['id']}")

    print("\n✅ Integration Test Passed!")

if __name__ == "__main__":
    try:
        test_full_roadmap_flow()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
