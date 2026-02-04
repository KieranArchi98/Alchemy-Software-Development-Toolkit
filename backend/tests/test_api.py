"""
Simple test script to verify backend API endpoints
Run with: python -m backend.test_api
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    response = requests.get("http://localhost:8000/health")
    print(f"✓ Health check: {response.json()}")

def test_create_project():
    """Test project creation"""
    response = requests.post(
        f"{BASE_URL}/projects/",
        json={"idea": "A tool to help developers plan software projects"}
    )
    data = response.json()
    print(f"✓ Created project: {data['project']['id']}")
    print(f"  Title: {data['project']['title']}")
    print(f"  Progress: {data['project']['progress']}%")
    print(f"  Messages: {len(data['project']['messages'])}")
    print(f"  Checkpoints: {len(data['project']['checkpoints'])}")
    print(f"  Artifacts: {len(data['project']['files'])}")
    return data['project']['id']

def test_send_message(project_id: str):
    """Test sending a message"""
    response = requests.post(
        f"{BASE_URL}/projects/message",
        json={
            "project_id": project_id,
            "content": "I want to build a web application for solo developers",
            "mode": "guided"
        }
    )
    data = response.json()
    print(f"✓ Sent message, received AI response")
    print(f"  AI: {data['message']['content'][:80]}...")
    return data['project']

def test_select_option(project_id: str, message_id: str):
    """Test selecting an option"""
    response = requests.post(
        f"{BASE_URL}/projects/option",
        json={
            "project_id": project_id,
            "message_id": message_id,
            "option_id": "solopreneur"
        }
    )
    data = response.json()
    print(f"✓ Selected option")
    print(f"  App archetype: {data['project']['state']['app_archetype']}")
    print(f"  Checkpoints: {len(data['project']['checkpoints'])}")

def test_get_artifacts(project_id: str):
    """Test getting artifacts"""
    response = requests.get(f"{BASE_URL}/projects/{project_id}/artifacts")
    data = response.json()
    print(f"✓ Retrieved {len(data['files'])} artifacts:")
    for file in data['files']:
        print(f"  - {file['name']} ({file['type']})")

def test_get_checkpoints(project_id: str):
    """Test getting checkpoints"""
    response = requests.get(f"{BASE_URL}/projects/{project_id}/checkpoints")
    data = response.json()
    print(f"✓ Retrieved {len(data['checkpoints'])} checkpoints:")
    for cp in data['checkpoints']:
        print(f"  - {cp['label']} ({cp['timestamp']})")

if __name__ == "__main__":
    print("\n🧪 Testing Alchemy Backend API\n")
    print("=" * 50)
    
    try:
        # Test health
        test_health()
        print()
        
        # Test project creation
        project_id = test_create_project()
        print()
        
        # Test message sending
        project = test_send_message(project_id)
        message_id = project['messages'][0]['id']
        print()
        
        # Test option selection
        test_select_option(project_id, message_id)
        print()
        
        # Test artifacts
        test_get_artifacts(project_id)
        print()
        
        # Test checkpoints
        test_get_checkpoints(project_id)
        print()
        
        print("=" * 50)
        print("✅ All tests passed!\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
