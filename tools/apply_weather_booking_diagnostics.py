#!/usr/bin/env python3
from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, got {count}")
    text = text.replace(old, new, 1)


def regex_once(pattern: str, replacement: str, label: str) -> None:
    global text
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {count}")


# ===== CSS: compact local diagnostics container =====
diagnostics_css = r'''
/* ===== Локальная диагностика сайта ===== */
.cb-diagnostics {
  position: relative;
  margin-top: 22px;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .08);
  border-radius: 22px;
  background: rgba(255, 255, 255, .88);
  box-shadow: 0 12px 34px rgba(45, 50, 69, .055);
}

.cb-diagnostics-summary {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 30px;
  align-items: center;
  gap: 12px;
  min-height: 66px;
  padding: 15px 18px;
  cursor: pointer;
  list-style: none;
  user-select: none;
}

.cb-diagnostics-summary::-webkit-details-marker {
  display: none;
}

.cb-diagnostics-summary-copy {
  display: grid;
  min-width: 0;
  gap: 4px;
}

.cb-diagnostics-summary-copy strong {
  font-size: 14px;
  font-weight: 810;
  letter-spacing: -.02em;
}

.cb-diagnostics-summary-copy small {
  color: #737985;
  font-size: 9px;
  line-height: 1.4;
}

.cb-diagnostics-toggle {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: #fff;
  font-size: 18px;
  transition: transform .2s ease, background .2s ease, color .2s ease;
}

.cb-diagnostics[open] .cb-diagnostics-toggle {
  transform: rotate(45deg);
  background: var(--cb-ink);
  color: #fff;
}

.cb-diagnostics-body {
  padding: 15px 18px 18px;
  border-top: 1px solid rgba(23, 23, 25, .07);
}

.cb-diagnostics-note {
  margin: 0;
  color: #69707c;
  font-size: 10px;
  line-height: 1.55;
}

.cb-diagnostics-list {
  display: grid;
  gap: 7px;
  max-height: 260px;
  margin: 14px 0 0;
  padding: 0;
  overflow: auto;
  list-style: none;
}

.cb-diagnostics-item {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 10px;
  padding: 10px 11px;
  border: 1px solid rgba(23, 23, 25, .07);
  background: #f8f8fb;
}

.cb-diagnostics-item.is-warning {
  background: #fff9e9;
}

.cb-diagnostics-item.is-error {
  background: #fff1ef;
}

.cb-diagnostics-time {
  color: #858a94;
  font-size: 8px;
  font-weight: 760;
  white-space: nowrap;
}

.cb-diagnostics-copy {
  display: grid;
  min-width: 0;
  gap: 3px;
}

.cb-diagnostics-copy strong {
  font-size: 10px;
  font-weight: 810;
}

.cb-diagnostics-copy span {
  color: #68707c;
  font-size: 9px;
  line-height: 1.4;
  overflow-wrap: anywhere;
}

.cb-diagnostics-empty {
  padding: 12px 0 2px;
  color: #737985;
  font-size: 10px;
}

.cb-diagnostics-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.cb-diagnostics-actions button {
  min-height: 40px;
  padding: 0 13px;
  border: 1px solid rgba(23, 23, 25, .10);
  background: #fff;
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 9px;
  font-weight: 810;
  letter-spacing: .045em;
  text-transform: uppercase;
}

.cb-diagnostics-actions button:first-child {
  background: linear-gradient(105deg, #e5fbf3, #e8f8fd 48%, #eee8ff);
}

@media (max-width: 600px) {
  .cb-diagnostics {
    margin-top: 14px;
    border-radius: 18px;
  }

  .cb-diagnostics-summary,
  .cb-diagnostics-body {
    padding-right: 14px;
    padding-left: 14px;
  }

  .cb-diagnostics-actions {
    display: grid;
  }

  .cb-diagnostics-actions button {
    width: 100%;
  }
}

'''
replace_once(
    '@media (min-width: 901px) {\n  .cb-profile-entry-card.is-desktop-placement {',
    diagnostics_css + '@media (min-width: 901px) {\n  .cb-profile-entry-card.is-desktop-placement {',
    "insert diagnostics css",
)

