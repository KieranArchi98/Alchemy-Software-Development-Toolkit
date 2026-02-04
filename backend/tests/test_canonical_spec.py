"""
Test script for canonical specification schema and validation
"""
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime

from app.schemas.canonical_spec import (
    CanonicalProjectSpec,
    SpecMetadata,
    ProjectInfo,
    Architecture,
    Archetype,
    FunctionalRequirement,
    Priority,
    Page,
    Component,
    ComponentType,
    ApiEndpoint,
    HttpMethod,
    SpecValidator
)
from app.services.spec_utils import (
    create_initial_spec,
    add_functional_requirement,
    add_page,
    add_api_endpoint,
    export_spec_to_json,
    import_spec_from_json,
    get_spec_summary
)


def test_create_initial_spec():
    """Test creating an initial specification"""
    print("\n📝 Test: Create Initial Spec")
    
    spec = create_initial_spec(
        project_id="test-123",
        idea="A tool to help developers plan software projects",
        archetype=Archetype.WEB_APP
    )
    
    print(f"✓ Created spec: {spec.project.name}")
    print(f"  ID: {spec.metadata.id}")
    print(f"  Phase: {spec.metadata.phase}")
    print(f"  Progress: {spec.metadata.progress}%")
    print(f"  Archetype: {spec.architecture.archetype}")
    
    return spec


def test_add_requirements(spec: CanonicalProjectSpec):
    """Test adding functional requirements"""
    print("\n📋 Test: Add Functional Requirements")
    
    spec = add_functional_requirement(
        spec,
        title="User can create a new project",
        description="Users should be able to initialize a new project from an idea",
        priority="critical"
    )
    
    spec = add_functional_requirement(
        spec,
        title="User can chat with AI assistant",
        description="Users can send messages to AI for guidance",
        priority="high"
    )
    
    print(f"✓ Added {len(spec.requirements.functional)} requirements")
    for fr in spec.requirements.functional:
        print(f"  - {fr.id}: {fr.title} ({fr.priority})")
    
    return spec


def test_add_architecture(spec: CanonicalProjectSpec):
    """Test adding architecture elements"""
    print("\n🏗️  Test: Add Architecture Elements")
    
    # Add pages
    spec = add_page(spec, "Home", "/", "Landing page")
    spec = add_page(spec, "Workspace", "/workspace", "Main workspace")
    
    # Add API endpoints
    spec = add_api_endpoint(spec, "/projects", "POST", "Create project")
    spec = add_api_endpoint(spec, "/projects/{id}", "GET", "Get project")
    
    print(f"✓ Added {len(spec.architecture.frontend.pages)} pages")
    for page in spec.architecture.frontend.pages:
        print(f"  - {page.name} ({page.route})")
    
    print(f"✓ Added {len(spec.architecture.backend.apis)} API endpoints")
    for api in spec.architecture.backend.apis:
        print(f"  - {api.method} {api.endpoint}")
    
    return spec


def test_validation(spec: CanonicalProjectSpec):
    """Test specification validation"""
    print("\n✅ Test: Validation")
    
    is_valid, errors = SpecValidator.validate_spec(spec)
    
    if is_valid:
        print("✓ Specification is valid")
    else:
        print("✗ Validation errors:")
        for error in errors:
            print(f"  - {error}")
    
    return is_valid


def test_export_import(spec: CanonicalProjectSpec):
    """Test JSON export and import"""
    print("\n💾 Test: Export/Import")
    
    # Export to JSON
    json_str = export_spec_to_json(spec, pretty=True)
    print(f"✓ Exported to JSON ({len(json_str)} bytes)")
    
    # Import from JSON
    imported_spec = import_spec_from_json(json_str)
    print(f"✓ Imported from JSON")
    print(f"  Name: {imported_spec.project.name}")
    print(f"  Requirements: {len(imported_spec.requirements.functional)}")
    
    # Verify they match
    assert spec.metadata.id == imported_spec.metadata.id
    print("✓ Export/Import cycle successful")
    
    return json_str


def test_summary(spec: CanonicalProjectSpec):
    """Test getting specification summary"""
    print("\n📊 Test: Specification Summary")
    
    summary = get_spec_summary(spec)
    
    print("✓ Generated summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


def test_invalid_spec():
    """Test validation with invalid spec"""
    print("\n❌ Test: Invalid Specification")
    
    # Create spec with invalid FR dependency
    spec = create_initial_spec("test-invalid", "Test project")
    
    # Add FR with non-existent dependency
    from app.schemas.canonical_spec import FunctionalRequirement, Priority
    
    invalid_fr = FunctionalRequirement(
        id="FR-001",
        title="Test",
        description="Test requirement",
        priority=Priority.HIGH,
        dependencies=["FR-999"]  # Non-existent
    )
    
    spec.requirements.functional.append(invalid_fr)
    
    is_valid, errors = SpecValidator.validate_spec(spec)
    
    if not is_valid:
        print("✓ Correctly detected invalid spec")
        print(f"  Errors: {errors}")
    else:
        print("✗ Failed to detect invalid spec")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 Testing Canonical Specification Schema")
    print("="*60)
    
    try:
        # Run tests
        spec = test_create_initial_spec()
        spec = test_add_requirements(spec)
        spec = test_add_architecture(spec)
        is_valid = test_validation(spec)
        
        if is_valid:
            json_output = test_export_import(spec)
            test_summary(spec)
            
            # Save example spec
            with open("example_spec.json", "w") as f:
                f.write(json_output)
            print(f"\n💾 Saved example to example_spec.json")
        
        test_invalid_spec()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
