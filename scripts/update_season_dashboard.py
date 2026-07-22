#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


season_days_old = '''.cb-season-days {
  color: inherit;
}
'''
season_days_new = '''.cb-season-days {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 48px;
  color: inherit;
}

.cb-season-days.is-ended {
  font-size: clamp(22px, 2.8vw, 34px);
  letter-spacing: -.045em;
}

.cb-season-ended {
  font-weight: 820;
}

.cb-season-sunset {
  width: 58px;
  height: 34px;
  flex: 0 0 auto;
  overflow: visible;
  filter: drop-shadow(0 7px 11px rgba(104, 77, 165, .14));
}

.cb-season-sunset-arc {
  fill: none;
  stroke: rgba(127, 103, 248, .34);
  stroke-width: 1.5;
  stroke-dasharray: 2.5 3.5;
}

.cb-season-sunset-horizon {
  fill: none;
  stroke: rgba(37, 88, 200, .52);
  stroke-width: 1.7;
  stroke-linecap: round;
}

.cb-season-sunset-sun {
  fill: var(--cb-yellow);
  stroke: var(--cb-coral);
  stroke-width: 1.6;
}
'''
replace_once(season_days_old, season_days_new, "стили счётчика сезона")

metric_old = '''.cb-season-metric strong {
  display: block;
  font-size: clamp(20px, 2.2vw, 28px);
  font-weight: 820;
  line-height: 1;
  letter-spacing: -.045em;
}
'''
metric_new = '''.cb-season-metric strong {
  display: flex;
  align-items: flex-start;
  gap: 3px;
  font-size: clamp(20px, 2.2vw, 28px);
  font-weight: 820;
  line-height: 1;
  letter-spacing: -.045em;
}

.cb-season-delta {
  position: relative;
  top: -.16em;
  color: var(--cb-blue);
  font-size: 10px;
  font-weight: 850;
  line-height: 1;
  letter-spacing: -.02em;
}

.cb-season-delta.is-zero {
  color: #8a8f99;
}
'''
replace_once(metric_old, metric_new, "стили сегодняшних прибавлений")

counter_old = '''function updateSeasonCounter(){
  var daysEl = $("cb-season-days");
  var fillEl = $("cb-season-fill");
  var captionEl = $("cb-season-caption");

  if(!daysEl || !fillEl || !captionEl) return;

  var seasonStart = new Date(2026, 3, 1);
  var seasonEnd = new Date(2026, 9, 20, 23, 59, 59);
  var now = new Date();

  var totalMs = seasonEnd.getTime() - seasonStart.getTime();
  var passedMs = now.getTime() - seasonStart.getTime();
  var leftMs = seasonEnd.getTime() - now.getTime();

  var daysLeft = Math.ceil(leftMs / 86400000);
  var progress = Math.round((passedMs / totalMs) * 100);

  if(now < seasonStart){
    var daysToStart = Math.ceil((seasonStart.getTime() - now.getTime()) / 86400000);
    daysEl.innerHTML = "<strong>" + daysToStart + "</strong> дн.";
    fillEl.style.width = "0%";
    captionEl.textContent = "Старт 1 апреля · финиш 20 октября 2026 года";
    return;
  }

  if(now > seasonEnd){
    daysEl.textContent = "Сезон завершён";
    fillEl.style.width = "100%";
    captionEl.textContent = "Новый сезон уже готовится";
    return;
  }

  progress = Math.max(0, Math.min(100, progress));
  daysLeft = Math.max(0, daysLeft);

  daysEl.innerHTML = "<strong>" + daysLeft + "</strong> дн.";
  fillEl.style.width = progress + "%";
  captionEl.textContent = "До 20 октября · сезон пройден на " + progress + "%";
}
'''
counter_new = '''function seasonSunsetIcon(progress, ended){
  var value = Math.max(0, Math.min(100, Number(progress) || 0)) / 100;
  var x = 8 + 40 * value;
  var y = ended ? 24.5 : 23 - 42 * value + 42 * value * value;
  return '<svg class="cb-season-sunset" viewBox="0 0 56 34" aria-hidden="true" focusable="false">' +
    '<path class="cb-season-sunset-arc" d="M8 23 Q28 2 48 23"/>' +
    '<path class="cb-season-sunset-horizon" d="M4 25h48M11 29h34"/>' +
    '<circle class="cb-season-sunset-sun" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="5.2"/>' +
  '</svg>';
}

function updateSeasonCounter(){
  var daysEl = $("cb-season-days");
  var fillEl = $("cb-season-fill");
  var captionEl = $("cb-season-caption");

  if(!daysEl || !fillEl || !captionEl) return;

  var seasonStart = new Date(2026, 3, 1);
  var seasonEnd = new Date(2026, 9, 20, 23, 59, 59);
  var now = new Date();

  var totalMs = seasonEnd.getTime() - seasonStart.getTime();
  var passedMs = now.getTime() - seasonStart.getTime();
  var leftMs = seasonEnd.getTime() - now.getTime();

  var daysLeft = Math.ceil(leftMs / 86400000);
  var progress = Math.round((passedMs / totalMs) * 100);

  if(now < seasonStart){
    var daysToStart = Math.ceil((seasonStart.getTime() - now.getTime()) / 86400000);
    daysEl.classList.remove("is-ended");
    daysEl.innerHTML = "<strong>" + daysToStart + "</strong> " + pluralCount(daysToStart, "день", "дня", "дней") + seasonSunsetIcon(0, false);
    fillEl.style.width = "0%";
    captionEl.textContent = "Старт 1 апреля · финиш 20 октября 2026 года";
    return;
  }

  if(now >= seasonEnd || daysLeft <= 0){
    daysEl.classList.add("is-ended");
    daysEl.innerHTML = '<span class="cb-season-ended">Сезон окончен</span>' + seasonSunsetIcon(100, true);
    fillEl.style.width = "100%";
    captionEl.textContent = "Новый сезон уже готовится";
    return;
  }

  progress = Math.max(0, Math.min(100, progress));
  daysLeft = Math.max(1, daysLeft);

  daysEl.classList.remove("is-ended");
  daysEl.innerHTML = "<strong>" + daysLeft + "</strong> " + pluralCount(daysLeft, "день", "дня", "дней") + seasonSunsetIcon(progress, false);
  fillEl.style.width = progress + "%";
  captionEl.textContent = "До 20 октября · сезон пройден на " + progress + "%";
}
'''
replace_once(counter_old, counter_new, "счётчик сезона")