# ===== HTML diagnostics container before CREACLOUD =====
diagnostics_html = r'''  <details id="cb-diagnostics" class="cb-diagnostics">
    <summary class="cb-diagnostics-summary">
      <span class="cb-diagnostics-summary-copy">
        <strong>Диагностика сайта</strong>
        <small id="cb-diagnostics-status">Ошибок не зафиксировано</small>
      </span>
      <span class="cb-diagnostics-toggle" aria-hidden="true">+</span>
    </summary>
    <div class="cb-diagnostics-body">
      <p class="cb-diagnostics-note">Журнал хранится только в этом браузере и не отправляется автоматически. Ники, телефоны, ссылки и содержимое форм в него не записываются.</p>
      <ol id="cb-diagnostics-list" class="cb-diagnostics-list" aria-live="polite"></ol>
      <div class="cb-diagnostics-actions">
        <button type="button" id="cb-diagnostics-copy">Скопировать журнал</button>
        <button type="button" id="cb-diagnostics-clear">Очистить журнал</button>
      </div>
    </div>
  </details>

'''
replace_once(
    '  <footer id="creacloud" class="cb-footer">',
    diagnostics_html + '  <footer id="creacloud" class="cb-footer">',
    "insert diagnostics html",
)

# ===== Constants and state =====
replace_once(
    'var WEATHER_REFRESH_INTERVAL = 3 * 60 * 60 * 1000;\n',
    'var WEATHER_REFRESH_INTERVAL = 3 * 60 * 60 * 1000;\n'
    'var WEATHER_REQUEST_TIMEOUT = 14000;\n'
    'var DIAGNOSTICS_STORAGE_KEY = "corsar_diagnostics_v1";\n'
    'var DIAGNOSTICS_MAX_ITEMS = 30;\n'
    'var DIAGNOSTICS_TTL = 14 * 24 * 60 * 60 * 1000;\n'
    'var PENDING_WRITES_STORAGE_KEY = "corsar_pending_writes_v1";\n'
    'var SITE_BUILD_ID = "2026-07-24.weather-booking-health";\n',
    "add constants",
)
replace_once(
    'var weatherLastRequestedAt = 0;\nvar weatherForecastByDate = Object.create(null);\nvar weatherActiveMonthKey = "";\n',
    'var weatherLastRequestedAt = 0;\nvar weatherForecastByDate = Object.create(null);\nvar weatherRequestController = null;\n',
    "weather state",
)
replace_once(
    '  text: "Уточнены мини-ЛК, пять свежих публикаций и персональная рекомендация при бронировании."',
    '  text: "Уточнены мини-ЛК, прогноз погоды, защита бронирований и локальная диагностика сайта."',
    "portal update",
)

