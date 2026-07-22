#!/usr/bin/env python3
from pathlib import Path
import re

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


config_before = re.search(r"var CONFIG = \{.*?\n\};", text, re.S).group(0)
tours_start = text.index("var TOURS_BY_DATE = {")
tours_end = text.index("\n};", tours_start) + 3
tours_before = text[tours_start:tours_end]
api_url_before = re.search(r'API_URL:\s*"([^"]+)"', text).group(1)

replace_once(
'''          <option value="new">Новая запись</option>
          <option value="transfer">Перенести существующую запись</option>
        </select>
        <div class="cb-field-hint">При переносе прежняя запись будет исключена из календаря, рейтинга и общей статистики.</div>''',
'''          <option value="new">Новая запись</option>
          <option value="transfer">Перенести существующую запись</option>
          <option value="cancel">Удалить бронирование</option>
        </select>
        <div class="cb-field-hint">Можно создать новую запись, перенести или удалить собственную активную бронь по указанному нику.</div>''',
"варианты действия"
)

replace_once(
'''      <div id="cb-transfer-source-field" class="cb-field cb-transfer-source-field" hidden>
        <label for="cb-transfer-source">Какую запись перенести</label>
        <select id="cb-transfer-source"><option value="">Сначала укажите существующий ник</option></select>
        <div class="cb-field-hint">Выберите прежнюю дату, а выше укажите новую дату и программу.</div>
      </div>
      <div class="cb-inline-note">На каждый тур в конкретную дату записывается только один креатор. При переносе прежняя запись автоматически освобождает место.</div>''',
'''      <div id="cb-transfer-source-field" class="cb-field cb-transfer-source-field" hidden>
        <label id="cb-transfer-source-label" for="cb-transfer-source">Какую запись перенести</label>
        <select id="cb-transfer-source"><option value="">Сначала укажите существующий ник</option></select>
        <div id="cb-transfer-source-hint" class="cb-field-hint">Выберите прежнюю дату, а выше укажите новую дату и программу.</div>
      </div>
      <div class="cb-inline-note">На каждый тур в конкретную дату записывается только один креатор. Перенос или удаление брони освобождает место и исключает прежнюю запись из рейтинга и статистики.</div>''',
"поле управления бронью"
)

old_render = '''function renderTransferOptions(){
  var mode = $("cb-booking-mode");
  var field = $("cb-transfer-source-field");
  var select = $("cb-transfer-source");
  var input = $("cb-telegram");
  var button = $("cb-submit");
  if(!mode || !field || !select) return;

  var isTransfer = mode.value === "transfer";
  field.hidden = !isTransfer;

  if(button && !bookingSubmitting){
    var buttonText = isTransfer ? "Сформировать перенос в WhatsApp" : "Сформировать заявку в WhatsApp";
    button.textContent = buttonText;
    button.setAttribute("data-idle-text", buttonText);
  }

  if(!isTransfer) return;

  var previousValue = select.value;
  var entries = getTransferableBookings(input ? input.value : "");
  select.innerHTML = "";

  var placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = entries.length ? "Выберите прежнюю запись" : "Нет записей, доступных для переноса";
  select.appendChild(placeholder);

  entries.forEach(function(booking){
    var option = document.createElement("option");
    option.value = bookingFingerprint(booking.date, booking.telegram, booking.tour);
    option.textContent = formatDateRu(normalizeDate(booking.date)) + " · " + canonicalTourName(booking.tour);
    select.appendChild(option);
  });

  select.disabled = !entries.length;
  if(entries.some(function(booking){
    return bookingFingerprint(booking.date, booking.telegram, booking.tour) === previousValue;
  })) select.value = previousValue;
}'''

