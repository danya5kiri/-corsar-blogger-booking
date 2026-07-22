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


notice_css = r'''
.cb-compact-notice[hidden] {
  display: none;
}

.cb-compact-notice {
  position: fixed;
  z-index: 2147483646;
  inset: 0;
  display: grid;
  place-items: center;
  box-sizing: border-box;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .24s ease, visibility .24s ease;
}

.cb-compact-notice.is-visible {
  opacity: 1;
  visibility: visible;
}

.cb-compact-notice-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(237, 241, 248, .58);
  backdrop-filter: blur(12px) saturate(108%);
  -webkit-backdrop-filter: blur(12px) saturate(108%);
}

.cb-compact-notice-card {
  position: relative;
  z-index: 1;
  width: min(420px, 100%);
  padding: 18px;
  border: 1px solid rgba(23, 23, 25, .09);
  background:
    radial-gradient(circle at 96% 4%, rgba(255, 255, 255, .88), transparent 34%),
    linear-gradient(140deg, rgba(255, 255, 255, .97), rgba(243, 239, 255, .95) 58%, rgba(233, 248, 251, .95));
  box-shadow: 0 28px 74px rgba(42, 45, 59, .22);
  color: var(--cb-ink);
  transform: translateY(12px) scale(.99);
  transition: transform .26s ease;
}

.cb-compact-notice.is-visible .cb-compact-notice-card {
  transform: translateY(0) scale(1);
}

.cb-compact-notice-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.cb-compact-notice-kicker {
  color: #5f6572;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.cb-compact-notice-close {
  display: grid;
  flex: 0 0 32px;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: rgba(255, 255, 255, .74);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 20px;
  line-height: 1;
}

.cb-compact-notice-title {
  margin: 12px 0 0;
  font-size: clamp(27px, 7vw, 38px);
  font-weight: 340;
  line-height: 1;
  letter-spacing: -.055em;
}

.cb-compact-notice-title strong {
  font-weight: 820;
}

.cb-compact-notice-list {
  display: grid;
  gap: 0;
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
}

.cb-compact-notice-item {
  display: grid;
  grid-template-columns: 20px minmax(0, 1fr);
  gap: 10px;
  padding: 10px 0;
  border-top: 1px solid rgba(23, 23, 25, .07);
  color: #606673;
  font-size: 11px;
  line-height: 1.45;
}

.cb-compact-notice-item::before {
  content: "✓";
  display: grid;
  place-items: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(78, 203, 237, .15);
  color: #276f82;
  font-size: 10px;
  font-weight: 850;
}

.cb-compact-notice-item strong {
  color: var(--cb-ink);
  font-weight: 800;
}

.cb-compact-notice-time {
  display: block;
  margin-top: 3px;
  color: #8b8f99;
  font-size: 8px;
  font-weight: 700;
}

.cb-compact-notice-action {
  width: 100%;
  min-height: 48px;
  margin-top: 14px;
  padding: 0 16px;
  border: 0;
  background: linear-gradient(105deg, var(--cb-blue), var(--cb-cyan) 68%, #8ce8f4);
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  font-weight: 800;
}

'''
replace_once(
    ".cb-message {\n",
    notice_css + ".cb-message {\n",
    "стили компактного уведомления",
)

mobile_old = '''  .cb-recent-events-mobile {
    display: block;
    grid-column: 1 / -1;
  }
'''
mobile_new = '''  .cb-recent-events-mobile {
    position: relative;
    z-index: 20;
    display: block;
    grid-column: 1 / -1;
    overflow: visible;
  }

  .cb-recent-events-mobile .cb-activity-head {
    position: relative;
    z-index: 2;
    background: linear-gradient(112deg, rgba(250, 250, 252, .82), rgba(221, 225, 232, .56) 58%, rgba(255, 255, 255, .68));
    backdrop-filter: blur(14px) saturate(105%);
    -webkit-backdrop-filter: blur(14px) saturate(105%);
  }

  .cb-recent-events-mobile .cb-activity-panel {
    position: absolute;
    z-index: 1;
    right: -1px;
    bottom: calc(100% + 7px);
    left: -1px;
    max-height: min(250px, 48vh);
    overflow: auto;
    padding: 8px 12px 7px 15px;
    border: 1px solid rgba(23, 23, 25, .08);
    background: linear-gradient(145deg, rgba(250, 250, 252, .97), rgba(226, 230, 237, .93) 58%, rgba(255, 255, 255, .95));
    box-shadow: 0 -16px 38px rgba(52, 58, 72, .12);
    backdrop-filter: blur(18px) saturate(108%);
    -webkit-backdrop-filter: blur(18px) saturate(108%);
  }
'''
replace_once(mobile_old, mobile_new, "мобильный блок последних событий")

