#!/usr/bin/env python3
"""
Basic test to verify the library works.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from simple_mongo_2 import SimpleMongo

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    
    from simple_mongo_2 import (
        AggregationPipeline,
        AggregationStage,
        AggregationFactory,
        PipelineBuilder
    )
    
    print("✓ All imports successful")
    print(f"  - SimpleMongo: {SimpleMongo}")
    print(f"  - AggregationPipeline: {AggregationPipeline}")
    print(f"  - AggregationStage: {AggregationStage}")
    print(f"  - AggregationFactory: {AggregationFactory}")
    print(f"  - PipelineBuilder: {PipelineBuilder}")
    
    return True

def test_client_creation():
    """Test client creation and basic methods."""
    print("\nTesting client creation...")
    
    try:
        # Create client with default settings
        client = SimpleMongo()
        
        # Test that we can access attributes
        print("✓ Client created successfully")
        
        # Test context manager
        with SimpleMongo() as ctx_client:
            print("✓ Context manager works")
        
        return True
    except Exception as e:
        print(f"✗ Client creation failed: {e}")
        return False

def test_documentation_files():
    """Verify that documentation files exist."""
    print("\nTesting documentation files...")
    
    files_to_check = [
        "README.md",
        "CHANGELOG.md",
        "docs/API_REFERENCE.md",
        "examples/basic_usage.py",
        "examples/advanced_aggregation.py",
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_pyproject_config():
    """Verify pyproject.toml configuration."""
    print("\nTesting pyproject.toml configuration...")
    
    import tomllib
    
    try:
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
        
        project = config.get("project", {})
        
        checks = [
            ("name", "simple-mongo-2"),
            ("version", "1.0.0"),
            ("requires-python", ">=3.14"),
        ]
        
        all_good = True
        for key, expected in checks:
            actual = project.get(key)
            if actual == expected:
                print(f"✓ {key}: {actual}")
            else:
                print(f"✗ {key}: expected {expected}, got {actual}")
                all_good = False
        
        # Check dependencies
        deps = project.get("dependencies", [])
        required_deps = ["dotenv>=0.9.9", "pymongo>=4.18.2"]
        
        for dep in required_deps:
            if any(dep in d for d in deps):
                print(f"✓ Dependency: {dep}")
            else:
                print(f"✗ Missing dependency: {dep}")
                all_good = False
        
        return all_good
    except Exception as e:
        print(f"✗ Failed to read pyproject.toml: {e}")
        return False

def main():
    """Run all tests."""
    print("Running simple-mongo-2 library tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_client_creation,
        test_documentation_files,
        test_pyproject_config,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"Test results: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())