#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = "grid-template-columns: minmax(190px, .9fr) minmax(280px, 1.1fr);"
new = "grid-template-columns: minmax(160px, .85fr) minmax(0, 1.15fr);"

if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("Не найден ожидаемый desktop-селектор мини-ЛК")

path.write_text(text, encoding="utf-8")
print("Адаптивная ширина мини-ЛК проверена")
