import sys
import json
import requests
from datetime import datetime, timedelta

BASE = "http://localhost:8000"
SESS = requests.Session()


def main():
    user = {
        "email": "conflicts_tester@example.com",
        "full_name": "Conflicts Tester",
        "cognito_sub": "sub-conflicts-001",
        "preferences": {},
    }
    r = SESS.post(f"{BASE}/api/v1/users/", json=user)
    if r.status_code not in (200, 201, 400):
        print("User create failed:", r.status_code, r.text)
        return 2

    start = datetime.utcnow() + timedelta(minutes=5)
    end = start + timedelta(hours=1)

    events = [
        {
            "title": "High Priority Meeting",
            "description": "Important discussion",
            "start_time": start.isoformat() + "Z",
            "end_time": end.isoformat() + "Z",
            "location": "Room A",
            "priority_level": 1,
        },
        {
            "title": "Low Priority Task",
            "description": "Routine work",
            "start_time": (start + timedelta(minutes=15)).isoformat() + "Z",
            "end_time": (end + timedelta(minutes=15)).isoformat() + "Z",
            "location": "Room A",
            "priority_level": 4,
        },
    ]

    for e in events:
        re = SESS.post(
            f"{BASE}/api/v1/events/?cognito_sub={user['cognito_sub']}", json=e
        )
        if re.status_code not in (200, 201):
            print("Event create failed:", re.status_code, re.text)
            return 3

    rc = SESS.get(
        f"{BASE}/api/v1/events/priority/conflicts?cognito_sub={user['cognito_sub']}"
    )
    if rc.status_code != 200:
        print("Conflicts API failed:", rc.status_code, rc.text)
        return 4

    data = rc.json()
    print(json.dumps({
        "conflicts_detected": data.get("conflicts_detected"),
        "summary": data.get("summary"),
    }, indent=2))

    # Expect at least one conflict due to overlap and priority diff
    return 0 if (data.get("conflicts_detected", 0) >= 1) else 5


if __name__ == "__main__":
    sys.exit(main())
