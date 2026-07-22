#!/usr/bin/env python3
from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


# Убираем экспериментальные переменные visualViewport.
replace_once(
    "  --cb-line: #e3e5eb;\n  --cb-visual-center-y: 50svh;\n  --cb-visual-bottom-gap: 0px;",
    "  --cb-line: #e3e5eb;",
    "CSS-переменные visualViewport",
)

# Возвращаем центрирование загрузчика средствами самого полноэкранного контейнера.
old_splash_inner = '''.cb-splash-inner {
  position: fixed;
  z-index: 1;
  top: var(--cb-visual-center-y, 50svh);
  left: 50%;
  display: flex;
  width: min(680px, calc(100vw - 48px));
  flex-direction: column;
  align-items: center;
  text-align: center;
  transform: translate(-50%, -50%);
}'''
new_splash_inner = '''.cb-splash-inner {
  position: relative;
  z-index: 1;
  display: flex;
  width: min(680px, calc(100vw - 48px));
  flex-direction: column;
  align-items: center;
  text-align: center;
}'''
replace_once(old_splash_inner, new_splash_inner, "центрирование загрузчика")

# Полностью убираем CSS внутрисайтового еженедельного уведомления.
css_start = text.find("\nbody.cb-push-open {")
css_end = text.find("\n.cb-message {", css_start)
if css_start < 0 or css_end < 0:
    raise RuntimeError("не найден CSS-блок еженедельного уведомления")
text = text[:css_start] + text[css_end:]

# Сообщения действий оставляем в стабильном левом нижнем углу без visualViewport.
old_mobile_message = '''  .cb-message {
    right: auto;
    bottom: calc(var(--cb-visual-bottom-gap, 0px) + 14px);
    left: 14px;
    width: auto;
    max-width: min(300px, calc(100vw - 28px));
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.42;
    transform: translate(-8px, 10px);
  }

  .cb-message.is-visible {
    transform: translate(0, 0);
  }'''
new_mobile_message = '''  .cb-message {
    right: auto;
    bottom: calc(14px + env(safe-area-inset-bottom));
    left: 14px;
    width: auto;
    max-width: min(300px, calc(100vw - 28px));
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.42;
    transform: translateY(10px);
  }

  .cb-message.is-visible {
    transform: translateY(0);
  }'''
replace_once(old_mobile_message, new_mobile_message, "мобильное служебное сообщение")

# Убираем HTML уведомления. Служебный toast остаётся на месте.
modal_start = text.find('<div id="cb-weekly-push"')
message_start = text.find('<div id="cb-message"', modal_start)
if modal_start < 0 or message_start < 0:
    raise RuntimeError("не найден HTML-блок еженедельного уведомления")
text = text[:modal_start] + text[message_start:]

# Убираем переменные уведомления.
for line in [
    'var WEEKLY_PUSH_STORAGE_KEY = "corsar_weekly_push_seen_v1";\n',
    'var WEEKLY_PUSH_TEST_DATE = "2026-07-22";\n',
    'var weeklyPushTimer = null;\n',
    'var weeklyPushRestoreFocus = null;\n',
]:
    if text.count(line) != 1:
        raise RuntimeError(f"не найдена переменная для удаления: {line.strip()}")
    text = text.replace(line, "", 1)

# Убираем расчёт visualViewport целиком.
visual_pattern = re.compile(
    r'\nfunction syncVisualViewportMetrics\(\)\{.*?\n\}\n\nfunction setupStickyNav\(\)\{',
    re.S,
)
text, visual_count = visual_pattern.subn('\nfunction setupStickyNav(){', text, count=1)
if visual_count != 1:
    raise RuntimeError(f"visualViewport-блок: ожидалось 1 совпадение, найдено {visual_count}")

# Убираем всю логику еженедельного уведомления.
push_pattern = re.compile(
    r'\nvar weeklyPushScrollY = 0;.*?\nfunction renderSeasonMetrics\(\)\{',
    re.S,
)
text, push_count = push_pattern.subn('\nfunction renderSeasonMetrics(){', text, count=1)
if push_count != 1:
    raise RuntimeError(f"JS-блок уведомления: ожидалось 1 совпадение, найдено {push_count}")

# Убираем вызовы экспериментальных функций.
for call in [
    '  setupVisualViewportMetrics();\n',
    '  setupWeeklyPush();\n',
]:
    if text.count(call) != 1:
        raise RuntimeError(f"вызов {call.strip()}: ожидалось 1 совпадение, найдено {text.count(call)}")
    text = text.replace(call, "", 1)

schedule_count = len(re.findall(r'^\s*scheduleWeeklyPush\(\);\s*$', text, re.M))
if schedule_count < 1:
    raise RuntimeError("не найден ни один вызов scheduleWeeklyPush")
text = re.sub(r'^\s*scheduleWeeklyPush\(\);\s*\n', '', text, flags=re.M)

if text == original:
    raise RuntimeError("index.html не изменён")

path.write_text(text, encoding="utf-8")
print("mobile regression overlay removed")
