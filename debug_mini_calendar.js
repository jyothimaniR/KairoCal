import requests
import json
from datetime import datetime

def debug_mini_calendar():
    try:
        print('🔍 Debugging MiniCalendar date issues...')
        print('Current date:', datetime.now().isoformat())
        print('Today (August 19, 2025):', datetime(2025, 8, 19).isoformat())
        
        # Fetch events
        response = requests.get('http://localhost:8000/api/v1/events?cognito_sub=frontend-test-user')
        events = response.json()
        
        print(f'\n📅 Found {len(events)} events')
        
        if events:
            # Show first few events with their dates
            print('\n🗓️ Sample events with dates:')
            for i, event in enumerate(events[:5]):
                start_time = event['start_time']
                # Parse the datetime string
                if isinstance(start_time, str):
                    if start_time.endswith('Z'):
                        parsed_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    else:
                        parsed_date = datetime.fromisoformat(start_time)
                else:
                    parsed_date = start_time
                
                date_key = f"{parsed_date.year}-{parsed_date.month:02d}-{parsed_date.day:02d}"
                print(f"{i+1}. {event['title']}")
                print(f"   Raw start_time: {start_time}")
                print(f"   Parsed date: {parsed_date}")
                print(f"   Date key: {date_key}")
                print(f"   Date: {parsed_date.strftime('%Y-%m-%d')}")
                print('')
            
            # Check events for today (August 19, 2025)
            today = datetime(2025, 8, 19)
            today_key = f"{today.year}-{today.month:02d}-{today.day:02d}"
            print(f'🎯 Looking for events on today ({today_key}):')
            
            todays_events = []
            for event in events:
                start_time = event['start_time']
                if isinstance(start_time, str):
                    if start_time.endswith('Z'):
                        event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    else:
                        event_date = datetime.fromisoformat(start_time)
                else:
                    event_date = start_time
                
                event_key = f"{event_date.year}-{event_date.month:02d}-{event_date.day:02d}"
                if event_key == today_key:
                    todays_events.append(event)
            
            print(f'Found {len(todays_events)} events for today')
            for event in todays_events:
                print(f"- {event['title']} at {event['start_time']}")
            
            # Check August 2025 events
            print(f'\n📅 Events in August 2025:')
            august_2025_events = []
            for event in events:
                start_time = event['start_time']
                if isinstance(start_time, str):
                    if start_time.endswith('Z'):
                        event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    else:
                        event_date = datetime.fromisoformat(start_time)
                else:
                    event_date = start_time
                
                if event_date.year == 2025 and event_date.month == 8:  # August
                    august_2025_events.append((event, event_date))
            
            print(f'Found {len(august_2025_events)} events in August 2025')
            for event, event_date in august_2025_events[:10]:
                print(f"- Day {event_date.day}: {event['title']}")
                
    except Exception as error:
        print(f'❌ Error: {error}')

if __name__ == "__main__":
    debug_mini_calendar()
