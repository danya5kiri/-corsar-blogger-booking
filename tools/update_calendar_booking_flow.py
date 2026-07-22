#!/usr/bin/env python3
from pathlib import Path

PATH = Path("index.html")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Ожидалось одно совпадение: {label}; найдено {count}")
    return text.replace(old, new, 1)


text = PATH.read_text(encoding="utf-8")

text = replace_once(
    text,
    ".cb-details-card {\n  margin-top: 12px;\n  padding: 20px;",
    ".cb-details-card {\n  margin-top: 12px;\n  scroll-margin-top: 104px;\n  padding: 20px;",
    "отступ карточки деталей",
)

old_css = """.cb-window-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(23,23,25,.10);
  font-size: 13px;
  line-height: 1.4;
}

.cb-window-status {
  color: #287866;
  white-space: nowrap;
}

.cb-window-status.has-bookings {
  color: #ae4f40;
}
"""
new_css = """.cb-window-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(23,23,25,.10);
  font-size: 13px;
  line-height: 1.4;
}

.cb-window-status {
  color: #287866;
  white-space: nowrap;
}

.cb-window-action {
  min-width: 88px;
  min-height: 38px;
  padding: 0 12px;
  border: 1px solid rgba(40, 120, 102, .28);
  border-radius: 999px;
  background: rgba(255, 255, 255, .58);
  color: #287866;
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .035em;
  text-transform: uppercase;
  transition: transform .2s ease, background .2s ease, border-color .2s ease, box-shadow .2s ease;
}

.cb-window-action:hover,
.cb-window-action:focus-visible {
  transform: translateY(-1px);
  outline: 0;
  border-color: #287866;
  background: #fff;
  box-shadow: 0 8px 20px rgba(40, 120, 102, .12);
}

.cb-window-status.has-bookings,
.cb-window-action:disabled {
  border-color: rgba(174, 79, 64, .18);
  background: rgba(255, 255, 255, .34);
  color: #ae4f40;
  cursor: default;
  opacity: .72;
  transform: none;
  box-shadow: none;
}

.cb-details-card.is-revealed {
  animation: cb-details-reveal .36s ease both;
}

@keyframes cb-details-reveal {
  from { opacity: .62; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
"""
text = replace_once(text, old_css, new_css, "стили свободных окон")

old_click = """        if(active){
          cell.onclick = function(){
            setFormDate(date);
            renderTours(date);
            renderCalendar();
            renderDetails(date);
            setMessage("Выбрано: <b>" + formatDateRu(date) + "</b>. Теперь выберите тур.", false);
            var bookingSection = $("booking");
            if(bookingSection && window.innerWidth < 700) bookingSection.scrollIntoView({behavior: "smooth", block: "start"});
          };
        }
"""
new_click = """        if(active){
          cell.onclick = function(){
            setFormDate(date);
            renderTours(date);
            renderCalendar();
            renderDetails(date, true);
            setMessage("Выбрано: <b>" + formatDateRu(date) + "</b>. Нажмите «свободно» у нужного тура.", false);
            var detailsSection = $("cb-details");
            if(detailsSection){
              window.requestAnimationFrame(function(){
                detailsSection.scrollIntoView({behavior: "smooth", block: "start"});
              });
            }
          };
        }
"""
text = replace_once(text, old_click, new_click, "обработчик выбора даты")

