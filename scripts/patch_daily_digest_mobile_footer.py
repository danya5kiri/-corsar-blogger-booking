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


replace_once(
'''  justify-content: space-between;
  gap: 18px;
  max-width: 720px;
  margin: 18px auto 0;
  padding: 15px 18px;
  border: 1px solid var(--cb-line);
  background: linear-gradient(100deg, #f5f1ff, #eefbfe);
  color: var(--cb-muted);
  text-align: left;
  font-size: 11px;
  line-height: 1.5;
}''',
'''  flex-direction: column;
  justify-content: center;
  gap: 14px;
  max-width: 720px;
  margin: 18px auto 0;
  padding: 18px;
  border: 1px solid var(--cb-line);
  background: linear-gradient(100deg, #f5f1ff, #eefbfe);
  color: var(--cb-muted);
  text-align: center;
  font-size: 11px;
  line-height: 1.5;
}''',
"центрирование обратной связи CREACLOUD",
)

replace_once(
'''  .cb-day-num + .cb-day-count {
    margin-top: 1px;
  }

  .cb-weekly-push {''',
'''  .cb-day-num + .cb-day-count {
    margin-top: 1px;
  }

  .cb-day-count-bookings {
    display: none;
  }

  .cb-weekly-push {''',
"скрытие количества записей в мобильном календаре",
)

replace_once(
'''          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count">записей: ' + count + '</span>' : '');''',
'''          (toursCount > 0 ? '<span class="cb-day-count">туров: ' + toursCount + '</span>' : '<span class="cb-day-count">нет туров</span>') +
          (count > 0 ? '<span class="cb-day-count cb-day-count-bookings">записей: ' + count + '</span>' : '');''',
"класс количества записей календаря",
)

replace_once(
'''var COMPACT_NOTICE_STORAGE_KEY = "corsar_compact_notice_seen_v1";
var COMPACT_NOTICE_TEST_DATE = "2026-07-22";
var LEADER_STATE_STORAGE_KEY = "corsar_leader_state_v1";''',
'''var COMPACT_NOTICE_STORAGE_KEY = "corsar_daily_notice_seen_v1";
var PORTAL_UPDATES = [{
  date: "2026-07-22",
  text: "Обновлены мобильный календарь, блок обратной связи CREACLOUD и ежедневная сводка портала."
}];
var LEADER_STATE_STORAGE_KEY = "corsar_leader_state_v1";''',
"настройки ежедневной сводки",
)

replace_once(
'''      <span class="cb-compact-notice-kicker">Важно на этой неделе</span>''',
'''      <span class="cb-compact-notice-kicker">Ежедневная сводка</span>''',
"заголовок ежедневной сводки",
)

replace_once(
'''function scheduleSiteNotices(){
  if(leaderChangeNoticeTimer) clearTimeout(leaderChangeNoticeTimer);
  if(compactNoticeTimer) clearTimeout(compactNoticeTimer);
  var leaderModal = $("cb-leader-change-notice");
  var compactModal = $("cb-compact-notice");
  if((leaderModal && !leaderModal.hidden) || (compactModal && !compactModal.hidden)) return;

  pendingLeaderChangeEvent = getLeaderChangesForToday();
  if(pendingLeaderChangeEvent){
    leaderChangeNoticeTimer = setTimeout(showLeaderChangeNotice, 900);
  } else {
    scheduleCompactNotice(900);
  }
}''',
'''function scheduleSiteNotices(){
  if(leaderChangeNoticeTimer) clearTimeout(leaderChangeNoticeTimer);
  if(compactNoticeTimer) clearTimeout(compactNoticeTimer);
  var compactModal = $("cb-compact-notice");
  if(compactModal && !compactModal.hidden) return;

  pendingLeaderChangeEvent = null;
  scheduleCompactNotice(900);
}''',
"единый запуск ежедневной сводки",
)

replace_once(
'''function shouldShowCompactNotice(){
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
}''',
'''function shouldShowCompactNotice(){
  var today = getTodayKey();
  if(!creatorDirectoryReady) return false;
  try {
    return localStorage.getItem(COMPACT_NOTICE_STORAGE_KEY) !== today;
  } catch(e) {
    return true;
  }
}

function rememberCompactNoticeSeen(){
  try { localStorage.setItem(COMPACT_NOTICE_STORAGE_KEY, getTodayKey()); } catch(e) {}
}''',
"ежедневная периодичность уведомления",
)