new_render = '''function renderTransferOptions(){
  var mode = $("cb-booking-mode");
  var field = $("cb-transfer-source-field");
  var select = $("cb-transfer-source");
  var input = $("cb-telegram");
  var button = $("cb-submit");
  var label = $("cb-transfer-source-label");
  var hint = $("cb-transfer-source-hint");
  if(!mode || !field || !select) return;

  var isTransfer = mode.value === "transfer";
  var isCancel = mode.value === "cancel";
  var isExistingAction = isTransfer || isCancel;
  field.hidden = !isExistingAction;

  if(label) label.textContent = isCancel ? "Какую бронь удалить" : "Какую запись перенести";
  if(hint) hint.textContent = isCancel
    ? "Показаны только активные брони выбранного ника. После удаления место сразу освободится."
    : "Выберите прежнюю дату, а выше укажите новую дату и программу.";

  if(button && !bookingSubmitting){
    var buttonText = isCancel
      ? "Удалить бронь и открыть WhatsApp"
      : (isTransfer ? "Сформировать перенос в WhatsApp" : "Сформировать заявку в WhatsApp");
    button.textContent = buttonText;
    button.setAttribute("data-idle-text", buttonText);
  }

  if(!isExistingAction) return;

  var previousValue = select.value;
  var entries = getTransferableBookings(input ? input.value : "");
  select.innerHTML = "";

  var placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = entries.length
    ? (isCancel ? "Выберите бронь для удаления" : "Выберите прежнюю запись")
    : (isCancel ? "У этого ника нет активных броней" : "Нет записей, доступных для переноса");
  select.appendChild(placeholder);

  entries.forEach(function(booking){
    var option = document.createElement("option");
    option.value = bookingFingerprint(booking.date, booking.telegram, booking.tour);
    option.textContent = formatDateRu(normalizeDate(booking.date)) + " · " + canonicalTourName(booking.tour);
    select.appendChild(option);
  });

  select.disabled = !entries.length;
  if(entries.some(function(booking){
    return bookingFingerprint(booking.date, booking.telegram, booking.tour) === previousValue;
  })) select.value = previousValue;
}'''
replace_once(old_render, new_render, "отрисовка действий")

insert_before = '''function isKnownScheduleExclusion(date, tour){'''
cancellation_helper = '''function getCancellationSourceFingerprint(booking){
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
}

'''
replace_once(insert_before, cancellation_helper + insert_before, "распознавание отмены")

old_resolver = '''function resolveEffectiveBookings(rows){
  var unique = Object.create(null);

  (Array.isArray(rows) ? rows : []).forEach(function(booking, index){
    if(!booking || isInactiveBooking(booking) || isDeletedCreator(booking.telegram) || isKnownBookingCancellation(booking)) return;
    var key = bookingFingerprint(booking.date, booking.telegram, booking.tour);
    unique[key] = {booking: booking, index: index};
  });

  var transferred = Object.create(null);
  Object.keys(unique).forEach(function(key){
    var sourceKey = getTransferSourceFingerprint(unique[key].booking);
    if(sourceKey && sourceKey !== key) transferred[sourceKey] = true;
  });

  KNOWN_BOOKING_TRANSFERS.forEach(function(correction){
    var sourceKey = bookingFingerprint(correction.from.date, correction.from.telegram, correction.from.tour);
    var targetKey = bookingFingerprint(correction.to.date, correction.to.telegram, correction.to.tour);
    if(unique[sourceKey] && unique[targetKey]) transferred[sourceKey] = true;
  });

  return Object.keys(unique).map(function(key){
    return {key: key, booking: unique[key].booking, index: unique[key].index};
  }).filter(function(entry){
    return !transferred[entry.key];
  }).sort(function(a, b){
    return a.index - b.index;
  }).map(function(entry){
    return entry.booking;
  });
}'''

