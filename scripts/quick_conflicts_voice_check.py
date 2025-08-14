import json
import sys
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    import requests  # type: ignore
except ImportError:  # Fallback minimal HTTP client
    requests = None  # type: ignore
    import urllib.request, urllib.error
    import ssl

    class _Resp:
        def __init__(self, status, data, headers):
            self.status_code = status
            self._data = data
            self.headers = headers
            self.text = data.decode('utf-8', errors='replace') if isinstance(data, bytes) else str(data)
        def json(self):
            return json.loads(self.text)
        def raise_for_status(self):
            if not (200 <= self.status_code < 300):
                raise RuntimeError(f"HTTP {self.status_code}: {self.text[:500]}")

    class _ReqFallback:
        def __init__(self):
            self._ctx = ssl.create_default_context()
        def get(self, url, params=None, timeout=10):
            if params:
                from urllib.parse import urlencode
                url += ('&' if '?' in url else '?') + urlencode(params)
            req = urllib.request.Request(url, method='GET')
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=self._ctx) as r:
                    return _Resp(r.status, r.read(), r.headers)
            except urllib.error.HTTPError as e:
                return _Resp(e.code, e.read(), e.headers)
        def post(self, url, params=None, json=None, timeout=10):
            data = None
            headers = {'Content-Type': 'application/json'}
            if json is not None:
                data = json_dump(json).encode('utf-8')
            if params:
                from urllib.parse import urlencode
                url += ('&' if '?' in url else '?') + urlencode(params)
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=self._ctx) as r:
                    return _Resp(r.status, r.read(), r.headers)
            except urllib.error.HTTPError as e:
                return _Resp(e.code, e.read(), e.headers)

    def json_dump(o):
        return json.dumps(o, default=str)

    requests = _ReqFallback()  # type: ignore

USER = 'test-user-1'

API_PORT = os.getenv('API_PORT', '8000')
API = f'http://localhost:{API_PORT}/api/v1'
print(f"[INFO] Using API base: {API}")

def ensure_user():
    # Try to fetch; if 404, create
    try:
        r = requests.get(f"{API}/users/me", params={"cognito_sub": USER}, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    payload = {"cognito_sub": USER, "email": "test-user-1@example.com", "full_name": "Test User"}
    r = requests.post(f"{API}/users", json=payload, timeout=10)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Failed to ensure user: {r.status_code} {r.text}")
    return r.json()

def ensure_tables():
    try:
        r = requests.post(API + '/../database/create-tables'.replace('/api/v1/..', ''), timeout=5)
    except Exception:
        return

def post_event(title: str, start: datetime, end: datetime):
    payload = {
        'title': title,
        'start_time': start.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'end_time': end.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    r = requests.post(
        f"{API}/events",
        params={"cognito_sub": USER, "auto_classify_priority": "true"},
        json=payload,
        timeout=10,
    )
    if r.status_code >= 400:
        try:
            print('[ERROR BODY]', r.text[:1000])
        except Exception:
            pass
        r.raise_for_status()
    return r.json()

def conflicts_check(start: datetime, end: datetime):
    payload = {
        'title': 'Probe',
        'start_time': start.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'end_time': end.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'include_event_details': True,
        'max_alternatives': 3,
    }
    r = requests.post(
        f"{API}/conflicts/check",
        params={"cognito_sub": USER, "engine": "basic_v1"},
        json=payload,
        timeout=10,
    )
    if r.status_code >= 400:
        print('[CONFLICTS ERROR BODY]', r.text[:1000])
    r.raise_for_status()
    return r.json()

def voice_create(text: str):
    payload = {
        'voice_text': text,
        'user_id': USER,  # accepts cognito_sub string
        'auto_schedule': True,
    }
    r = requests.post(
        f"{API}/voice/create-event",
        json=payload,
        timeout=15,
    )
    # Intentionally not raise_for_status to show error body
    try:
        data = r.json()
    except Exception:
        data = {'status': r.status_code, 'text': r.text}
    return r.status_code, data


def wait_ready(timeout=25):
    base = API.rsplit('/api/v1',1)[0]
    url = base + '/ready'
    for i in range(timeout):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"[READY] Server ready after {i}s -> {url}")
                return True
        except Exception:
            pass
        time.sleep(1)
    print('[WARN] Server not reporting ready; continuing anyway')
    return False

def main():
    print('[STEP] Waiting for /ready ...')
    wait_ready()
    print('Ensuring test user exists...')
    u = ensure_user()
    print('[OK] user id:', u.get('id'))
    ensure_tables()
    now = datetime.now(timezone.utc)
    start = now + timedelta(minutes=15)
    end = start + timedelta(hours=1)

    print('Creating overlap events...')
    a = post_event('Overlap A', start, end)
    b = post_event('Overlap B', start, end)
    print('[OK] Created:', a.get('id'), b.get('id'))

    print('Server conflicts/check (engine=basic_v1):')
    cc = conflicts_check(start, end)
    print(f"[INFO] Conflicts detected: {len(cc)}")
    print(json.dumps(cc, indent=2, default=str)[:2000])

    print('Voice create (tomorrow 12 PM):')
    tomorrow_noon = 'Lunch meeting with my boss tomorrow at 12 PM'
    status, v = voice_create(tomorrow_noon)
    print('status:', status)
    print(json.dumps(v, indent=2, default=str)[:2000])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('ERROR:', e)
        sys.exit(1)