# ===== Diagnostics and pending-write journal =====
diagnostics_js = r'''
function sanitizeDiagnosticDetail(value){
  return String(value || "")
    .replace(/https?:\/\/\S+/gi, "[url]")
    .replace(/@[a-z0-9_]{3,}/gi, "[@user]")
    .replace(/\+?\d[\d\s()\-]{6,}\d/g, "[number]")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 180);
}

function readDiagnostics(){
  try {
    var values = JSON.parse(localStorage.getItem(DIAGNOSTICS_STORAGE_KEY) || "[]");
    if(!Array.isArray(values)) return [];
    var cutoff = Date.now() - DIAGNOSTICS_TTL;
    return values.filter(function(item){ return item && Number(item.createdAt) >= cutoff; }).slice(-DIAGNOSTICS_MAX_ITEMS);
  } catch(e) {
    return [];
  }
}

function writeDiagnostics(values){
  try { localStorage.setItem(DIAGNOSTICS_STORAGE_KEY, JSON.stringify((values || []).slice(-DIAGNOSTICS_MAX_ITEMS))); } catch(e) {}
}

function recordDiagnostic(area, code, detail, level){
  var values = readDiagnostics();
  var now = Date.now();
  var safeArea = String(area || "runtime").slice(0, 32);
  var safeCode = String(code || "unknown").slice(0, 64);
  var safeDetail = sanitizeDiagnosticDetail(detail) || "Техническое событие без дополнительных данных";
  var previous = values.length ? values[values.length - 1] : null;

  if(previous && previous.area === safeArea && previous.code === safeCode && now - Number(previous.createdAt || 0) < 10 * 60 * 1000){
    previous.createdAt = now;
    previous.detail = safeDetail;
    previous.level = level || previous.level || "warning";
    previous.repeats = Number(previous.repeats || 1) + 1;
  } else {
    values.push({
      createdAt: now,
      area: safeArea,
      code: safeCode,
      detail: safeDetail,
      level: level === "error" ? "error" : "warning",
      repeats: 1,
      build: SITE_BUILD_ID
    });
  }

  writeDiagnostics(values);
  renderDiagnostics();
}

function formatDiagnosticTime(value){
  var date = new Date(Number(value));
  if(isNaN(date.getTime())) return "—";
  try {
    return date.toLocaleString("ru-RU", {
      timeZone: "Asia/Vladivostok",
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit"
    });
  } catch(e) {
    return date.toLocaleString("ru-RU");
  }
}

function renderDiagnostics(){
  var root = $("cb-diagnostics");
  var status = $("cb-diagnostics-status");
  var list = $("cb-diagnostics-list");
  if(!root || !status || !list) return;

  var values = readDiagnostics();
  status.textContent = values.length
    ? values.length + " " + pluralCount(values.length, "событие", "события", "событий") + " за последние 14 дней"
    : "Ошибок не зафиксировано";

  if(!values.length){
    list.innerHTML = '<li class="cb-diagnostics-empty">Журнал пуст. Сайт не обнаружил технических ошибок в этом браузере.</li>';
    return;
  }

  list.innerHTML = values.slice().reverse().map(function(item){
    var repeatText = Number(item.repeats || 1) > 1 ? " · повторов: " + Number(item.repeats) : "";
    return '<li class="cb-diagnostics-item is-' + (item.level === "error" ? "error" : "warning") + '">' +
      '<time class="cb-diagnostics-time">' + escapeHtml(formatDiagnosticTime(item.createdAt)) + '</time>' +
      '<span class="cb-diagnostics-copy"><strong>' + escapeHtml(item.area + " / " + item.code) + '</strong>' +
      '<span>' + escapeHtml(item.detail + repeatText) + '</span></span></li>';
  }).join("");
}

function diagnosticsText(){
  var values = readDiagnostics();
  var lines = [
    "КОРСАР / журнал диагностики",
    "Сборка: " + SITE_BUILD_ID,
    "Сформирован: " + formatDiagnosticTime(Date.now()),
    "Событий: " + values.length,
    ""
  ];
  values.forEach(function(item, index){
    lines.push((index + 1) + ". [" + formatDiagnosticTime(item.createdAt) + "] " + item.area + " / " + item.code + " — " + item.detail + (Number(item.repeats || 1) > 1 ? " (повторов: " + item.repeats + ")" : ""));
  });
  if(!values.length) lines.push("Ошибок не зафиксировано.");
  return lines.join("\n");
}

function copyDiagnostics(){
  var value = diagnosticsText();
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(value).then(function(){
      setMessage("Журнал диагностики скопирован.", false);
    }).catch(function(){
      recordDiagnostic("diagnostics", "clipboard_failed", "Браузер не разрешил автоматическое копирование", "warning");
      setMessage("Не удалось скопировать журнал автоматически.", true);
    });
    return;
  }

  var textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.setAttribute("readonly", "readonly");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand("copy");
    setMessage("Журнал диагностики скопирован.", false);
  } catch(e) {
    setMessage("Не удалось скопировать журнал автоматически.", true);
  }
  document.body.removeChild(textarea);
}

function clearDiagnostics(){
  writeDiagnostics([]);
  renderDiagnostics();
  setMessage("Журнал диагностики очищен.", false);
}

function runRuntimeHealthChecks(){
  var requiredIds = [
    "corsar-blogger-booking", "cb-calendar", "cb-date", "cb-tour", "cb-telegram", "cb-submit",
    "cb-report-telegram", "cb-report-tour", "cb-report-link", "cb-report-submit", "cb-diagnostics"
  ];
  var missing = requiredIds.filter(function(id){ return !$(id); });
  if(missing.length) recordDiagnostic("runtime", "missing_elements", "Не найдены обязательные элементы интерфейса: " + missing.join(", "), "error");

  var seenIds = Object.create(null);
  var duplicateIds = [];
  Array.prototype.forEach.call(document.querySelectorAll("[id]"), function(node){
    var id = node.id;
    if(!id) return;
    if(seenIds[id]) duplicateIds.push(id);
    seenIds[id] = true;
  });
  if(duplicateIds.length) recordDiagnostic("runtime", "duplicate_ids", "Повторяющиеся идентификаторы: " + duplicateIds.join(", "), "error");

  if(CONFIG.SEASON_START > CONFIG.SEASON_END || CONFIG.BOOKING_START > CONFIG.SEASON_END){
    recordDiagnostic("schedule", "invalid_season_bounds", "Некорректные границы сезона или начала бронирования", "error");
  }

  var invalidDates = [];
  var duplicateTours = [];
  Object.keys(TOURS_BY_DATE).forEach(function(date){
    if(!isDateInSeason(date)) invalidDates.push(date);
    var seenTours = Object.create(null);
    (TOURS_BY_DATE[date] || []).forEach(function(tour){
      var key = normalizeTour(tour);
      if(key && seenTours[key]) duplicateTours.push(date);
      seenTours[key] = true;
    });
  });
  if(invalidDates.length) recordDiagnostic("schedule", "dates_outside_season", "Даты вне сезона: " + invalidDates.slice(0, 8).join(", "), "error");
  if(duplicateTours.length) recordDiagnostic("schedule", "duplicate_tours", "Повторяющиеся туры в датах: " + duplicateTours.slice(0, 8).join(", "), "warning");
  if(TOTAL_UNIQUE_TOURS !== 8) recordDiagnostic("ranking", "unique_tour_count", "Ожидалось 8 уникальных категорий, получено " + TOTAL_UNIQUE_TOURS, "error");
}

function setupDiagnostics(){
  var copy = $("cb-diagnostics-copy");
  var clear = $("cb-diagnostics-clear");
  if(copy) copy.onclick = copyDiagnostics;
  if(clear) clear.onclick = clearDiagnostics;

  window.addEventListener("error", function(event){
    var location = event && event.lineno ? " строка " + event.lineno : "";
    recordDiagnostic("runtime", "javascript_error", String((event && event.message) || "Неизвестная ошибка") + location, "error");
  });
  window.addEventListener("unhandledrejection", function(event){
    var reason = event && event.reason;
    recordDiagnostic("runtime", "unhandled_promise", reason && reason.message ? reason.message : String(reason || "Необработанная ошибка Promise"), "error");
  });

  renderDiagnostics();
  setTimeout(runRuntimeHealthChecks, 0);
}

function readPendingWrites(){
  try {
    var values = JSON.parse(localStorage.getItem(PENDING_WRITES_STORAGE_KEY) || "[]");
    if(!Array.isArray(values)) return [];
    return values.filter(function(item){ return item && Number(item.createdAt) > Date.now() - 24 * 60 * 60 * 1000; }).slice(-20);
  } catch(e) {
    return [];
  }
}

function writePendingWrites(values){
  try { localStorage.setItem(PENDING_WRITES_STORAGE_KEY, JSON.stringify((values || []).slice(-20))); } catch(e) {}
}

function rememberPendingWrite(value){
  var values = readPendingWrites();
  values.push(Object.assign({createdAt: Date.now(), reported: false}, value || {}));
  writePendingWrites(values);
}

function isPendingWriteConfirmed(item){
  if(!item) return true;
  if(item.kind === "booking") return !!findBookingByFingerprint(item.targetKey);
  if(item.kind === "transfer") return !!findBookingByFingerprint(item.targetKey) && !findBookingByFingerprint(item.sourceKey);
  if(item.kind === "cancel") return !findBookingByFingerprint(item.sourceKey);
  return true;
}

function reconcilePendingWrites(){
  var values = readPendingWrites();
  if(!values.length) return;
  var remaining = [];
  values.forEach(function(item){
    if(isPendingWriteConfirmed(item)) return;
    var age = Date.now() - Number(item.createdAt || 0);
    if(age >= 2 * 60 * 1000 && !item.reported){
      item.reported = true;
      recordDiagnostic("booking", "write_not_confirmed", "Отправленная операция " + String(item.kind || "booking") + " не появилась в базе после повторной загрузки", "error");
    }
    remaining.push(item);
  });
  writePendingWrites(remaining);
}

'''
replace_once('var loaderTimer = null;\n', diagnostics_js + 'var loaderTimer = null;\n', "insert diagnostics js")

