#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = ".cb-season-metric span {\n"
new = ".cb-season-metric > span {\n"
count = text.count(old)
if count != 1:
    raise RuntimeError(f"Ожидался один общий селектор подписи, найдено {count}")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Селектор подписи метрики уточнён")
