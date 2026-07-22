#!/usr/bin/env python3
from pathlib import Path
import re

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise RuntimeError(f"Не найден фрагмент: {label}")
    text = text.replace(old, new, 1)


# 1. Компактная лента событий в пустой области главной и погодные элементы календаря.
hero_actions_anchor = '''.cb-hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 34px;
}

.cb-link-button {'''
hero_actions_styles = '''.cb-hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 34px;
}

.cb-recent-events {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .08);
  background:
    radial-gradient(circle at 94% 4%, rgba(255,255,255,.82), transparent 35%),
    linear-gradient(118deg, #eafaf4 0%, #fff6dd 52%, #f1ecff 100%);
  color: var(--cb-ink);
  box-shadow: 0 14px 32px rgba(68, 78, 102, .08);
}

.cb-recent-events::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: linear-gradient(180deg, var(--cb-mint), var(--cb-yellow), var(--cb-lilac-strong));
}

.cb-recent-events-desktop {
  max-width: 680px;
  margin: 24px 0 auto;
  padding: 14px 16px 10px 18px;
}

.cb-recent-events-mobile {
  display: none;
  padding: 15px 16px 10px 18px;
}

.cb-activity-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 4px;
}

.cb-activity-title {
  font-size: 11px;
  font-weight: 840;
  letter-spacing: .075em;
  text-transform: uppercase;
}

.cb-activity-live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #557063;
  font-size: 8px;
  font-weight: 820;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.cb-activity-live::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #55b995;
  box-shadow: 0 0 0 4px rgba(85, 185, 149, .13);
}

.cb-activity-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.cb-activity-item {
  display: grid;
  grid-template-columns: 8px minmax(0, 1fr) auto;
  align-items: start;
  gap: 9px;
  padding: 7px 0;
  border-top: 1px solid rgba(23, 23, 25, .08);
}

.cb-activity-dot {
  width: 7px;
  height: 7px;
  margin-top: 4px;
  border-radius: 50%;
  background: var(--cb-cyan);
}

.cb-activity-item.is-creator .cb-activity-dot {
  background: #55b995;
}

.cb-activity-item.is-content .cb-activity-dot {
  background: var(--cb-rose);
}

.cb-activity-item.is-leader .cb-activity-dot {
  background: var(--cb-yellow);
  box-shadow: 0 0 0 3px rgba(255, 214, 107, .22);
}

.cb-activity-copy {
  min-width: 0;
  color: #5f6572;
  font-size: 10px;
  line-height: 1.38;
}

.cb-activity-copy strong {
  color: var(--cb-ink);
  font-weight: 820;
}

.cb-activity-time {
  padding-top: 1px;
  color: #8b8f99;
  font-size: 8px;
  font-weight: 720;
  line-height: 1.35;
  white-space: nowrap;
}

.cb-activity-empty {
  padding: 14px 0 6px;
  color: var(--cb-muted);
  font-size: 10px;
  line-height: 1.45;
}

.cb-link-button {'''
replace_once(hero_actions_anchor, hero_actions_styles, "стили ленты событий")

replace_once(
    '''.cb-day {
  width: 100%;''',
    '''.cb-day {
  position: relative;
  width: 100%;''',
    "позиционирование погодного значка в дате",
)

replace_once(
    '''.cb-day-num {
  display: block;
  font-size: 13px;
  font-weight: 800;
}

.cb-details-card {''',
    '''.cb-day-num {
  display: block;
  font-size: 13px;
  font-weight: 800;
}

.cb-day-weather {
  position: absolute;
  top: 3px;
  right: 3px;
  display: grid;
  place-items: center;
  width: 16px;
  height: 16px;
  pointer-events: none;
}

.cb-day-weather .cb-weather-icon {
  width: 16px;
  height: 16px;
  filter: none;
}

.cb-details-card {''',
    "стили погодного значка календаря",
)