old_details = """function renderDetails(date){
  var el = $("cb-details");
  if(!el) return;

  if(!date){
    el.innerHTML = '<h3>Выберите дату</h3><div class="cb-small">Покажем доступные туры и текущие записи.</div>';
    return;
  }

  var rows = getBookingsByDate(date);
  var tours = getToursByDate(date);

  var html = '<h3>' + escapeHtml(formatDateRu(date)) + '</h3>';

  if(tours.length){
    html += '<div class="cb-small" style="margin-bottom:12px">Программы и текущая занятость</div><div class="cb-window-list">';
    tours.forEach(function(tour){
      var tourCount = rows.filter(function(row){ return normalizeTour(row.tour) === normalizeTour(tour); }).length;
      var occupiedText = tourCount > 1
        ? "занято · " + tourCount + " " + pluralCount(tourCount, "запись", "записи", "записей")
        : "занято";
      html += '<div class="cb-window-row"><span>' + escapeHtml(tour) + '</span><span class="cb-window-status' + (tourCount ? ' has-bookings' : '') + '">' + (tourCount ? occupiedText : 'свободно') + '</span></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="cb-small">По расписанию на эту дату туров нет.</div>';
  }

  if(rows.length){
    html += '<h3 style="margin-top:20px">Кто уже записан</h3>';
    html += '<div class="cb-date-list">';
    rows.forEach(function(b){
      var tg = normalizeTelegram(b.telegram) || "без Telegram";
      var tour = b.tour || "тур не указан";
      html += '<div class="cb-date-row"><b>' + escapeHtml(tg) + '</b><span class="cb-tour-name">' + escapeHtml(tour) + '</span></div>';
    });
    html += '</div>';
  }

  el.innerHTML = html;
}
"""
new_details = """function renderDetails(date, animate){
  var el = $("cb-details");
  if(!el) return;

  if(!date){
    el.innerHTML = '<h3>Выберите дату</h3><div class="cb-small">Покажем доступные туры и текущие записи.</div>';
    return;
  }

  var rows = getBookingsByDate(date);
  var tours = getToursByDate(date);

  var html = '<h3>' + escapeHtml(formatDateRu(date)) + '</h3>';

  if(tours.length){
    html += '<div class="cb-small" style="margin-bottom:12px">Программы и текущая занятость · нажмите «свободно», чтобы перейти к записи</div><div class="cb-window-list">';
    tours.forEach(function(tour, tourIndex){
      var tourCount = rows.filter(function(row){ return normalizeTour(row.tour) === normalizeTour(tour); }).length;
      var occupied = tourCount > 0;
      var occupiedText = tourCount > 1
        ? "занято · " + tourCount + " " + pluralCount(tourCount, "запись", "записи", "записей")
        : "занято";
      var actionLabel = occupied ? "Тур занят: " + tour : "Выбрать свободный тур: " + tour;
      html += '<div class="cb-window-row"><span>' + escapeHtml(tour) + '</span>' +
        '<button type="button" class="cb-window-status cb-window-action' + (occupied ? ' has-bookings' : '') + '" data-tour-index="' + tourIndex + '" aria-label="' + escapeHtml(actionLabel) + '"' + (occupied ? ' disabled' : '') + '>' +
        (occupied ? occupiedText : 'свободно') + '</button></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="cb-small">По расписанию на эту дату туров нет.</div>';
  }

  if(rows.length){
    html += '<h3 style="margin-top:20px">Кто уже записан</h3>';
    html += '<div class="cb-date-list">';
    rows.forEach(function(b){
      var tg = normalizeTelegram(b.telegram) || "без Telegram";
      var tour = b.tour || "тур не указан";
      html += '<div class="cb-date-row"><b>' + escapeHtml(tg) + '</b><span class="cb-tour-name">' + escapeHtml(tour) + '</span></div>';
    });
    html += '</div>';
  }

  el.innerHTML = html;

  if(animate){
    el.classList.remove("is-revealed");
    void el.offsetWidth;
    el.classList.add("is-revealed");
  }

  Array.prototype.forEach.call(el.querySelectorAll(".cb-window-action:not(:disabled)"), function(action){
    action.onclick = function(){
      var tourIndex = Number(this.getAttribute("data-tour-index"));
      var chosenTour = tours[tourIndex];
      if(!chosenTour) return;

      if(hasBookingSlotConflict(date, chosenTour)){
        renderDetails(date, true);
        setMessage("Этот тур уже занят. Выберите другую свободную программу.", true);
        return;
      }

      setFormDate(date);
      renderTours(date);

      var tourSelect = $("cb-tour");
      if(tourSelect){
        var chosenKey = normalizeTour(chosenTour);
        Array.prototype.some.call(tourSelect.options, function(option){
          if(!option.disabled && normalizeTour(option.value) === chosenKey){
            tourSelect.value = option.value;
            return true;
          }
          return false;
        });
      }

      renderCalendar();
      renderDetails(date);
      renderTransferOptions();
      setMessage("Выбраны <b>" + formatDateRu(date) + "</b> и тур <b>" + escapeHtml(canonicalTourName(chosenTour)) + "</b>. Укажите ник креатора.", false);

      var bookingSection = $("booking");
      if(bookingSection) bookingSection.scrollIntoView({behavior: "smooth", block: "start"});
    };
  });
}
"""
text = replace_once(text, old_details, new_details, "карточка программ и занятости")

if 'API_URL: "https://script.google.com/macros/s/' not in text:
    raise RuntimeError("API_URL повреждён")
if "function submitBooking(){" not in text or "function submitReport(){" not in text:
    raise RuntimeError("Функции отправки форм повреждены")
if "var TOURS_BY_DATE = {" not in text:
    raise RuntimeError("Расписание повреждено")
if 'detailsSection.scrollIntoView({behavior: "smooth", block: "start"})' not in text:
    raise RuntimeError("Не настроен переход к программам")
if 'bookingSection.scrollIntoView({behavior: "smooth", block: "start"})' not in text:
    raise RuntimeError("Не настроен переход к бронированию")
if '.cb-window-action:not(:disabled)' not in text:
    raise RuntimeError("Не настроены активные свободные окна")

PATH.write_text(text, encoding="utf-8")
print("Календарный сценарий обновлён безопасно")