# ===== Remove current-month weather restriction and describe forecast horizon =====
replace_once(
    'function getActiveWeatherMonthKey(){\n  return getTodayKey().slice(0, 7);\n}\n\n',
    '',
    "remove active weather month helper",
)
replace_once(
    'function isWeatherDateInActiveMonth(date){\n  return String(date || "").slice(0, 7) === getActiveWeatherMonthKey();\n}\n\n',
    'function getWeatherLeadDays(date){\n'
    '  var start = String(getTodayKey()).split("-");\n'
    '  var target = String(date || "").split("-");\n'
    '  if(start.length !== 3 || target.length !== 3) return 0;\n'
    '  var startValue = Date.UTC(Number(start[0]), Number(start[1]) - 1, Number(start[2]));\n'
    '  var targetValue = Date.UTC(Number(target[0]), Number(target[1]) - 1, Number(target[2]));\n'
    '  return Math.round((targetValue - startValue) / 86400000);\n'
    '}\n\n'
    'function getWeatherForecastTitle(date){\n'
    '  return getWeatherLeadDays(date) > 7 ? "Предварительный прогноз" : "Прогноз на эту дату";\n'
    '}\n\n',
    "replace weather month helper",
)
replace_once(
    '    var wind = Number(daily.wind_speed_10m_max && daily.wind_speed_10m_max[index]);\n'
    '    if(!date || !Number.isFinite(code) || !Number.isFinite(max) || !Number.isFinite(min)) return;\n'
    '    next[date] = {\n'
    '      date: date,\n'
    '      code: code,\n'
    '      max: max,\n'
    '      min: min,\n'
    '      feels: feels,\n'
    '      precipitation: precipitation,\n'
    '      wind: wind\n'
    '    };',
    '    var wind = Number(daily.wind_speed_10m_max && daily.wind_speed_10m_max[index]);\n'
    '    var gust = Number(daily.wind_gusts_10m_max && daily.wind_gusts_10m_max[index]);\n'
    '    if(!date || !Number.isFinite(code) || !Number.isFinite(max) || !Number.isFinite(min)) return;\n'
    '    next[date] = {\n'
    '      date: date,\n'
    '      code: code,\n'
    '      max: max,\n'
    '      min: min,\n'
    '      feels: feels,\n'
    '      precipitation: precipitation,\n'
    '      wind: wind,\n'
    '      gust: gust\n'
    '    };',
    "weather gust map",
)
replace_once(
    '  if(Number.isFinite(forecast.wind)) parts.push("ветер до " + Math.round(forecast.wind) + " км/ч");\n',
    '  if(Number.isFinite(forecast.wind)) parts.push("ветер до " + Math.round(forecast.wind) + " км/ч");\n'
    '  if(Number.isFinite(forecast.gust)) parts.push("порывы до " + Math.round(forecast.gust) + " км/ч");\n',
    "weather brief gust",
)