replace_once(
    '''.cb-details-card h3 {
  margin: 0 0 14px;
  font-size: 21px;
}

.cb-date-list {''',
    '''.cb-details-card h3 {
  margin: 0 0 14px;
  font-size: 21px;
}

.cb-date-weather-summary {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  align-items: center;
  gap: 11px;
  margin: -2px 0 14px;
  padding: 11px 13px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: rgba(255, 255, 255, .58);
}

.cb-date-weather-summary .cb-weather-icon {
  width: 32px;
  height: 32px;
  filter: none;
}

.cb-date-weather-summary strong {
  display: block;
  font-size: 10px;
  font-weight: 820;
  letter-spacing: .045em;
  text-transform: uppercase;
}

.cb-date-weather-summary span {
  display: block;
  margin-top: 3px;
  color: #686e7d;
  font-size: 11px;
  line-height: 1.4;
}

.cb-date-weather-summary.is-pending {
  grid-template-columns: 1fr;
}

.cb-date-list {''',
    "стили прогноза выбранной даты",
)

# Адаптивное размещение: на мобильных лента находится после блока сезона.
replace_once(
    '''  .cb-hero-title {
    margin-top: 52px;
  }

  .cb-hero-stats {''',
    '''  .cb-hero-title {
    margin-top: 52px;
  }

  .cb-recent-events-desktop {
    display: none;
  }

  .cb-recent-events-mobile {
    display: block;
    grid-column: 1 / -1;
  }

  .cb-hero-stats {''',
    "перенос ленты на мобильных",
)

replace_once(
    '''  .cb-link-button-sequenced {
    justify-content: flex-start;
    text-align: left;
  }

  .cb-hero-stats {''',
    '''  .cb-link-button-sequenced {
    justify-content: flex-start;
    text-align: left;
  }

  .cb-activity-item {
    grid-template-columns: 7px minmax(0, 1fr);
    gap: 8px;
  }

  .cb-activity-time {
    grid-column: 2;
    padding-top: 0;
    text-align: left;
  }

  .cb-hero-stats {''',
    "компактная мобильная лента",
)

# 2. Разметка главной: desktop-лента в пустой области, mobile-лента после сезона.
replace_once(
    '''          <p class="cb-hero-text">Выбирайте морское путешествие, создавайте живой контент о Владивостоке и возвращайтесь сюда, чтобы поделиться готовой публикацией.</p>
        </div>
        <div class="cb-hero-actions">''',
    '''          <p class="cb-hero-text">Выбирайте морское путешествие, создавайте живой контент о Владивостоке и возвращайтесь сюда, чтобы поделиться готовой публикацией.</p>
        </div>
        <div id="cb-recent-events-desktop" class="cb-recent-events cb-recent-events-desktop" aria-live="polite">
          <div class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span></div>
          <div class="cb-activity-empty">Загружаем последние события...</div>
        </div>
        <div class="cb-hero-actions">''',
    "desktop-лента на главной",
)

replace_once(
    '''          <div class="cb-stat-label">Владивосток сейчас</div>''',
    '''          <div class="cb-stat-label">Владивосток завтра</div>''',
    "заголовок прогноза на завтра",
)

replace_once(
    '''          </div>
        </article>
        <div class="cb-leaders-carousel" aria-label="Лидеры сезона">''',
    '''          </div>
        </article>
        <div id="cb-recent-events-mobile" class="cb-recent-events cb-recent-events-mobile" aria-live="polite">
          <div class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span></div>
          <div class="cb-activity-empty">Загружаем последние события...</div>
        </div>
        <div class="cb-leaders-carousel" aria-label="Лидеры сезона">''',
    "mobile-лента после сезона",
)

# 3. Состояние прогноза.
replace_once(
    '''var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;
var weatherLastRequestedAt = 0;''',
    '''var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;
var weatherLastRequestedAt = 0;
var weatherForecastByDate = Object.create(null);
var weatherActiveMonthKey = "";''',
    "состояние погодного прогноза",
)

