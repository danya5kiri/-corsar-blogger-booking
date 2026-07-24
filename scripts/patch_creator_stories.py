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


stories_css = r'''

/* ===== Истории креаторов ===== */
.cb-stories-shell {
  position: relative;
  margin-top: 22px;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .08);
  border-radius: 28px;
  background:
    radial-gradient(circle at 94% 10%, rgba(78, 203, 237, .20), transparent 19rem),
    radial-gradient(circle at 4% 96%, rgba(234, 90, 167, .12), transparent 18rem),
    linear-gradient(135deg, rgba(255,255,255,.96), rgba(246,243,255,.97) 55%, rgba(238,251,254,.97));
  box-shadow: 0 18px 58px rgba(28, 31, 41, .065);
}

.cb-stories-shell::before {
  content: "";
  position: absolute;
  z-index: 0;
  top: 0;
  right: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--cb-blue), var(--cb-lilac-strong) 35%, var(--cb-cyan) 68%, var(--cb-coral));
}

.cb-stories-summary {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 34px;
  align-items: center;
  gap: 18px;
  min-height: 92px;
  padding: 22px 26px;
  cursor: pointer;
  list-style: none;
  user-select: none;
}

.cb-stories-summary::-webkit-details-marker {
  display: none;
}

.cb-stories-summary-copy {
  display: grid;
  min-width: 0;
  gap: 5px;
}

.cb-stories-kicker {
  color: #787d89;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .105em;
  text-transform: uppercase;
}

.cb-stories-summary-title {
  overflow: hidden;
  color: var(--cb-ink);
  font-size: clamp(20px, 2.5vw, 30px);
  font-weight: 760;
  line-height: 1.08;
  letter-spacing: -.045em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-stories-summary-meta {
  max-width: 330px;
  color: #737887;
  text-align: right;
  font-size: 10px;
  font-weight: 650;
  line-height: 1.45;
}

.cb-stories-toggle {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  font-size: 21px;
  font-weight: 420;
  line-height: 1;
  transition: transform .22s ease, background .22s ease;
}

.cb-stories-shell[open] .cb-stories-toggle {
  transform: rotate(45deg);
  background: var(--cb-ink);
  color: #fff;
}

.cb-stories-body {
  position: relative;
  z-index: 1;
  padding: 0 26px 26px;
  border-top: 1px solid rgba(23, 23, 25, .07);
}

.cb-stories-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px 0 14px;
}

.cb-stories-intro {
  max-width: 620px;
  color: #727785;
  font-size: 11px;
  line-height: 1.5;
}

.cb-stories-controls {
  display: inline-flex;
  flex: 0 0 auto;
  gap: 7px;
}

.cb-stories-nav {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  padding: 0;
  border: 1px solid rgba(23, 23, 25, .10);
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 22px;
  transition: transform .18s ease, background .18s ease;
}

.cb-stories-nav:hover:not(:disabled) {
  transform: translateY(-2px);
  background: #fff;
}

.cb-stories-nav:disabled {
  cursor: default;
  opacity: .35;
}

.cb-stories-track {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overscroll-behavior-inline: contain;
  padding: 2px 2px 10px;
  scroll-behavior: smooth;
  scroll-snap-type: x proximity;
  scrollbar-width: thin;
  scrollbar-color: rgba(127, 103, 248, .34) transparent;
}

.cb-story-card {
  position: relative;
  display: flex;
  flex: 0 0 188px;
  min-height: 250px;
  overflow: hidden;
  flex-direction: column;
  justify-content: space-between;
  scroll-snap-align: start;
  padding: 15px;
  border: 1px solid rgba(23,23,25,.10);
  background: linear-gradient(150deg, #ffe28a, #ffbaa7 46%, #ded4ff 75%, #c9f4fa);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  text-align: left;
  box-shadow: 0 12px 30px rgba(58, 62, 83, .09);
  transition: transform .2s ease, box-shadow .2s ease, opacity .2s ease;
}

.cb-story-card::after {
  content: "";
  position: absolute;
  right: -36px;
  bottom: -54px;
  width: 130px;
  height: 130px;
  border: 1px solid rgba(255,255,255,.72);
  border-radius: 50%;
  box-shadow: 0 0 0 18px rgba(255,255,255,.10), 0 0 0 36px rgba(255,255,255,.08);
}

.cb-story-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 36px rgba(58, 62, 83, .15);
}

.cb-story-card.is-seen {
  opacity: .72;
}

.cb-story-card.is-tone-2,
.cb-story-viewer-visual.is-tone-2 {
  background: linear-gradient(150deg, #dff6ec, #bdeff5 45%, #d8d0ff 78%, #ffdbe7);
}

.cb-story-card.is-tone-3,
.cb-story-viewer-visual.is-tone-3 {
  background: linear-gradient(150deg, #ffe2d7, #ffd66b 42%, #efc9e2 70%, #c6edff);
}

.cb-story-card.is-tone-4,
.cb-story-viewer-visual.is-tone-4 {
  background: linear-gradient(150deg, #e7e1ff, #c8ecff 46%, #c9f2e2 74%, #ffd6bc);
}

.cb-story-card.is-tone-5,
.cb-story-viewer-visual.is-tone-5 {
  background: linear-gradient(150deg, #d9efff, #d9d0ff 44%, #ffcddd 74%, #ffe7a7);
}

.cb-story-card-top,
.cb-story-card-main,
.cb-story-card-bottom {
  position: relative;
  z-index: 1;
}

.cb-story-card-top,
.cb-story-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.cb-story-index,
.cb-story-platform {
  font-size: 8px;
  font-weight: 840;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-story-platform {
  overflow: hidden;
  text-align: right;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-story-card-main {
  display: grid;
  gap: 9px;
  margin: 26px 0 18px;
}

.cb-story-creator {
  overflow: hidden;
  font-size: 21px;
  font-weight: 820;
  letter-spacing: -.05em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-story-tour {
  display: -webkit-box;
  overflow: hidden;
  font-size: 13px;
  font-weight: 620;
  line-height: 1.32;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.cb-story-date {
  color: rgba(23,23,25,.68);
  font-size: 9px;
  font-weight: 690;
}

.cb-story-new {
  padding: 4px 7px;
  border: 1px solid rgba(23,23,25,.10);
  background: rgba(255,255,255,.64);
  font-size: 7px;
  font-weight: 850;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-stories-empty {
  padding: 24px 0 6px;
  color: #747987;
  font-size: 11px;
  line-height: 1.5;
}

.cb-story-viewer[hidden] {
  display: none;
}

.cb-story-viewer {
  position: fixed;
  z-index: 2147483645;
  inset: 0;
  display: grid;
  place-items: center;
  box-sizing: border-box;
  padding: max(14px, env(safe-area-inset-top)) 14px max(14px, env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  transition: opacity .24s ease, visibility .24s ease;
}

.cb-story-viewer.is-visible {
  opacity: 1;
  visibility: visible;
}

.cb-story-viewer-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(22, 24, 31, .72);
  backdrop-filter: blur(12px) saturate(108%);
  -webkit-backdrop-filter: blur(12px) saturate(108%);
}

.cb-story-viewer-card {
  position: relative;
  z-index: 1;
  width: min(430px, 100%);
  max-height: calc(100dvh - 28px);
  overflow: auto;
  padding: 14px;
  border: 1px solid rgba(255,255,255,.15);
  background: #f8f8fb;
  box-shadow: 0 30px 90px rgba(0,0,0,.38);
  color: var(--cb-ink);
  transform: translateY(12px) scale(.99);
  transition: transform .25s ease;
}

.cb-story-viewer.is-visible .cb-story-viewer-card {
  transform: translateY(0) scale(1);
}

.cb-story-viewer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 0 10px;
}

.cb-story-viewer-kicker {
  color: #767b88;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .10em;
  text-transform: uppercase;
}

.cb-story-viewer-close {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  padding: 0;
  border: 1px solid rgba(23,23,25,.10);
  border-radius: 50%;
  background: #fff;
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 21px;
  line-height: 1;
}

.cb-story-viewer-visual {
  position: relative;
  display: flex;
  min-height: min(520px, 62vh);
  overflow: hidden;
  flex-direction: column;
  justify-content: space-between;
  padding: 22px;
  background: linear-gradient(150deg, #ffe28a, #ffbaa7 46%, #ded4ff 75%, #c9f4fa);
}

.cb-story-viewer-visual::after {
  content: "";
  position: absolute;
  right: -64px;
  bottom: -82px;
  width: 230px;
  height: 230px;
  border: 2px solid rgba(255,255,255,.66);
  border-radius: 50%;
  box-shadow: 0 0 0 28px rgba(255,255,255,.10), 0 0 0 56px rgba(255,255,255,.08);
}

.cb-story-viewer-heading,
.cb-story-viewer-copy,
.cb-story-viewer-meta {
  position: relative;
  z-index: 1;
}

.cb-story-viewer-heading,
.cb-story-viewer-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-story-viewer-copy {
  display: grid;
  gap: 12px;
}

.cb-story-viewer-title {
  margin: 0;
  overflow-wrap: anywhere;
  font-size: clamp(31px, 9vw, 47px);
  font-weight: 820;
  line-height: .96;
  letter-spacing: -.065em;
}

.cb-story-viewer-tour {
  margin: 0;
  max-width: 330px;
  font-size: 17px;
  font-weight: 570;
  line-height: 1.34;
}

.cb-story-viewer-footer {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr) 44px;
  gap: 8px;
  margin-top: 10px;
}

.cb-story-viewer-nav,
.cb-story-viewer-action {
  display: grid;
  place-items: center;
  min-height: 46px;
  border: 1px solid rgba(23,23,25,.10);
  background: #fff;
  color: var(--cb-ink);
  font: inherit;
  font-weight: 800;
  text-decoration: none;
}

.cb-story-viewer-nav {
  padding: 0;
  cursor: pointer;
  font-size: 23px;
}

.cb-story-viewer-nav:disabled {
  opacity: .35;
}

.cb-story-viewer-action {
  padding: 0 12px;
  background: linear-gradient(105deg, #ffd66b, #ffb09e 42%, #cbbdff 72%, #8ce8f4);
  font-size: 11px;
  text-align: center;
}

@media (max-width: 900px) {
  .cb-stories-summary {
    grid-template-columns: minmax(0, 1fr) 34px;
    gap: 10px;
    min-height: 82px;
    padding: 18px 20px;
  }

  .cb-stories-summary-meta {
    grid-column: 1 / -1;
    grid-row: 2;
    max-width: none;
    margin-top: -3px;
    text-align: left;
  }

  .cb-stories-toggle {
    grid-column: 2;
    grid-row: 1;
  }

  .cb-stories-body {
    padding: 0 20px 20px;
  }

  .cb-story-card {
    flex-basis: 166px;
    min-height: 230px;
  }
}

@media (max-width: 600px) {
  .cb-stories-shell {
    margin-top: 14px;
    border-radius: 22px;
  }

  .cb-stories-summary {
    min-height: 76px;
    padding: 16px;
  }

  .cb-stories-summary-title {
    font-size: 19px;
  }

  .cb-stories-summary-meta {
    font-size: 9px;
  }

  .cb-stories-body {
    padding: 0 14px 16px;
  }

  .cb-stories-toolbar {
    align-items: flex-start;
    padding: 14px 0 12px;
  }

  .cb-stories-intro {
    font-size: 10px;
  }

  .cb-stories-controls {
    display: none;
  }

  .cb-stories-track {
    gap: 9px;
    margin-right: -14px;
    padding-right: 14px;
  }

  .cb-story-card {
    flex-basis: min(148px, 43vw);
    min-height: 214px;
    padding: 13px;
  }

  .cb-story-creator {
    font-size: 18px;
  }

  .cb-story-tour {
    font-size: 11px;
  }

  .cb-story-viewer-card {
    padding: 10px;
  }

  .cb-story-viewer-visual {
    min-height: min(500px, 66vh);
    padding: 18px;
  }

  .cb-story-viewer-footer {
    grid-template-columns: 42px minmax(0, 1fr) 42px;
  }
}
'''
replace_once("\n\n\n.cb-compact-notice[hidden] {", stories_css + "\n\n.cb-compact-notice[hidden] {", "CSS историй")