new_weather = r'''function loadWeather(){
  var tempEl = $("cb-weather-temp");
  var metaEl = $("cb-weather-meta");
  if(!tempEl || !metaEl || !window.fetch) return;

  weatherLastRequestedAt = Date.now();
  if(weatherRequestController && typeof weatherRequestController.abort === "function") weatherRequestController.abort();

  var controller = typeof AbortController === "function" ? new AbortController() : null;
  weatherRequestController = controller;
  var timeout = setTimeout(function(){
    if(controller && typeof controller.abort === "function") controller.abort();
  }, WEATHER_REQUEST_TIMEOUT);

  function finishRequest(){
    clearTimeout(timeout);
    if(weatherRequestController === controller) weatherRequestController = null;
  }

  var url = "https://api.open-meteo.com/v1/forecast?latitude=43.1155&longitude=131.8855&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max&timezone=Asia%2FVladivostok&forecast_days=16&models=best_match&cell_selection=land&temperature_unit=celsius&wind_speed_unit=kmh";
  var options = {cache: "no-store"};
  if(controller) options.signal = controller.signal;

  fetch(url, options)
    .then(function(response){
      if(!response.ok) throw new Error("weather-http-" + response.status);
      return response.json();
    })
    .then(function(data){
      finishRequest();
      var nextForecast = buildWeatherForecastMap(data && data.daily ? data.daily : {});
      var tomorrow = nextForecast[getTomorrowKey()];
      if(!tomorrow) throw new Error("weather-data-missing");

      weatherForecastByDate = nextForecast;
      tempEl.innerHTML = '<span class="cb-weather-number"><strong>' + formatSignedTemperature(tomorrow.max).replace("°", "") + '</strong>°</span>' + weatherIcon(tomorrow.code);

      var metaParts = [
        weatherLabel(tomorrow.code),
        "от " + formatSignedTemperature(tomorrow.min) + " до " + formatSignedTemperature(tomorrow.max)
      ];
      if(Number.isFinite(tomorrow.feels)) metaParts.push("ощущается до " + formatSignedTemperature(tomorrow.feels));
      if(Number.isFinite(tomorrow.wind)) metaParts.push("ветер до " + Math.round(tomorrow.wind) + " км/ч");
      if(Number.isFinite(tomorrow.gust)) metaParts.push("порывы до " + Math.round(tomorrow.gust) + " км/ч");
      metaEl.textContent = metaParts.join(" · ");
      metaEl.title = "Источник: Open-Meteo Best Match. Используется последний доступный высокоразрешённый прогноз для Владивостока.";

      renderCalendar();
      var selected = getFormDate();
      if(selected) renderDetails(selected);
    })
    .catch(function(error){
      finishRequest();
      if(error && error.name === "AbortError" && Date.now() - weatherLastRequestedAt < 1000) return;
      tempEl.textContent = "—";
      metaEl.textContent = "Прогноз на завтра временно недоступен";
      recordDiagnostic("weather", "forecast_request_failed", error && error.message ? error.message : "Не удалось получить прогноз", "warning");
    });
}

function setupWeatherRefresh(){
  loadWeather();
  setInterval(loadWeather, WEATHER_REFRESH_INTERVAL);

  document.addEventListener("visibilitychange", function(){
    if(document.hidden) return;
    if(Date.now() - weatherLastRequestedAt >= WEATHER_REFRESH_INTERVAL) loadWeather();
  });
}

function renderTourSelect'''
regex_once(
    r'function loadWeather\(\)\{.*?\n\}\n\nfunction setupWeatherRefresh\(\)\{.*?\n\}\n\nfunction renderTourSelect',
    new_weather,
    "replace weather loader",
)
replace_once(
    '        var forecast = active && isWeatherDateInActiveMonth(date) ? getWeatherForecast(date) : null;\n',
    '        var forecast = active ? getWeatherForecast(date) : null;\n',
    "calendar cross-month weather",
)
replace_once(
    "    html += '<div class=\"cb-date-weather-summary\">' + weatherIcon(forecast.code) + '<div><strong>Прогноз на эту дату</strong><span>' + escapeHtml(formatWeatherBrief(forecast)) + '</span></div></div>';",
    "    html += '<div class=\"cb-date-weather-summary\">' + weatherIcon(forecast.code) + '<div><strong>' + escapeHtml(getWeatherForecastTitle(date)) + '</strong><span>' + escapeHtml(formatWeatherBrief(forecast)) + '</span></div></div>';",
    "forecast horizon title",
)

