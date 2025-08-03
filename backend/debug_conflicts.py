# backend/debug_conflicts.py
"""
Detailed debugging script to identify exact issues
"""

import sys
import os
from datetime import datetime, timedelta

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def debug_step_by_step():
    """Debug each component step by step"""
    print("🔍 STEP-BY-STEP DEBUGGING")
    print("=" * 50)
    
    # Step 1: Test basic imports
    print("Step 1: Testing basic imports...")
    try:
        print("  Importing enum...")
        from enum import Enum
        print("  ✅ enum imported")
        
        print("  Importing dataclasses...")
        from dataclasses import dataclass
        print("  ✅ dataclasses imported")
        
        print("  Importing datetime...")
        from datetime import datetime, timedelta
        print("  ✅ datetime imported")
        
        print("  Importing typing...")
        from typing import List, Optional, Dict, Any
        print("  ✅ typing imported")
        
    except Exception as e:
        print(f"  ❌ Basic import failed: {e}")
        return False
    
    # Step 2: Test app imports
    print("\nStep 2: Testing app imports...")
    try:
        print("  Importing app.models.event...")
        from app.models.event import Event
        print("  ✅ Event model imported")
        
        print("  Importing app.models.user...")
        from app.models.user import User  
        print("  ✅ User model imported")
        
    except Exception as e:
        print(f"  ❌ App model import failed: {e}")
        print(f"  💡 Error details: {type(e).__name__}: {e}")
        return False
    
    # Step 3: Test Day 1 analytics import
    print("\nStep 3: Testing Day 1 analytics import...")
    try:
        print("  Importing UserBehaviorAnalyzer...")
        from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
        print("  ✅ UserBehaviorAnalyzer imported")
        
        print("  Importing TimeSlotSuggestion...")
        from app.nlp.user_behavior_analytics import TimeSlotSuggestion
        print("  ✅ TimeSlotSuggestion imported")
        
        print("  Importing UserPattern...")
        from app.nlp.user_behavior_analytics import UserPattern
        print("  ✅ UserPattern imported")
        
    except Exception as e:
        print(f"  ❌ Day 1 analytics import failed: {e}")
        print(f"  💡 Error details: {type(e).__name__}: {e}")
        print("  🔧 This might be the main issue - Day 1 analytics missing")
        return False
    
    # Step 4: Test conflict detector import
    print("\nStep 4: Testing conflict detector import...")
    try:
        print("  Importing SmartConflictDetector...")
        from app.services.conflict_detector import SmartConflictDetector
        print("  ✅ SmartConflictDetector imported")
        
        print("  Importing ConflictType...")
        from app.services.conflict_detector import ConflictType
        print("  ✅ ConflictType imported")
        
        print("  Importing ConflictDetection...")
        from app.services.conflict_detector import ConflictDetection
        print("  ✅ ConflictDetection imported")
        
    except Exception as e:
        print(f"  ❌ Conflict detector import failed: {e}")
        print(f"  💡 Error details: {type(e).__name__}: {e}")
        return False
    
    # Step 5: Test creating instances
    print("\nStep 5: Testing instance creation...")
    try:
        from unittest.mock import Mock
        
        print("  Creating mock database...")
        mock_db = Mock()
        print("  ✅ Mock database created")
        
        print("  Creating SmartConflictDetector...")
        detector = SmartConflictDetector(mock_db)
        print("  ✅ SmartConflictDetector instance created")
        print(f"  📊 Default buffer minutes: {detector.default_buffer_minutes}")
        
    except Exception as e:
        print(f"  ❌ Instance creation failed: {e}")
        print(f"  💡 Error details: {type(e).__name__}: {e}")
        return False
    
    # Step 6: Test basic methods
    print("\nStep 6: Testing basic methods...")
    try:
        print("  Testing _infer_event_priority...")
        priority = detector._infer_event_priority({"title": "Test Meeting"})
        print(f"  ✅ Priority inference works: {priority}")
        
        print("  Testing _locations_conflict...")
        conflict = detector._locations_conflict("Room A", "Room A")
        print(f"  ✅ Location conflict detection works: {conflict}")
        
        print("  Testing _calculate_overlap_severity...")
        start1 = datetime(2025, 7, 29, 10, 0)
        end1 = datetime(2025, 7, 29, 11, 0)
        start2 = datetime(2025, 7, 29, 10, 30)
        end2 = datetime(2025, 7, 29, 11, 30)
        
        severity = detector._calculate_overlap_severity(start2, end2, start1, end1)
        print(f"  ✅ Severity calculation works: {severity}")
        
    except Exception as e:
        print(f"  ❌ Method testing failed: {e}")
        print(f"  💡 Error details: {type(e).__name__}: {e}")
        import traceback
        print("  📋 Full traceback:")
        traceback.print_exc()
        return False
    
    print("\n🎉 ALL DEBUGGING STEPS PASSED!")
    return True