stories_html = r'''

  <details id="cb-creator-stories" class="cb-stories-shell">
    <summary class="cb-stories-summary">
      <span class="cb-stories-summary-copy">
        <span class="cb-stories-kicker">Материалы мастерской</span>
        <strong id="cb-stories-summary-title" class="cb-stories-summary-title">Загружаем истории креаторов...</strong>
      </span>
      <span id="cb-stories-summary-meta" class="cb-stories-summary-meta">Свежие публикации появятся после загрузки данных.</span>
      <span class="cb-stories-toggle" aria-hidden="true">+</span>
    </summary>
    <div class="cb-stories-body">
      <div class="cb-stories-toolbar">
        <div class="cb-stories-intro">Последние работы участников после морских путешествий. Откройте карточку, чтобы посмотреть автора, программу и перейти к публикации.</div>
        <div class="cb-stories-controls" aria-label="Прокрутка историй">
          <button type="button" id="cb-stories-prev" class="cb-stories-nav" aria-label="Предыдущие истории">‹</button>
          <button type="button" id="cb-stories-next" class="cb-stories-nav" aria-label="Следующие истории">›</button>
        </div>
      </div>
      <div id="cb-stories-track" class="cb-stories-track" aria-live="polite">
        <div class="cb-stories-empty">Загружаем опубликованные материалы...</div>
      </div>
    </div>
  </details>
'''
replace_once("\n  <section id=\"calendar\" class=\"cb-section cb-calendar-shell\">", stories_html + "\n  <section id=\"calendar\" class=\"cb-section cb-calendar-shell\">", "HTML блока историй")

