#!/usr/bin/env python3
from pathlib import Path

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


push_css = r'''
body.cb-push-open {
  overflow: hidden;
}

.cb-weekly-push[hidden] {
  display: none;
}

.cb-weekly-push {
  position: fixed;
  z-index: 9800;
  inset: 0;
  display: grid;
  place-items: center;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .28s ease, visibility .28s ease;
}

.cb-weekly-push.is-visible {
  opacity: 1;
  visibility: visible;
}

.cb-weekly-push-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(237, 241, 248, .60);
  backdrop-filter: blur(14px) saturate(112%);
  -webkit-backdrop-filter: blur(14px) saturate(112%);
}

.cb-weekly-push-card {
  position: relative;
  z-index: 1;
  width: min(520px, 100%);
  max-height: min(720px, calc(100vh - 36px));
  overflow: auto;
  border: 1px solid rgba(23, 23, 25, .09);
  background:
    radial-gradient(circle at 92% 4%, rgba(255,255,255,.88), transparent 31%),
    linear-gradient(140deg, rgba(255,255,255,.96) 0%, rgba(243,239,255,.94) 52%, rgba(233,248,251,.94) 100%);
  color: var(--cb-ink);
  box-shadow: 0 34px 90px rgba(42, 45, 59, .24);
  transform: translateY(18px) scale(.985);
  transition: transform .30s ease;
}

.cb-weekly-push.is-visible .cb-weekly-push-card {
  transform: translateY(0) scale(1);
}

.cb-weekly-push-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px 20px 0;
}

.cb-weekly-push-kicker {
  display: inline-flex;
  width: fit-content;
  padding: 6px 9px;
  background: rgba(223, 246, 236, .78);
  color: #31584d;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.cb-weekly-push-close {
  display: grid;
  flex: 0 0 36px;
  place-items: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 22px;
  line-height: 1;
}

.cb-weekly-push-body {
  padding: 14px 20px 20px;
}

.cb-weekly-push-title {
  margin: 0;
  font-size: clamp(31px, 7vw, 48px);
  font-weight: 340;
  line-height: .98;
  letter-spacing: -.06em;
}

.cb-weekly-push-title strong {
  display: block;
  font-weight: 820;
}

.cb-weekly-push-intro {
  margin: 14px 0 0;
  color: var(--cb-muted);
  font-size: 13px;
  line-height: 1.55;
}

.cb-weekly-push-weather {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  align-items: center;
  gap: 11px;
  margin-top: 16px;
  padding: 11px 13px;
  border: 1px solid rgba(23,23,25,.07);
  background: rgba(255,255,255,.52);
}

.cb-weekly-push-weather .cb-weather-icon {
  width: 32px;
  height: 32px;
  filter: none;
}

.cb-weekly-push-weather strong,
.cb-weekly-push-section-title {
  display: block;
  font-size: 9px;
  font-weight: 840;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-weekly-push-weather span {
  display: block;
  margin-top: 3px;
  color: #676d7b;
  font-size: 11px;
  line-height: 1.4;
}

.cb-weekly-push-section {
  margin-top: 18px;
}

.cb-weekly-push-updates,
.cb-weekly-push-events {
  display: grid;
  gap: 0;
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
}

.cb-weekly-push-updates li,
.cb-weekly-push-event {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr);
  gap: 10px;
  padding: 9px 0;
  border-top: 1px solid rgba(23,23,25,.07);
  color: #5f6572;
  font-size: 11px;
  line-height: 1.45;
}

.cb-weekly-push-updates li::before {
  content: "✓";
  display: grid;
  place-items: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(78,203,237,.15);
  color: #276f82;
  font-size: 10px;
  font-weight: 850;
}

.cb-weekly-push-event {
  grid-template-columns: 7px minmax(0, 1fr) auto;
  gap: 8px;
}

.cb-weekly-push-event-dot {
  width: 6px;
  height: 6px;
  margin-top: 5px;
  border-radius: 50%;
  background: var(--cb-lilac-strong);
}

.cb-weekly-push-event-copy strong {
  color: var(--cb-ink);
  font-weight: 800;
}

.cb-weekly-push-event time {
  color: #8b8f99;
  font-size: 8px;
  white-space: nowrap;
}

.cb-weekly-push-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  width: 100%;
  min-height: 52px;
  margin-top: 18px;
  padding: 0 18px;
  border: 0;
  background: linear-gradient(105deg, var(--cb-blue), var(--cb-cyan) 68%, #8ce8f4);
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  font-weight: 800;
}

.cb-weekly-push-action::after {
  content: "✓";
  font-size: 16px;
}
'''
replace_once(".cb-message {\n", push_css + "\n.cb-message {\n", "CSS уведомления")

