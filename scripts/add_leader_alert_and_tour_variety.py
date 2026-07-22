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


def insert_before(marker: str, addition: str, label: str) -> None:
    global text
    count = text.count(marker)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(marker, addition + marker, 1)


def replace_block(start_marker: str, end_marker: str, replacement: str, label: str) -> None:
    global text
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f"{label}: начало блока не найдено")
    end = text.find(end_marker, start)
    if end < 0:
        raise RuntimeError(f"{label}: конец блока не найден")
    text = text[:start] + replacement + text[end:]


ranking_css = r'''
.cb-rank-main {
  display: grid;
  min-width: 0;
  gap: 7px;
}

.cb-rank-coverage {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  min-width: 0;
  color: #777c89;
  font-size: 9px;
  font-weight: 700;
  line-height: 1.25;
}

.cb-rank-coverage-copy {
  white-space: nowrap;
}

.cb-rank-coverage-copy strong {
  color: var(--cb-ink);
  font-size: 11px;
  font-weight: 840;
}

.cb-rank-coverage-dots {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.cb-rank-coverage-dot {
  width: 7px;
  height: 7px;
  border: 1px solid rgba(23, 23, 25, .12);
  border-radius: 50%;
  background: rgba(255,255,255,.54);
}

.cb-rank-coverage-dot.is-filled {
  border-color: transparent;
  background: linear-gradient(135deg, var(--cb-blue), var(--cb-cyan) 54%, var(--cb-lilac-strong));
  box-shadow: 0 0 0 2px rgba(78, 203, 237, .09);
}

.cb-rank-row.is-top-1 .cb-rank-coverage-dot.is-filled {
  background: linear-gradient(135deg, #ff9e67, #7f67f8 58%, #4ecbed);
}

'''
insert_before(".cb-rank-score {\n", ranking_css, "стили уникальных туров")

mobile_ranking_old = '''  .cb-rank-score {
    font-size: 27px;
  }

  .cb-results-grid {
'''
mobile_ranking_new = '''  .cb-rank-score {
    font-size: 27px;
  }

  .cb-rank-main {
    gap: 6px;
  }

  .cb-rank-coverage {
    gap: 6px;
    font-size: 8px;
  }

  .cb-rank-coverage-copy {
    white-space: normal;
  }

  .cb-rank-coverage-dot {
    width: 6px;
    height: 6px;
  }

  .cb-results-grid {
'''
replace_once(mobile_ranking_old, mobile_ranking_new, "мобильные стили рейтинга")

leader_notice_css = r'''
.cb-leader-change-notice[hidden] {
  display: none;
}

.cb-leader-change-notice {
  position: fixed;
  z-index: 2147483647;
  inset: 0;
  display: grid;
  place-items: center;
  box-sizing: border-box;
  padding: max(18px, env(safe-area-inset-top)) 18px max(18px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .24s ease, visibility .24s ease;
}

.cb-leader-change-notice.is-visible {
  opacity: 1;
  visibility: visible;
}

.cb-leader-change-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(237, 241, 248, .62);
  backdrop-filter: blur(13px) saturate(112%);
  -webkit-backdrop-filter: blur(13px) saturate(112%);
}

.cb-leader-change-card {
  position: relative;
  z-index: 1;
  width: min(440px, 100%);
  padding: 18px;
  border: 1px solid rgba(23, 23, 25, .09);
  background:
    radial-gradient(circle at 92% 4%, rgba(255,255,255,.91), transparent 32%),
    linear-gradient(140deg, rgba(255, 247, 218, .98), rgba(255, 229, 220, .96) 44%, rgba(229, 222, 255, .96) 72%, rgba(224, 248, 251, .96));
  box-shadow: 0 30px 78px rgba(42, 45, 59, .24);
  color: var(--cb-ink);
  transform: translateY(12px) scale(.99);
  transition: transform .26s ease;
}

.cb-leader-change-notice.is-visible .cb-leader-change-card {
  transform: translateY(0) scale(1);
}

.cb-leader-change-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.cb-leader-change-kicker {
  color: #625d68;
  font-size: 9px;
  font-weight: 840;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.cb-leader-change-close {
  display: grid;
  flex: 0 0 32px;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 1px solid rgba(23, 23, 25, .11);
  border-radius: 50%;
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 20px;
  line-height: 1;
}

.cb-leader-change-title {
  margin: 12px 0 0;
  font-size: clamp(29px, 7vw, 40px);
  font-weight: 340;
  line-height: .98;
  letter-spacing: -.055em;
}

.cb-leader-change-title strong {
  display: block;
  font-weight: 830;
}

.cb-leader-change-intro {
  margin: 10px 0 0;
  color: #686473;
  font-size: 11px;
  line-height: 1.45;
}

.cb-leader-change-list {
  display: grid;
  gap: 8px;
  margin: 15px 0 0;
  padding: 0;
  list-style: none;
}

.cb-leader-change-item {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  align-items: center;
  gap: 11px;
  padding: 11px 12px;
  border: 1px solid rgba(23,23,25,.07);
  background: rgba(255,255,255,.54);
}

.cb-leader-change-badge {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--cb-ink);
  color: #fff;
  font-size: 14px;
  font-weight: 840;
}

.cb-leader-change-copy {
  display: grid;
  min-width: 0;
  gap: 3px;
}

.cb-leader-change-copy small {
  color: #797480;
  font-size: 8px;
  font-weight: 820;
  letter-spacing: .075em;
  text-transform: uppercase;
}

.cb-leader-change-copy strong {
  overflow: hidden;
  font-size: 18px;
  font-weight: 830;
  letter-spacing: -.035em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-leader-change-copy span {
  color: #6f6a76;
  font-size: 9px;
  line-height: 1.4;
}

.cb-leader-change-action {
  width: 100%;
  min-height: 48px;
  margin-top: 14px;
  padding: 0 16px;
  border: 0;
  background: linear-gradient(105deg, var(--cb-ink), #344c92 58%, var(--cb-cyan));
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  font-weight: 800;
}

'''
insert_before(".cb-message {\n", leader_notice_css, "стили уведомления о лидере")