metrics_old = '''function renderSeasonMetrics(){
  var creatorsEl = $("cb-season-creators");
  var bookingsEl = $("cb-season-bookings");
  if(!creatorsEl || !bookingsEl) return;

  if(!creatorDirectoryReady){
    creatorsEl.textContent = "—";
    bookingsEl.textContent = "—";
    return;
  }

  var creators = Object.create(null);
  var activeBookings = bookings.filter(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    var date = normalizeDate(booking.date);
    if(isInactiveBooking(booking) || !creator || isDeletedCreator(creator) || !isDateInSeason(date)) return false;
    creators[creator] = true;
    return true;
  });

  creatorsEl.textContent = Object.keys(creators).length;
  bookingsEl.textContent = activeBookings.length;
}
'''
metrics_new = '''function getTodaySeasonMetrics(activeBookings){
  var today = getTodayKey();
  var firstBookingByCreator = Object.create(null);
  var bookingsToday = 0;

  activeBookings.forEach(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    if(creator && !firstBookingByCreator[creator]) firstBookingByCreator[creator] = booking;

    var timestamp = getActivityTimestamp(booking);
    if(Number.isFinite(timestamp) && getVladivostokDateKey(new Date(timestamp)) === today){
      bookingsToday += 1;
    }
  });

  var creatorsToday = Object.keys(firstBookingByCreator).filter(function(creator){
    var timestamp = getActivityTimestamp(firstBookingByCreator[creator]);
    return Number.isFinite(timestamp) && getVladivostokDateKey(new Date(timestamp)) === today;
  }).length;

  return {creators: creatorsToday, bookings: bookingsToday};
}

function renderSeasonMetricValue(element, total, today, label){
  var delta = Math.max(0, Number(today) || 0);
  element.innerHTML = String(total) + '<sup class="cb-season-delta' + (delta === 0 ? ' is-zero' : '') + '" title="Сегодня: +' + delta + '">+' + delta + '</sup>';
  element.setAttribute("aria-label", String(total) + " " + label + ". Сегодня добавлено: " + delta);
}

function renderSeasonMetrics(){
  var creatorsEl = $("cb-season-creators");
  var bookingsEl = $("cb-season-bookings");
  if(!creatorsEl || !bookingsEl) return;

  if(!creatorDirectoryReady){
    creatorsEl.textContent = "—";
    bookingsEl.textContent = "—";
    return;
  }

  var creators = Object.create(null);
  var activeBookings = bookings.filter(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    var date = normalizeDate(booking.date);
    if(isInactiveBooking(booking) || !creator || isDeletedCreator(creator) || !isDateInSeason(date)) return false;
    creators[creator] = true;
    return true;
  });
  var todayMetrics = getTodaySeasonMetrics(activeBookings);

  renderSeasonMetricValue(creatorsEl, Object.keys(creators).length, todayMetrics.creators, "креаторов в сезоне");
  renderSeasonMetricValue(bookingsEl, activeBookings.length, todayMetrics.bookings, "записей на туры");
}
'''
replace_once(metrics_old, metrics_new, "метрики сезона")

path.write_text(text, encoding="utf-8")
