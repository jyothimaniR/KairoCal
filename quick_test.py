#!/usr/bin/env python3
import requests

payload = {
    'title': 'Test All-Day Event',
    'start_time': '2025-08-17T00:00:00',
    'end_time': '2025-08-17T23:59:00', 
    'is_all_day': True,
    'description': 'Test'
}

response = requests.post(
    'http://127.0.0.1:8000/api/v1/conflicts/check',
    json=payload,
    params={'cognito_sub': 'frontend-test-user'}
)

print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    conflicts_count = len(result.get('conflicts', []))
    print(f'Conflicts: {conflicts_count}')
    if conflicts_count == 0:
        print('🎉 SUCCESS: All-day event returns no conflicts!')
    else:
        print('❌ FAILURE: All-day event still showing conflicts')
else:
    print(f'Error: {response.text}')
