"""
Integration test for Chat Intents and Mode constraints
"""
import json
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000/api/v1"

def test_chat_intents():
    print("\n🚀 Starting Chat Intent Test")
    print("=" * 60)
    
    # 1. Create Project
    response = requests.post(f"{BASE_URL}/projects/", json={"idea": "Chat Test App"})
    project_id = response.json()['project']['id']
    print(f"✓ Created Project: {project_id}")
    
    def send_msg(content, mode):
        res = requests.post(
            f"{BASE_URL}/projects/message",
            json={"project_id": project_id, "content": content, "mode": mode}
        )
        data = res.json()
        return data['message']['content'], data['project']

    # 2. Test Research Mode (Info)
    print("\n📚 Test: Research Query")
    reply, _ = send_msg("What is the best database?", "research")
    print(f"User: What is the best database?")
    print(f"AI: {reply}")
    assert "analyzed your request" in reply
    
    # 3. Test Mutation in Research Mode (Should Fail)
    print("\n🛡️ Test: Mutation in Research Mode")
    reply, proj = send_msg("Change styling to Tailwind", "research")
    print(f"User: Change styling to Tailwind (Mode: Research)")
    print(f"AI: {reply}")
    assert "Switch to Update Mode" in reply
    assert proj['spec']['architecture']['frontend']['styling'] != "Tailwind CSS"
    print("✓ Mutation correctly blocked")
    
    # 4. Test Design Decision (Allowed in Update/Guided)
    print("\n✅ Test: Design Decision (Update Mode)")
    reply, proj = send_msg("I want to use Tailwind CSS", "update")
    print(f"User: I want to use Tailwind CSS (Mode: Update)")
    print(f"AI: {reply}")
    
    current_style = proj['spec']['architecture']['frontend']['styling']
    print(f"Styling in Spec: {current_style}")
    assert current_style == "Tailwind CSS"
    print("✓ Spec updated successfully")
    
    # 5. Checkpoint Created?
    cps = proj['checkpoints']
    last_cp = cps[-1]
    print(f"\n✓ Checkpoint created: {last_cp['label']}")
    assert "design_decision" in last_cp['label']

    print("\n✅ Chat Intent Test Passed!")

if __name__ == "__main__":
    try:
        test_chat_intents()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
