#!/usr/bin/env python3
"""
User expectation analysis for voice commands
"""

print('🤔 User expectation analysis:')
print()

cases = [
    {
        'input': 'meeting with team for 2 hours',
        'user_expectation': 'A 2-hour meeting at reasonable time (like 10am-12pm)',
        'current_behavior': 'All-day event (00:00-23:59)',
        'makes_sense': False
    },
    {
        'input': 'coffee break for 15 minutes', 
        'user_expectation': 'A 15-minute break at reasonable time',
        'current_behavior': 'All-day event (00:00-23:59)',
        'makes_sense': False
    },
    {
        'input': 'lunch with Alex at 1:30 pm for 30 minutes',
        'user_expectation': '30-minute lunch at 1:30 PM',
        'current_behavior': '30-minute lunch at 1:30 PM',
        'makes_sense': True
    },
    {
        'input': 'quick call at 4pm',
        'user_expectation': 'Call at 4 PM with default duration',
        'current_behavior': '30-minute call at 4 PM',
        'makes_sense': True
    },
    {
        'input': 'team meeting tomorrow',
        'user_expectation': 'All-day event (no specific time/duration)',
        'current_behavior': 'Would be all-day',
        'makes_sense': True
    }
]

for case in cases:
    print(f"Input: '{case['input']}'")
    print(f"  User expects: {case['user_expectation']}")
    print(f"  Current behavior: {case['current_behavior']}")
    print(f"  Makes sense: {'✅' if case['makes_sense'] else '❌'}")
    print()

print('🤔 Revised logic suggestion:')
print('1. Has start time + duration → Use both ✅')
print('2. Has start time, no duration → Use start time + default duration ✅') 
print('3. No start time, has duration → Use reasonable start time + duration ❌ (currently all-day)')
print('4. No start time, no duration → All-day event ✅')
print()
print('The issue: Cases 3 should use duration with reasonable start time, not all-day')
