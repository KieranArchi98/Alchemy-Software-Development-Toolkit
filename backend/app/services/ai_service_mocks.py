from app.services.question_engine import Question, Answer

def mock_web_app_question() -> Question:
    """Simulate a dynamic question for web apps"""
    return Question(
        id="Q_DYNAMIC_FALLBACK_1",
        order=100,
        category="refinement",
        question="Do you need a dashboard for data visualization?",
        description="Offline Analysis: Based on your project architecture, a dashboard might be useful.",
        fieldPath="architecture.frontend.components",
        answers=[
            Answer(
                id="dash-yes",
                label="Yes, comprehensive dashboard",
                description="Charts, graphs, and summary stats",
                value={
                    "id": "dashboard-component",
                    "name": "Dashboard",
                    "type": "feature",
                    "description": "Data visualization dashboard"
                },
                recommended=True
            ),
            Answer(
                id="dash-simple",
                label="Simple stats only",
                description="Basic counters and lists",
                value={
                    "id": "stats-component",
                    "name": "SimpleStats",
                    "type": "feature",
                    "description": "Basic statistics display"
                },
                recommended=False
            ),
            Answer(
                id="dash-no",
                label="No dashboard needed",
                description="Focus on lists and forms",
                value=None, 
                recommended=False
            )
        ],
        aiDefault="dash-yes",
        multiSelect=False
    )
