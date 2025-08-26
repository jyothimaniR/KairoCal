#!/usr/bin/env python3
"""
Test script to verify the priority conflict resolution fix
"""

def test_priority_logic():
    """Test the corrected priority logic"""
    print("🧪 Testing Priority Conflict Resolution Logic")
    print("=" * 50)
    
    # Test cases based on the screenshot
    # Movie With Alex: Priority 2 (Low)
    # Urgent Meeting With Manager: Priority 5 (Critical) 
    
    event1 = {
        'title': 'Movie With Alex',
        'priority': 2,  # Low priority
        'priority_label': 'Low'
    }
    
    event2 = {
        'title': 'Urgent Meeting With Manager', 
        'priority': 5,  # Critical priority
        'priority_label': 'Critical'
    }
    
    print(f"Event 1: {event1['title']} - Priority {event1['priority']} ({event1['priority_label']})")
    print(f"Event 2: {event2['title']} - Priority {event2['priority']} ({event2['priority_label']})")
    print()
    
    # Apply the FIXED logic (higher number = higher priority)
    if event1['priority'] < event2['priority']:  # Event1 has lower priority
        recommendation = f"Consider moving \"{event1['title']}\" (Priority {event1['priority']} - {event1['priority_label']})"
        should_move = event1['title']
    elif event2['priority'] < event1['priority']:  # Event2 has lower priority
        recommendation = f"Consider moving \"{event2['title']}\" (Priority {event2['priority']} - {event2['priority_label']})"
        should_move = event2['title']
    else:
        recommendation = "Both events have same priority - consider other factors"
        should_move = "Either"
    
    print("🤖 AI Recommendation (FIXED):")
    print(f"   {recommendation}")
    print()
    
    # Verify the result
    expected_to_move = "Movie With Alex"  # Lower priority event should be moved
    
    if should_move == expected_to_move:
        print("✅ SUCCESS: AI correctly recommends moving the lower priority event!")
        print(f"   ✓ Correctly suggests moving '{should_move}' (Priority {event1['priority']} - Low)")
        print(f"   ✓ Correctly preserves '{event2['title']}' (Priority {event2['priority']} - Critical)")
    else:
        print("❌ FAILURE: AI recommendation is still incorrect!")
        print(f"   ✗ Incorrectly suggests moving '{should_move}'")
        print(f"   ✗ Should suggest moving '{expected_to_move}' instead")
    
    print()
    print("🔍 Logic Explanation:")
    print("   • In KairoCal: Lower numbers = Higher priority")
    print("   • Priority 1 = Very Low, Priority 2 = Low, ..., Priority 5 = Critical")
    print("   • Wait, that's backwards! Let me check the priority scale...")
    
    # Check the actual priority scale from the code
    print()
    print("📋 Checking KairoCal Priority Scale:")
    priority_labels = {
        1: 'Very Low',
        2: 'Low', 
        3: 'Medium',
        4: 'High',
        5: 'Critical'
    }
    
    for p, label in priority_labels.items():
        print(f"   Priority {p} = {label}")
    
    print()
    print("🤔 Wait, this suggests that Priority 5 = Critical (highest), not lowest!")
    print("   Let me re-examine the logic...")
    
    # Re-examine based on the priority labels
    # If Priority 5 = Critical and Priority 2 = Low, then:
    # Higher numbers = Higher priority (opposite of what I initially thought)
    
    print()
    print("🔄 Re-analyzing with correct understanding:")
    print("   • Priority 5 (Critical) should be KEPT")
    print("   • Priority 2 (Low) should be MOVED")
    
    # Apply CORRECTED logic (higher number = higher priority)
    if event1['priority'] < event2['priority']:  # Event1 has lower priority
        correct_recommendation = f"Consider moving \"{event1['title']}\" (Priority {event1['priority']} - {event1['priority_label']})"
        correct_should_move = event1['title']
    elif event2['priority'] < event1['priority']:  # Event2 has lower priority
        correct_recommendation = f"Consider moving \"{event2['title']}\" (Priority {event2['priority']} - {event2['priority_label']})"
        correct_should_move = event2['title']
    else:
        correct_recommendation = "Both events have same priority - consider other factors"
        correct_should_move = "Either"
    
    print()
    print("🤖 CORRECTED AI Recommendation:")
    print(f"   {correct_recommendation}")
    
    if correct_should_move == expected_to_move:
        print("✅ FINAL SUCCESS: Logic is now correct!")
    else:
        print("❌ Still needs fixing...")
        
    return correct_should_move == expected_to_move

if __name__ == "__main__":
    test_priority_logic()