def test_with_minimal_dependencies():
    """Test with minimal dependencies to isolate issues"""
    print("\n🔧 TESTING WITH MINIMAL DEPENDENCIES")
    print("=" * 50)
    
    try:
        # Skip the UserBehaviorAnalyzer import and create a mock
        print("Creating minimal mock implementations...")
        
        from enum import Enum
        from dataclasses import dataclass
        from typing import List, Dict, Any
        from datetime import datetime
        from unittest.mock import Mock
        
        # Mock the analytics classes if they're causing issues
        class MockUserPattern:
            def __init__(self):
                self.preferred_hours = [9, 10, 14, 15]
                self.preferred_days = [1, 2, 3, 4]
        
        class MockTimeSlotSuggestion:
            def __init__(self, start_time, end_time, confidence=0.8, reasoning="Mock suggestion"):
                self.start_time = start_time
                self.end_time = end_time
                self.confidence = confidence
                self.reasoning = reasoning
            
            def to_dict(self):
                return {
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                    "confidence": self.confidence,
                    "reasoning": self.reasoning
                }
        
        class MockUserBehaviorAnalyzer:
            def analyze_user_patterns(self, events):
                return MockUserPattern()
            
            def suggest_optimal_times(self, duration_minutes, event_type, user_patterns, avoid_conflicts=True, reference_date=None):
                base_time = datetime(2025, 7, 29, 14, 0)
                return [
                    MockTimeSlotSuggestion(base_time, base_time + timedelta(minutes=duration_minutes)),
                    MockTimeSlotSuggestion(base_time + timedelta(hours=2), base_time + timedelta(hours=2, minutes=duration_minutes//60))
                ]
        
        print("✅ Mock implementations created")
        
        # Now try to import and modify the conflict detector
        print("Importing conflict detector with mocked dependencies...")
        
        # Temporarily replace the import
        import sys
        
        # Create a mock module for the analytics
        mock_analytics_module = Mock()
        mock_analytics_module.UserBehaviorAnalyzer = MockUserBehaviorAnalyzer
        mock_analytics_module.TimeSlotSuggestion = MockTimeSlotSuggestion  
        mock_analytics_module.UserPattern = MockUserPattern
        
        sys.modules['app.nlp.user_behavior_analytics'] = mock_analytics_module
        
        # Now try importing the conflict detector
        from app.services.conflict_detector import SmartConflictDetector, ConflictType, ConflictSeverity
        print("✅ Conflict detector imported with mocked analytics")
        
        # Test basic functionality
        mock_db = Mock()
        detector = SmartConflictDetector(mock_db)
        
        # Test priority inference
        priority = detector._infer_event_priority({"title": "URGENT Meeting"})
        print(f"✅ Priority inference: {priority}")
        
        # Test severity calculation
        severity = detector._calculate_overlap_severity(
            datetime(2025, 7, 29, 10, 30),
            datetime(2025, 7, 29, 11, 30),
            datetime(2025, 7, 29, 10, 0),
            datetime(2025, 7, 29, 11, 0)
        )
        print(f"✅ Severity calculation: {severity}")
        
        print("\n🎉 MINIMAL DEPENDENCY TEST PASSED!")
        print("💡 The issue is likely with Day 1 analytics import")
        return True
        
    except Exception as e:
        print(f"❌ Minimal dependency test failed: {e}")
        import traceback
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

def check_day1_analytics():
    """Specifically check Day 1 analytics availability"""
    print("\n🔍 CHECKING DAY 1 ANALYTICS")
    print("=" * 50)
    
    try:
        print("Checking if user_behavior_analytics.py exists...")
        analytics_path = os.path.join(os.path.dirname(__file__), 'app', 'nlp', 'user_behavior_analytics.py')
        
        if os.path.exists(analytics_path):
            print(f"✅ Found: {analytics_path}")
            
            # Check file size
            size = os.path.getsize(analytics_path)
            print(f"📊 File size: {size} bytes")
            
            if size > 1000:  # Should be a substantial file
                print("✅ File appears to have substantial content")
            else:
                print("⚠️ File seems very small - might be empty or incomplete")
                
            # Try to read first few lines
            print("\n📄 First 10 lines of the file:")
            with open(analytics_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        break
                    print(f"  {i+1}: {line.rstrip()}")
                    
        else:
            print(f"❌ File not found: {analytics_path}")
            print("💡 This is the main issue - Day 1 analytics file is missing")
            return False
            
        # Try importing specific classes
        print("\n🔍 Testing specific class imports...")
        try:
            from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
            print("✅ UserBehaviorAnalyzer imported successfully")
        except ImportError as e:
            print(f"❌ UserBehaviorAnalyzer import failed: {e}")
            return False
            
        try:
            from app.nlp.user_behavior_analytics import TimeSlotSuggestion
            print("✅ TimeSlotSuggestion imported successfully")
        except ImportError as e:
            print(f"❌ TimeSlotSuggestion import failed: {e}")
            return False
            
        try:
            from app.nlp.user_behavior_analytics import UserPattern
            print("✅ UserPattern imported successfully")
        except ImportError as e:
            print(f"❌ UserPattern import failed: {e}")
            return False
            
        print("\n✅ Day 1 analytics appears to be working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Day 1 analytics check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debugging steps"""
    print("🐛 DETAILED CONFLICT DETECTION DEBUGGING")
    print("=" * 60)
    
    # Step-by-step debugging
    step_by_step_ok = debug_step_by_step()
    
    if not step_by_step_ok:
        print("\n🔧 Trying with minimal dependencies...")
        minimal_ok = test_with_minimal_dependencies()
        
        print("\n🔍 Checking Day 1 analytics specifically...")
        day1_ok = check_day1_analytics()
        
        print("\n📊 DEBUGGING SUMMARY")
        print("=" * 40)
        print(f"Step-by-step test: {'✅' if step_by_step_ok else '❌'}")
        print(f"Minimal dependencies: {'✅' if minimal_ok else '❌'}")
        print(f"Day 1 analytics: {'✅' if day1_ok else '❌'}")
        
        if minimal_ok and not day1_ok:
            print("\n💡 DIAGNOSIS: Day 1 analytics is the issue")
            print("🔧 SOLUTIONS:")
            print("1. Create a minimal user_behavior_analytics.py file")
            print("2. Or modify conflict_detector.py to work without Day 1")
            print("3. For now, the conflict detection logic itself works!")
        elif not minimal_ok:
            print("\n💡 DIAGNOSIS: Deeper import issues")
            print("🔧 Check Python path and module structure")
    else:
        print("\n🎉 ALL DEBUGGING PASSED!")
        print("✅ Conflict detection system is fully functional")

if __name__ == "__main__":
    main()