# ===== Booking invariants: selected tour must belong to the date; only future active records can be transferred/cancelled =====
transfer_function = r'''function getTransferableBookings(telegram){
  var creator = normalizeTelegram(telegram);
  var todayKey = getTodayKey();
  if(!creator || isDeletedCreator(creator)) return [];

  return bookings.filter(function(booking){
    var date = normalizeDate(booking.date);
    return !isInactiveBooking(booking) &&
      normalizeTelegram(booking.telegram) === creator &&
      isDateInSeason(date) &&
      date >= todayKey;
  }).sort(function(a, b){
    return normalizeDate(a.date).localeCompare(normalizeDate(b.date)) ||
      normalizeTour(a.tour).localeCompare(normalizeTour(b.tour), "ru");
  });
}

function isTransferableBookingForCreator(booking, telegram){
  if(!booking) return false;
  var creator = normalizeTelegram(telegram);
  var date = normalizeDate(booking.date);
  return !!creator && !isDeletedCreator(creator) && !isInactiveBooking(booking) &&
    normalizeTelegram(booking.telegram) === creator && isDateInSeason(date) && date >= getTodayKey();
}

function isTourScheduledOnDate(date, tour){
  var key = normalizeTour(tour);
  if(!key) return false;
  return getToursByDate(date).some(function(item){ return normalizeTour(item) === key; });
}
'''
regex_once(
    r'function getTransferableBookings\(telegram\)\{.*?\n\}\n',
    transfer_function,
    "add booking invariant helpers",
)
replace_once(
    '  if(!source || normalizeTelegram(source.telegram) !== tg){\n    setMessage("Выберите активную бронь, принадлежащую указанному нику.", true);',
    '  if(!source || normalizeTelegram(source.telegram) !== tg || !isTransferableBookingForCreator(source, tg)){\n    setMessage("Выберите активную будущую бронь, принадлежащую указанному нику.", true);',
    "cancel source initial",
)
replace_once(
    '      if(!source || normalizeTelegram(source.telegram) !== tg){\n        bookingSubmitting = false;',
    '      if(!source || normalizeTelegram(source.telegram) !== tg || !isTransferableBookingForCreator(source, tg)){\n        bookingSubmitting = false;',
    "cancel source refreshed",
)
count_transfer = text.count('if(!transferSource || normalizeTelegram(transferSource.telegram) !== tg){')
if count_transfer != 2:
    raise SystemExit(f"transfer source guards: expected 2, got {count_transfer}")