leader_notice_markup = '''
<div id="cb-leader-change-notice" class="cb-leader-change-notice" hidden role="dialog" aria-modal="true" aria-labelledby="cb-leader-change-title">
  <div id="cb-leader-change-backdrop" class="cb-leader-change-backdrop"></div>
  <article class="cb-leader-change-card">
    <div class="cb-leader-change-top">
      <span class="cb-leader-change-kicker">Событие дня</span>
      <button type="button" id="cb-leader-change-close" class="cb-leader-change-close" aria-label="Закрыть уведомление">×</button>
    </div>
    <div id="cb-leader-change-body"></div>
    <button type="button" id="cb-leader-change-action" class="cb-leader-change-action">Смотреть обновлённый рейтинг</button>
  </article>
</div>

'''
insert_before('<div id="cb-compact-notice" class="cb-compact-notice"', leader_notice_markup, "разметка уведомления о лидере")

vars_old = '''var COMPACT_NOTICE_STORAGE_KEY = "corsar_compact_notice_seen_v1";
var COMPACT_NOTICE_TEST_DATE = "2026-07-22";
var compactNoticeTimer = null;
var compactNoticeRestoreFocus = null;
'''
vars_new = '''var COMPACT_NOTICE_STORAGE_KEY = "corsar_compact_notice_seen_v1";
var COMPACT_NOTICE_TEST_DATE = "2026-07-22";
var LEADER_STATE_STORAGE_KEY = "corsar_leader_state_v1";
var LEADER_EVENT_STORAGE_KEY = "corsar_leader_event_v1";
var compactNoticeTimer = null;
var compactNoticeRestoreFocus = null;
var leaderChangeNoticeTimer = null;
var leaderChangeRestoreFocus = null;
var pendingLeaderChangeEvent = null;
'''
replace_once(vars_old, vars_new, "переменные уведомлений")

