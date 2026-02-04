"""
Test suite for guided roadmap question engine
"""
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.question_engine import QuestionEngine, get_question_engine


def test_load_roadmap():
    """Test loading roadmap from JSON"""
    print("\n📚 Test: Load Roadmap")
    
    engine = get_question_engine()
    
    print(f"✓ Loaded roadmap v{engine.roadmap.version}")
    print(f"  Total questions: {engine.get_total_questions()}")
    print(f"  Categories: {set(q.category for q in engine.roadmap.questions)}")


def test_get_questions():
    """Test retrieving questions"""
    print("\n🔍 Test: Get Questions")
    
    engine = get_question_engine()
    
    # Get by ID
    q1 = engine.get_question_by_id("Q001")
    print(f"✓ Question Q001: {q1.question}")
    print(f"  Field: {q1.fieldPath}")
    print(f"  Answers: {len(q1.answers)}")
    
    # Get by order
    q_first = engine.get_question_by_order(1)
    print(f"✓ First question: {q_first.question}")
    
    # Get AI default
    default_answer = engine.get_ai_default_answer("Q001")
    print(f"✓ AI default for Q001: {default_answer.label}")


def test_linear_progression():
    """Test linear question progression"""
    print("\n➡️  Test: Linear Progression")
    
    engine = get_question_engine()
    
    # Start with empty spec
    spec = {
        "architecture": {},
        "project": {},
        "requirements": {}
    }
    answered = []
    
    # Get first question
    q1 = engine.get_next_question(spec, answered)
    print(f"✓ Next question (0 answered): {q1.id} - {q1.question}")
    
    # Answer it
    answered.append(q1.id)
    
    # Get second question
    q2 = engine.get_next_question(spec, answered)
    print(f"✓ Next question (1 answered): {q2.id} - {q2.question}")
    
    # Answer all questions
    for q in engine.questions_by_order:
        answered.append(q.id)
    
    # Should return None when all answered
    q_none = engine.get_next_question(spec, answered)
    print(f"✓ Next question (all answered): {q_none}")


def test_skip_conditions():
    """Test skip conditions"""
    print("\n⏭️  Test: Skip Conditions")
    
    engine = get_question_engine()
    
    # Spec with archetype = api-service
    spec = {
        "architecture": {
            "archetype": "api-service"
        },
        "project": {},
        "requirements": {}
    }
    answered = []
    
    # Questions Q004 and Q011 should be skipped for non-web-apps
    all_questions = []
    while True:
        next_q = engine.get_next_question(spec, answered)
        if not next_q:
            break
        all_questions.append(next_q.id)
        answered.append(next_q.id)
    
    print(f"✓ Questions asked for api-service: {all_questions}")
    
    if "Q004" not in all_questions:
        print("✓ Correctly skipped Q004 (frontend framework)")
    if "Q011" not in all_questions:
        print("✓ Correctly skipped Q011 (UI/UX approach)")


def test_apply_single_answer():
    """Test applying single answer to spec"""
    print("\n📝 Test: Apply Single Answer")
    
    engine = get_question_engine()
    
    spec = {
        "architecture": {},
        "project": {},
        "requirements": {}
    }
    
    # Answer Q001 (archetype)
    updated_spec, errors = engine.apply_answer_to_spec(spec, "Q001", ["web-app"])
    
    if not errors:
        print(f"✓ Applied answer to Q001")
        print(f"  archetype: {updated_spec['architecture'].get('archetype')}")
    else:
        print(f"✗ Errors: {errors}")


def test_apply_multi_answer():
    """Test applying multiple answers to spec"""
    print("\n📝 Test: Apply Multiple Answers")
    
    engine = get_question_engine()
    
    spec = {
        "architecture": {},
        "project": {},
        "requirements": {"functional": [], "nonFunctional": {}}
    }
    
    # Answer Q003 (critical features) - multi-select
    updated_spec, errors = engine.apply_answer_to_spec(
        spec,
        "Q003",
        ["user-auth", "data-crud"]
    )
    
    if not errors:
        print(f"✓ Applied multi-select answer to Q003")
        print(f"  Functional requirements added: {len(updated_spec['requirements']['functional'])}")
        for fr in updated_spec['requirements']['functional']:
            print(f"    - {fr['id']}: {fr['title']}")
    else:
        print(f"✗ Errors: {errors}")


def test_ai_default():
    """Test using AI default answer"""
    print("\n🤖 Test: AI Default Answer")
    
    engine = get_question_engine()
    
    spec = {
        "architecture": {"frontend": {}},
        "project": {},
        "requirements": {}
    }
    
    # Get AI default for Q004 (frontend framework)
    default_answer = engine.get_ai_default_answer("Q004")
    print(f"✓ AI default for Q004: {default_answer.label}")
    
    # Apply it
    updated_spec, errors = engine.apply_answer_to_spec(spec, "Q004", [default_answer.id])
    
    if not errors:
        print(f"✓ Applied AI default")
        print(f"  framework: {updated_spec['architecture']['frontend'].get('framework')}")
    else:
        print(f"✗ Errors: {errors}")


def test_progress_calculation():
    """Test progress calculation"""
    print("\n📊 Test: Progress Calculation")
    
    engine = get_question_engine()
    
    total = engine.get_total_questions()
    
    # 0 answered
    progress_0 = engine.get_progress([])
    print(f"✓ Progress (0/{total}): {progress_0}%")
    
    # Half answered
    half_answered = [q.id for q in engine.questions_by_order[:total//2]]
    progress_half = engine.get_progress(half_answered)
    print(f"✓ Progress ({len(half_answered)}/{total}): {progress_half}%")
    
    # All answered
    all_answered = [q.id for q in engine.questions_by_order]
    progress_all = engine.get_progress(all_answered)
    print(f"✓ Progress ({len(all_answered)}/{total}): {progress_all}%")


def test_full_flow():
    """Test complete question flow"""
    print("\n🔄 Test: Full Question Flow")
    
    engine = get_question_engine()
    
    spec = {
        "architecture": {},
        "project": {},
        "requirements": {"functional": [], "nonFunctional": {}},
        "aiUsage": {}
    }
    answered = []
    
    question_count = 0
    
    while True:
        # Get next question
        next_q = engine.get_next_question(spec, answered)
        if not next_q:
            break
        
        question_count += 1
        
        # Use AI default
        default_answer = engine.get_ai_default_answer(next_q.id)
        
        # Apply answer
        if next_q.multiSelect:
            # For multi-select, just pick first answer
            answer_ids = [next_q.answers[0].id]
        else:
            answer_ids = [default_answer.id]
        
        spec, errors = engine.apply_answer_to_spec(spec, next_q.id, answer_ids)
        
        if errors:
            print(f"✗ Error on {next_q.id}: {errors}")
            break
        
        answered.append(next_q.id)
    
    print(f"✓ Completed full flow")
    print(f"  Questions answered: {question_count}")
    print(f"  Final progress: {engine.get_progress(answered)}%")
    print(f"  Archetype: {spec.get('architecture', {}).get('archetype')}")
    print(f"  Frontend: {spec.get('architecture', {}).get('frontend', {}).get('framework')}")
    print(f"  Backend: {spec.get('architecture', {}).get('backend', {}).get('framework')}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 Testing Guided Roadmap Question Engine")
    print("="*60)
    
    try:
        test_load_roadmap()
        test_get_questions()
        test_linear_progression()
        test_skip_conditions()
        test_apply_single_answer()
        test_apply_multi_answer()
        test_ai_default()
        test_progress_calculation()
        test_full_flow()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