text = text.replace(
    'if(!transferSource || normalizeTelegram(transferSource.telegram) !== tg){',
    'if(!transferSource || normalizeTelegram(transferSource.telegram) !== tg || !isTransferableBookingForCreator(transferSource, tg)){',
)
replace_once(
    '  if(isExcludedTour(tour)){\n    setMessage("Эта программа недоступна для записи.", true);\n    return;\n  }\n\n  if(!tg){',
    '  if(isExcludedTour(tour)){\n    setMessage("Эта программа недоступна для записи.", true);\n    return;\n  }\n\n'
    '  if(!isTourScheduledOnDate(date, tour)){\n'
    '    recordDiagnostic("booking", "stale_tour_selection", "Выбранный тур отсутствует в актуальном расписании указанной даты", "warning");\n'
    '    renderTours(date);\n'
    '    setMessage("Этот тур отсутствует в актуальном расписании выбранной даты. Выберите программу заново.", true);\n'
    '    return;\n'
    '  }\n\n'
    '  if(!tg){',
    "initial scheduled tour validation",
)
replace_once(
    '      submissionFingerprint = mode === "transfer"\n        ? "transfer:" + sourceFingerprint + "=>" + fingerprint\n        : "booking:" + fingerprint;\n',
    '      if(!isBookableDate(date) || !isTourScheduledOnDate(date, tour)){\n'
    '        bookingSubmitting = false;\n'
    '        setSubmitBusy("cb-submit", false, "");\n'
    '        renderDataViews();\n'
    '        recordDiagnostic("booking", "schedule_changed_during_check", "Дата или программа перестала быть доступна во время контрольной проверки", "warning");\n'
    '        setMessage("Расписание изменилось во время проверки. Выберите дату и тур заново.", true);\n'
    '        return;\n'
    '      }\n\n'
    '      submissionFingerprint = mode === "transfer"\n        ? "transfer:" + sourceFingerprint + "=>" + fingerprint\n        : "booking:" + fingerprint;\n',
    "refreshed scheduled tour validation",
)

