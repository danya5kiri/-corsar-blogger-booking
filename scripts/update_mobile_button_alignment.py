#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text

old_booking = '''.cb-link-button-booking {
  background: var(--cb-ink);
  color: #fff;
}'''
new_booking = '''.cb-link-button-booking {
  border-color: transparent;
  background: linear-gradient(105deg, var(--cb-coral) 0%, #ffad58 52%, var(--cb-yellow) 100%);
  color: #fff;
  box-shadow: 0 12px 28px rgba(255, 143, 118, .24);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-booking:hover,
.cb-link-button-booking:focus-visible {
  border-color: transparent;
  color: #fff;
  filter: saturate(1.06) brightness(1.02);
  box-shadow: 0 16px 32px rgba(255, 143, 118, .30);
}'''
if old_booking not in text:
    raise RuntimeError("Не найден текущий стиль кнопки записи")
text = text.replace(old_booking, new_booking, 1)

old_mobile = '''  .cb-link-button {
    width: 100%;
  }

  .cb-hero-stats {'''
new_mobile = '''  .cb-link-button {
    width: 100%;
  }

  .cb-link-button-sequenced {
    justify-content: flex-start;
    text-align: left;
  }

  .cb-hero-stats {'''
if old_mobile not in text:
    raise RuntimeError("Не найден мобильный блок кнопок")
text = text.replace(old_mobile, new_mobile, 1)

script_before = original[original.index("<script>"):original.rindex("</script>") + len("</script>")]
script_after = text[text.index("<script>"):text.rindex("</script>") + len("</script>")]
if script_before != script_after:
    raise RuntimeError("JavaScript был изменён")

for required in [
    'href="https://t.me/+nYzsW9t8e38xZGJi"',
    'href="#calendar"',
    'href="#content"',
    'id="cb-submit"',
    'id="cb-report-submit"',
    'https://script.google.com/macros/s/',
]:
    if original.count(required) != text.count(required):
        raise RuntimeError(f"Изменено количество ключевого элемента: {required}")

path.write_text(text, encoding="utf-8")
print("Мобильное выравнивание и оранжевый градиент обновлены")
