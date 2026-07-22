#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


season_css_old = '''.cb-season-days {
  color: inherit;
}
'''
season_css_new = '''.cb-season-days {
  display: flex;
  align-items: center;
  gap: 10px;
  color: inherit;
}

.cb-season-days-value {
  min-width: 0;
}

.cb-season-sunset {
  --cb-sun-x: 0px;
  --cb-sun-y: 0px;
  display: inline-flex;
  width: clamp(44px, 5vw, 58px);
  height: 34px;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  opacity: .92;
}

.cb-season-sunset svg {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.cb-season-sunset-sun {
  transform: translate(var(--cb-sun-x), var(--cb-sun-y));
  transform-origin: center;
  transition: transform .55s ease;
}

.cb-season-sunset.is-ended .cb-season-sunset-sun {
  opacity: .78;
}
'''
replace_once(season_css_old, season_css_new, "стили сезонного счётчика")

metric_css_old = '''.cb-season-metric strong {
  display: block;
  font-size: clamp(20px, 2.2vw, 28px);
  font-weight: 820;
  line-height: 1;
  letter-spacing: -.045em;
}
'''
metric_css_new = '''.cb-season-metric strong {
  display: flex;
  align-items: flex-start;
  gap: 3px;
  font-size: clamp(20px, 2.2vw, 28px);
  font-weight: 820;
  line-height: 1;
  letter-spacing: -.045em;
}

.cb-season-metric-total {
  min-width: 0;
}

.cb-season-delta {
  position: relative;
  top: -.2em;
  display: inline-block;
  color: #5a4ed1;
  font-size: 9px;
  font-weight: 840;
  line-height: 1;
  letter-spacing: -.02em;
  white-space: nowrap;
}
'''
replace_once(metric_css_old, metric_css_new, "стили дневного прироста")

season_markup_old = '''          <div id="cb-season-days" class="cb-season-days">считаем...</div>
'''
season_markup_new = '''          <div id="cb-season-days" class="cb-season-days">
            <span id="cb-season-days-value" class="cb-season-days-value">считаем...</span>
            <span id="cb-season-sunset" class="cb-season-sunset" aria-hidden="true">
              <svg viewBox="0 0 64 34" focusable="false">
                <defs>
                  <linearGradient id="cb-season-sunset-gradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stop-color="#2558c8"/>
                    <stop offset="46%" stop-color="#7f67f8"/>
                    <stop offset="76%" stop-color="#ff8f76"/>
                    <stop offset="100%" stop-color="#ffd66b"/>
                  </linearGradient>
                </defs>
                <path d="M4 25.5C17 22 27 28 39 24.5S54 22 60 24" fill="none" stroke="url(#cb-season-sunset-gradient)" stroke-width="2.2" stroke-linecap="round"/>
                <g class="cb-season-sunset-sun">
                  <circle cx="20" cy="13" r="6" fill="#ffd66b" stroke="#171719" stroke-width="1.5"/>
                  <g fill="none" stroke="#ea5aa7" stroke-width="1.5" stroke-linecap="round">
                    <path d="M20 3v3M20 20v3M10 13h3M27 13h3M13 6l2 2M25 18l2 2M27 6l-2 2M15 18l-2 2"/>
                  </g>
                </g>
              </svg>
            </span>
          </div>
'''
replace_once(season_markup_old, season_markup_new, "разметка сезонного счётчика")

season_function_old = '''function updateSeasonCounter(){
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
season_function_new = '''function setSeasonSunProgress(progress, ended){
  var sunEl = $("cb-season-sunset");
  if(!sunEl) return;
  var value = Math.max(0, Math.min(100, Number(progress) || 0));
  sunEl.style.setProperty("--cb-sun-x", (value * .12).toFixed(1) + "px");
  sunEl.style.setProperty("--cb-sun-y", (value * .085).toFixed(1) + "px");
  sunEl.classList.toggle("is-ended", !!ended);
}

function updateSeasonCounter(){
  var daysEl = $("cb-season-days-value") || $("cb-season-days");
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
    daysEl.innerHTML = "<strong>" + daysToStart + "</strong> " + pluralCount(daysToStart, "день", "дня", "дней");
    fillEl.style.width = "0%";
    captionEl.textContent = "Старт 1 апреля · финиш 20 октября 2026 года";
    setSeasonSunProgress(0, false);
    return;
  }

  if(now > seasonEnd){
    daysEl.textContent = "Сезон окончен";
    fillEl.style.width = "100%";
    captionEl.textContent = "Сезон завершён 20 октября 2026 года";
    setSeasonSunProgress(100, true);
    return;
  }

  progress = Math.max(0, Math.min(100, progress));
  daysLeft = Math.max(0, daysLeft);

  daysEl.innerHTML = "<strong>" + daysLeft + "</strong> " + pluralCount(daysLeft, "день", "дня", "дней");
  fillEl.style.width = progress + "%";
  captionEl.textContent = "До 20 октября · сезон пройден на " + progress + "%";
  setSeasonSunProgress(progress, false);
}
'''
replace_once(season_function_old, season_function_new, "логика сезонного счётчика")

metrics_function_old = '''function renderSeasonMetrics(){
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
metrics_function_new = '''function isActivityCreatedToday(item){
  var timestamp = getActivityTimestamp(item);
  return Number.isFinite(timestamp) && getVladivostokDateKey(new Date(timestamp)) === getTodayKey();
}

function renderSeasonMetricValue(element, total, todayDelta, deltaLabel){
  if(!element) return;
  var safeTotal = Math.max(0, Number(total) || 0);
  var safeDelta = Math.max(0, Number(todayDelta) || 0);
  element.innerHTML = '<span class="cb-season-metric-total">' + safeTotal + '</span><sup class="cb-season-delta" title="' + escapeHtml(deltaLabel) + '">+' + safeDelta + '</sup>';
  element.setAttribute("aria-label", safeTotal + ". Сегодня: плюс " + safeDelta);
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
  var firstBookingByCreator = Object.create(null);
  var activeBookings = bookings.filter(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    var date = normalizeDate(booking.date);
    if(isInactiveBooking(booking) || !creator || isDeletedCreator(creator) || !isDateInSeason(date)) return false;
    creators[creator] = true;
    if(!firstBookingByCreator[creator]) firstBookingByCreator[creator] = booking;
    return true;
  });

  var bookingsToday = activeBookings.filter(isActivityCreatedToday).length;
  var creatorsToday = Object.keys(firstBookingByCreator).filter(function(creator){
    return isActivityCreatedToday(firstBookingByCreator[creator]);
  }).length;

  renderSeasonMetricValue(creatorsEl, Object.keys(creators).length, creatorsToday, "Новых креаторов сегодня");
  renderSeasonMetricValue(bookingsEl, activeBookings.length, bookingsToday, "Новых активных записей сегодня");
}
'''
replace_once(metrics_function_old, metrics_function_new, "дневные показатели дашборда")

if text == original:
    raise RuntimeError("index.html не изменился")

path.write_text(text, encoding="utf-8")
print("Сезонный дашборд обновлён")