# ===== Pending write confirmation and diagnostics in data/network paths =====
replace_once(
    '    function fail(){\n      if(settled) return;\n      settled = true;\n      cleanup();\n      reject(new Error("remote-data"));\n    }',
    '    function fail(){\n      if(settled) return;\n      settled = true;\n      cleanup();\n      recordDiagnostic("data", "remote_fetch_failed", "Не получен ответ рабочей базы за отведённое время", "error");\n      reject(new Error("remote-data"));\n    }',
    "remote data diagnostic",
)
replace_once(
    '  creatorDirectoryReady = true;\n}',
    '  creatorDirectoryReady = true;\n  reconcilePendingWrites();\n}',
    "reconcile pending writes",
)
replace_once(
    '      .then(function(){\n        bookings = resolveEffectiveBookings(bookings.concat([payload]));\n        rememberSubmission(BOOKING_STORAGE_KEY, submissionFingerprint);',
    '      .then(function(){\n        rememberPendingWrite({kind: "cancel", sourceKey: sourceFingerprint});\n        bookings = resolveEffectiveBookings(bookings.concat([payload]));\n        rememberSubmission(BOOKING_STORAGE_KEY, submissionFingerprint);',
    "remember pending cancellation",
)
replace_once(
    '      .catch(function(){\n        bookingSubmitting = false;\n        setSubmitBusy("cb-submit", false, "");\n        setMessage("Не удалось удалить бронь. Повторите попытку.", true);',
    '      .catch(function(error){\n        bookingSubmitting = false;\n        setSubmitBusy("cb-submit", false, "");\n        recordDiagnostic("booking", "cancel_write_failed", error && error.message ? error.message : "Сетевой сбой удаления", "error");\n        setMessage("Не удалось удалить бронь. Повторите попытку.", true);',
    "cancel write diagnostic",
)
replace_once(
    '    .catch(function(){\n      bookingSubmitting = false;\n      setSubmitBusy("cb-submit", false, "");\n      setMessage("Не удалось проверить актуальную бронь. Обновите страницу и попробуйте ещё раз.", true);',
    '    .catch(function(error){\n      bookingSubmitting = false;\n      setSubmitBusy("cb-submit", false, "");\n      recordDiagnostic("booking", "cancel_preflight_failed", error && error.message ? error.message : "Не выполнена проверка базы", "error");\n      setMessage("Не удалось проверить актуальную бронь. Обновите страницу и попробуйте ещё раз.", true);',
    "cancel preflight diagnostic",
)
replace_once(
    '      .then(function(){\n        bookings = resolveEffectiveBookings(bookings.concat([payload]));\n        rememberSubmission(BOOKING_STORAGE_KEY, submissionFingerprint);',
    '      .then(function(){\n        rememberPendingWrite({kind: mode === "transfer" ? "transfer" : "booking", targetKey: fingerprint, sourceKey: mode === "transfer" ? sourceFingerprint : ""});\n        bookings = resolveEffectiveBookings(bookings.concat([payload]));\n        rememberSubmission(BOOKING_STORAGE_KEY, submissionFingerprint);',
    "remember pending booking",
)
replace_once(
    '      .catch(function(){\n        bookingSubmitting = false;\n        setSubmitBusy("cb-submit", false, "");\n        setMessage("Не удалось отправить заявку. Повторите попытку.", true);',
    '      .catch(function(error){\n        bookingSubmitting = false;\n        setSubmitBusy("cb-submit", false, "");\n        recordDiagnostic("booking", "write_request_failed", error && error.message ? error.message : "Сетевой сбой отправки", "error");\n        setMessage("Не удалось отправить заявку. Повторите попытку.", true);',
    "booking write diagnostic",
)
replace_once(
    '    .catch(function(){\n      bookingSubmitting = false;\n      setSubmitBusy("cb-submit", false, "");\n      setMessage("Не удалось проверить актуальные записи. Обновите страницу и попробуйте ещё раз.", true);',
    '    .catch(function(error){\n      bookingSubmitting = false;\n      setSubmitBusy("cb-submit", false, "");\n      recordDiagnostic("booking", "preflight_failed", error && error.message ? error.message : "Не выполнена повторная проверка базы", "error");\n      setMessage("Не удалось проверить актуальные записи. Обновите страницу и попробуйте ещё раз.", true);',
    "booking preflight diagnostic",
)

# ===== Initialise diagnostics before network activity =====
replace_once(
    '  updateSeasonCounter();\n  setInterval(updateSeasonCounter, 3600000);\n  setupWeatherRefresh();',
    '  setupDiagnostics();\n  updateSeasonCounter();\n  setInterval(updateSeasonCounter, 3600000);\n  setupWeatherRefresh();',
    "init diagnostics",
)

# Safety assertions.
required = [
    'models=best_match',
    'forecast_days=16',
    'var forecast = active ? getWeatherForecast(date) : null;',
    'function isTourScheduledOnDate(date, tour)',
    'function isTransferableBookingForCreator(booking, telegram)',
    'id="cb-diagnostics"',
    'function setupDiagnostics()',
    'function reconcilePendingWrites()',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"missing required marker: {marker}")

for forbidden in ['isWeatherDateInActiveMonth', 'weatherActiveMonthKey', 'window.visualViewport', 'document.body.style.position = "fixed"']:
    if forbidden in text:
        raise SystemExit(f"forbidden marker remains: {forbidden}")

path.write_text(text, encoding="utf-8")
print("Weather, booking safety and diagnostics patch applied")
