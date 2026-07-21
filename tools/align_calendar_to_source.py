#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import date, timedelta
from pathlib import Path

INDEX = Path("index.html")
SOURCE_COMMIT = "9beacbf4d17dded92684f9926c790bf4e6ebbe98"
SOURCE_PATH = "data/tours-sync.json"
START = "2026-07-22"
END = "2026-10-20"
EXPECTED_API = "https://script.google.com/macros/s/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/exec"

CANONICAL_TOURS = [
    "Барбекю на островах",
    "Вечерний круиз на яхте с саксофоном",
    "Путешествие на остров Рикорда",
    "Путешествие на остров Русский",
    "Отдых на катере с рыбалкой",
    "Путешествие на остров Шкота",
    'Прогулка "Архипелаг"',
    "Путешествие на остров Аскольд",
    "Вечерняя прогулка на катере с рассказами от капитана",
]


def matching_brace_end(text: str, start: int) -> int:
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


def extract_schedule(text: str) -> tuple[int, int, dict[str, list[str]]]:
    marker = "var TOURS_BY_DATE ="
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise RuntimeError("Не найден TOURS_BY_DATE")
    start = text.find("{", marker_pos)
    end = matching_brace_end(text, start)
    return start, end, json.loads(text[start:end])


def expected_dates() -> list[str]:
    current = date.fromisoformat(START)
    last = date.fromisoformat(END)
    result: list[str] = []
    while current <= last:
        result.append(current.isoformat())
        current += timedelta(days=1)
    return result


def source_snapshot() -> dict[str, object]:
    url = (
        "https://raw.githubusercontent.com/danya5kiri/-corsar-blogger-booking/"
        f"{SOURCE_COMMIT}/{SOURCE_PATH}"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "CorsarCalendarCheck/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8")
    payload = json.loads(raw)
    if payload.get("source") != "https://katermorekorsar.ru/tours":
        raise RuntimeError("Неверный источник контрольного расписания")
    return payload


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Ожидалось одно совпадение {label}, найдено: {count}")
    return text.replace(old, new, 1)


