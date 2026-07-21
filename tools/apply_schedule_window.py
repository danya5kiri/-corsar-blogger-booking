#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, timedelta
from pathlib import Path

INDEX = Path("index.html")
BOOKING_START = "2026-07-22"
SEASON_END = "2026-10-20"


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Ожидалось одно совпадение, найдено {count}: {old[:90]}")
    return text.replace(old, new, 1)


def object_end(text: str, start: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        char = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise RuntimeError("Не найден конец TOURS_BY_DATE")


def schedule_block(text: str) -> str:
    marker = "var TOURS_BY_DATE ="
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise RuntimeError("Не найден TOURS_BY_DATE")
    start = text.find("{", marker_pos)
    return text[start:object_end(text, start)]


def validate_schedule(text: str) -> None:
    schedule = json.loads(schedule_block(text))
    first = date.fromisoformat(BOOKING_START)
    last = date.fromisoformat(SEASON_END)
    expected = []
    cursor = first
    while cursor <= last:
        expected.append(cursor.isoformat())
        cursor += timedelta(days=1)
    missing = [day for day in expected if day not in schedule]
    if missing:
        raise RuntimeError(f"В расписании отсутствуют даты: {', '.join(missing[:10])}")
    if len(expected) != 91:
        raise RuntimeError(f"Неверное число дат периода: {len(expected)}")


def main() -> None:
    original = INDEX.read_text(encoding="utf-8")
    original_schedule_hash = hashlib.sha256(schedule_block(original).encode("utf-8")).hexdigest()
    original_api = re.search(r'API_URL:\s*"([^"]+)"', original)
    if not original_api:
        raise RuntimeError("Не найден API_URL")

    updated = original
    updated = replace_once(
        updated,
        '<input id="cb-date" type="date" min="2026-04-01" max="2026-10-01">',
        '<input id="cb-date" type="date" min="2026-07-22" max="2026-10-20">',
    )
    updated = replace_once(
        updated,
        '<div id="cb-season-caption" class="cb-season-caption">Сезон завершится 1 октября 2026 года.</div>',
        '<div id="cb-season-caption" class="cb-season-caption">Сезон завершится 20 октября 2026 года.</div>',
    )
    updated = replace_once(
        updated,
        '  SEASON_START: "2026-04-01",\n  SEASON_END: "2026-10-01",',
        '  SEASON_START: "2026-04-01",\n  BOOKING_START: "2026-07-22",\n  SEASON_END: "2026-10-20",',
    )
    updated = replace_once(
        updated,
        '  var seasonEnd = new Date(2026, 9, 1, 23, 59, 59);',
        '  var seasonEnd = new Date(2026, 9, 20, 23, 59, 59);',
    )
    updated = replace_once(
        updated,
        '    captionEl.textContent = "Старт 1 апреля · финиш 1 октября 2026 года";',
        '    captionEl.textContent = "Старт 1 апреля · финиш 20 октября 2026 года";',
    )
    updated = replace_once(
        updated,
        '  captionEl.textContent = "До 1 октября · сезон пройден на " + progress + "%";',
        '  captionEl.textContent = "До 20 октября · сезон пройден на " + progress + "%";',
    )
    updated = replace_once(
        updated,
        'function isBookableDate(date){\n  return isDateInSeason(date) && date >= getTodayKey();\n}',
        'function isBookableDate(date){\n  return isDateInSeason(date) && date >= CONFIG.BOOKING_START && date >= getTodayKey();\n}',
    )
    updated = replace_once(
        updated,
        '    setMessage("Дата должна быть в период с 1 апреля по 1 октября 2026 года.", true);',
        '    setMessage("Дата должна быть не позднее 20 октября 2026 года.", true);',
    )

    if hashlib.sha256(schedule_block(updated).encode("utf-8")).hexdigest() != original_schedule_hash:
        raise RuntimeError("Защитная проверка: блок расписания был изменён")
    updated_api = re.search(r'API_URL:\s*"([^"]+)"', updated)
    if not updated_api or updated_api.group(1) != original_api.group(1):
        raise RuntimeError("Защитная проверка: API_URL был изменён")

    validate_schedule(updated)

    protected_markers = [
        "function fetchRemoteRows(timeoutMs)",
        "function applyRemoteRows(allRows)",
        "function submitBooking()",
        "function submitReport()",
        "function resolveEffectiveBookings(rows)",
    ]
    for marker in protected_markers:
        if original.count(marker) != 1 or updated.count(marker) != 1:
            raise RuntimeError(f"Защитная проверка не пройдена: {marker}")

    INDEX.write_text(updated, encoding="utf-8", newline="\n")
    print("Период бронирования расширен: 22.07.2026–20.10.2026; 91 дата проверена")


if __name__ == "__main__":
    main()
