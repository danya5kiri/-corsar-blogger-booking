#!/usr/bin/env python3
from pathlib import Path

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text

old_actions = '''        <div class="cb-hero-actions">
          <a class="cb-link-button" href="#booking">Записаться на тур</a>
          <a class="cb-link-button cb-link-button-content" href="#content">Добавить контент</a>
          <a class="cb-link-button cb-link-button-chat" href="https://t.me/+nYzsW9t8e38xZGJi" target="_blank" rel="noopener noreferrer">Вступить в чат</a>
        </div>'''

new_actions = '''        <div class="cb-hero-actions">
          <a class="cb-link-button cb-link-button-chat cb-link-button-sequenced" href="https://t.me/+nYzsW9t8e38xZGJi" target="_blank" rel="noopener noreferrer"><span class="cb-link-button-step" aria-hidden="true">1</span><span>Вступить в чат</span></a>
          <a class="cb-link-button cb-link-button-booking cb-link-button-sequenced" href="#calendar"><span class="cb-link-button-step" aria-hidden="true">2</span><span>Записаться на тур</span></a>
          <a class="cb-link-button cb-link-button-content cb-link-button-sequenced" href="#content"><span class="cb-link-button-step" aria-hidden="true">3</span><span>Добавить контент</span></a>
        </div>'''

if old_actions not in text:
    raise RuntimeError("Не найден исходный блок кнопок на главной")
text = text.replace(old_actions, new_actions, 1)

old_primary = '''.cb-link-button:first-child {
  background: var(--cb-ink);
  color: #fff;
}'''
new_primary = '''.cb-link-button-booking {
  background: var(--cb-ink);
  color: #fff;
}'''
if old_primary not in text:
    raise RuntimeError("Не найден стиль основной кнопки")
text = text.replace(old_primary, new_primary, 1)

base_button_end = '''  font-weight: 750;
  transition: transform .2s ease, background .2s ease, color .2s ease;
}

.cb-link-button-booking {'''
sequence_styles = '''  font-weight: 750;
  transition: transform .2s ease, background .2s ease, color .2s ease;
}

.cb-link-button-sequenced {
  gap: 12px;
  white-space: nowrap;
}

.cb-link-button-step {
  display: inline-flex;
  flex: 0 0 22px;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: 1px solid currentColor;
  color: inherit;
  font-size: 10px;
  font-weight: 850;
  line-height: 1;
  opacity: .76;
}

.cb-link-button-booking {'''
if base_button_end not in text:
    raise RuntimeError("Не найдено место для стилей последовательности")
text = text.replace(base_button_end, sequence_styles, 1)

# Гарантируем, что функциональная часть сайта осталась побайтно прежней.
script_before = original[original.index("<script>"):original.rindex("</script>") + len("</script>")]
script_after = text[text.index("<script>"):text.rindex("</script>") + len("</script>")]
if script_before != script_after:
    raise RuntimeError("JavaScript был изменён")

for required in [
    'id="calendar"',
    'id="booking"',
    'id="content"',
    'id="cb-submit"',
    'id="cb-report-submit"',
    'https://script.google.com/macros/s/',
]:
    if original.count(required) != text.count(required):
        raise RuntimeError(f"Изменено количество ключевого элемента: {required}")

PATH.write_text(text, encoding="utf-8")
print("Навигационные кнопки главной обновлены")
