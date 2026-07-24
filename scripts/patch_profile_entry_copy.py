#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = "Поездки, уникальные программы, публикации, места в рейтингах и персональная рекомендация."
new = "Уникальные туры, ближайшая бронь, публикации и персональная рекомендация."

if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("Не найдено описание входа в мини-ЛК")

path.write_text(text, encoding="utf-8")
print("Описание мини-ЛК уточнено")