new_resolver = '''function resolveEffectiveBookings(rows){
  var unique = Object.create(null);
  var cancelledAt = Object.create(null);

  (Array.isArray(rows) ? rows : []).forEach(function(booking, index){
    if(!booking) return;

    var cancellationKey = getCancellationSourceFingerprint(booking);
    if(cancellationKey){
      cancelledAt[cancellationKey] = index;
      return;
    }

    if(isInactiveBooking(booking) || isDeletedCreator(booking.telegram) || isKnownBookingCancellation(booking)) return;
    var key = bookingFingerprint(booking.date, booking.telegram, booking.tour);
    unique[key] = {booking: booking, index: index};
  });

  var transferred = Object.create(null);
  Object.keys(unique).forEach(function(key){
    var sourceKey = getTransferSourceFingerprint(unique[key].booking);
    if(sourceKey && sourceKey !== key) transferred[sourceKey] = true;
  });

  KNOWN_BOOKING_TRANSFERS.forEach(function(correction){
    var sourceKey = bookingFingerprint(correction.from.date, correction.from.telegram, correction.from.tour);
    var targetKey = bookingFingerprint(correction.to.date, correction.to.telegram, correction.to.tour);
    if(unique[sourceKey] && unique[targetKey]) transferred[sourceKey] = true;
  });

  return Object.keys(unique).map(function(key){
    return {key: key, booking: unique[key].booking, index: unique[key].index};
  }).filter(function(entry){
    var cancellationIndex = cancelledAt[entry.key];
    var cancelledAfterBooking = typeof cancellationIndex === "number" && cancellationIndex >= entry.index;
    return !transferred[entry.key] && !cancelledAfterBooking;
  }).sort(function(a, b){
    return a.index - b.index;
  }).map(function(entry){
    return entry.booking;
  });
}'''
replace_once(old_resolver, new_resolver, "эффективные бронирования")

helper_anchor = '''function submitBooking(){'''
cancel_submitter = '''function submitBookingCancellation(tg, sourceFingerprint){
  if(!tg){
    setMessage("Введите Telegram.", true);
    return;
  }

  if(isDeletedCreator(tg)){
    setMessage("Этот профиль удалён и недоступен для управления бронированиями.", true);
    return;
  }

  var knownCreator = findCreatorEntry(tg, getKnownCreatorDirectory());
  if(!knownCreator){
    setCreatorIdentityState("cb-telegram", "cb-booking-creator-state", getKnownCreatorDirectory(), "booking");
    setMessage("Для удаления выберите существующий ник креатора из подсказок.", true);
    return;
  }

  tg = knownCreator.name;
  $("cb-telegram").value = tg;

  var source = findBookingByFingerprint(sourceFingerprint);
  if(!source || normalizeTelegram(source.telegram) !== tg){
    setMessage("Выберите активную бронь, принадлежащую указанному нику.", true);
    renderTransferOptions();
    return;
  }

  var cancellationText = formatDateRu(normalizeDate(source.date)) + " — " + canonicalTourName(source.tour);
  if(!window.confirm("Удалить бронь " + cancellationText + " для " + tg + "?")) return;

  var submissionFingerprint = "cancel:" + sourceFingerprint;
  if(wasRecentlySubmitted(BOOKING_STORAGE_KEY, submissionFingerprint)){
    setMessage("Удаление этой брони уже отправлено.", true);
    return;
  }

  bookingSubmitting = true;
  setSubmitBusy("cb-submit", true, "Проверяем бронь...");
  setMessage("Проверяем актуальную бронь...", false);

  refreshRemoteDataForCheck()
    .then(function(){
      var refreshedCreator = findCreatorEntry(tg, getKnownCreatorDirectory());
      if(refreshedCreator) tg = refreshedCreator.name;

      source = findBookingByFingerprint(sourceFingerprint);
      if(!source || normalizeTelegram(source.telegram) !== tg){
        bookingSubmitting = false;
        setSubmitBusy("cb-submit", false, "");
        renderDataViews();
        setMessage("Эта бронь уже изменена или не принадлежит указанному нику.", true);
        return;
      }

      if(wasRecentlySubmitted(BOOKING_STORAGE_KEY, submissionFingerprint)){
        bookingSubmitting = false;
        setSubmitBusy("cb-submit", false, "");
        setMessage("Удаление этой брони уже отправлено.", true);
        return;
      }

      var sourceDate = normalizeDate(source.date);
      var sourceTour = String(source.tour || "").trim();
      var payload = {
        date: sourceDate,
        telegram: tg,
        tour: sourceTour,
        name: "",
        phone: "",
        count: 1,
        participants: 1,
        status: "Отмена",
        operation: "cancel",
        cancelBookingKey: sourceFingerprint,
        previousDate: sourceDate,
        previousTour: sourceTour,
        previousTelegram: tg,
        comment: "Удаление бронирования креатором [cancelBooking:" + encodeURIComponent(sourceFingerprint) + "]",
        dedupeKey: submissionFingerprint,
        requestId: "cancel-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8)
      };

      setSubmitBusy("cb-submit", true, "Удаляем бронь...");
      setMessage("Удаляем бронь...", false);

      fetch(CONFIG.API_URL, {
        method: "POST",
        mode: "no-cors",
        body: JSON.stringify(payload)
      })
      .then(function(){
        bookings = resolveEffectiveBookings(bookings.concat([payload]));
        rememberSubmission(BOOKING_STORAGE_KEY, submissionFingerprint);
        $("cb-telegram").value = "";
        if($("cb-booking-mode")) $("cb-booking-mode").value = "new";
        if($("cb-transfer-source")) $("cb-transfer-source").value = "";
        bookingSubmitting = false;
        renderDataViews();
        setSubmitBusy("cb-submit", false, "");
        renderTransferOptions();

        var text = [
          "Здравствуйте! Креатор удалил бронирование на морскую поездку.",
          "",
          "Креатор: " + tg,
          "Дата: " + formatDateRu(sourceDate),
          "Тур: " + canonicalTourName(sourceTour),
          "",
          "Прошу учесть отмену бронирования."
        ].join("\\n");
        var whatsappUrl = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);

        setMessage("Бронь удалена. Место освобождено; открываем WhatsApp.", false);
        setTimeout(function(){ window.location.href = whatsappUrl; }, 650);
      })
      .catch(function(){
        bookingSubmitting = false;
        setSubmitBusy("cb-submit", false, "");
        setMessage("Не удалось удалить бронь. Повторите попытку.", true);
      });
    })
    .catch(function(){
      bookingSubmitting = false;
      setSubmitBusy("cb-submit", false, "");
      setMessage("Не удалось проверить актуальную бронь. Обновите страницу и попробуйте ещё раз.", true);
    });
}

'''
replace_once(helper_anchor, cancel_submitter + helper_anchor, "отправка удаления")

