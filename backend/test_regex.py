import re

text = "Coffee Chat With Colleague At Liverpool Cafe"
pattern = r'(?:^|\s)(?:at|in|@)\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s+(?:coming|today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next|this|last)\b|\s*$)'

print(f"Testing pattern on: '{text}'")
print(f"Pattern: {pattern}")

matches = list(re.finditer(pattern, text, re.IGNORECASE))
print(f"Found {len(matches)} matches:")

for i, match in enumerate(matches):
    print(f"  Match {i+1}: '{match.group(1)}' at position {match.start()}")
    print(f"    Full match: '{match.group(0)}'")
    print(f"    Groups: {match.groups()}")

# Let's also test a simpler pattern that might catch both
pattern2 = r'(?:at|in)\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s|$)'
print(f"\nTesting simpler pattern: {pattern2}")
matches2 = list(re.finditer(pattern2, text, re.IGNORECASE))
print(f"Found {len(matches2)} matches:")

for i, match in enumerate(matches2):
    print(f"  Match {i+1}: '{match.group(1)}' at position {match.start()}")
    print(f"    Full match: '{match.group(0)}'")
