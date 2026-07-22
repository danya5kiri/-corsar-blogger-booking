#!/usr/bin/env python3
from pathlib import Path
import re

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text

section_ids = ["booking", "content", "calendar", "ranking", "results"]
blocks = {}
for section_id in section_ids:
    pattern = re.compile(
        rf'^  <section id="{re.escape(section_id)}"\b.*?^  </section>\n?',
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Не найден раздел: {section_id}")
    blocks[section_id] = match.group(0).rstrip() + "\n\n"

# Сохраняем стили и JavaScript побайтно: меняется только порядок HTML-секций и подписи.
style_before = text[text.index("<style>"):text.index("</style>") + len("</style>")]
script_before = text[text.index("<script>"):text.rindex("</script>") + len("</script>")]

# Удаляем исходные пять секций из их текущих мест.
for section_id in section_ids:
    text = text.replace(blocks[section_id].rstrip() + "\n", "", 1)

# Нумерация учитывает главную как первый экран: календарь становится вторым разделом.
kickers = {
    "calendar": "02 / Расписание",
    "booking": "03 / Бронирование",
    "content": "04 / Готовый материал",
    "ranking": "05 / Статистика",
    "results": "06 / Итоги туров",
}

def set_kicker(block: str, value: str) -> str:
    updated, count = re.subn(
        r'(<div class="cb-section-kicker">)[^<]*(</div>)',
        rf'\g<1>{value}\g<2>',
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"Не удалось заменить бейдж: {value}")
    return updated

for section_id, value in kickers.items():
    blocks[section_id] = set_kicker(blocks[section_id], value)

footer_marker = '  <footer id="creacloud" class="cb-footer">'
footer_index = text.index(footer_marker)
ordered_sections = "".join(
    blocks[section_id]
    for section_id in ["calendar", "booking", "content", "ranking", "results"]
)
text = text[:footer_index] + ordered_sections + text[footer_index:]

nav_pattern = re.compile(
    r'    <div class="cb-nav-links">\n.*?^    </div>',
    re.MULTILINE | re.DOTALL,
)
nav_replacement = '''    <div class="cb-nav-links">
      <a href="#home" data-section="home" class="is-active">Главная</a>
      <a href="#calendar" data-section="calendar">Календарь</a>
      <a href="#booking" data-section="booking">Запись</a>
      <a href="#content" data-section="content">Контент</a>
      <a href="#ranking" data-section="ranking">Рейтинг</a>
      <a href="#results" data-section="results">Итоги</a>
    </div>'''
text, nav_count = nav_pattern.subn(nav_replacement, text, count=1)
if nav_count != 1:
    raise RuntimeError("Не удалось обновить порядок навигации")

style_after = text[text.index("<style>"):text.index("</style>") + len("</style>")]
script_after = text[text.index("<script>"):text.rindex("</script>") + len("</script>")]
if style_before != style_after:
    raise RuntimeError("CSS был изменён")
if script_before != script_after:
    raise RuntimeError("JavaScript был изменён")

expected_order = ["home", "calendar", "booking", "content", "ranking", "results"]
positions = [text.index(f'<section id="{section_id}"') for section_id in expected_order]
if positions != sorted(positions):
    raise RuntimeError("Нарушен требуемый порядок разделов")

for section_id in expected_order:
    if text.count(f'<section id="{section_id}"') != 1:
        raise RuntimeError(f"Раздел {section_id} потерян или продублирован")

if text == original:
    print("Порядок уже актуален")
else:
    PATH.write_text(text, encoding="utf-8")
    print("Порядок разделов и нумерация обновлены")