# Вспомогательные функции дат Владивостока.
date_anchor = '''function bookingFingerprint(date, telegram, tour){'''
date_helpers = '''function addDaysToDateKey(dateKey, amount){
  var parts = String(dateKey || "").split("-");
  if(parts.length !== 3) return "";
  var value = new Date(Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]) + Number(amount || 0)));
  return value.getUTCFullYear() + "-" + pad(value.getUTCMonth() + 1) + "-" + pad(value.getUTCDate());
}

function getTomorrowKey(){
  return addDaysToDateKey(getTodayKey(), 1);
}

function getVladivostokDateKey(value){
  var date = value instanceof Date ? value : new Date(value);
  if(isNaN(date.getTime())) return "";
  try {
    var parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Vladivostok",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).formatToParts(date);
    var values = {};
    parts.forEach(function(part){ values[part.type] = part.value; });
    return values.year + "-" + values.month + "-" + values.day;
  } catch(e) {
    return date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
  }
}

function getActiveWeatherMonthKey(){
  return getTodayKey().slice(0, 7);
}

function bookingFingerprint(date, telegram, tour){'''
replace_once(date_anchor, date_helpers, "функции дат для прогноза")

# Полностью заменяем прежний текущий прогноз на единый ежедневный прогноз до 16 дней.
weather_pattern = re.compile(
    r'function loadWeather\(\)\{.*?\n\}\n\nfunction setupWeatherRefresh\(\)\{.*?\n\}\n\nfunction renderTourSelect',
    re.DOTALL,
)
weather_replacement = r'''function formatSignedTemperature(value){
  var number = Math.round(Number(value));
  if(!Number.isFinite(number)) return "—";
  return (number > 0 ? "+" : "") + number + "°";
}

function getWeatherForecast(date){
  return weatherForecastByDate[String(date || "")] || null;
}

function isWeatherDateInActiveMonth(date){
  return String(date || "").slice(0, 7) === getActiveWeatherMonthKey();
}

function formatWeatherCalendarLabel(forecast){
  if(!forecast) return "";
  return weatherLabel(forecast.code) + ", " + formatSignedTemperature(forecast.min) + "…" + formatSignedTemperature(forecast.max);
}

function formatWeatherBrief(forecast){
  if(!forecast) return "Прогноз пока уточняется";
  var parts = [
    weatherLabel(forecast.code),
    "от " + formatSignedTemperature(forecast.min) + " до " + formatSignedTemperature(forecast.max)
  ];
  if(Number.isFinite(forecast.precipitation)) parts.push("вероятность осадков " + Math.round(forecast.precipitation) + "%");
  if(Number.isFinite(forecast.wind)) parts.push("ветер до " + Math.round(forecast.wind) + " км/ч");
  return parts.join(" · ");
}

function buildWeatherForecastMap(daily){
  var next = Object.create(null);
  var dates = Array.isArray(daily && daily.time) ? daily.time : [];
  dates.forEach(function(date, index){
    var code = Number(daily.weather_code && daily.weather_code[index]);
    var max = Number(daily.temperature_2m_max && daily.temperature_2m_max[index]);
    var min = Number(daily.temperature_2m_min && daily.temperature_2m_min[index]);
    var feels = Number(daily.apparent_temperature_max && daily.apparent_temperature_max[index]);
    var precipitation = Number(daily.precipitation_probability_max && daily.precipitation_probability_max[index]);
    var wind = Number(daily.wind_speed_10m_max && daily.wind_speed_10m_max[index]);
    if(!date || !Number.isFinite(code) || !Number.isFinite(max) || !Number.isFinite(min)) return;
    next[date] = {
      date: date,
      code: code,
      max: max,
      min: min,
      feels: feels,
      precipitation: precipitation,
      wind: wind
    };
  });
  return next;
}

function loadWeather(){
  var tempEl = $("cb-weather-temp");
  var metaEl = $("cb-weather-meta");
  if(!tempEl || !metaEl || !window.fetch) return;

  weatherLastRequestedAt = Date.now();
  weatherActiveMonthKey = getActiveWeatherMonthKey();

  var url = "https://api.open-meteo.com/v1/forecast?latitude=43.1155&longitude=131.8855&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,precipitation_probability_max,wind_speed_10m_max&timezone=Asia%2FVladivostok&forecast_days=16";

  fetch(url)
    .then(function(response){
      if(!response.ok) throw new Error("weather");
      return response.json();
    })
    .then(function(data){
      var nextForecast = buildWeatherForecastMap(data && data.daily ? data.daily : {});
      var tomorrow = nextForecast[getTomorrowKey()];
      if(!tomorrow) throw new Error("weather-data");

      weatherForecastByDate = nextForecast;
      tempEl.innerHTML = '<span class="cb-weather-number"><strong>' + formatSignedTemperature(tomorrow.max).replace("°", "") + '</strong>°</span>' + weatherIcon(tomorrow.code);

      var metaParts = [
        weatherLabel(tomorrow.code),
        "от " + formatSignedTemperature(tomorrow.min) + " до " + formatSignedTemperature(tomorrow.max)
      ];
      if(Number.isFinite(tomorrow.feels)) metaParts.push("ощущается до " + formatSignedTemperature(tomorrow.feels));
      if(Number.isFinite(tomorrow.wind)) metaParts.push("ветер до " + Math.round(tomorrow.wind) + " км/ч");
      metaEl.textContent = metaParts.join(" · ");

      renderCalendar();
      var selected = getFormDate();
      if(selected) renderDetails(selected);
    })
    .catch(function(){
      tempEl.textContent = "—";
      metaEl.textContent = "Прогноз на завтра временно недоступен";
    });
}

function setupWeatherRefresh(){
  weatherActiveMonthKey = getActiveWeatherMonthKey();
  loadWeather();
  setInterval(loadWeather, WEATHER_REFRESH_INTERVAL);

  setInterval(function(){
    var currentMonthKey = getActiveWeatherMonthKey();
    if(currentMonthKey !== weatherActiveMonthKey){
      weatherActiveMonthKey = currentMonthKey;
      loadWeather();
    }
  }, 15 * 60 * 1000);

  document.addEventListener("visibilitychange", function(){
    if(document.hidden) return;
    var monthChanged = getActiveWeatherMonthKey() !== weatherActiveMonthKey;
    if(monthChanged || Date.now() - weatherLastRequestedAt >= WEATHER_REFRESH_INTERVAL){
      loadWeather();
    }
  });
}

function renderTourSelect'''
text, weather_count = weather_pattern.subn(weather_replacement, text, count=1)
if weather_count != 1:
    raise RuntimeError("Не удалось заменить погодный модуль")