viewer_html = r'''

<div id="cb-story-viewer" class="cb-story-viewer" hidden role="dialog" aria-modal="true" aria-labelledby="cb-story-viewer-title">
  <div id="cb-story-viewer-backdrop" class="cb-story-viewer-backdrop"></div>
  <article class="cb-story-viewer-card">
    <div class="cb-story-viewer-top">
      <span class="cb-story-viewer-kicker">Истории креаторов</span>
      <button type="button" id="cb-story-viewer-close" class="cb-story-viewer-close" aria-label="Закрыть историю">×</button>
    </div>
    <div id="cb-story-viewer-body"><h2 id="cb-story-viewer-title" class="cb-story-viewer-title">История креатора</h2></div>
    <div class="cb-story-viewer-footer">
      <button type="button" id="cb-story-viewer-prev" class="cb-story-viewer-nav" aria-label="Предыдущая история">‹</button>
      <a id="cb-story-viewer-action" class="cb-story-viewer-action" href="#" target="_blank" rel="noopener noreferrer">Смотреть публикацию ↗</a>
      <button type="button" id="cb-story-viewer-next" class="cb-story-viewer-nav" aria-label="Следующая история">›</button>
    </div>
  </article>
</div>
'''
replace_once("\n<div id=\"cb-leader-change-notice\"", viewer_html + "\n<div id=\"cb-leader-change-notice\"", "HTML просмотрщика историй")

