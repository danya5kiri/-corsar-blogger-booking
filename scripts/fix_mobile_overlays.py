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


replace_once(
'''html {
  scroll-behavior: smooth;
  background: var(--cb-canvas);
}''',
'''html {
  min-height: 100%;
  scroll-behavior: smooth;
  background: var(--cb-canvas);
}''',
"минимальная высота html",
)

replace_once(
'''body {
  margin: 0;
  min-width: 320px;''',
'''body {
  margin: 0;
  min-width: 320px;
  min-height: 100%;''',
"минимальная высота body",
)

replace_once(
'''body.cb-lock-scroll {
  overflow: hidden;
}''',
'''html.cb-overlay-lock {
  overflow: hidden;
  overscroll-behavior: none;
}

body.cb-lock-scroll {
  overflow: hidden;
  overscroll-behavior: none;
}''',
"блокировка загрузочного экрана",
)

replace_once(
'''.cb-splash {
  position: fixed;
  z-index: 9999;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #f7f7fb;
  transition: opacity .55s ease, visibility .55s ease;
}''',
'''.cb-splash {
  position: fixed;
  z-index: 9999;
  inset: 0;
  display: grid;
  width: 100vw;
  min-width: 100%;
  min-height: 100vh;
  height: 100vh;
  height: 100svh;
  height: 100lvh;
  place-items: center;
  overflow: hidden;
  overscroll-behavior: none;
  touch-action: none;
  isolation: isolate;
  padding: max(24px, env(safe-area-inset-top)) 24px max(24px, env(safe-area-inset-bottom));
  background: #f7f7fb;
  transition: opacity .55s ease, visibility .55s ease;
}''',
"полноэкранная загрузка",
)

replace_once(
'''body.cb-push-open {
  overflow: hidden;
}''',
'''body.cb-push-open {
  overflow: hidden;
  overscroll-behavior: none;
}''',
"блокировка уведомления",
)

replace_once(
'''.cb-weekly-push {
  position: fixed;
  z-index: 9800;
  inset: 0;
  display: grid;
  place-items: center;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .28s ease, visibility .28s ease;
}''',
'''.cb-weekly-push {
  position: fixed;
  z-index: 9800;
  inset: 0;
  display: grid;
  width: 100vw;
  min-width: 100%;
  min-height: 100vh;
  height: 100vh;
  height: 100svh;
  height: 100lvh;
  place-items: center;
  overflow: hidden;
  overscroll-behavior: none;
  isolation: isolate;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .28s ease, visibility .28s ease;
}''',
"полноэкранное уведомление",
)

replace_once(
'''  max-height: min(720px, calc(100vh - 36px));''',
'''  max-height: min(720px, calc(100dvh - 36px));''',
"высота карточки уведомления",
)

replace_once(
'''@media (max-width: 600px) {
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
  }''',
'''@media (max-width: 600px) {
  .cb-day {
    display: flex;
    min-height: 68px;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 4px 1px 6px;
  }

  .cb-day-weather {
    position: static;
    order: 1;
    width: 14px;
    height: 14px;
    margin: 0 auto 1px;
  }

  .cb-day-weather .cb-weather-icon {
    width: 14px;
    height: 14px;
  }

  .cb-day-num {
    order: 2;
    min-height: 17px;
    line-height: 17px;
  }

  .cb-day-count {
    order: 3;
    margin-top: 1px;
  }

  .cb-weekly-push {
    align-items: end;
    padding: max(12px, env(safe-area-inset-top)) 12px max(12px, env(safe-area-inset-bottom));
  }

  .cb-weekly-push-card {
    width: 100%;
    max-height: calc(100dvh - max(24px, env(safe-area-inset-top)) - max(24px, env(safe-area-inset-bottom)));
  }''',
"мобильная погода и уведомление",
)

old_title = "Последние события креаторов"
if text.count(old_title) != 3:
    raise RuntimeError(f"название блока: ожидалось 3 совпадения, найдено {text.count(old_title)}")
text = text.replace(old_title, "Последние события")

replace_once(
'''var weeklyPushTimer = null;
var weeklyPushRestoreFocus = null;
var weatherLastRequestedAt = 0;''',
'''var weeklyPushTimer = null;
var weeklyPushRestoreFocus = null;
var viewportLockScrollY = 0;
var viewportLocks = Object.create(null);
var weatherLastRequestedAt = 0;''',
"переменные блокировки позиции",
)

replace_once(
'''function $(id){ return document.getElementById(id); }
function pad(n){ return String(n).padStart(2,"0"); }
function makeDate(y,m,d){ return y + "-" + pad(m+1) + "-" + pad(d); }

function setupStickyNav(){''',
'''function $(id){ return document.getElementById(id); }
function pad(n){ return String(n).padStart(2,"0"); }
function makeDate(y,m,d){ return y + "-" + pad(m+1) + "-" + pad(d); }

function lockViewportScroll(reason){
  var key = String(reason || "overlay");
  if(viewportLocks[key]) return;

  if(!Object.keys(viewportLocks).length){
    viewportLockScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
    document.documentElement.classList.add("cb-overlay-lock");
    document.body.style.position = "fixed";
    document.body.style.top = (-viewportLockScrollY) + "px";
    document.body.style.right = "0";
    document.body.style.left = "0";
    document.body.style.width = "100%";
  }

  viewportLocks[key] = true;
}

function unlockViewportScroll(reason){
  var key = String(reason || "overlay");
  if(!viewportLocks[key]) return;
  delete viewportLocks[key];
  if(Object.keys(viewportLocks).length) return;

  var restoreY = viewportLockScrollY;
  document.body.style.position = "";
  document.body.style.top = "";
  document.body.style.right = "";
  document.body.style.left = "";
  document.body.style.width = "";
  document.documentElement.classList.remove("cb-overlay-lock");
  window.requestAnimationFrame(function(){ window.scrollTo(0, restoreY); });
}

function setupStickyNav(){''',
"функции сохранения позиции страницы",
)

replace_once(
'''function finishLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Всё готово", "success");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
    scheduleWeeklyPush();
  }, 520);
}

function failLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Расписание временно недоступно", "error");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
  }, 1100);
}''',
'''function finishLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Всё готово", "success");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
    unlockViewportScroll("splash");
    scheduleWeeklyPush();
  }, 520);
}

function failLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Расписание временно недоступно", "error");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
    unlockViewportScroll("splash");
  }, 1100);
}''',
"восстановление позиции после загрузки",
)

replace_once(
'''function closeWeeklyPush(){
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
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });''',
'''function closeWeeklyPush(){
  var modal = $("cb-weekly-push");
  if(!modal || modal.hidden) return;
  rememberWeeklyPushSeen();
  modal.classList.remove("is-visible");
  document.body.classList.remove("cb-push-open");
  setTimeout(function(){
    modal.hidden = true;
    unlockViewportScroll("weekly-push");
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
  lockViewportScroll("weekly-push");
  document.body.classList.add("cb-push-open");
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });''',
"сохранение позиции при уведомлении",
)

replace_once(
'''function init(){
  if(!$("corsar-blogger-booking")) return;

  updateSeasonCounter();''',
'''function init(){
  if(!$("corsar-blogger-booking")) return;

  lockViewportScroll("splash");
  updateSeasonCounter();''',
"фиксация загрузочного экрана",
)

if text == original:
    raise RuntimeError("index.html не изменён")

PATH.write_text(text, encoding="utf-8")
print("mobile overlay patch applied")
