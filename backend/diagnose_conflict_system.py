# backend/diagnose_conflict_system.py
"""
Diagnostic Script for Conflict Detection System
Identifies and fixes common issues
"""

import os
import sys
import importlib.util
from pathlib import Path

def diagnose_project_structure():
    """Check project structure and identify issues"""
    print("🔍 DIAGNOSING PROJECT STRUCTURE")
    print("=" * 50)
    
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if we're in the right place
    if not (current_dir / "app").exists():
        print("❌ Not in backend directory or app folder missing")
        print("💡 Make sure you're running from backend/ directory")
        return False
    
    print("✅ Found app directory")
    
    # Check required folders
    required_folders = ["api", "core", "models", "nlp", "schemas"]
    missing_folders = []
    
    for folder in required_folders:
        folder_path = current_dir / "app" / folder
        if folder_path.exists():
            print(f"✅ Found app/{folder}/")
        else:
            print(f"❌ Missing app/{folder}/")
            missing_folders.append(folder)
    
    # Check if services folder exists
    services_path = current_dir / "app" / "services"
    if services_path.exists():
        print("✅ Found app/services/")
    else:
        print("❌ Missing app/services/ - this is where conflict_detector.py should go")
        missing_folders.append("services")
    
    return len(missing_folders) == 0

def check_file_existence():
    """Check if required files exist"""
    print("\n🔍 CHECKING FILE EXISTENCE")
    print("=" * 50)
    
    current_dir = Path.cwd()
    
    # Files that should exist
    expected_files = {
        "app/main.py": "Main FastAPI application",
        "app/__init__.py": "App package init",
        "app/api/__init__.py": "API package init", 
        "app/models/__init__.py": "Models package init",
        "app/nlp/__init__.py": "NLP package init",
        "app/schemas/__init__.py": "Schemas package init",
        "app/nlp/user_behavior_analytics.py": "Day 1 analytics (needed for Day 2)"
    }
    
    missing_files = []
    
    for file_path, description in expected_files.items():
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description}")
            missing_files.append(file_path)
    
    # Check if conflict detection files exist (Day 2 files)
    day2_files = {
        "app/services/conflict_detector.py": "Main conflict detection service",
        "app/api/conflicts.py": "Conflict detection API endpoints",
        "app/schemas/conflicts.py": "Conflict detection schemas"
    }
    
    print(f"\n📋 Day 2 Files Status:")
    day2_missing = []
    
    for file_path, description in day2_files.items():
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description} (NEEDS TO BE CREATED)")
            day2_missing.append(file_path)
    
    return missing_files, day2_missing

