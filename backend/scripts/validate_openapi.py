"""CI helper: validate that generated OpenAPI matches committed specification.

Usage (CI):
  python backend/scripts/validate_openapi.py --fail-on-diff

It will:
  * Import the FastAPI app
  * Dump current openapi.json
  * Compare to stored snapshot in backend/openapi_snapshot.json (if exists)
  * Fail with non-zero exit if differences found (unless snapshot missing – then creates it)
"""
import json, sys, argparse, difflib, os
from importlib import import_module

SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "openapi_snapshot.json")

parser = argparse.ArgumentParser()
parser.add_argument("--fail-on-diff", action="store_true")
parser.add_argument("--light-mode", action="store_true", help="Generate spec with heavy features disabled (legacy mode)")
args = parser.parse_args()

sys.path.insert(0, "/app")

if args.light_mode:
    os.environ.setdefault("DISABLE_NLP", "true")
    os.environ.setdefault("DISABLE_ANALYTICS", "true")
    os.environ.setdefault("DISABLE_CONFLICTS", "true")
    os.environ.setdefault("DISABLE_WEBSOCKETS", "true")

try:
    mod = import_module("app.main")
    app = getattr(mod, "app")
except Exception as e:
    print(f"ERROR: Unable to import FastAPI app: {e}")
    sys.exit(1)

current = app.openapi()

if not os.path.exists(SNAPSHOT_PATH):
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, sort_keys=True)
    print("Snapshot created. (First run)")
    sys.exit(0)

with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
    snapshot = json.load(f)

if current == snapshot:
    print("OpenAPI spec matches snapshot.")
    sys.exit(0)

print("OpenAPI spec drift detected.")
if args.fail_on_diff:
    # Produce a readable diff of top-level keys (full diff could be large)
    a = json.dumps(snapshot, indent=2, sort_keys=True).splitlines()
    b = json.dumps(current, indent=2, sort_keys=True).splitlines()
    for line in difflib.unified_diff(a, b, fromfile="snapshot", tofile="current", lineterm=""):
        print(line)
    sys.exit(2)
else:
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, sort_keys=True)
    print("Snapshot updated (diff not enforced).")