replace_once(
'''function buildCompactNoticeMarkup(){
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
}''',
'''function compactCreatorList(names, limit){
  var unique = [];
  var seen = Object.create(null);
  (names || []).forEach(function(name){
    var creator = normalizeTelegram(name);
    if(!creator || seen[creator]) return;
    seen[creator] = true;
    unique.push(creator);
  });
  unique.sort(function(a, b){ return a.localeCompare(b, "ru"); });
  var max = Math.max(1, Number(limit) || 3);
  var visible = unique.slice(0, max).map(escapeHtml).join(", ");
  return visible + (unique.length > max ? " и ещё " + (unique.length - max) : "");
}

function getDailyActivitySummary(dateKey){
  var firstBookingByCreator = Object.create(null);
  var bookingCreators = [];
  var contentCreators = [];
  var bookingsCount = 0;
  var contentCount = 0;

  bookings.forEach(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    var tripDate = normalizeDate(booking.date);
    var timestamp = getActivityTimestamp(booking);
    if(isInactiveBooking(booking) || !creator || isDeletedCreator(creator) || !isDateInSeason(tripDate) || !Number.isFinite(timestamp)) return;

    if(!firstBookingByCreator[creator] || timestamp < firstBookingByCreator[creator]) firstBookingByCreator[creator] = timestamp;
    if(getVladivostokDateKey(new Date(timestamp)) === dateKey){
      bookingsCount += 1;
      bookingCreators.push(creator);
    }
  });

  getPublishedContentItems().forEach(function(report){
    var creator = getReportCreator(report);
    var timestamp = getActivityTimestamp(report);
    if(!creator || isDeletedCreator(creator) || !Number.isFinite(timestamp)) return;
    if(getVladivostokDateKey(new Date(timestamp)) === dateKey){
      contentCount += 1;
      contentCreators.push(creator);
    }
  });

  var newCreators = Object.keys(firstBookingByCreator).filter(function(creator){
    return getVladivostokDateKey(new Date(firstBookingByCreator[creator])) === dateKey;
  });

  return {
    newCreators: newCreators,
    bookings: bookingsCount,
    bookingCreators: bookingCreators,
    content: contentCount,
    contentCreators: contentCreators
  };
}

function buildDailyPeriodNoticeItem(label, summary){
  var parts = [];
  if(summary.newCreators.length){
    parts.push(summary.newCreators.length + " " + pluralCount(summary.newCreators.length, "новый креатор", "новых креатора", "новых креаторов") + ": " + compactCreatorList(summary.newCreators, 3));
  }
  if(summary.bookings){
    parts.push(summary.bookings + " " + pluralCount(summary.bookings, "бронирование", "бронирования", "бронирований") + (summary.bookingCreators.length ? ": " + compactCreatorList(summary.bookingCreators, 3) : ""));
  }
  if(summary.content){
    parts.push(summary.content + " " + pluralCount(summary.content, "публикация", "публикации", "публикаций") + (summary.contentCreators.length ? ": " + compactCreatorList(summary.contentCreators, 2) : ""));
  }
  if(!parts.length) parts.push("новых регистраций, броней и публикаций пока нет");
  return '<li class="cb-compact-notice-item"><span><strong>' + escapeHtml(label) + ':</strong> ' + parts.join(" · ") + '</span></li>';
}

function buildUniqueLeaderTransitionTimeline(){
  var seenTours = Object.create(null);
  var visits = Object.create(null);
  var previousLeader = "";
  var transitions = [];
  var ordered = bookings.map(function(booking, index){
    return {booking: booking, index: index, timestamp: getActivityTimestamp(booking)};
  }).filter(function(entry){
    var creator = normalizeTelegram(entry.booking.telegram);
    return !isInactiveBooking(entry.booking) && creator && !isDeletedCreator(creator) && Number.isFinite(entry.timestamp);
  }).sort(function(a, b){
    return a.timestamp - b.timestamp || a.index - b.index;
  });

  ordered.forEach(function(entry){
    var booking = entry.booking;
    var creator = normalizeTelegram(booking.telegram);
    visits[creator] = (visits[creator] || 0) + 1;
    if(!seenTours[creator]) seenTours[creator] = Object.create(null);
    if(!isExcludedTour(booking.tour)){
      var tourKey = normalizeTour(booking.tour);
      if(tourKey) seenTours[creator][tourKey] = true;
    }

    var currentLeader = Object.keys(visits).map(function(name){
      return {name: name, uniqueTours: Object.keys(seenTours[name] || {}).length, visits: visits[name]};
    }).filter(function(item){ return item.uniqueTours > 0; }).sort(function(a, b){
      return b.uniqueTours - a.uniqueTours || b.visits - a.visits || a.name.localeCompare(b.name, "ru");
    })[0];
    var currentName = currentLeader ? currentLeader.name : "";

    if(previousLeader && currentName && currentName !== previousLeader){
      transitions.push({
        kind: "unique",
        previous: previousLeader,
        current: currentName,
        score: currentLeader.uniqueTours,
        date: getVladivostokDateKey(new Date(entry.timestamp)),
        sortValue: entry.timestamp
      });
    }
    previousLeader = currentName;
  });

  return transitions;
}

function buildDailyLeaderChangesNotice(todayKey, yesterdayKey){
  var activeBookings = bookings.filter(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    return !isInactiveBooking(booking) && creator && !isDeletedCreator(creator);
  });
  var activeReports = getPublishedContentItems().filter(function(report){
    var creator = getReportCreator(report);
    return creator && !isDeletedCreator(creator);
  });
  var transitions = buildLeaderTransitionTimeline(activeBookings, "visits", function(booking){ return booking.telegram; })
    .concat(buildLeaderTransitionTimeline(activeReports, "content", getReportCreator))
    .concat(buildUniqueLeaderTransitionTimeline())
    .filter(function(change){ return change.date === todayKey || change.date === yesterdayKey; })
    .sort(function(a, b){ return a.sortValue - b.sortValue; });

  var latest = Object.create(null);
  transitions.forEach(function(change){ latest[change.date + ":" + change.kind] = change; });
  var labels = {visits: "по турам", content: "по контенту", unique: "по уникальным турам"};
  var parts = Object.keys(latest).sort().map(function(key){
    var change = latest[key];
    var dayLabel = change.date === todayKey ? "сегодня" : "вчера";
    return dayLabel + " " + labels[change.kind] + " — <strong>" + escapeHtml(change.current) + "</strong>";
  });
  if(!parts.length) return "";
  return '<li class="cb-compact-notice-item"><span><strong>Смена лидеров:</strong> ' + parts.join(" · ") + '</span></li>';
}

function getCurrentUniqueLeaderSnapshot(){
  var visits = Object.create(null);
  bookings.forEach(function(booking){
    var creator = normalizeTelegram(booking.telegram);
    if(isInactiveBooking(booking) || !creator || isDeletedCreator(creator)) return;
    visits[creator] = (visits[creator] || 0) + 1;
  });
  var leader = Object.keys(visits).map(function(name){
    return {name: name, visits: visits[name], uniqueTours: Math.min(getCreatorTourVariety(name), TOTAL_UNIQUE_TOURS)};
  }).filter(function(item){ return item.uniqueTours > 0; }).sort(function(a, b){
    return b.uniqueTours - a.uniqueTours || b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  })[0];
  return leader || {name: "", visits: 0, uniqueTours: 0};
}

function buildCurrentLeadersNotice(){
  var snapshot = getCurrentLeaderSnapshot();
  var unique = getCurrentUniqueLeaderSnapshot();
  var parts = [];
  if(snapshot.visits.name) parts.push("туры — <strong>" + escapeHtml(snapshot.visits.name) + "</strong> (" + snapshot.visits.score + ")");
  if(snapshot.content.name) parts.push("контент — <strong>" + escapeHtml(snapshot.content.name) + "</strong> (" + snapshot.content.score + ")");
  if(unique.name) parts.push("уникальные — <strong>" + escapeHtml(unique.name) + "</strong> (" + unique.uniqueTours + "/" + TOTAL_UNIQUE_TOURS + ")");
  if(!parts.length) return "";
  return '<li class="cb-compact-notice-item"><span><strong>Лидеры сейчас:</strong> ' + parts.join(" · ") + '</span></li>';
}

function buildPortalUpdatesNotice(todayKey, yesterdayKey){
  var updates = PORTAL_UPDATES.filter(function(update){
    return update && (update.date === todayKey || update.date === yesterdayKey) && update.text;
  });
  if(!updates.length) return "";
  return '<li class="cb-compact-notice-item"><span><strong>Портал:</strong> ' + updates.map(function(update){ return escapeHtml(update.text); }).join(" ") + '</span></li>';
}

function buildCompactNoticeMarkup(){
  var todayKey = getTodayKey();
  var yesterdayKey = addDaysToDateKey(todayKey, -1);
  var items = [
    buildDailyPeriodNoticeItem("Сегодня", getDailyActivitySummary(todayKey)),
    buildDailyPeriodNoticeItem("Вчера", getDailyActivitySummary(yesterdayKey))
  ];
  var changes = buildDailyLeaderChangesNotice(todayKey, yesterdayKey);
  var leaders = buildCurrentLeadersNotice();
  var portal = buildPortalUpdatesNotice(todayKey, yesterdayKey);
  if(changes) items.push(changes);
  if(leaders) items.push(leaders);
  if(portal) items.push(portal);

  return '<h2 id="cb-compact-notice-title" class="cb-compact-notice-title">Сводка <strong>мастерской</strong></h2>' +
    '<ul class="cb-compact-notice-list">' + items.slice(0, 5).join('') + '</ul>';
}''',
"ежедневная сводка сегодня и вчера",
)

replace_once(
'''  setupCreatorIdentityInputs();
  setupLeaderChangeNotice();
  setupCompactNotice();''',
'''  setupCreatorIdentityInputs();
  setupCompactNotice();''',
"отключение отдельного уведомления лидеров",
)

path.write_text(text, encoding="utf-8")
print("Патч ежедневной сводки применён")