def test_imports():
    """Test if critical imports work"""
    print("\n🔍 TESTING IMPORTS")
    print("=" * 50)
    
    # Add app to Python path
    current_dir = Path.cwd()
    app_path = str(current_dir / "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
        print(f"✅ Added {app_path} to Python path")
    
    import_tests = [
        ("app.config", "App configuration"),
        ("app.models", "Database models"),
        ("app.nlp.user_behavior_analytics", "Day 1 analytics (required for Day 2)"),
        ("app.services.conflict_detector", "Day 2 conflict detection"),
        ("app.api.conflicts", "Day 2 conflict API"),
    ]
    
    successful_imports = []
    failed_imports = []
    
    for module_name, description in import_tests:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - {description}")
            successful_imports.append(module_name)
        except ImportError as e:
            print(f"❌ {module_name} - {description}")
            print(f"   Error: {e}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"💥 {module_name} - {description}")
            print(f"   Unexpected error: {e}")
            failed_imports.append((module_name, str(e)))
    
    return successful_imports, failed_imports

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 CHECKING DEPENDENCIES")
    print("=" * 50)
    
    required_packages = [
        "fastapi",
        "sqlalchemy", 
        "pydantic",
        "datetime",
        "typing",
        "enum",
        "dataclasses",
        "unittest"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def generate_fix_script():
    """Generate a script to fix common issues"""
    print("\n🔧 GENERATING FIX SCRIPT")
    print("=" * 50)
    
    fix_script = """#!/bin/bash
# Auto-generated fix script for KairoCal conflict detection

echo "🔧 Fixing KairoCal project structure..."

# Ensure we're in the backend directory
if [ ! -d "app" ]; then
    echo "❌ Please run this from the backend/ directory"
    exit 1
fi

# Create missing directories
echo "📁 Creating missing directories..."
mkdir -p app/services
mkdir -p app/schemas

# Create missing __init__.py files
echo "📄 Creating missing __init__.py files..."
touch app/services/__init__.py
touch app/schemas/__init__.py

# Add basic content to services/__init__.py
cat > app/services/__init__.py << 'EOF'
# Services package
from .conflict_detector import SmartConflictDetector, ConflictAnalytics

__all__ = ["SmartConflictDetector", "ConflictAnalytics"]
EOF

echo "✅ Basic structure fixes complete!"
echo "📋 Next steps:"
echo "1. Place conflict_detector.py in app/services/"
echo "2. Place conflicts.py (API) in app/api/"
echo "3. Place conflicts.py (schemas) in app/schemas/"
echo "4. Run the diagnostic script again"
"""
    
    with open("fix_project_structure.sh", "w") as f:
        f.write(fix_script)
    
    print("✅ Created fix_project_structure.sh")
    print("🚀 Run: bash fix_project_structure.sh")

def provide_recommendations():
    """Provide specific recommendations based on diagnosis"""
    print("\n💡 RECOMMENDATIONS")
    print("=" * 50)
    
    # Get current directory info
    current_dir = Path.cwd()
    
    print("🎯 IMMEDIATE ACTIONS NEEDED:")
    print()
    
    # Check if services folder exists
    services_path = current_dir / "app" / "services"
    if not services_path.exists():
        print("1. CREATE SERVICES FOLDER:")
        print("   mkdir -p app/services")
        print("   touch app/services/__init__.py")
        print()
    
    # Check if files need to be placed
    conflict_detector_path = current_dir / "app" / "services" / "conflict_detector.py"
    if not conflict_detector_path.exists():
        print("2. PLACE CONFLICT DETECTOR FILE:")
        print("   📁 Copy conflict_detector.py to: app/services/conflict_detector.py")
        print()
    
    api_conflicts_path = current_dir / "app" / "api" / "conflicts.py"
    if not api_conflicts_path.exists():
        print("3. PLACE API ENDPOINTS FILE:")
        print("   📁 Copy conflicts.py (API) to: app/api/conflicts.py")
        print()
    
    schema_conflicts_path = current_dir / "app" / "schemas" / "conflicts.py"
    if not schema_conflicts_path.exists():
        print("4. PLACE SCHEMAS FILE:")
        print("   📁 Copy conflicts.py (schemas) to: app/schemas/conflicts.py")
        print()
    
    print("5. UPDATE IMPORTS:")
    print("   📝 Make sure all import statements use correct paths")
    print()
    
    print("6. TEST AGAIN:")
    print("   🧪 python test_conflict_detection_fixed.py")
    print()
    
    print("🚀 QUICK FIX COMMAND:")
    print("bash fix_project_structure.sh  # Run the generated fix script")

def main():
    """Run complete diagnosis"""
    print("🩺 KAIROCAL CONFLICT DETECTION DIAGNOSTIC")
    print("=" * 60)
    
    # Step 1: Check structure
    structure_ok = diagnose_project_structure()
    
    # Step 2: Check files
    missing_files, day2_missing = check_file_existence()
    
    # Step 3: Test imports
    successful_imports, failed_imports = test_imports()
    
    # Step 4: Check dependencies
    missing_packages = check_dependencies()
    
    # Step 5: Generate fixes
    generate_fix_script()
    
    # Step 6: Provide recommendations
    provide_recommendations()
    
    # Summary
    print("\n📊 DIAGNOSIS SUMMARY")
    print("=" * 60)
    print(f"Project Structure: {'✅ OK' if structure_ok else '❌ Issues found'}")
    print(f"Missing Core Files: {len(missing_files)}")
    print(f"Missing Day 2 Files: {len(day2_missing)}")
    print(f"Failed Imports: {len(failed_imports)}")
    print(f"Missing Packages: {len(missing_packages)}")
    
    if structure_ok and len(missing_files) == 0 and len(failed_imports) == 0:
        print("\n🎉 SYSTEM LOOKS GOOD!")
        print("✅ Ready to run conflict detection tests")
    elif len(day2_missing) == len(failed_imports):
        print("\n🔧 FIXABLE ISSUES")
        print("✅ Just need to place the Day 2 files in correct locations")
    else:
        print("\n⚠️ ISSUES NEED ATTENTION")
        print("🔧 Follow the recommendations above")
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Run: bash fix_project_structure.sh")
    print("2. Place the Day 2 files in correct locations")
    print("3. Run: python test_conflict_detection_fixed.py")
    print("4. Then run: python test_conflict_detection.py")

if __name__ == "__main__":
    main()