replace_once(
    'var COMPACT_NOTICE_STORAGE_KEY = "corsar_daily_notice_seen_v1";',
    'var COMPACT_NOTICE_STORAGE_KEY = "corsar_daily_notice_seen_v1";\nvar CREATOR_STORY_STORAGE_KEY = "corsar_creator_stories_seen_v1";',
    "ключ просмотренных историй",
)

replace_once(
    'var pendingLeaderChangeEvent = null;',
    'var pendingLeaderChangeEvent = null;\nvar creatorStoryItems = [];\nvar creatorStoryIndex = 0;\nvar creatorStoryRestoreFocus = null;',
    "состояние историй",
)

stories_js = r'''

function getCreatorStoryIdentity(report){
  var link = normalizeContentLink(getReportLink(report));
  if(link) return link;
  return [getReportCreator(report), normalizeTour(getReportTour(report)), normalizeDate(report && report.date)].join("|");
}

function readCreatorStorySeen(){
  try {
    var value = JSON.parse(localStorage.getItem(CREATOR_STORY_STORAGE_KEY) || "{}");
    return value && typeof value === "object" ? value : {};
  } catch(e) {
    return {};
  }
}

function markCreatorStorySeen(report){
  var key = getCreatorStoryIdentity(report);
  if(!key) return;
  var seen = readCreatorStorySeen();
  seen[key] = getTodayKey();
  try { localStorage.setItem(CREATOR_STORY_STORAGE_KEY, JSON.stringify(seen)); } catch(e) {}
}

function isCreatorStoryRecent(report){
  var timestamp = getActivityTimestamp(report);
  if(!Number.isFinite(timestamp)) return false;
  var dateKey = getVladivostokDateKey(new Date(timestamp));
  var today = getTodayKey();
  return dateKey === today || dateKey === addDaysToDateKey(today, -1);
}

function formatCreatorStoryDate(report){
  var date = normalizeDate(report && report.date);
  return /^\d{4}-\d{2}-\d{2}$/.test(date) ? formatDateRu(date) : "Дата поездки уточняется";
}

function getCreatorStoryTone(index){
  return (Math.abs(Number(index) || 0) % 5) + 1;
}

function scrollCreatorStories(direction){
  var track = $("cb-stories-track");
  if(!track) return;
  var card = track.querySelector(".cb-story-card");
  var amount = card ? card.offsetWidth + 12 : Math.max(180, track.clientWidth * .72);
  if(typeof track.scrollBy === "function"){
    track.scrollBy({left: amount * direction, behavior: "smooth"});
  } else {
    track.scrollLeft += amount * direction;
  }
}

function renderCreatorStories(){
  var track = $("cb-stories-track");
  var summaryTitle = $("cb-stories-summary-title");
  var summaryMeta = $("cb-stories-summary-meta");
  var prev = $("cb-stories-prev");
  var next = $("cb-stories-next");
  if(!track || !summaryTitle || !summaryMeta) return;

  creatorStoryItems = getPublishedContentItems().slice(0, 10);
  if(!creatorStoryItems.length){
    summaryTitle.textContent = "Истории креаторов";
    summaryMeta.textContent = "Пока нет опубликованных материалов";
    track.innerHTML = '<div class="cb-stories-empty">Истории появятся после добавления первой готовой публикации.</div>';
    if(prev) prev.disabled = true;
    if(next) next.disabled = true;
    return;
  }

  var latest = creatorStoryItems[0];
  summaryTitle.textContent = creatorStoryItems.length + " " + pluralCount(creatorStoryItems.length, "свежая история", "свежие истории", "свежих историй");
  summaryMeta.textContent = "Последняя: " + (getReportCreator(latest) || "креатор") + " · " + getContentPlatform(getReportLink(latest));

  var seen = readCreatorStorySeen();
  track.innerHTML = creatorStoryItems.map(function(report, index){
    var creator = getReportCreator(report) || "креатор";
    var tour = getReportTour(report) || "Морское путешествие «Корсар»";
    var platform = getContentPlatform(getReportLink(report));
    var identity = getCreatorStoryIdentity(report);
    var seenClass = seen[identity] ? " is-seen" : "";
    var recent = isCreatorStoryRecent(report);
    return '<button type="button" class="cb-story-card is-tone-' + getCreatorStoryTone(index) + seenClass + '" data-story-index="' + index + '" aria-label="Открыть историю ' + escapeHtml(creator) + ': ' + escapeHtml(tour) + '">' +
      '<span class="cb-story-card-top"><span class="cb-story-index">' + String(index + 1).padStart(2, "0") + ' / ' + String(creatorStoryItems.length).padStart(2, "0") + '</span><span class="cb-story-platform">' + escapeHtml(platform) + '</span></span>' +
      '<span class="cb-story-card-main"><strong class="cb-story-creator">' + escapeHtml(creator) + '</strong><span class="cb-story-tour">' + escapeHtml(tour) + '</span></span>' +
      '<span class="cb-story-card-bottom"><span class="cb-story-date">' + escapeHtml(formatCreatorStoryDate(report)) + '</span>' + (recent ? '<span class="cb-story-new">Новое</span>' : '') + '</span>' +
    '</button>';
  }).join("");

  Array.prototype.forEach.call(track.querySelectorAll(".cb-story-card"), function(card){
    card.onclick = function(){ openCreatorStory(Number(this.getAttribute("data-story-index")), this); };
  });
  if(prev) prev.disabled = creatorStoryItems.length < 2;
  if(next) next.disabled = creatorStoryItems.length < 2;
}

function renderCreatorStoryViewer(){
  var body = $("cb-story-viewer-body");
  var action = $("cb-story-viewer-action");
  var prev = $("cb-story-viewer-prev");
  var next = $("cb-story-viewer-next");
  if(!body || !action || !creatorStoryItems.length) return;

  creatorStoryIndex = ((creatorStoryIndex % creatorStoryItems.length) + creatorStoryItems.length) % creatorStoryItems.length;
  var report = creatorStoryItems[creatorStoryIndex];
  var creator = getReportCreator(report) || "креатор";
  var tour = getReportTour(report) || "Морское путешествие «Корсар»";
  var platform = getContentPlatform(getReportLink(report));
  var recent = isCreatorStoryRecent(report);

  body.innerHTML = '<div class="cb-story-viewer-visual is-tone-' + getCreatorStoryTone(creatorStoryIndex) + '">' +
    '<div class="cb-story-viewer-heading"><span>' + escapeHtml(platform) + '</span><span>' + String(creatorStoryIndex + 1).padStart(2, "0") + ' / ' + String(creatorStoryItems.length).padStart(2, "0") + '</span></div>' +
    '<div class="cb-story-viewer-copy"><h2 id="cb-story-viewer-title" class="cb-story-viewer-title">' + escapeHtml(creator) + '</h2><p class="cb-story-viewer-tour">' + escapeHtml(tour) + '</p></div>' +
    '<div class="cb-story-viewer-meta"><span>' + escapeHtml(formatCreatorStoryDate(report)) + '</span><span>' + (recent ? "Новое" : "Материал сезона") + '</span></div>' +
  '</div>';
  action.href = getReportLink(report);
  action.setAttribute("aria-label", "Открыть публикацию " + creator + " на площадке " + platform);
  if(prev) prev.disabled = creatorStoryItems.length < 2;
  if(next) next.disabled = creatorStoryItems.length < 2;

  markCreatorStorySeen(report);
  var card = document.querySelector('.cb-story-card[data-story-index="' + creatorStoryIndex + '"]');
  if(card) card.classList.add("is-seen");
}

function openCreatorStory(index, source){
  var viewer = $("cb-story-viewer");
  if(!viewer || !creatorStoryItems.length) return;
  creatorStoryRestoreFocus = source || document.activeElement;
  creatorStoryIndex = Number(index) || 0;
  renderCreatorStoryViewer();
  viewer.hidden = false;
  window.requestAnimationFrame(function(){ viewer.classList.add("is-visible"); });
  var close = $("cb-story-viewer-close");
  if(close) setTimeout(function(){ close.focus(); }, 60);
}

function closeCreatorStory(){
  var viewer = $("cb-story-viewer");
  if(!viewer || viewer.hidden) return;
  viewer.classList.remove("is-visible");
  setTimeout(function(){
    viewer.hidden = true;
    if(creatorStoryRestoreFocus && typeof creatorStoryRestoreFocus.focus === "function") creatorStoryRestoreFocus.focus();
    creatorStoryRestoreFocus = null;
  }, 240);
}

function stepCreatorStory(direction){
  if(creatorStoryItems.length < 2) return;
  creatorStoryIndex += direction;
  renderCreatorStoryViewer();
}

function setupCreatorStories(){
  var prev = $("cb-stories-prev");
  var next = $("cb-stories-next");
  var viewerPrev = $("cb-story-viewer-prev");
  var viewerNext = $("cb-story-viewer-next");
  var close = $("cb-story-viewer-close");
  var backdrop = $("cb-story-viewer-backdrop");

  if(prev) prev.onclick = function(){ scrollCreatorStories(-1); };
  if(next) next.onclick = function(){ scrollCreatorStories(1); };
  if(viewerPrev) viewerPrev.onclick = function(){ stepCreatorStory(-1); };
  if(viewerNext) viewerNext.onclick = function(){ stepCreatorStory(1); };
  if(close) close.onclick = closeCreatorStory;
  if(backdrop) backdrop.onclick = closeCreatorStory;

  document.addEventListener("keydown", function(event){
    var viewer = $("cb-story-viewer");
    if(!viewer || viewer.hidden) return;
    if(event.key === "Escape") closeCreatorStory();
    if(event.key === "ArrowLeft") stepCreatorStory(-1);
    if(event.key === "ArrowRight") stepCreatorStory(1);
  });
}
'''
replace_once("\nfunction getCreatorGroupId(creator){", stories_js + "\nfunction getCreatorGroupId(creator){", "JavaScript историй")

replace_once(
    "  renderAnalytics();\n  renderResults();\n  renderRecentCreatorEvents();",
    "  renderAnalytics();\n  renderResults();\n  renderCreatorStories();\n  renderRecentCreatorEvents();",
    "рендер историй после загрузки",
)

replace_once(
    "        renderResults();\n        renderCreatorOptions();\n        renderRecentCreatorEvents();",
    "        renderResults();\n        renderCreatorOptions();\n        renderCreatorStories();\n        renderRecentCreatorEvents();",
    "рендер историй после добавления контента",
)

replace_once(
    "  setupCreatorIdentityInputs();\n  setupCompactNotice();",
    "  setupCreatorIdentityInputs();\n  setupCreatorStories();\n  setupCompactNotice();",
    "инициализация историй",
)

path.write_text(text, encoding="utf-8")