replace_once(
'''  var mode = $("cb-booking-mode") && $("cb-booking-mode").value === "transfer" ? "transfer" : "new";''',
'''  var selectedMode = $("cb-booking-mode") ? String($("cb-booking-mode").value || "") : "";
  var mode = selectedMode === "transfer" ? "transfer" : (selectedMode === "cancel" ? "cancel" : "new");''',
"чтение режима"
)

replace_once(
'''  if(bookingSubmitting){
    setMessage("Заявка уже обрабатывается.", true);
    return;
  }

  if(!date){''',
'''  if(bookingSubmitting){
    setMessage("Заявка уже обрабатывается.", true);
    return;
  }

  if(mode === "cancel"){
    submitBookingCancellation(tg, sourceFingerprint);
    return;
  }

  if(!date){''',
"ветка удаления"
)

config_after = re.search(r"var CONFIG = \{.*?\n\};", text, re.S).group(0)
tours_start_after = text.index("var TOURS_BY_DATE = {")
tours_end_after = text.index("\n};", tours_start_after) + 3
tours_after = text[tours_start_after:tours_end_after]
api_url_after = re.search(r'API_URL:\s*"([^"]+)"', text).group(1)

if config_after != config_before or tours_after != tours_before or api_url_after != api_url_before:
    raise RuntimeError("Расписание, CONFIG или API были изменены")

required = [
    '<option value="cancel">Удалить бронирование</option>',
    'operation: "cancel"',
    'cancelBookingKey: sourceFingerprint',
    'normalizeTelegram(source.telegram) !== tg',
    'Удалить бронь и открыть WhatsApp',
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f"Не найден обязательный маркер: {marker}")

if text == original:
    raise RuntimeError("index.html не изменён")

PATH.write_text(text, encoding="utf-8")
print("Логика удаления брони добавлена безопасно")