notice_html = '''
<div id="cb-compact-notice" class="cb-compact-notice" hidden role="dialog" aria-modal="true" aria-labelledby="cb-compact-notice-title">
  <div id="cb-compact-notice-backdrop" class="cb-compact-notice-backdrop"></div>
  <article class="cb-compact-notice-card">
    <div class="cb-compact-notice-top">
      <span class="cb-compact-notice-kicker">Важно на этой неделе</span>
      <button type="button" id="cb-compact-notice-close" class="cb-compact-notice-close" aria-label="Закрыть уведомление">×</button>
    </div>
    <div id="cb-compact-notice-body"></div>
    <button type="button" id="cb-compact-notice-action" class="cb-compact-notice-action">Прочитано</button>
  </article>
</div>

'''
replace_once(
    '<div id="cb-message" class="cb-message" role="status" aria-live="polite"></div>\n',
    notice_html + '<div id="cb-message" class="cb-message" role="status" aria-live="polite"></div>\n',
    "разметка компактного уведомления",
)

replace_once(
    'var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;\n',
    'var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;\nvar COMPACT_NOTICE_STORAGE_KEY = "corsar_compact_notice_seen_v1";\nvar COMPACT_NOTICE_TEST_DATE = "2026-07-22";\nvar compactNoticeTimer = null;\nvar compactNoticeRestoreFocus = null;\n',
    "переменные уведомления",
)

functions = r'''

function getWeekdayFromDateKey(dateKey){
  var parts = String(dateKey || "").split("-");
  if(parts.length !== 3) return -1;
  return new Date(Date.UTC(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]))).getUTCDay();
}

function shouldShowCompactNotice(){
  var today = getTodayKey();
  if(today === COMPACT_NOTICE_TEST_DATE) return true;
  if(getWeekdayFromDateKey(today) !== 5) return false;
  try {
    return localStorage.getItem(COMPACT_NOTICE_STORAGE_KEY) !== today;
  } catch(e) {
    return true;
  }
}

function rememberCompactNoticeSeen(){
  var today = getTodayKey();
  if(today === COMPACT_NOTICE_TEST_DATE) return;
  try { localStorage.setItem(COMPACT_NOTICE_STORAGE_KEY, today); } catch(e) {}
}

function buildCompactNoticeMarkup(){
  var items = [];
  var forecast = getWeatherForecast(getTomorrowKey());
  if(forecast){
    items.push('<li class="cb-compact-notice-item"><span><strong>Владивосток завтра:</strong> ' + escapeHtml(formatWeatherBrief(forecast)) + '</span></li>');
  }

  items.push('<li class="cb-compact-notice-item"><span>Свою бронь можно перенести или удалить в разделе <strong>«Запись»</strong>.</span></li>');

  var event = creatorDirectoryReady ? buildRecentCreatorEvents()[0] : null;
  if(event){
    items.push('<li class="cb-compact-notice-item"><span>' + event.copy + '<time class="cb-compact-notice-time">' + escapeHtml(event.time) + '</time></span></li>');
  }

  return '<h2 id="cb-compact-notice-title" class="cb-compact-notice-title">Привет, <strong>креатор!</strong></h2>' +
    '<ul class="cb-compact-notice-list">' + items.join('') + '</ul>';
}

function closeCompactNotice(){
  var modal = $("cb-compact-notice");
  if(!modal || modal.hidden) return;
  rememberCompactNoticeSeen();
  modal.classList.remove("is-visible");
  setTimeout(function(){
    modal.hidden = true;
    if(compactNoticeRestoreFocus && typeof compactNoticeRestoreFocus.focus === "function") compactNoticeRestoreFocus.focus();
    compactNoticeRestoreFocus = null;
  }, 240);
}

function showCompactNotice(){
  if(!shouldShowCompactNotice()) return;
  var modal = $("cb-compact-notice");
  var body = $("cb-compact-notice-body");
  if(!modal || !body) return;

  compactNoticeRestoreFocus = document.activeElement;
  body.innerHTML = buildCompactNoticeMarkup();
  modal.hidden = false;
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });

  var close = $("cb-compact-notice-close");
  if(close) setTimeout(function(){ close.focus(); }, 60);
}

function scheduleCompactNotice(){
  if(compactNoticeTimer) clearTimeout(compactNoticeTimer);
  compactNoticeTimer = setTimeout(showCompactNotice, 900);
}

function setupCompactNotice(){
  var close = $("cb-compact-notice-close");
  var action = $("cb-compact-notice-action");
  var backdrop = $("cb-compact-notice-backdrop");
  if(close) close.onclick = closeCompactNotice;
  if(action) action.onclick = closeCompactNotice;
  if(backdrop) backdrop.onclick = closeCompactNotice;
  document.addEventListener("keydown", function(event){
    if(event.key === "Escape") closeCompactNotice();
  });
}
'''
replace_once(
    '\n\nfunction renderSeasonMetrics(){\n',
    functions + '\n\nfunction renderSeasonMetrics(){\n',
    "функции компактного уведомления",
)

replace_once(
    '      renderDataViews();\n      finishLoader("Мастерская открыта");\n',
    '      renderDataViews();\n      finishLoader("Мастерская открыта");\n      scheduleCompactNotice();\n',
    "запуск уведомления после загрузки",
)

replace_once(
    '  setupCreatorIdentityInputs();\n\n  var submit = $("cb-submit");\n',
    '  setupCreatorIdentityInputs();\n  setupCompactNotice();\n\n  var submit = $("cb-submit");\n',
    "инициализация уведомления",
)

if text == original:
    raise RuntimeError("index.html не изменён")

path.write_text(text, encoding="utf-8")
print("Безопасное уведомление и мобильное раскрытие событий добавлены")
