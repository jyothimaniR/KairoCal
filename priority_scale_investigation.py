#!/usr/bin/env python3
"""
CRITICAL PRIORITY SCALE INVESTIGATION

This script will thoroughly test the priority scale inconsistency between:
1. BERT model output (claims: 1=least, 5=critical)  
2. Frontend display (claims: 1=critical, 5=least)

This is a CRITICAL system issue that must be resolved.
"""

import requests
import sqlite3
from datetime import datetime
import json

class PriorityScaleInvestigation:
    def __init__(self):
        self.api_base = 'http://127.0.0.1:8000/api/v1'
        self.db_path = 'backend/kairocal.db'
        self.test_user = 'frontend-test-user'
    
    def test_critical_event_priority_flow(self):
        """Test an obviously CRITICAL event through the entire flow"""
        print("🚨 TESTING CRITICAL EVENT PRIORITY FLOW")
        print("="*60)
        
        critical_event = "URGENT emergency meeting with CEO right now - system failure"
        print(f"Test Input: '{critical_event}'")
        print("Expected: This should clearly be CRITICAL priority")
        
        try:
            # Step 1: Create event via voice API
            response = requests.post(
                f"{self.api_base}/voice/create-event",
                json={
                    "voice_text": critical_event,
                    "user_id": self.test_user
                }
            )
            
            if response.status_code == 200:
                full_response = response.json()
                print("\n📋 FULL API RESPONSE ANALYSIS:")
                print(json.dumps(full_response, indent=2))
                
                # Extract all priority-related information
                event_data = full_response.get('event_data', {})
                bert_classification = full_response.get('bert_classification', {})
                
                api_priority = event_data.get('priority_level')
                bert_priority = bert_classification.get('priority') 
                bert_final_priority = bert_classification.get('final_priority')
                
                print(f"\n🔍 PRIORITY VALUES EXTRACTED:")
                print(f"   event_data.priority_level: {api_priority}")
                print(f"   bert_classification.priority: {bert_priority}")
                print(f"   bert_classification.final_priority: {bert_final_priority}")
                
                # Step 2: Check what's stored in database
                event_id = full_response.get('event_id')
                if event_id:
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
                        print(f"   database.priority_level: {db_priority}")
                        
                        # Step 3: Analyze the priority scale
                        print(f"\n🧪 PRIORITY SCALE ANALYSIS:")
                        
                        if api_priority == 1:
                            print(f"   ✅ Priority 1 assigned - Frontend treats this as CRITICAL")
                        elif api_priority == 5:
                            print(f"   ⚠️  Priority 5 assigned - BERT treats this as CRITICAL")
                        else:
                            print(f"   🤔 Priority {api_priority} assigned - Unclear scale")
                        
                        # Step 4: Determine which scale is actually being used
                        print(f"\n🎯 SCALE DETERMINATION:")
                        if bert_priority == 5 and api_priority == 5:
                            print("   📊 BERT Scale (1=low, 5=critical) is being used")
                            print("   ❌ CONFLICT: Frontend expects 1=critical, 5=low")
                            return "BERT_SCALE", api_priority, bert_priority
                        elif bert_priority == 1 and api_priority == 1:
                            print("   📊 Frontend Scale (1=critical, 5=low) is being used") 
                            print("   ✅ CONSISTENT: Both use same scale")
                            return "FRONTEND_SCALE", api_priority, bert_priority
                        else:
                            print("   ❓ UNCLEAR: Scales don't match expected patterns")
                            return "UNCLEAR", api_priority, bert_priority
                    else:
                        print("   ❌ Event not found in database")
                        return "DB_ERROR", None, None
                else:
                    print("   ❌ No event_id returned")
                    return "API_ERROR", None, None
            else:
                print(f"   ❌ API request failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return "API_FAILED", None, None
                
        except Exception as e:
            print(f"❌ Exception during test: {e}")
            return "EXCEPTION", None, None
    
    def test_low_priority_event_flow(self):
        """Test an obviously LOW priority event"""
        print("\n🟢 TESTING LOW PRIORITY EVENT FLOW")
        print("="*60)
        
        low_event = "casual coffee chat with friend sometime next week"
        print(f"Test Input: '{low_event}'")
        print("Expected: This should clearly be LOW priority")
        
        try:
            response = requests.post(
                f"{self.api_base}/voice/create-event",
                json={
                    "voice_text": low_event,
                    "user_id": self.test_user
                }
            )
            
            if response.status_code == 200:
                full_response = response.json()
                event_data = full_response.get('event_data', {})
                bert_classification = full_response.get('bert_classification', {})
                
                api_priority = event_data.get('priority_level')
                bert_priority = bert_classification.get('priority')
                
                print(f"\n🔍 LOW PRIORITY EVENT RESULTS:")
                print(f"   API Priority: {api_priority}")
                print(f"   BERT Priority: {bert_priority}")
                
                if api_priority == 5:
                    print("   📊 Priority 5 for LOW event - Using BERT scale (1=low, 5=critical)")
                    return "BERT_SCALE", api_priority
                elif api_priority == 1:
                    print("   📊 Priority 1 for LOW event - Using Frontend scale (1=critical, 5=low)")
                    return "FRONTEND_SCALE", api_priority  
                else:
                    print(f"   🤔 Priority {api_priority} for LOW event - Need to analyze")
                    return "UNCLEAR", api_priority
            else:
                print(f"❌ API failed: {response.status_code}")
                return "API_FAILED", None
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return "EXCEPTION", None
    
    def analyze_frontend_priority_display(self):
        """Analyze how frontend displays priorities"""
        print("\n🖥️ ANALYZING FRONTEND PRIORITY DISPLAY")
        print("="*60)
        
        try:
            # Check the priority utility functions
            priority_utils_file = "frontend/src/utils/priorityUtils.tsx"
            modal_file = "frontend/src/components/modals/PriorityChangeModal.tsx"
            
            files_to_check = [
                (priority_utils_file, "Priority Utils"),
                (modal_file, "Priority Modal")
            ]
            
            for file_path, file_name in files_to_check:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    print(f"\n📄 {file_name} Analysis:")
                    
                    # Look for priority level definitions
                    if "CRITICAL" in content:
                        # Find the line with CRITICAL and extract context
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if "CRITICAL" in line and ("level" in line or "1" in line or "5" in line):
                                print(f"   Found: {line.strip()}")
                                # Show surrounding lines for context
                                for j in range(max(0, i-2), min(len(lines), i+3)):
                                    if j != i:
                                        print(f"   Context: {lines[j].strip()}")
                                break
                    
                    # Look for priority arrays or objects
                    if "level: 1" in content:
                        print("   ✅ Found 'level: 1' - Frontend uses 1=critical scale")
                    elif "level: 5" in content:
                        print("   ⚠️ Found 'level: 5' - Check if this is critical")
                    
                except FileNotFoundError:
                    print(f"   ❌ {file_name} file not found: {file_path}")
                    
        except Exception as e:
            print(f"❌ Frontend analysis error: {e}")
    
    def check_backend_bert_configuration(self):
        """Check backend BERT configuration"""
        print("\n🧠 ANALYZING BACKEND BERT CONFIGURATION")
        print("="*60)
        
        try:
            # Check BERT-related files for priority mapping
            bert_files = [
                "backend/app/services/nlp_service.py",
                "backend/app/api/voice.py",
                "backend/app/services/bert_classifier.py"
            ]
            
            for file_path in bert_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    print(f"\n📄 Analyzing {file_path}:")
                    
                    # Look for priority mappings
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if any(keyword in line.lower() for keyword in ['priority', 'critical', '1', '5']):
                            if any(op in line for op in ['=', ':', 'level']):
                                print(f"   Line {i+1}: {line.strip()}")
                                
                except FileNotFoundError:
                    print(f"   ❌ File not found: {file_path}")
                    
        except Exception as e:
            print(f"❌ Backend analysis error: {e}")
    
    def generate_priority_scale_report(self, critical_result, low_result):
        """Generate comprehensive priority scale analysis report"""
        print("\n" + "="*80)
        print("🚨 CRITICAL PRIORITY SCALE INVESTIGATION REPORT")
        print("="*80)
        
        critical_scale, critical_api, critical_bert = critical_result if len(critical_result) == 3 else (critical_result[0], critical_result[1], None)
        low_scale, low_api = low_result if len(low_result) == 2 else (low_result[0], None)
        
        print(f"\n📊 SCALE DETECTION RESULTS:")
        print(f"   Critical Event Scale: {critical_scale}")
        print(f"   Low Priority Event Scale: {low_scale}")
        
        if critical_scale == low_scale:
            print(f"\n✅ CONSISTENT SCALE DETECTED: {critical_scale}")
        else:
            print(f"\n❌ INCONSISTENT SCALES DETECTED!")
            print(f"   Critical events using: {critical_scale}")
            print(f"   Low events using: {low_scale}")
        
        print(f"\n🎯 PRIORITY VALUES OBSERVED:")
        if critical_api is not None:
            print(f"   Critical event got priority: {critical_api}")
        if low_api is not None:
            print(f"   Low event got priority: {low_api}")
        
        # Determine the actual scale being used
        if critical_scale == "BERT_SCALE" or low_scale == "BERT_SCALE":
            print(f"\n📋 SYSTEM CURRENTLY USING: BERT SCALE")
            print(f"   1 = Lowest priority")
            print(f"   5 = Highest priority (CRITICAL)")
            print(f"   ❌ CONFLICT: Frontend displays assume opposite scale!")
        elif critical_scale == "FRONTEND_SCALE" or low_scale == "FRONTEND_SCALE":
            print(f"\n📋 SYSTEM CURRENTLY USING: FRONTEND SCALE") 
            print(f"   1 = Highest priority (CRITICAL)")
            print(f"   5 = Lowest priority")
            print(f"   ✅ CONSISTENT: Frontend displays match this scale")
        else:
            print(f"\n❓ SCALE UNCLEAR - NEEDS MANUAL INVESTIGATION")
        
        print(f"\n🚨 CRITICAL ACTION REQUIRED:")
        if critical_scale == "BERT_SCALE":
            print(f"   1. Fix frontend priority display logic")
            print(f"   2. Update priority modal to match BERT scale")
            print(f"   3. Verify all priority comparisons in code")
        elif critical_scale != low_scale:
            print(f"   1. Fix inconsistent priority assignment")
            print(f"   2. Ensure single scale throughout system")
            print(f"   3. Test all priority-dependent features")
        
        print("="*80)
        
        return critical_scale, low_scale

def main():
    """Run comprehensive priority scale investigation"""
    print("🚨 STARTING CRITICAL PRIORITY SCALE INVESTIGATION")
    print("This investigation will determine the true priority scale conflict.")
    
    investigator = PriorityScaleInvestigation()
    
    # Test critical event
    critical_result = investigator.test_critical_event_priority_flow()
    
    # Test low priority event  
    low_result = investigator.test_low_priority_event_flow()
    
    # Analyze frontend configuration
    investigator.analyze_frontend_priority_display()
    
    # Analyze backend configuration
    investigator.check_backend_bert_configuration()
    
    # Generate comprehensive report
    critical_scale, low_scale = investigator.generate_priority_scale_report(critical_result, low_result)
    
    # Return results for potential automated fixes
    return critical_scale, low_scale

if __name__ == "__main__":
    main()
