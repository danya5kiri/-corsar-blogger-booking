#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

if 'class="cb-link-button cb-link-button-chat"' in text:
    raise SystemExit("Кнопка чата уже добавлена")

script_before = text[text.index("<script>"):]

css_marker = '''.cb-link-button-content:hover,
.cb-link-button-content:focus-visible {
  border-color: rgba(23, 23, 25, .28);
  background: #fff;
  color: var(--cb-ink);
  box-shadow: 0 16px 30px rgba(42, 45, 59, .15);
}

.cb-link-button:hover {
'''

css_replacement = '''.cb-link-button-content:hover,
.cb-link-button-content:focus-visible {
  border-color: rgba(23, 23, 25, .28);
  background: #fff;
  color: var(--cb-ink);
  box-shadow: 0 16px 30px rgba(42, 45, 59, .15);
}

.cb-link-button-chat {
  border-color: transparent;
  background: linear-gradient(105deg, var(--cb-blue) 0%, var(--cb-cyan) 66%, #8ce8f4 100%);
  color: #fff;
  box-shadow: 0 12px 28px rgba(37, 88, 200, .22);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-chat:hover,
.cb-link-button-chat:focus-visible {
  border-color: transparent;
  color: #fff;
  filter: saturate(1.08) brightness(1.03);
  box-shadow: 0 16px 32px rgba(37, 88, 200, .28);
}

.cb-link-button:hover {
'''

html_marker = '''          <a class="cb-link-button" href="#booking">Записаться на тур</a>
          <a class="cb-link-button cb-link-button-content" href="#content">Добавить контент</a>
'''

html_replacement = '''          <a class="cb-link-button" href="#booking">Записаться на тур</a>
          <a class="cb-link-button cb-link-button-content" href="#content">Добавить контент</a>
          <a class="cb-link-button cb-link-button-chat" href="https://t.me/+nYzsW9t8e38xZGJi" target="_blank" rel="noopener noreferrer">Вступить в чат</a>
'''

if text.count(css_marker) != 1:
    raise RuntimeError("Не найден точный CSS-маркер кнопок")
if text.count(html_marker) != 1:
    raise RuntimeError("Не найден точный HTML-блок кнопок")

text = text.replace(css_marker, css_replacement, 1)
text = text.replace(html_marker, html_replacement, 1)

script_after = text[text.index("<script>"):]
if script_after != script_before:
    raise RuntimeError("JavaScript был затронут")

checks = {
    "кнопка": text.count('class="cb-link-button cb-link-button-chat"') == 1,
    "ссылка": text.count('https://t.me/+nYzsW9t8e38xZGJi') == 1,
    "стиль": text.count('.cb-link-button-chat {') == 1,
    "бронирование": text.count('href="#booking">Записаться на тур</a>') == 1,
    "контент": text.count('href="#content">Добавить контент</a>') == 1,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError("Не пройдены проверки: " + ", ".join(failed))

path.write_text(text, encoding="utf-8")
print("Кнопка Telegram-чата добавлена; JavaScript не изменён")