mobile_css = r'''

@media (max-width: 600px) {
  .cb-day {
    min-height: 64px;
    padding: 5px 1px 6px;
  }

  .cb-day-num {
    min-height: 17px;
    line-height: 17px;
  }

  .cb-day-weather {
    position: static;
    width: 14px;
    height: 14px;
    margin: 1px auto 0;
  }

  .cb-day-weather .cb-weather-icon {
    width: 14px;
    height: 14px;
  }

  .cb-day-weather + .cb-day-count {
    margin-top: 1px;
  }

  .cb-weekly-push {
    align-items: end;
    padding: 12px 12px max(12px, env(safe-area-inset-bottom));
  }

  .cb-weekly-push-card {
    width: 100%;
    max-height: calc(100vh - max(24px, env(safe-area-inset-top)) - 12px);
  }

  .cb-weekly-push-topline {
    padding: 15px 16px 0;
  }

  .cb-weekly-push-body {
    padding: 12px 16px 16px;
  }

  .cb-weekly-push-event {
    grid-template-columns: 7px minmax(0, 1fr);
  }

  .cb-weekly-push-event time {
    grid-column: 2;
  }
}
'''
replace_once("</style>\n</head>", mobile_css + "\n</style>\n</head>", "мобильные стили")

push_html = r'''
<div id="cb-weekly-push" class="cb-weekly-push" role="dialog" aria-modal="true" aria-labelledby="cb-weekly-push-title" hidden>
  <div class="cb-weekly-push-backdrop" aria-hidden="true"></div>
  <section class="cb-weekly-push-card">
    <div class="cb-weekly-push-topline">
      <span class="cb-weekly-push-kicker">Новости мастерской</span>
      <button type="button" id="cb-weekly-push-close" class="cb-weekly-push-close" aria-label="Закрыть уведомление">×</button>
    </div>
    <div id="cb-weekly-push-body" class="cb-weekly-push-body"></div>
  </section>
</div>

'''
replace_once('<div id="cb-message" class="cb-message" role="status" aria-live="polite"></div>', push_html + '<div id="cb-message" class="cb-message" role="status" aria-live="polite"></div>', "HTML уведомления")

replace_once(
    'var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;\nvar weatherLastRequestedAt = 0;',
    'var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;\nvar WEEKLY_PUSH_STORAGE_KEY = "corsar_weekly_push_seen_v1";\nvar WEEKLY_PUSH_TEST_DATE = "2026-07-22";\nvar weeklyPushTimer = null;\nvar weeklyPushRestoreFocus = null;\nvar weatherLastRequestedAt = 0;',
    "переменные уведомления"
)