# 4. Маленький погодный значок только в активных окнах текущего месяца.
calendar_old = '''        var active = isBookableDate(date) && toursCount > 0;

        var cell = document.createElement("button");
        cell.type = "button";
        cell.className = "cb-day";

        if(toursCount > 0) cell.className += " has-tours";
        if(count > 0) cell.className += " busy";
        if(date === formDate) cell.className += " selected";
        if(!active) cell.className += " is-disabled";
        cell.disabled = !active;
        cell.setAttribute("aria-label", active ? formatDateRu(date) + ", туров: " + toursCount + ", записей: " + count : formatDateRu(date) + ", туров нет");

        cell.innerHTML =
          '<span class="cb-day-num">' + day + '</span>' +
          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count">записей: ' + count + '</span>' : '');'''
calendar_new = '''        var active = isBookableDate(date) && toursCount > 0;
        var forecast = active && isWeatherDateInActiveMonth(date) ? getWeatherForecast(date) : null;
        var forecastLabel = forecast ? formatWeatherCalendarLabel(forecast) : "";

        var cell = document.createElement("button");
        cell.type = "button";
        cell.className = "cb-day";

        if(toursCount > 0) cell.className += " has-tours";
        if(count > 0) cell.className += " busy";
        if(date === formDate) cell.className += " selected";
        if(!active) cell.className += " is-disabled";
        cell.disabled = !active;
        var ariaLabel = active ? formatDateRu(date) + ", туров: " + toursCount + ", записей: " + count : formatDateRu(date) + ", туров нет";
        if(forecastLabel) ariaLabel += ", прогноз: " + forecastLabel;
        cell.setAttribute("aria-label", ariaLabel);

        cell.innerHTML =
          '<span class="cb-day-num">' + day + '</span>' +
          (forecast ? '<span class="cb-day-weather" title="' + escapeHtml(forecastLabel) + '">' + weatherIcon(forecast.code) + '</span>' : '') +
          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count">записей: ' + count + '</span>' : '');'''