def main() -> None:
    original = INDEX.read_text(encoding="utf-8")
    api_before = re.search(r'API_URL:\s*"([^"]+)"', original)
    if not api_before or api_before.group(1) != EXPECTED_API:
        raise RuntimeError("API бронирований отличается от ожидаемого")

    start, end, current_schedule = extract_schedule(original)
    archive = {key: value for key, value in current_schedule.items() if key < START}
    archive_hash = hashlib.sha256(
        json.dumps(archive, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()

    snapshot = source_snapshot()
    source_schedule_all = snapshot.get("schedule")
    if not isinstance(source_schedule_all, dict):
        raise RuntimeError("В снимке отсутствует расписание")

    source_schedule = {
        key: value
        for key, value in source_schedule_all.items()
        if START <= key <= END
    }
    dates = expected_dates()
    if sorted(source_schedule) != dates:
        missing = sorted(set(dates) - set(source_schedule))
        extra = sorted(set(source_schedule) - set(dates))
        raise RuntimeError(f"Диапазон источника неполный: missing={missing}, extra={extra}")

    if any(
        re.search(r"(?:2\s*[-–—]?\s*[хx]?\s*[-–—]?\s*днев|двух\s*[-–—]?\s*днев|ноч[её]вк)", tour, re.I)
        for tours in source_schedule.values()
        for tour in tours
    ):
        raise RuntimeError("В однодневное расписание попал тур с ночёвкой")

    merged = dict(sorted({**archive, **source_schedule}.items()))
    schedule_json = json.dumps(merged, ensure_ascii=False, indent=2)
    updated = original[:start] + schedule_json + original[end:]

    canonical_start = updated.find("var CANONICAL_TOURS = [")
    canonical_end = updated.find("];", canonical_start)
    if canonical_start < 0 or canonical_end < 0:
        raise RuntimeError("Не найден CANONICAL_TOURS")
    canonical_end += 2
    canonical_text = "var CANONICAL_TOURS = " + json.dumps(CANONICAL_TOURS, ensure_ascii=False, indent=2) + ";"
    updated = updated[:canonical_start] + canonical_text + updated[canonical_end:]

    function_pattern = re.compile(r"function canonicalTourName\(v\)\{.*?\n\}", re.S)
    canonical_function = '''function canonicalTourName(v){
  var original = String(v || "").trim().replace(/\\s+/g, " ");
  var tour = original.toLowerCase().replace(/ё/g, "е");

  if(!tour) return "";
  if(tour.indexOf("барбекю") !== -1 || tour.indexOf("купальный круиз") !== -1) return CANONICAL_TOURS[0];
  if((tour.indexOf("вечерний круиз") !== -1 || tour.indexOf("саксофон") !== -1) && tour.indexOf("без саксофона") === -1) return CANONICAL_TOURS[1];
  if(tour.indexOf("рассказ") !== -1 || tour.indexOf("вечерняя прогулка на катере") !== -1 || tour.indexOf("без саксофона") !== -1) return CANONICAL_TOURS[8];
  if(/острова?\\s+рик[оа]рда/.test(tour)) return CANONICAL_TOURS[2];
  if(/острова?\\s+русск/.test(tour)) return CANONICAL_TOURS[3];
  if(tour.indexOf("отдых на катере") !== -1 && (tour.indexOf("рыбал") !== -1 || tour.indexOf("32") !== -1)) return CANONICAL_TOURS[4];
  if(tour.indexOf("остров шкота") !== -1) return CANONICAL_TOURS[5];
  if(tour.indexOf("архипелаг") !== -1 || (tour.indexOf("желтухин") !== -1 && tour.indexOf("карамзин") !== -1)) return CANONICAL_TOURS[6];
  if(tour.indexOf("остров аскольд") !== -1) return CANONICAL_TOURS[7];

  return original;
}'''
    updated, count = function_pattern.subn(lambda _match: canonical_function, updated, count=1)
    if count != 1:
        raise RuntimeError("Не удалось заменить canonicalTourName")

    updated = replace_once(
        updated,
        '<div class="cb-field-hint">Сначала показаны туры текущей даты. В группе «Добавить новый тур» доступны остальные однодневные программы сезона.</div>',
        '<div class="cb-field-hint">Показаны только программы из актуального расписания на выбранную дату.</div>',
        "подсказки формы",
    )

    old_render_fragment = '''  var scheduledTours = getToursByDate(date);
  var scheduledKeys = Object.create(null);
  var additionalTours = [];

  scheduledTours = scheduledTours.filter(function(tour){
    var key = normalizeTour(tour);
    if(!key || scheduledKeys[key]) return false;
    scheduledKeys[key] = true;
    return true;
  });

  additionalTours = getAllTours().filter(function(tour){
    return !scheduledKeys[normalizeTour(tour)];
  });

  var availableTours = scheduledTours.concat(additionalTours);'''
    new_render_fragment = '''  var scheduledTours = getToursByDate(date);
  var scheduledKeys = Object.create(null);

  scheduledTours = scheduledTours.filter(function(tour){
    var key = normalizeTour(tour);
    if(!key || scheduledKeys[key]) return false;
    scheduledKeys[key] = true;
    return true;
  });

  var availableTours = scheduledTours;'''
    updated = replace_once(updated, old_render_fragment, new_render_fragment, "списка доступных туров")
    updated = replace_once(
        updated,
        '  appendGroup("Туры по календарю", scheduledTours);\n  appendGroup("Добавить новый тур", additionalTours);',
        '  appendGroup("Туры по календарю", scheduledTours);',
        "группы дополнительных туров",
    )

    _, _, final_schedule = extract_schedule(updated)
    final_archive = {key: value for key, value in final_schedule.items() if key < START}
    final_archive_hash = hashlib.sha256(
        json.dumps(final_archive, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if final_archive_hash != archive_hash:
        raise RuntimeError("Архив расписания до 22.07 был изменён")
    if {key: final_schedule[key] for key in dates} != source_schedule:
        raise RuntimeError("Итоговое расписание не совпало с источником")
    if sorted(key for key in final_schedule if key >= START) != dates:
        raise RuntimeError("После 20.10 остались лишние даты")
    if 'BOOKING_START: "2026-07-22"' not in updated or 'SEASON_END: "2026-10-20"' not in updated:
        raise RuntimeError("Границы периода бронирования изменены")
    api_after = re.search(r'API_URL:\s*"([^"]+)"', updated)
    if not api_after or api_after.group(1) != EXPECTED_API:
        raise RuntimeError("API бронирований был изменён")
    for required in ("resolveEffectiveBookings", "fetchRemoteRows", "applyRemoteRows", "submitBooking", "submitReport"):
        if f"function {required}" not in updated:
            raise RuntimeError(f"Повреждена функция хранения данных: {required}")

    INDEX.write_text(updated, encoding="utf-8", newline="\n")
    print(json.dumps({
        "archivePreserved": True,
        "start": START,
        "end": END,
        "dateCount": len(dates),
        "tourCount": len({tour for tours in source_schedule.values() for tour in tours}),
        "apiPreserved": True,
        "unscheduledBookingOptionsRemoved": True,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
