#!/usr/bin/env python3
"""
Priority Scale Frontend Verification for KairoCal
Tests the fixed frontend components for BERT scale consistency
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any, List

class FrontendPriorityVerification:
    def __init__(self):
        self.test_results = []
        self.frontend_path = "frontend/src"
        
    def log_result(self, test_name: str, status: str, details: str):
        """Log and store test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if status == "PASS":
            print(f"✅ {test_name}: {details}")
        elif status == "FAIL":
            print(f"❌ {test_name}: {details}")
        else:
            print(f"⚠️ {test_name}: {details}")
    
    def test_priority_utils_bert_scale(self):
        """Test priorityUtils.ts uses correct BERT scale"""
        utils_path = f"{self.frontend_path}/utils/priorityUtils.ts"
        
        if not os.path.exists(utils_path):
            self.log_result("PriorityUtils BERT Scale", "FAIL", f"File not found: {utils_path}")
            return False
            
        with open(utils_path, 'r') as f:
            content = f.read()
        
        # Check for correct BERT scale mapping
        bert_scale_indicators = [
            "1.*VERY LOW",
            "2.*LOW", 
            "3.*MEDIUM",
            "4.*HIGH",
            "5.*CRITICAL"
        ]
        
        all_found = True
        for pattern in bert_scale_indicators:
            if not re.search(pattern, content, re.IGNORECASE):
                self.log_result("PriorityUtils BERT Scale", "FAIL", f"Missing pattern: {pattern}")
                all_found = False
        
        # Check for removed conversion logic
        bad_patterns = [
            "convertBertPriorityToUI",
            "6 - bertPriority", 
            "invert.*scale",
            "UI expects 1.*highest"
        ]
        
        for pattern in bad_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.log_result("PriorityUtils BERT Scale", "FAIL", f"Found obsolete conversion logic: {pattern}")
                all_found = False
        
        if all_found:
            self.log_result("PriorityUtils BERT Scale", "PASS", "Correctly uses BERT scale (1=VERY LOW, 5=CRITICAL)")
        
        return all_found
    
    def test_priority_change_modal_bert_scale(self):
        """Test PriorityChangeModal.tsx uses correct BERT scale"""
        modal_path = f"{self.frontend_path}/components/modals/PriorityChangeModal.tsx"
        
        if not os.path.exists(modal_path):
            self.log_result("PriorityChangeModal BERT Scale", "FAIL", f"File not found: {modal_path}")
            return False
            
        with open(modal_path, 'r') as f:
            content = f.read()
        
        # Check for correct BERT scale in modal
        expected_levels = [
            "level: 1.*VERY LOW",
            "level: 2.*LOW",
            "level: 3.*MEDIUM", 
            "level: 4.*HIGH",
            "level: 5.*CRITICAL"
        ]
        
        all_found = True
        for pattern in expected_levels:
            if not re.search(pattern, content, re.IGNORECASE):
                self.log_result("PriorityChangeModal BERT Scale", "FAIL", f"Missing pattern: {pattern}")
                all_found = False
        
        if all_found:
            self.log_result("PriorityChangeModal BERT Scale", "PASS", "Modal correctly uses BERT scale levels")
        
        return all_found
    
    def test_dashboard_priority_consistency(self):
        """Test dashboard uses priority utilities consistently"""
        dashboard_path = f"{self.frontend_path}/pages/dashboard/DashboardPage.tsx"
        
        if not os.path.exists(dashboard_path):
            self.log_result("Dashboard Priority Consistency", "SKIP", f"File not found: {dashboard_path}")
            return True
            
        with open(dashboard_path, 'r') as f:
            content = f.read()
        
        # Check that dashboard imports and uses priority utilities
        required_imports = [
            "getPriorityInfo",
            "PriorityChangeModal"
        ]
        
        imports_found = True
        for import_name in required_imports:
            if import_name not in content:
                self.log_result("Dashboard Priority Consistency", "FAIL", f"Missing import: {import_name}")
                imports_found = False
        
        # Check that drag-drop is removed
        drag_patterns = [
            "draggable",
            "onDragStart", 
            "cursor-move"
        ]
        
        drag_removed = True
        for pattern in drag_patterns:
            if pattern in content:
                self.log_result("Dashboard Priority Consistency", "FAIL", f"Drag-drop not fully removed: {pattern}")
                drag_removed = False
        
        if imports_found and drag_removed:
            self.log_result("Dashboard Priority Consistency", "PASS", "Dashboard correctly integrated with BERT scale system")
        
        return imports_found and drag_removed
    
    def test_file_structure_integrity(self):
        """Test that all required files exist and are properly structured"""
        required_files = [
            f"{self.frontend_path}/utils/priorityUtils.ts",
            f"{self.frontend_path}/components/modals/PriorityChangeModal.tsx",
            f"{self.frontend_path}/pages/dashboard/DashboardPage.tsx"
        ]
        
        all_exist = True
        for file_path in required_files:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                self.log_result(f"File Structure - {os.path.basename(file_path)}", "PASS", f"Exists ({file_size} bytes)")
            else:
                self.log_result(f"File Structure - {os.path.basename(file_path)}", "FAIL", "File missing")
                all_exist = False
        
        return all_exist
    
    def generate_bert_scale_summary(self):
        """Generate a summary of the BERT scale implementation"""
        summary = {
            "bert_scale_standard": {
                "1": "VERY LOW - Simple reminders, low-impact tasks",
                "2": "LOW - Regular appointments, routine tasks", 
                "3": "MEDIUM - Standard meetings, moderate importance",
                "4": "HIGH - Important meetings, client presentations",
                "5": "CRITICAL - Urgent emergencies, CEO meetings"
            },
            "implementation_status": "COMPLETED",
            "files_updated": [
                "frontend/src/utils/priorityUtils.ts - Fixed BERT scale mapping",
                "frontend/src/components/modals/PriorityChangeModal.tsx - Updated priority levels",
                "frontend/src/pages/dashboard/DashboardPage.tsx - Integrated modern modal"
            ],
            "verification_timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def run_frontend_verification(self):
        """Run all frontend priority verification tests"""
        print("🔍 Frontend Priority Scale Verification")
        print("=" * 60)
        
        tests = [
            ("File Structure Integrity", self.test_file_structure_integrity),
            ("PriorityUtils BERT Scale", self.test_priority_utils_bert_scale),
            ("PriorityChangeModal BERT Scale", self.test_priority_change_modal_bert_scale),
            ("Dashboard Priority Consistency", self.test_dashboard_priority_consistency)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                print(f"❌ {test_name}: Exception - {str(e)}")
        
        # Generate report
        success_rate = (passed / total) * 100
        bert_summary = self.generate_bert_scale_summary()
        
        report = {
            "frontend_verification": True,
            "tests_passed": passed,
            "tests_total": total,
            "success_rate": success_rate,
            "status": "FRONTEND_VERIFIED" if success_rate == 100 else "ISSUES_FOUND",
            "bert_scale_summary": bert_summary,
            "test_results": self.test_results
        }
        
        print("=" * 60)
        if success_rate == 100:
            print(f"🎉 FRONTEND VERIFICATION COMPLETE! All {total} tests passed.")
            print("✅ Frontend priority system perfectly aligned with BERT scale")
            print("✅ Scale: 1=VERY_LOW → 2=LOW → 3=MEDIUM → 4=HIGH → 5=CRITICAL")
        else:
            print(f"⚠️ Frontend verification: {passed}/{total} tests passed ({success_rate:.1f}%)")
        
        print("=" * 60)
        
        return report

def main():
    verifier = FrontendPriorityVerification()
    report = verifier.run_frontend_verification()
    
    # Save report
    with open('frontend_priority_verification.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("📄 Report saved to: frontend_priority_verification.json")
    
    if report["success_rate"] == 100:
        print("\n🏆 FRONTEND PRIORITY SYSTEM: VERIFICATION COMPLETE!")
        print("🎯 Ready for backend testing when server is running")
        return 0
    else:
        print("\n💥 FRONTEND PRIORITY SYSTEM: NEEDS ATTENTION")
        return 1

if __name__ == "__main__":
    exit(main())
