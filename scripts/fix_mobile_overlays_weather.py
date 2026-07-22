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
'''body.cb-lock-scroll {
  overflow: hidden;
}
''',
'''body.cb-lock-scroll {
  overflow: hidden;
  height: 100vh;
  height: 100dvh;
  overscroll-behavior: none;
  touch-action: none;
}

body.cb-lock-scroll #corsar-blogger-booking {
  visibility: hidden;
}
''',
"блокировка загрузочной страницы",
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
}
''',
'''.cb-splash {
  position: fixed;
  z-index: 2147483647;
  inset: 0;
  display: grid;
  width: 100%;
  height: 100vh;
  height: 100dvh;
  min-height: 100svh;
  place-items: center;
  overflow: hidden;
  box-sizing: border-box;
  padding: max(24px, env(safe-area-inset-top)) 24px max(24px, env(safe-area-inset-bottom));
  background: #f7f7fb;
  isolation: isolate;
  overscroll-behavior: none;
  transition: opacity .55s ease, visibility .55s ease;
}
''',
"полноэкранный splash",
)

replace_once(
'''body.cb-push-open {
  overflow: hidden;
}
''',
'''body.cb-push-open {
  overflow: hidden;
  overscroll-behavior: none;
}
''',
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
}
''',
'''.cb-weekly-push {
  position: fixed;
  z-index: 2147483646;
  inset: 0;
  display: grid;
  width: 100%;
  height: 100vh;
  height: 100dvh;
  min-height: 100svh;
  place-items: center;
  overflow: hidden;
  box-sizing: border-box;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  overscroll-behavior: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity .28s ease, visibility .28s ease;
}
''',
"полноэкранное уведомление",
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
  }
''',
'''@media (max-width: 600px) {
  .cb-day {
    min-height: 70px;
    padding: 4px 1px 6px;
  }

  .cb-day-num {
    min-height: 17px;
    line-height: 17px;
  }

  .cb-day-weather {
    position: static;
    width: 14px;
    height: 14px;
    margin: 0 auto 1px;
  }

  .cb-day-weather .cb-weather-icon {
    width: 14px;
    height: 14px;
  }

  .cb-day-num + .cb-day-count {
    margin-top: 1px;
  }

  .cb-weekly-push {
    align-items: center;
    min-height: 100dvh;
    padding: max(12px, env(safe-area-inset-top)) 12px max(12px, env(safe-area-inset-bottom));
  }

  .cb-weekly-push-card {
    width: 100%;
    max-height: calc(100dvh - 24px);
  }
''',
"мобильные стили погоды и уведомления",
)

old_calendar = '''        cell.innerHTML =
          '<span class="cb-day-num">' + day + '</span>' +
          (forecast ? '<span class="cb-day-weather" title="' + escapeHtml(forecastLabel) + '">' + weatherIcon(forecast.code) + '</span>' : '') +
          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count">записей: ' + count + '</span>' : '');
'''
new_calendar = '''        cell.innerHTML =
          (forecast ? '<span class="cb-day-weather" title="' + escapeHtml(forecastLabel) + '">' + weatherIcon(forecast.code) + '</span>' : '') +
          '<span class="cb-day-num">' + day + '</span>' +
          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count">записей: ' + count + '</span>' : '');
'''
replace_once(old_calendar, new_calendar, "порядок значка погоды и даты")

text = text.replace("Последние события креаторов", "Последние события")
if "Последние события креаторов" in text:
    raise RuntimeError("старое название блока осталось в файле")
if text.count("Последние события") < 3:
    raise RuntimeError("новое название блока применилось не ко всем представлениям")

marker = '''function getWeekdayFromDateKey(dateKey){
'''
insert = '''var weeklyPushScrollY = 0;

function lockWeeklyPushViewport(){
  weeklyPushScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
  document.body.style.position = "fixed";
  document.body.style.top = "-" + weeklyPushScrollY + "px";
  document.body.style.right = "0";
  document.body.style.left = "0";
  document.body.style.width = "100%";
  document.body.classList.add("cb-push-open");
}

function unlockWeeklyPushViewport(){
  var restoreY = weeklyPushScrollY;
  document.body.classList.remove("cb-push-open");
  document.body.style.position = "";
  document.body.style.top = "";
  document.body.style.right = "";
  document.body.style.left = "";
  document.body.style.width = "";
  weeklyPushScrollY = 0;
  window.scrollTo(0, restoreY);
}

function getWeekdayFromDateKey(dateKey){
'''
replace_once(marker, insert, "фиксация положения страницы")

replace_once(
'''  modal.classList.remove("is-visible");
  document.body.classList.remove("cb-push-open");
  setTimeout(function(){
''',
'''  modal.classList.remove("is-visible");
  unlockWeeklyPushViewport();
  setTimeout(function(){
''',
"восстановление прокрутки после уведомления",
)

replace_once(
'''  body.innerHTML = buildWeeklyPushMarkup();
  modal.hidden = false;
  document.body.classList.add("cb-push-open");
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });
''',
'''  body.innerHTML = buildWeeklyPushMarkup();
  modal.hidden = false;
  lockWeeklyPushViewport();
  var card = modal.querySelector(".cb-weekly-push-card");
  if(card) card.scrollTop = 0;
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });
''',
"открытие уведомления без скачка страницы",
)

if text == original:
    raise RuntimeError("index.html не изменился")
if 'API_URL: "https://script.google.com/macros/s/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/exec"' not in text:
    raise RuntimeError("API_URL изменён")
for token in ['id="cb-submit"', 'id="cb-report-submit"', 'id="cb-calendar"', 'function submitBooking()', 'function submitReport()']:
    if token not in text:
        raise RuntimeError(f"утрачена рабочая часть: {token}")
if text.index('class="cb-day-weather"') > text.index('class="cb-day-num"', text.index('cell.innerHTML =')):
    raise RuntimeError("значок погоды не перенесён перед датой")

PATH.write_text(text, encoding="utf-8")
print("Mobile overlay and weather fixes applied")
