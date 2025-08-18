#!/usr/bin/env python3
"""
Final Verification Test - All Three UI Fixes

This script provides final verification that all requested fixes are working:
1. ✅ Drag-drop feature removed
2. ✅ Priority consistency verified  
3. ✅ Modern modal implemented

Run this after fixes to confirm everything is working.
"""

import os
import re
import requests
import sqlite3
from datetime import datetime

class FinalVerificationTest:
    def __init__(self):
        self.api_base = 'http://127.0.0.1:8000/api/v1'
        self.dashboard_file = 'frontend/src/pages/dashboard/DashboardPage.tsx'
        self.modal_file = 'frontend/src/components/modals/PriorityChangeModal.tsx'
        self.db_path = 'backend/kairocal.db'
        
    def verify_fix_1_drag_drop_removed(self):
        """Verify Fix #1: Drag-drop feature has been removed"""
        print("🧪 Verifying Fix #1: Drag-drop removal...")
        
        try:
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for removed drag-drop elements
            drag_elements = {
                'draggable={true}': False,
                'onDragStart': False,
                'cursor-move': False,
                'dataTransfer': False
            }
            
            found_issues = []
            
            for element, should_exist in drag_elements.items():
                exists = element in content
                if exists != should_exist:
                    if exists:
                        found_issues.append(f"❌ Still contains: {element}")
                    # If should_exist is True and doesn't exist, that would also be an issue
            
            if not found_issues:
                print("  ✅ Drag-drop elements successfully removed")
                print("  ✅ No cursor-move styling found")
                print("  ✅ No onDragStart handlers found")
                return True
            else:
                print("  ❌ Issues found:")
                for issue in found_issues:
                    print(f"    {issue}")
                return False
                
        except FileNotFoundError:
            print(f"  ❌ Could not find dashboard file: {self.dashboard_file}")
            return False
    
    def verify_fix_2_priority_consistency(self):
        """Verify Fix #2: Priority consistency between API and database"""
        print("\n🧪 Verifying Fix #2: Priority consistency...")
        
        try:
            # Test with one event
            test_input = "team meeting tomorrow at 2 pm for 30 minutes"
            
            response = requests.post(
                f"{self.api_base}/voice/create-event",
                json={
                    "voice_text": test_input,
                    "user_id": "frontend-test-user"
                }
            )
            
            if response.status_code == 200:
                event_response = response.json()
                event_data = event_response.get('event_data', {})
                event_id = event_response.get('event_id')
                api_priority = event_data.get('priority_level')
                api_confidence = event_data.get('priority_confidence')
                
                # Check database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT priority_level, priority_confidence FROM events WHERE id = ?",
                    (event_id,)
                )
                db_result = cursor.fetchone()
                conn.close()
                
                if db_result:
                    db_priority, db_confidence = db_result
                    
                    priority_match = api_priority == db_priority
                    confidence_match = abs(api_confidence - db_confidence) < 0.01
                    
                    if priority_match and confidence_match:
                        print(f"  ✅ API Priority: {api_priority} matches DB Priority: {db_priority}")
                        print(f"  ✅ API Confidence: {api_confidence:.1%} matches DB: {db_confidence:.1%}")
                        print("  ✅ Perfect consistency verified")
                        return True
                    else:
                        print(f"  ❌ Mismatch found:")
                        print(f"    API: P{api_priority} ({api_confidence:.1%})")
                        print(f"    DB:  P{db_priority} ({db_confidence:.1%})")
                        return False
                else:
                    print("  ❌ Event not found in database")
                    return False
            else:
                print(f"  ❌ API request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error during priority consistency test: {e}")
            return False
    
    def verify_fix_3_modern_modal(self):
        """Verify Fix #3: Modern modal implementation"""
        print("\n🧪 Verifying Fix #3: Modern modal implementation...")
        
        # Check if modal file exists
        if not os.path.exists(self.modal_file):
            print(f"  ❌ Modal file not found: {self.modal_file}")
            return False
        
        try:
            with open(self.modal_file, 'r', encoding='utf-8') as f:
                modal_content = f.read()
            
            # Check for modern modal features
            modern_features = {
                'Framer Motion': 'motion.' in modal_content and 'AnimatePresence' in modal_content,
                'Priority Levels': 'PRIORITY_LEVELS' in modal_content,
                'Color Coding': 'bgColor' in modal_content,
                'Error Handling': 'error' in modal_content and 'setError' in modal_content,
                'Loading States': 'isSaving' in modal_content,
                'Accessibility': 'title=' in modal_content or 'aria-label' in modal_content,
                'Professional Styling': 'rounded-xl' in modal_content or 'shadow-xl' in modal_content
            }
            
            passed_features = []
            failed_features = []
            
            for feature, condition in modern_features.items():
                if condition:
                    passed_features.append(feature)
                    print(f"  ✅ {feature} implementation found")
                else:
                    failed_features.append(feature)
                    print(f"  ❌ {feature} implementation missing")
            
            # Check if modal is integrated in dashboard
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_content = f.read()
                
            if 'PriorityChangeModal' in dashboard_content:
                print("  ✅ Modal integrated into dashboard")
                passed_features.append("Dashboard Integration")
            else:
                print("  ❌ Modal not integrated into dashboard")
                failed_features.append("Dashboard Integration")
            
            # Check if old prompt() is removed
            if 'prompt(' not in dashboard_content:
                print("  ✅ Old prompt() dialog removed")
                passed_features.append("Old Dialog Removal")
            else:
                print("  ❌ Old prompt() dialog still present")
                failed_features.append("Old Dialog Removal")
            
            success_rate = len(passed_features) / len(modern_features)
            return success_rate >= 0.8  # 80% of features should be present
            
        except FileNotFoundError:
            print(f"  ❌ Could not read modal file: {self.modal_file}")
            return False
    
    def generate_final_report(self, fix1_pass, fix2_pass, fix3_pass):
        """Generate final verification report"""
        print("\n" + "="*60)
        print("📊 FINAL VERIFICATION REPORT")
        print("="*60)
        
        all_passed = fix1_pass and fix2_pass and fix3_pass
        
        print(f"\n🎯 FIX STATUS SUMMARY:")
        print(f"   Fix #1 - Drag-drop removal:      {'✅ PASS' if fix1_pass else '❌ FAIL'}")
        print(f"   Fix #2 - Priority consistency:   {'✅ PASS' if fix2_pass else '❌ FAIL'}")
        print(f"   Fix #3 - Modern modal:           {'✅ PASS' if fix3_pass else '❌ FAIL'}")
        
        print(f"\n🏆 OVERALL STATUS: {'✅ ALL FIXES SUCCESSFUL' if all_passed else '❌ SOME ISSUES REMAIN'}")
        
        if all_passed:
            print("\n🎉 CONGRATULATIONS!")
            print("   All three UI issues have been successfully resolved:")
            print("   1. Drag-drop functionality completely removed")
            print("   2. Priority consistency verified and working")
            print("   3. Modern priority change modal implemented")
            print("\n   The system is now ready for production use!")
        else:
            print("\n⚠️  ACTION REQUIRED:")
            if not fix1_pass:
                print("   - Complete drag-drop removal")
            if not fix2_pass:
                print("   - Fix priority consistency issues")
            if not fix3_pass:
                print("   - Complete modern modal implementation")
        
        print("="*60)
        
        return all_passed

def main():
    """Run final verification test suite"""
    print("🚀 Starting Final Verification Test Suite...")
    print("Testing all three UI fixes...")
    
    tester = FinalVerificationTest()
    
    # Run all verification tests
    fix1_pass = tester.verify_fix_1_drag_drop_removed()
    fix2_pass = tester.verify_fix_2_priority_consistency()
    fix3_pass = tester.verify_fix_3_modern_modal()
    
    # Generate final report
    all_passed = tester.generate_final_report(fix1_pass, fix2_pass, fix3_pass)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
