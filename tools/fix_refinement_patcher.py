#!/usr/bin/env python3
from pathlib import Path

path = Path("tools/apply_redesign_refinements.py")
text = path.read_text(encoding="utf-8")
old = "    marker = 'console.log(`\\n${passed} design mode tests passed.`);'"
new = "    marker = r'console.log(`\\n${passed} design mode tests passed.`);'"
if new not in text:
    if text.count(old) != 1:
        raise SystemExit("refinement test marker source not found")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
print("refinement patcher marker fixed")