replace_once(calendar_old, calendar_new, "погода в ячейках календаря")

# Краткий прогноз перед списком свободных туров.
replace_once(
    '''  var html = '<h3>' + escapeHtml(formatDateRu(date)) + '</h3>';

  if(tours.length){''',
    '''  var html = '<h3>' + escapeHtml(formatDateRu(date)) + '</h3>';
  var forecast = getWeatherForecast(date);
  if(forecast){
    html += '<div class="cb-date-weather-summary">' + weatherIcon(forecast.code) + '<div><strong>Прогноз на эту дату</strong><span>' + escapeHtml(formatWeatherBrief(forecast)) + '</span></div></div>';
  } else if(date >= getTodayKey()){
    html += '<div class="cb-date-weather-summary is-pending"><div><strong>Прогноз на эту дату</strong><span>Уточняется и появится автоматически ближе к дате.</span></div></div>';
  }

  if(tours.length){''',
    "текстовый прогноз выбранной даты",
)

# 5. Лента событий из существующей базы: брони, первые действия и смена лидера.
activity_functions = r'''function parseActivityTimestampValue(value){
  if(value === null || typeof value === "undefined" || value === "") return NaN;
  if(typeof value === "number"){
    if(value > 1000000000000) return value;
    if(value > 1000000000) return value * 1000;
  }

  var raw = String(value).trim();
  if(!raw) return NaN;
  if(/^\d{13}$/.test(raw)) return Number(raw);
  if(/^\d{10}$/.test(raw)) return Number(raw) * 1000;

  var direct = Date.parse(raw);
  if(Number.isFinite(direct)) return direct;

  var ru = raw.match(/^(\d{1,2})[.\/-](\d{1,2})[.\/-](\d{4})(?:[ ,T]+(\d{1,2}):(\d{2})(?::(\d{2}))?)?/);
  if(ru){
    return new Date(Number(ru[3]), Number(ru[2]) - 1, Number(ru[1]), Number(ru[4] || 0), Number(ru[5] || 0), Number(ru[6] || 0)).getTime();
  }

  return NaN;
}

function getActivityTimestamp(item){
  if(!item) return NaN;
  var candidates = [
    item.timestamp,
    item.createdAt,
    item.created_at,
    item.submittedAt,
    item.submitted_at,
    item.addedAt,
    item.recordedAt,
    item.dateTime,
    item.datetime,
    item.created,
    item["Дата создания"],
    item["Дата и время"],
    item["Время создания"],
    item["Timestamp"]
  ];

  for(var i = 0; i < candidates.length; i++){
    var parsed = parseActivityTimestampValue(candidates[i]);
    if(Number.isFinite(parsed)) return parsed;
  }

  var requestId = String(item.requestId || "");
  var requestMatch = requestId.match(/(?:booking|content|cancel|report)-(\d{13})/i);
  return requestMatch ? Number(requestMatch[1]) : NaN;
}

function getActivityOrder(item, fallback){
  var direct = Number(item && item.__activityIndex);
  return Number.isFinite(direct) ? direct : Number(fallback || 0);
}

function getActivitySortValue(item, fallback){
  var timestamp = getActivityTimestamp(item);
  return Number.isFinite(timestamp) ? timestamp : getActivityOrder(item, fallback);
}

function formatActivityTime(item){
  var timestamp = getActivityTimestamp(item);
  if(!Number.isFinite(timestamp)) return "недавно";

  var date = new Date(timestamp);
  var dateKey = getVladivostokDateKey(date);
  var today = getTodayKey();
  var time = new Intl.DateTimeFormat("ru-RU", {
    timeZone: "Asia/Vladivostok",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);

  if(dateKey === today) return "сегодня, " + time;
  if(dateKey === addDaysToDateKey(today, -1)) return "вчера, " + time;

  var day = new Intl.DateTimeFormat("ru-RU", {
    timeZone: "Asia/Vladivostok",
    day: "numeric",
    month: "short"
  }).format(date).replace(/\.$/, "");
  return day + ", " + time;
}

function formatActivityTripDate(date){
  var parts = String(date || "").split("-");
  if(parts.length !== 3) return "";
  var value = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  return value.toLocaleDateString("ru-RU", {day: "numeric", month: "long"});
}

function getLeaderFromTotals(totals){
  return Object.keys(totals).sort(function(a, b){
    return totals[b] - totals[a] || a.localeCompare(b, "ru");
  })[0] || "";
}

function buildRecentCreatorEvents(){
  var events = [];
  var bookingTotals = Object.create(null);
  var currentBookingLeader = "";
  var orderedBookings = bookings.slice().sort(function(a, b){
    return getActivityOrder(a, bookings.indexOf(a)) - getActivityOrder(b, bookings.indexOf(b));
  });

  orderedBookings.forEach(function(booking, index){
    var creator = normalizeTelegram(booking.telegram);
    var date = normalizeDate(booking.date);
    var tour = canonicalTourName(booking.tour || "");
    if(!creator || isDeletedCreator(creator) || isInactiveBooking(booking)) return;

    bookingTotals[creator] = (bookingTotals[creator] || 0) + 1;
    var isFirst = bookingTotals[creator] === 1;
    var copy = isFirst
      ? '<strong>' + escapeHtml(creator) + '</strong> оформил первую бронь и стал новым креатором' + (tour ? ' · ' + escapeHtml(tour) : '') + (date ? ' · ' + escapeHtml(formatActivityTripDate(date)) : '')
      : '<strong>' + escapeHtml(creator) + '</strong> забронировал ' + escapeHtml(tour || "морской тур") + (date ? ' · ' + escapeHtml(formatActivityTripDate(date)) : '');

    events.push({
      key: "booking:" + bookingFingerprint(date, creator, tour) + ":" + index,
      kind: isFirst ? "creator" : "booking",
      copy: copy,
      time: formatActivityTime(booking),
      sortValue: getActivitySortValue(booking, index),
      priority: 2
    });

    var leader = getLeaderFromTotals(bookingTotals);
    if(leader && leader !== currentBookingLeader){
      currentBookingLeader = leader;
      events.push({
        key: "visit-leader:" + leader + ":" + index,
        kind: "leader",
        copy: '<strong>' + escapeHtml(leader) + '</strong> занял первое место по количеству туров · ' + bookingTotals[leader] + ' ' + pluralCount(bookingTotals[leader], "тур", "тура", "туров"),
        time: formatActivityTime(booking),
        sortValue: getActivitySortValue(booking, index),
        priority: 1
      });
    }
  });

  var contentTotals = Object.create(null);
  var currentContentLeader = "";
  var published = getPublishedContentItems().slice().sort(function(a, b){
    return getActivityOrder(a, reports.indexOf(a)) - getActivityOrder(b, reports.indexOf(b));
  });

  published.forEach(function(report, index){
    var creator = getReportCreator(report);
    var tour = canonicalTourName(getReportTour(report));
    if(!creator || isDeletedCreator(creator)) return;

    contentTotals[creator] = (contentTotals[creator] || 0) + 1;
    var isFirst = contentTotals[creator] === 1;
    events.push({
      key: "content:" + normalizeContentLink(getReportLink(report)) + ":" + index,
      kind: "content",
      copy: '<strong>' + escapeHtml(creator) + '</strong> добавил ' + (isFirst ? 'первый' : 'новый') + ' контент' + (tour ? ' · ' + escapeHtml(tour) : ''),
      time: formatActivityTime(report),
      sortValue: getActivitySortValue(report, 100000 + index),
      priority: 2
    });

    var leader = getLeaderFromTotals(contentTotals);
    if(leader && leader !== currentContentLeader){
      currentContentLeader = leader;
      events.push({
        key: "content-leader:" + leader + ":" + index,
        kind: "leader",
        copy: '<strong>' + escapeHtml(leader) + '</strong> занял первое место по опубликованному контенту · ' + contentTotals[leader] + ' ' + pluralCount(contentTotals[leader], "работа", "работы", "работ"),
        time: formatActivityTime(report),
        sortValue: getActivitySortValue(report, 100000 + index),
        priority: 1
      });
    }
  });

  return events.sort(function(a, b){
    return b.sortValue - a.sortValue || b.priority - a.priority || a.key.localeCompare(b.key, "ru");
  }).slice(0, 5);
}

function renderRecentCreatorEvents(){
  var roots = [$("cb-recent-events-desktop"), $("cb-recent-events-mobile")].filter(Boolean);
  if(!roots.length) return;

  var events = creatorDirectoryReady ? buildRecentCreatorEvents() : [];
  var body = '<div class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span></div>';

  if(!creatorDirectoryReady){
    body += '<div class="cb-activity-empty">Загружаем последние события...</div>';
  } else if(!events.length){
    body += '<div class="cb-activity-empty">События появятся после первой брони или публикации.</div>';
  } else {
    body += '<ol class="cb-activity-list">' + events.map(function(event){
      return '<li class="cb-activity-item is-' + escapeHtml(event.kind) + '">' +
        '<span class="cb-activity-dot" aria-hidden="true"></span>' +
        '<span class="cb-activity-copy">' + event.copy + '</span>' +
        '<time class="cb-activity-time">' + escapeHtml(event.time) + '</time>' +
      '</li>';
    }).join("") + '</ol>';
  }

  roots.forEach(function(root){ root.innerHTML = body; });
}

function renderSeasonMetrics(){'''
replace_once('function renderSeasonMetrics(){', activity_functions, "функции ленты событий")