push_js = r'''
function getWeekdayFromDateKey(dateKey){
  var parts = String(dateKey || "").split("-");
  if(parts.length !== 3) return -1;
  return new Date(Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]))).getUTCDay();
}

function shouldShowWeeklyPush(){
  var today = getTodayKey();
  if(today === WEEKLY_PUSH_TEST_DATE) return true;
  if(getWeekdayFromDateKey(today) !== 5) return false;
  try {
    return localStorage.getItem(WEEKLY_PUSH_STORAGE_KEY) !== today;
  } catch(e) {
    return true;
  }
}

function rememberWeeklyPushSeen(){
  var today = getTodayKey();
  if(today === WEEKLY_PUSH_TEST_DATE) return;
  try { localStorage.setItem(WEEKLY_PUSH_STORAGE_KEY, today); } catch(e) {}
}

function buildWeeklyPushMarkup(){
  var forecast = getWeatherForecast(getTomorrowKey());
  var weatherMarkup = forecast
    ? '<div class="cb-weekly-push-weather">' + weatherIcon(forecast.code) + '<div><strong>Владивосток завтра</strong><span>' + escapeHtml(formatWeatherBrief(forecast)) + '</span></div></div>'
    : '';
  var updates = [
    'Свои бронирования теперь можно перенести или удалить прямо в разделе записи.',
    'В календаре появился прогноз погоды для активных дат, а на главной — прогноз на завтра.',
    'Последние события креаторов обновляются заново при каждом входе на сайт.'
  ];
  var events = creatorDirectoryReady ? buildRecentCreatorEvents().slice(0, 3) : [];
  var eventMarkup = events.length
    ? '<div class="cb-weekly-push-section"><span class="cb-weekly-push-section-title">Последняя активность</span><ol class="cb-weekly-push-events">' + events.map(function(event){
        return '<li class="cb-weekly-push-event"><span class="cb-weekly-push-event-dot" aria-hidden="true"></span><span class="cb-weekly-push-event-copy">' + event.copy + '</span><time>' + escapeHtml(event.time) + '</time></li>';
      }).join('') + '</ol></div>'
    : '';

  return '<h2 id="cb-weekly-push-title" class="cb-weekly-push-title">Привет, <strong>креатор!</strong></h2>' +
    '<p class="cb-weekly-push-intro">Коротко собрали изменения мастерской и свежую активность участников.</p>' +
    weatherMarkup +
    '<div class="cb-weekly-push-section"><span class="cb-weekly-push-section-title">Что нового</span><ul class="cb-weekly-push-updates">' + updates.map(function(item){ return '<li>' + escapeHtml(item) + '</li>'; }).join('') + '</ul></div>' +
    eventMarkup +
    '<button type="button" id="cb-weekly-push-action" class="cb-weekly-push-action">Прочитано</button>';
}

function closeWeeklyPush(){
  var modal = $("cb-weekly-push");
  if(!modal || modal.hidden) return;
  rememberWeeklyPushSeen();
  modal.classList.remove("is-visible");
  document.body.classList.remove("cb-push-open");
  setTimeout(function(){
    modal.hidden = true;
    if(weeklyPushRestoreFocus && typeof weeklyPushRestoreFocus.focus === "function") weeklyPushRestoreFocus.focus();
    weeklyPushRestoreFocus = null;
  }, 280);
}

function showWeeklyPush(){
  if(!shouldShowWeeklyPush()) return;
  var modal = $("cb-weekly-push");
  var body = $("cb-weekly-push-body");
  if(!modal || !body) return;

  weeklyPushRestoreFocus = document.activeElement;
  body.innerHTML = buildWeeklyPushMarkup();
  modal.hidden = false;
  document.body.classList.add("cb-push-open");
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });

  var close = $("cb-weekly-push-close");
  var action = $("cb-weekly-push-action");
  if(close) close.onclick = closeWeeklyPush;
  if(action) action.onclick = closeWeeklyPush;
  setTimeout(function(){ if(close) close.focus(); }, 60);
}

function scheduleWeeklyPush(){
  if(weeklyPushTimer) clearTimeout(weeklyPushTimer);
  weeklyPushTimer = setTimeout(showWeeklyPush, 760);
}

function setupWeeklyPush(){
  var close = $("cb-weekly-push-close");
  if(close) close.onclick = closeWeeklyPush;
  document.addEventListener("keydown", function(event){
    if(event.key === "Escape") closeWeeklyPush();
  });
}

'''
replace_once("function renderSeasonMetrics(){\n", push_js + "function renderSeasonMetrics(){\n", "JavaScript уведомления")

replace_once(
    '    if(splash) splash.classList.add("is-hidden");\n    document.body.classList.remove("cb-lock-scroll");\n  }, 520);',
    '    if(splash) splash.classList.add("is-hidden");\n    document.body.classList.remove("cb-lock-scroll");\n    scheduleWeeklyPush();\n  }, 520);',
    "запуск уведомления после загрузки"
)

replace_once(
    '        renderResults();\n        renderCreatorOptions();\n        reportSubmitting = false;',
    '        renderResults();\n        renderCreatorOptions();\n        renderRecentCreatorEvents();\n        reportSubmitting = false;',
    "обновление событий после контента"
)

replace_once(
    '  setupCreatorIdentityInputs();\n\n  var submit = $("cb-submit");',
    '  setupCreatorIdentityInputs();\n  setupWeeklyPush();\n\n  var submit = $("cb-submit");',
    "инициализация уведомления"
)

replace_once(
    '  loadData();\n}',
    '  loadData();\n\n  window.addEventListener("pageshow", function(event){\n    if(!event.persisted) return;\n    refreshRemoteDataForCheck().then(function(){\n      renderDataViews();\n      scheduleWeeklyPush();\n    }).catch(function(){});\n  });\n}',
    "обновление событий при возврате на страницу"
)

if text == original:
    raise RuntimeError("index.html не изменён")

PATH.write_text(text, encoding="utf-8")
print("Готово: уведомление, обновление событий и мобильная погода добавлены")
