#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = '<div class="cb-stat-label">Лидер по количеству уникальных туров</div>'
new = '<div class="cb-stat-label">Лидер по уникальным турам</div>'
count = text.count(old)
if count != 1:
    raise RuntimeError(f"Ожидалось одно совпадение заголовка, найдено: {count}")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