# Сохраняем порядок строк исходной базы для событий, не меняя рабочие объекты API.
apply_pattern = re.compile(
    r'function applyRemoteRows\(allRows\)\{.*?\n\}\n\nfunction renderDataViews',
    re.DOTALL,
)
apply_replacement = r'''function applyRemoteRows(allRows){
  var preparedRows = (Array.isArray(allRows) ? allRows : []).map(function(item, index){
    if(!item || typeof item !== "object") return item;
    var prepared = Object.assign({}, item);
    prepared.__activityIndex = index;
    return prepared;
  });

  reports = preparedRows.filter(function(item){
    return item && item.type === "content_report" && !isDeletedCreator(getReportCreator(item));
  });

  bookings = resolveEffectiveBookings(preparedRows.filter(function(item){
    return !item.type || item.type !== "content_report";
  }));

  creatorDirectoryReady = true;
}

function renderDataViews'''
text, apply_count = apply_pattern.subn(apply_replacement, text, count=1)
if apply_count != 1:
    raise RuntimeError("Не удалось обновить подготовку строк базы")

replace_once(
    '''  renderSeasonMetrics();
  renderAnalytics();
  renderResults();''',
    '''  renderSeasonMetrics();
  renderAnalytics();
  renderResults();
  renderRecentCreatorEvents();''',
    "вызов ленты событий",
)

# Базовые гарантии: ключевые формы и ссылки сохранены, секции не продублированы.
for required in [
    'id="calendar"',
    'id="booking"',
    'id="content"',
    'id="cb-submit"',
    'id="cb-report-submit"',
    'https://script.google.com/macros/s/',
    'https://t.me/+nYzsW9t8e38xZGJi',
]:
    if original.count(required) != text.count(required):
        raise RuntimeError(f"Изменено количество ключевого элемента: {required}")

for added in [
    'id="cb-recent-events-desktop"',
    'id="cb-recent-events-mobile"',
    'function renderRecentCreatorEvents()',
    'daily=weather_code,temperature_2m_max',
    'class="cb-day-weather"',
    'Прогноз на эту дату',
]:
    if added not in text:
        raise RuntimeError(f"Не добавлен обязательный элемент: {added}")

PATH.write_text(text, encoding="utf-8")
print("Прогноз на завтра, погода календаря и лента событий добавлены")
