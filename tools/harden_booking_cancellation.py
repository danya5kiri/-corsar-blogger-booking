#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

old = '''function getCancellationSourceFingerprint(booking){
  if(!booking) return "";

  var operation = String(booking.operation || "").trim().toLowerCase();
  var direct = booking.cancelBookingKey || booking.cancelsBookingKey || booking.deletedBookingKey;
  if(operation !== "cancel" && !direct) return "";
  if(direct) return decodeTransferFingerprint(direct);

  var previousDate = normalizeDate(booking.previousDate || booking.date);
  var previousTour = booking.previousTour || booking.tour;
  var creator = booking.previousTelegram || booking.telegram;
  return previousDate && previousTour && creator
    ? bookingFingerprint(previousDate, creator, previousTour)
    : "";
}'''

new = '''function getCancellationSourceFingerprint(booking){
  if(!booking) return "";

  var operation = String(booking.operation || "").trim().toLowerCase();
  var direct = booking.cancelBookingKey || booking.cancelsBookingKey || booking.deletedBookingKey;
  if(direct) return decodeTransferFingerprint(direct);

  var comment = String(booking.comment || "");
  var marker = comment.match(/\\[cancelBooking:([^\\]]+)\\]/i);
  if(marker) return decodeTransferFingerprint(marker[1]);
  if(operation !== "cancel") return "";

  var previousDate = normalizeDate(booking.previousDate || booking.date);
  var previousTour = booking.previousTour || booking.tour;
  var creator = booking.previousTelegram || booking.telegram;
  return previousDate && previousTour && creator
    ? bookingFingerprint(previousDate, creator, previousTour)
    : "";
}'''

if text.count(old) != 1:
    raise RuntimeError(f"Функция отмены: ожидалось 1 совпадение, найдено {text.count(old)}")
text = text.replace(old, new, 1)

old_hint = '    ? "Показаны только активные брони выбранного ника. После удаления место сразу освободится."'
new_hint = '    ? "Дата и тур берутся из выбранной ниже брони. Показаны только активные записи этого ника; после удаления место освободится."'
if text.count(old_hint) != 1:
    raise RuntimeError(f"Подсказка: ожидалось 1 совпадение, найдено {text.count(old_hint)}")
text = text.replace(old_hint, new_hint, 1)

required = [
    'comment.match(/\\[cancelBooking:([^\\]]+)\\]/i)',
    'if(operation !== "cancel") return "";',
    'Дата и тур берутся из выбранной ниже брони.',
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f"Не найден маркер: {marker}")

path.write_text(text, encoding="utf-8")
print("Отмена брони усилена")