leader_helpers = r'''
function getLeaderFromScoreTotals(totals){
  var names = Object.keys(totals || {});
  if(!names.length) return "";
  return names.sort(function(a, b){
    return Number(totals[b] || 0) - Number(totals[a] || 0) || a.localeCompare(b, "ru");
  })[0] || "";
}

function getCurrentLeaderSnapshot(){
  var visitTotals = Object.create(null);
  var contentTotals = Object.create(null);

  bookings.forEach(function(booking){
    if(isInactiveBooking(booking)) return;
    var creator = normalizeTelegram(booking.telegram);
    if(!creator || isDeletedCreator(creator)) return;
    visitTotals[creator] = (visitTotals[creator] || 0) + 1;
  });

  getPublishedContentItems().forEach(function(report){
    var creator = getReportCreator(report);
    if(!creator || isDeletedCreator(creator)) return;
    contentTotals[creator] = (contentTotals[creator] || 0) + 1;
  });

  var visitsLeader = getLeaderFromScoreTotals(visitTotals);
  var contentLeader = getLeaderFromScoreTotals(contentTotals);
  return {
    visits: {name: visitsLeader, score: visitsLeader ? visitTotals[visitsLeader] : 0},
    content: {name: contentLeader, score: contentLeader ? contentTotals[contentLeader] : 0}
  };
}

function buildLeaderTransitionTimeline(items, kind, creatorGetter){
  var totals = Object.create(null);
  var previousLeader = "";
  var transitions = [];
  var ordered = (items || []).map(function(item, index){
    return {
      item: item,
      index: index,
      sortValue: getActivitySortValue(item, index),
      timestamp: getActivityTimestamp(item)
    };
  }).sort(function(a, b){
    return a.sortValue - b.sortValue || a.index - b.index;
  });

  ordered.forEach(function(entry){
    var creator = normalizeTelegram(creatorGetter(entry.item));
    if(!creator || isDeletedCreator(creator)) return;
    totals[creator] = (totals[creator] || 0) + 1;
    var currentLeader = getLeaderFromScoreTotals(totals);

    if(previousLeader && currentLeader && currentLeader !== previousLeader && Number.isFinite(entry.timestamp)){
      transitions.push({
        kind: kind,
        previous: previousLeader,
        current: currentLeader,
        score: totals[currentLeader],
        date: getVladivostokDateKey(new Date(entry.timestamp)),
        sortValue: entry.timestamp
      });
    }

    previousLeader = currentLeader;
  });

  return transitions;
}

function readLeaderStorage(key){
  try {
    var value = JSON.parse(localStorage.getItem(key) || "null");
    return value && typeof value === "object" ? value : null;
  } catch(e) {
    return null;
  }
}

function writeLeaderStorage(key, value){
  try { localStorage.setItem(key, JSON.stringify(value)); } catch(e) {}
}

function getLeaderChangesForToday(){
  var today = getTodayKey();
  var snapshot = getCurrentLeaderSnapshot();
  var previousSnapshot = readLeaderStorage(LEADER_STATE_STORAGE_KEY);
  var storedEvent = readLeaderStorage(LEADER_EVENT_STORAGE_KEY);
  var changesByKind = Object.create(null);

  if(storedEvent && storedEvent.date === today && Array.isArray(storedEvent.changes)){
    storedEvent.changes.forEach(function(change){
      if(change && change.kind) changesByKind[change.kind] = change;
    });
  }

  var deterministic = buildLeaderTransitionTimeline(bookings, "visits", function(booking){ return booking.telegram; })
    .concat(buildLeaderTransitionTimeline(getPublishedContentItems(), "content", getReportCreator))
    .filter(function(change){ return change.date === today; })
    .sort(function(a, b){ return a.sortValue - b.sortValue; });

  deterministic.forEach(function(change){
    changesByKind[change.kind] = change;
  });

  ["visits", "content"].forEach(function(kind){
    var before = previousSnapshot && previousSnapshot[kind];
    var now = snapshot[kind];
    if(before && before.name && now && now.name && before.name !== now.name){
      changesByKind[kind] = {
        kind: kind,
        previous: before.name,
        current: now.name,
        score: now.score,
        date: today,
        sortValue: Date.now()
      };
    }
  });

  writeLeaderStorage(LEADER_STATE_STORAGE_KEY, snapshot);

  var changes = Object.keys(changesByKind).map(function(kind){ return changesByKind[kind]; }).filter(function(change){
    return change && change.current && change.date === today;
  });

  if(changes.length){
    var event = {date: today, changes: changes};
    writeLeaderStorage(LEADER_EVENT_STORAGE_KEY, event);
    return event;
  }

  return null;
}

function buildLeaderChangeMarkup(event){
  var changes = event && Array.isArray(event.changes) ? event.changes : [];
  var list = changes.map(function(change){
    var isVisits = change.kind === "visits";
    var label = isVisits ? "Новый лидер по посещениям" : "Новый лидер по контенту";
    var scoreText = isVisits
      ? change.score + " " + pluralCount(change.score, "поездка", "поездки", "поездок")
      : change.score + " " + pluralCount(change.score, "работа", "работы", "работ");
    var previousText = change.previous ? "Смена: " + escapeHtml(change.previous) + " → " : "";
    return '<li class="cb-leader-change-item">' +
      '<span class="cb-leader-change-badge" aria-hidden="true">1</span>' +
      '<span class="cb-leader-change-copy"><small>' + escapeHtml(label) + '</small><strong>' + escapeHtml(change.current) + '</strong>' +
      '<span>' + previousText + escapeHtml(change.current) + ' · ' + escapeHtml(scoreText) + '</span></span></li>';
  }).join("");

  return '<h2 id="cb-leader-change-title" class="cb-leader-change-title">Новый лидер <strong>сезона</strong></h2>' +
    '<p class="cb-leader-change-intro">Рейтинг изменился сегодня. Уведомление будет доступно весь день.</p>' +
    '<ul class="cb-leader-change-list">' + list + '</ul>';
}

function closeLeaderChangeNotice(openRanking){
  var modal = $("cb-leader-change-notice");
  if(!modal || modal.hidden) return;
  modal.classList.remove("is-visible");
  setTimeout(function(){
    modal.hidden = true;
    if(openRanking){
      var ranking = $("ranking");
      if(ranking) ranking.scrollIntoView({behavior: "smooth", block: "start"});
    } else if(leaderChangeRestoreFocus && typeof leaderChangeRestoreFocus.focus === "function"){
      leaderChangeRestoreFocus.focus();
    }
    leaderChangeRestoreFocus = null;
    if(shouldShowCompactNotice()) scheduleCompactNotice(360);
  }, 240);
}

function showLeaderChangeNotice(){
  if(!pendingLeaderChangeEvent) return;
  var modal = $("cb-leader-change-notice");
  var body = $("cb-leader-change-body");
  if(!modal || !body) return;

  leaderChangeRestoreFocus = document.activeElement;
  body.innerHTML = buildLeaderChangeMarkup(pendingLeaderChangeEvent);
  modal.hidden = false;
  window.requestAnimationFrame(function(){ modal.classList.add("is-visible"); });
  var close = $("cb-leader-change-close");
  if(close) setTimeout(function(){ close.focus(); }, 60);
}

function scheduleSiteNotices(){
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
}

function setupLeaderChangeNotice(){
  var close = $("cb-leader-change-close");
  var action = $("cb-leader-change-action");
  var backdrop = $("cb-leader-change-backdrop");
  if(close) close.onclick = function(){ closeLeaderChangeNotice(false); };
  if(action) action.onclick = function(){ closeLeaderChangeNotice(true); };
  if(backdrop) backdrop.onclick = function(){ closeLeaderChangeNotice(false); };
  document.addEventListener("keydown", function(event){
    if(event.key === "Escape") closeLeaderChangeNotice(false);
  });
}

'''
insert_before("function getWeekdayFromDateKey(dateKey){\n", leader_helpers, "логика смены лидеров")

