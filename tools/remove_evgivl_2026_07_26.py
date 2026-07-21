#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

INDEX = Path("index.html")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Ожидалось одно совпадение {label}, найдено: {count}")
    return text.replace(old, new, 1)


def main() -> None:
    original = INDEX.read_text(encoding="utf-8")
    updated = original

    transfer_block = '''var KNOWN_BOOKING_TRANSFERS = [{
  from: {
    date: "2026-07-23",
    telegram: "@a4fanaseva",
    tour: "Путешествие на остров Аскольд на катере 32ft"
  },
  to: {
    date: "2026-07-29",
    telegram: "@a4fanaseva",
    tour: "Путешествие на остров Аскольд на катере 32ft"
  }
}];'''

    corrections_block = transfer_block + '''
var KNOWN_SCHEDULE_EXCLUSIONS = [{
  date: "2026-07-26",
  tour: "Барбекю на островах"
}];
var KNOWN_BOOKING_CANCELLATIONS = [{
  date: "2026-07-26",
  telegram: "@evgivl",
  tour: "Барбекю на островах"
}];'''
    updated = replace_once(updated, transfer_block, corrections_block, "блока корректировок")

    transfer_function_end = '''function getTransferSourceFingerprint(booking){
  if(!booking) return "";

  var direct = booking.transferFromKey || booking.replacesBookingKey || booking.previousBookingKey;
  if(direct) return decodeTransferFingerprint(direct);

  var previousDate = normalizeDate(booking.previousDate || booking.fromDate);
  var previousTour = booking.previousTour || booking.fromTour;
  var creator = booking.previousTelegram || booking.fromTelegram || booking.telegram;
  if(previousDate && previousTour && creator){
    return bookingFingerprint(previousDate, creator, previousTour);
  }

  var comment = String(booking.comment || "");
  var marker = comment.match(/\\[transferFrom:([^\\]]+)\\]/i);
  return marker ? decodeTransferFingerprint(marker[1]) : "";
}'''

    helper_functions = transfer_function_end + '''

function isKnownScheduleExclusion(date, tour){
  var slot = bookingSlotFingerprint(date, tour);
  return KNOWN_SCHEDULE_EXCLUSIONS.some(function(correction){
    return bookingSlotFingerprint(correction.date, correction.tour) === slot;
  });
}

function isKnownBookingCancellation(booking){
  if(!booking) return false;
  var key = bookingFingerprint(booking.date, booking.telegram, booking.tour);
  return KNOWN_BOOKING_CANCELLATIONS.some(function(correction){
    return bookingFingerprint(correction.date, correction.telegram, correction.tour) === key;
  });
}'''
    updated = replace_once(updated, transfer_function_end, helper_functions, "функции корректировок")

    old_resolve_guard = '''    if(!booking || isInactiveBooking(booking) || isDeletedCreator(booking.telegram)) return;
    var key = bookingFingerprint(booking.date, booking.telegram, booking.tour);'''
    new_resolve_guard = '''    if(!booking || isInactiveBooking(booking) || isDeletedCreator(booking.telegram) || isKnownBookingCancellation(booking)) return;
    var key = bookingFingerprint(booking.date, booking.telegram, booking.tour);'''
    updated = replace_once(updated, old_resolve_guard, new_resolve_guard, "фильтра отменённых записей")

    old_schedule_filter = '''  return (TOURS_BY_DATE[date] || []).filter(function(tour){
    return !isExcludedTour(tour);
  });'''
    new_schedule_filter = '''  return (TOURS_BY_DATE[date] || []).filter(function(tour){
    return !isExcludedTour(tour) && !isKnownScheduleExclusion(date, tour);
  });'''
    updated = replace_once(updated, old_schedule_filter, new_schedule_filter, "фильтра расписания")

    date_match = re.search(r'"2026-07-26"\s*:\s*\[(.*?)\n\s*\]', updated, re.S)
    if not date_match:
        raise RuntimeError("Не найдена дата 2026-07-26")
    if "Барбекю" in date_match.group(1):
        raise RuntimeError("Барбекю осталось в массиве расписания на 26.07")

    for token in (
        'date: "2026-07-26"',
        'telegram: "@evgivl"',
        'tour: "Барбекю на островах"',
        "isKnownScheduleExclusion(date, tour)",
        "isKnownBookingCancellation(booking)",
    ):
        if token not in updated:
            raise RuntimeError(f"Не применена корректировка: {token}")

    INDEX.write_text(updated, encoding="utf-8", newline="\n")
    print("Запись @evgivl 26.07 на барбекю исключена; барбекю на эту дату заблокировано")


if __name__ == "__main__":
    main()
