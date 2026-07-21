#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

API_URL = "https://script.google.com/macros/s/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/exec"
OUT = Path("unmatched-content-audit.json")

ALIASES = {"@a4anaseva": "@a4fanaseva"}
DELETED = {"@ник", "@тест", "@nik", "@test"}
INACTIVE = {"отмена", "не пришел", "не пришёл", "отменено", "cancelled", "canceled"}

CANONICAL = [
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


def normalize_telegram(value: object) -> str:
    tg = re.sub(r"\s+", "", str(value or "").strip().lower())
    if tg and not tg.startswith("@"):
        tg = "@" + tg
    return ALIASES.get(tg, tg)


def canonical_tour(value: object) -> str:
    original = re.sub(r"\s+", " ", str(value or "").strip())
    tour = original.lower().replace("ё", "е")
    if not tour:
        return ""
    if "барбекю" in tour or "купальный круиз" in tour:
        return CANONICAL[0]
    if ("вечерний круиз" in tour or "саксофон" in tour) and "без саксофона" not in tour:
        return CANONICAL[1]
    if "рассказ" in tour or "вечерняя прогулка на катере" in tour or "без саксофона" in tour:
        return CANONICAL[8]
    if re.search(r"острова?\s+рик[оа]рда", tour):
        return CANONICAL[2]
    if re.search(r"острова?\s+русск", tour):
        return CANONICAL[3]
    if "отдых на катере" in tour and ("рыбал" in tour or "32" in tour):
        return CANONICAL[4]
    if "остров шкота" in tour:
        return CANONICAL[5]
    if "архипелаг" in tour or ("желтухин" in tour and "карамзин" in tour):
        return CANONICAL[6]
    if "остров аскольд" in tour:
        return CANONICAL[7]
    return original


def normalize_tour(value: object) -> str:
    return re.sub(r"\s+", " ", canonical_tour(value).lower())


def normalize_date(value: object) -> str:
    raw = str(value or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw
    if raw:
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    return raw


def fetch_rows() -> list[dict]:
    callback = "auditCallback"
    url = API_URL + "?" + urllib.parse.urlencode({"callback": callback, "t": "audit"})
    request = urllib.request.Request(url, headers={"User-Agent": "corsar-content-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8-sig")
    match = re.search(r"^[^(]+\((.*)\)\s*;?\s*$", text, re.S)
    if not match:
        raise RuntimeError("API не вернул JSONP")
    rows = json.loads(match.group(1))
    if not isinstance(rows, list):
        raise RuntimeError("API вернул не массив")
    return [row for row in rows if isinstance(row, dict)]


def main() -> None:
    rows = fetch_rows()
    bookings = []
    reports = []
    for row in rows:
        if row.get("type") == "content_report":
            reports.append(row)
            continue
        status = str(row.get("status") or "").strip().lower()
        tg = normalize_telegram(row.get("telegram"))
        if status in INACTIVE or not tg or tg in DELETED:
            continue
        bookings.append(row)

    by_creator_tour: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for booking in bookings:
        key = (normalize_telegram(booking.get("telegram")), normalize_tour(booking.get("tour")))
        if key[0] and key[1]:
            by_creator_tour[key].append(booking)

    for values in by_creator_tour.values():
        values.sort(key=lambda row: normalize_date(row.get("date")), reverse=True)

    unresolved = []
    resolved = []
    not_found_reports = []
    for report in reports:
        status = str(report.get("matchStatus") or "").strip()
        if status != "Запись не найдена":
            continue
        tg = normalize_telegram(report.get("telegram") or report.get("creator") or report.get("nickname") or report.get("name"))
        tour = normalize_tour(report.get("tour") or report.get("tourName"))
        item = {
            "telegram": tg,
            "reportTour": report.get("tour") or report.get("tourName"),
            "reportDate": normalize_date(report.get("date")),
            "link": report.get("link") or report.get("url") or report.get("contentUrl"),
            "createdAt": report.get("createdAt"),
        }
        not_found_reports.append(item)
        matches = by_creator_tour.get((tg, tour), [])
        if matches:
            match = matches[0]
            item = dict(item)
            item.update({
                "matchedDate": normalize_date(match.get("date")),
                "matchedTour": match.get("tour"),
                "matchedTelegram": normalize_telegram(match.get("telegram")),
            })
            resolved.append(item)
        else:
            unresolved.append(item)

    result = {
        "totalRows": len(rows),
        "bookingRows": len(bookings),
        "contentRows": len(reports),
        "notFoundCount": len(not_found_reports),
        "resolvedCount": len(resolved),
        "unresolvedCount": len(unresolved),
        "resolved": resolved,
        "unresolved": unresolved,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("notFoundCount", "resolvedCount", "unresolvedCount")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
