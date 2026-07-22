#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = '''@media (min-width: 901px) {
  .cb-hero-actions {
'''
new = '''@media (min-width: 901px) {
  .cb-route-line {
    bottom: clamp(170px, 18vw, 220px);
  }

  .cb-hero-actions {
'''
count = text.count(old)
if count != 1:
    raise RuntimeError(f"Ожидалось одно место для desktop-правки, найдено {count}")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Декоративная линия поднята только в desktop-разметке")
