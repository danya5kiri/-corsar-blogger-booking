#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = "Лидер по количеству уникальных туров"
new = "Лидер по уникальным турам"
count = text.count(old)
if count != 2:
    raise RuntimeError(f"Ожидалось 2 совпадения, найдено {count}")
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