schedule_old = '''function scheduleCompactNotice(){
  if(compactNoticeTimer) clearTimeout(compactNoticeTimer);
  compactNoticeTimer = setTimeout(showCompactNotice, 900);
}
'''
schedule_new = '''function scheduleCompactNotice(delay){
  if(compactNoticeTimer) clearTimeout(compactNoticeTimer);
  compactNoticeTimer = setTimeout(showCompactNotice, Number(delay) || 900);
}
'''
replace_once(schedule_old, schedule_new, "параметр задержки пятничного уведомления")

render_analytics = r'''function getCreatorTourVariety(creator){
  var seen = Object.create(null);
  bookings.forEach(function(booking){
    if(isInactiveBooking(booking) || normalizeTelegram(booking.telegram) !== creator || isExcludedTour(booking.tour)) return;
    var key = normalizeTour(booking.tour);
    if(key) seen[key] = true;
  });
  return Object.keys(seen).length;
}

function renderTourVarietyDots(uniqueTours, visits){
  var ratio = visits > 0 ? Math.max(0, Math.min(1, uniqueTours / visits)) : 0;
  var filled = uniqueTours > 0 ? Math.max(1, Math.round(ratio * 5)) : 0;
  var dots = "";
  for(var i = 0; i < 5; i++){
    dots += '<span class="cb-rank-coverage-dot' + (i < filled ? ' is-filled' : '') + '"></span>';
  }
  return dots;
}

function renderAnalytics(){
  var el = $("cb-analytics");
  if(!el) return;

  var users = {};

  bookings.forEach(function(b){
    if(isInactiveBooking(b)) return;
    var tg = normalizeTelegram(b.telegram);
    if(isDeletedCreator(tg)) return;
    if(tg){
      if(!users[tg]) users[tg] = 0;
      users[tg] += 1;
    }
  });

  var ranking = Object.keys(users).map(function(tg){
    return {name: tg, visits: users[tg], uniqueTours: getCreatorTourVariety(tg)};
  }).sort(function(a, b){
    return b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  var leaderName = $("cb-leader-name");
  var leaderVisits = $("cb-leader-visits");
  var leaderCard = $("cb-leader-card");
  var leaderAction = $("cb-leader-action");
  if(ranking.length){
    leaderName.textContent = ranking[0].name;
    leaderVisits.textContent = ranking[0].visits + " " + pluralCount(ranking[0].visits, "тур", "тура", "туров") + " · первое место";
    if(leaderCard){
      leaderCard.setAttribute("data-creator", ranking[0].name);
      leaderCard.setAttribute("aria-disabled", "false");
      leaderCard.setAttribute("aria-label", "Показать опубликованные работы лидера " + ranking[0].name);
      leaderCard.onclick = function(){
        focusCreatorResults(this.getAttribute("data-creator"));
      };
    }
    if(leaderAction) leaderAction.hidden = false;
  } else {
    leaderName.textContent = "Пока нет";
    leaderVisits.textContent = "Первая поездка откроет рейтинг";
    if(leaderCard){
      leaderCard.removeAttribute("data-creator");
      leaderCard.setAttribute("aria-disabled", "true");
      leaderCard.setAttribute("aria-label", "Лидер сезона пока не определён");
      leaderCard.onclick = null;
    }
    if(leaderAction) leaderAction.hidden = true;
  }

  if(!ranking.length){
    el.innerHTML = '<div class="cb-empty-state">Пока нет данных для рейтинга.</div>';
    return;
  }

  el.innerHTML = '<div id="cb-ranking-list" class="cb-ranking-list' + (rankingExpanded ? ' is-expanded' : '') + '">' + ranking.map(function(item, index){
    var place = index + 1;
    var podiumClass = place <= 3 ? ' is-podium is-top-' + place : '';
    var varietyText = item.uniqueTours + " " + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") +
      " из " + item.visits + " " + pluralCount(item.visits, "поездки", "поездок", "поездок");
    return '<div class="cb-rank-row' + podiumClass + '">' +
      '<span class="cb-rank-num" aria-label="' + place + ' место">' + String(place).padStart(2, "0") + '</span>' +
      '<span class="cb-rank-main"><span class="cb-rank-name">' + escapeHtml(item.name) + '</span>' +
        '<span class="cb-rank-coverage" title="' + escapeHtml(varietyText + '. Двухдневные программы не учитываются в уникальных турах.') + '">' +
          '<span class="cb-rank-coverage-copy"><strong>' + item.uniqueTours + '</strong> ' + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") + ' из ' + item.visits + '</span>' +
          '<span class="cb-rank-coverage-dots" aria-hidden="true">' + renderTourVarietyDots(item.uniqueTours, item.visits) + '</span>' +
        '</span></span>' +
      '<span class="cb-rank-score">' + item.visits + '<small>' + pluralCount(item.visits, "поездка", "поездки", "поездок") + '</small></span>' +
      '</div>';
  }).join("") + '</div>' + (ranking.length > 5 ?
    '<button type="button" id="cb-ranking-toggle" class="cb-ranking-toggle" aria-controls="cb-ranking-list" aria-expanded="' + (rankingExpanded ? 'true' : 'false') + '">' +
      (rankingExpanded ? 'Свернуть до 5 мест' : 'Показать все') +
    '</button>' : '');

  var rankingToggle = $("cb-ranking-toggle");
  if(rankingToggle){
    rankingToggle.onclick = function(){
      rankingExpanded = !rankingExpanded;
      renderAnalytics();
    };
  }
}

'''
replace_block("function renderAnalytics(){\n", "function getReportLink(report){\n", render_analytics, "рендер рейтинга")

replace_once("      scheduleCompactNotice();\n", "      scheduleSiteNotices();\n", "запуск уведомлений после загрузки")
replace_once("  setupCompactNotice();\n", "  setupLeaderChangeNotice();\n  setupCompactNotice();\n", "инициализация уведомления лидеров")

pageshow_old = '''    refreshRemoteDataForCheck().then(function(){
      renderDataViews();
    }).catch(function(){});
'''
pageshow_new = '''    refreshRemoteDataForCheck().then(function(){
      renderDataViews();
      scheduleSiteNotices();
    }).catch(function(){});
'''
replace_once(pageshow_old, pageshow_new, "уведомления после возврата на страницу")

if text == original:
    raise RuntimeError("index.html не изменён")

path.write_text(text, encoding="utf-8")
print("Патч уведомления лидеров и уникальных туров применён")
