#!/usr/bin/env python3
from pathlib import Path
import re

index_path = Path("index.html")
test_path = Path("tests/site_health_test.js")
text = index_path.read_text(encoding="utf-8")
tests = test_path.read_text(encoding="utf-8")


def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, got {count}")
    return source.replace(old, new, 1)


def regex_once(source: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {count}")
    return updated


# 1. Entry card title and close control in the opened profile.
text = replace_once(text, '<strong id="cb-profile-entry-title">Откройте мини-ЛК</strong>', '<strong id="cb-profile-entry-title">Открыть ЛК</strong>', "profile entry title")
text = replace_once(
    text,
    '    </div>\n    <div id="cb-profile-dashboard" class="cb-profile-dashboard" aria-live="polite"></div>\n  </section>',
    '    </div>\n    <button type="button" id="cb-profile-close" class="cb-profile-close" aria-label="Закрыть личный кабинет и вернуться на главную">×</button>\n    <div id="cb-profile-dashboard" class="cb-profile-dashboard" aria-live="polite"></div>\n  </section>',
    "profile close button",
)

# 2. Move diagnostics below CREACLOUD, still inside the main site container.
diagnostics_match = re.search(r'  <details id="cb-diagnostics" class="cb-diagnostics">[\s\S]*?  </details>\n\n', text)
if not diagnostics_match:
    raise SystemExit("diagnostics block not found")
diagnostics_block = diagnostics_match.group(0)
text = text[:diagnostics_match.start()] + text[diagnostics_match.end():]
text = replace_once(text, '  </footer>\n</main>', '  </footer>\n\n' + diagnostics_block + '</main>', "move diagnostics below footer")

# 3. Visual refinements and the active-control rounding rule.
css = r'''
/* ===== ЛК, материалы и активные элементы ===== */
.cb-profile-entry-card {
  isolation: isolate;
  border-color: rgba(82, 75, 131, .16);
  background:
    radial-gradient(circle at 92% 4%, rgba(255,255,255,.88), transparent 34%),
    linear-gradient(125deg, #fff0a8 0%, #ffd6df 37%, #ddd6ff 69%, #cff5fa 100%);
  box-shadow: 0 18px 42px rgba(96, 79, 151, .17), 0 2px 0 rgba(255,255,255,.74) inset;
  transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-profile-entry-card::after {
  content: "";
  position: absolute;
  z-index: -1;
  right: -58px;
  bottom: -82px;
  width: 190px;
  height: 190px;
  border: 1px solid rgba(255,255,255,.72);
  border-radius: 50%;
  box-shadow: 0 0 0 26px rgba(255,255,255,.10), 0 0 0 52px rgba(255,255,255,.07);
  pointer-events: none;
}

.cb-profile-entry-card:hover,
.cb-profile-entry-card:focus-within {
  transform: translateY(-2px);
  filter: saturate(1.04);
  box-shadow: 0 24px 50px rgba(96, 79, 151, .22), 0 2px 0 rgba(255,255,255,.82) inset;
}

.cb-profile-entry-copy,
.cb-profile-entry-form,
.cb-profile-entry-state {
  position: relative;
  z-index: 1;
}

.cb-profile-entry-copy strong {
  font-size: 24px;
}

.cb-profile-entry-copy span:last-child {
  max-width: 620px;
  color: #555b68;
  font-size: 10px;
}

.cb-profile-entry-form input {
  border-color: rgba(54, 50, 79, .16);
  border-radius: 999px;
  background: rgba(255,255,255,.80);
}

.cb-profile-entry-form button {
  border-radius: 999px;
  background: linear-gradient(105deg, #ffd24f, #ff9b87 40%, #ad98ff 72%, #64d8ed);
  box-shadow: 0 10px 24px rgba(91, 82, 146, .18);
}

.cb-profile-close {
  position: absolute;
  z-index: 4;
  top: 22px;
  right: 22px;
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  padding: 0;
  border: 1px solid rgba(23,23,25,.12);
  background: rgba(255,255,255,.82);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 23px;
  line-height: 1;
  box-shadow: 0 8px 20px rgba(54, 53, 86, .09);
}

.cb-profile-overview {
  padding-right: 72px;
}

.cb-profile-overview-copy h3 {
  max-width: 100%;
  overflow: visible;
  font-size: clamp(25px, 4.3vw, 48px);
  line-height: 1.02;
  overflow-wrap: anywhere;
  text-overflow: clip;
  white-space: normal;
  word-break: break-word;
}

.cb-profile-achievements {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 4px;
}

.cb-profile-achievement {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 30px;
  padding: 0 10px;
  border: 1px solid rgba(23,23,25,.09);
  border-radius: 999px;
  background: rgba(255,255,255,.62);
  color: #4f5562;
  font-size: 8px;
  font-weight: 820;
  letter-spacing: .055em;
  text-transform: uppercase;
}

.cb-profile-achievement.is-primary {
  background: rgba(23,23,25,.88);
  color: #fff;
}

.cb-profile-achievement-icon {
  display: grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  font-size: 9px;
  line-height: 1;
}

.cb-profile-achievement.is-primary .cb-profile-achievement-icon {
  background: linear-gradient(135deg, #ffd66b, #ffb09e 48%, #cbbdff);
}

.cb-stories-today-index {
  display: inline-flex;
  align-items: center;
  min-height: 23px;
  margin-left: 7px;
  padding: 0 8px;
  border: 1px solid rgba(23,23,25,.09);
  border-radius: 999px;
  background: linear-gradient(105deg, #f2f3f6, #e9eaf0 52%, #f4f1fb);
  color: #666c78;
  vertical-align: .16em;
  font-size: 8px;
  font-weight: 840;
  letter-spacing: .055em;
  white-space: nowrap;
  text-transform: uppercase;
}

.cb-story-card {
  border-radius: 22px;
}

.cb-story-add-card {
  align-items: flex-start;
  justify-content: space-between;
  border-color: rgba(23,23,25,.08);
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.76), transparent 34%),
    linear-gradient(145deg, #f2f3f5 0%, #e3e5ea 46%, #d8dbe2 74%, #f1eef7 100%);
  color: #525865;
}

.cb-story-add-card::after {
  border-color: rgba(255,255,255,.82);
}

.cb-story-add-plus {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border: 1px solid rgba(23,23,25,.11);
  border-radius: 50%;
  background: rgba(255,255,255,.72);
  color: var(--cb-ink);
  font-size: 30px;
  font-weight: 300;
  line-height: 1;
}

.cb-story-add-copy {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 8px;
  margin-top: auto;
}

.cb-story-add-copy strong {
  font-size: 20px;
  font-weight: 820;
  letter-spacing: -.045em;
}

.cb-story-add-copy span {
  color: #6c727e;
  font-size: 10px;
  line-height: 1.4;
}

.cb-story-viewer-card,
.cb-story-viewer-visual {
  border-radius: 24px;
}

#corsar-blogger-booking button:not(:disabled):not([aria-disabled="true"]),
.cb-story-viewer button:not(:disabled),
.cb-leader-change-notice button:not(:disabled),
.cb-compact-notice button:not(:disabled) {
  border-radius: 999px;
}

#corsar-blogger-booking .cb-story-card,
#corsar-blogger-booking .cb-leader-card[aria-disabled="false"] {
  border-radius: 22px;
}

.cb-link-button,
.cb-result-link,
.cb-footer-feedback a,
.cb-story-viewer-action {
  border-radius: 999px;
}

@media (max-width: 600px) {
  .cb-profile-close {
    top: 16px;
    right: 16px;
  }

  .cb-profile-overview {
    padding-right: 58px;
  }

  .cb-profile-overview-copy h3 {
    font-size: clamp(25px, 10vw, 38px);
  }

  .cb-stories-today-index {
    margin-left: 4px;
    padding: 0 6px;
  }
}

'''
text = replace_once(text, '/* ===== Локальная диагностика сайта ===== */', css + '/* ===== Локальная диагностиика сайта ===== */', "insert visual css")
# Normalize the intentional insertion marker typo back to the original comment.
text = text.replace('/* ===== Локальная диагностиика сайта ===== */', '/* ===== Локальная диагностика сайта ===== */', 1)

# 4. Creator achievements and revised profile rendering.
achievements_js = r'''
function getCreatorProfileAchievements(data){
  var achievements = [];
  var trips = data && data.bookings ? data.bookings.length : 0;
  var materials = data && data.reports ? data.reports.length : 0;
  var unique = Number(data && data.uniqueCount) || 0;
  var level;

  if(unique >= TOTAL_UNIQUE_TOURS || trips >= 10 || materials >= 5){
    level = {label: "Гуру", icon: "★", primary: true};
  } else if(trips >= 5 || unique >= 4 || materials >= 3){
    level = {label: "Достигатор", icon: "◆", primary: true};
  } else if(trips >= 2 || unique >= 2 || materials >= 1){
    level = {label: "Продвинутый", icon: "↗", primary: true};
  } else {
    level = {label: "Новичок", icon: "●", primary: true};
  }
  achievements.push(level);

  if(data && data.visitRank === 1 && trips > 0) achievements.push({label: "Лидер поездок", icon: "01"});
  if(data && data.uniqueRank === 1 && unique > 0) achievements.push({label: "Исследователь сезона", icon: "◎"});
  if(data && data.contentRank === 1 && materials > 0) achievements.push({label: "Автор сезона", icon: "✦"});
  if(unique >= TOTAL_UNIQUE_TOURS) achievements.push({label: "Все маршруты", icon: "✓"});
  else if(materials >= 3) achievements.push({label: "Контент-мейкер", icon: "+"});
  else if(trips >= 3) achievements.push({label: "Постоянный участник", icon: "∞"});

  return achievements.slice(0, 4);
}

function renderCreatorProfileAchievements(data){
  var achievements = getCreatorProfileAchievements(data);
  return '<div class="cb-profile-achievements" aria-label="Достижения креатора">' + achievements.map(function(item){
    return '<span class="cb-profile-achievement' + (item.primary ? ' is-primary' : '') + '"><span class="cb-profile-achievement-icon" aria-hidden="true">' + escapeHtml(item.icon) + '</span>' + escapeHtml(item.label) + '</span>';
  }).join("") + '</div>';
}

'''
text = replace_once(text, 'function buildCreatorProfileRecommendation(data){', achievements_js + 'function buildCreatorProfileRecommendation(data){', "creator achievements")

profile_function = r'''function renderCreatorProfile(){
  var section = $("creator-profile");
  var dashboard = $("cb-profile-dashboard");
  if(!section || !dashboard) return;
  if(!activeCreatorProfile){
    section.hidden = true;
    currentCreatorProfileRecommendation = null;
    return;
  }

  var entry = findCreatorEntry(activeCreatorProfile, getKnownCreatorDirectory());
  if(!entry){
    activeCreatorProfile = "";
    currentCreatorProfileRecommendation = null;
    section.hidden = true;
    return;
  }

  activeCreatorProfile = entry.name;
  var data = getCreatorProfileData(activeCreatorProfile);
  currentCreatorProfileRecommendation = data.recommendation;
  section.hidden = false;

  dashboard.innerHTML = '<div class="cb-profile-overview"><div class="cb-profile-overview-copy"><small>Профиль сезона</small><h3>' + escapeHtml(data.creator) + '</h3><p>' + data.bookings.length + ' ' + pluralCount(data.bookings.length, "поездка", "поездки", "поездок") + ' в учёте · ' + data.reports.length + ' ' + pluralCount(data.reports.length, "публикация", "публикации", "публикаций") + '.</p>' + renderCreatorProfileAchievements(data) + '</div><div class="cb-profile-overview-score"><strong>' + data.uniqueCount + '</strong><small>/ ' + TOTAL_UNIQUE_TOURS + '</small></div></div>' +
    '<div class="cb-profile-progress"><div class="cb-profile-progress-copy"><small class="cb-profile-block-label">Охват программ</small><strong>' + data.uniqueCount + ' ' + pluralCount(data.uniqueCount, "уникальный тур", "уникальных тура", "уникальных туров") + ' из ' + TOTAL_UNIQUE_TOURS + '</strong><span>Две вечерние программы учитываются как одна категория; двухдневные туры в уникальность не входят.</span></div><div class="cb-profile-progress-stars" aria-label="Пройдено ' + data.uniqueCount + ' из ' + TOTAL_UNIQUE_TOURS + ' уникальных туров">' + renderTourVarietyStars(data.uniqueCount) + '</div></div>' +
    buildCreatorProfileRecommendation(data) + buildCreatorProfileActivity(data) +
    '<div class="cb-profile-actions">' + (data.upcomingBookings.length ? '<button type="button" id="cb-profile-manage" class="cb-profile-action">Управлять бронированием</button>' : '') + (data.bookings.length ? '<button type="button" id="cb-profile-add-content" class="cb-profile-action">Добавить контент</button>' : '') + '</div>';

  var bookNext = $("cb-profile-book-next");
  var manage = $("cb-profile-manage");
  var addContent = $("cb-profile-add-content");
  if(bookNext) bookNext.onclick = prefillCreatorProfileRecommendation;
  if(manage) manage.onclick = openCreatorProfileBookingManagement;
  if(addContent) addContent.onclick = openCreatorProfileContentForm;
}

function closeCreatorProfile(){
  activeCreatorProfile = "";
  currentCreatorProfileRecommendation = null;
  var section = $("creator-profile");
  var dashboard = $("cb-profile-dashboard");
  if(section) section.hidden = true;
  if(dashboard) dashboard.innerHTML = "";
  setCreatorProfileEntryState("Личный кабинет закрыт. Введите ник, чтобы открыть его снова.", "");
  if(window.location.hash === "#creator-profile") window.location.hash = "home";
  var home = $("home");
  if(home) window.requestAnimationFrame(function(){ home.scrollIntoView({behavior: "smooth", block: "start"}); });
}

function selectCreatorProfileTourOption'''
text = regex_once(text, r'function renderCreatorProfile\(\)\{[\s\S]*?\n\}\n\nfunction selectCreatorProfileTourOption', profile_function, "replace profile render")

setup_profile = r'''function setupCreatorProfile(){
  var input = $("cb-profile-entry-input");
  var submit = $("cb-profile-entry-submit");
  var close = $("cb-profile-close");
  var card = document.querySelector(".cb-profile-entry-card");
  if(submit) submit.onclick = openCreatorProfileFromEntry;
  if(close) close.onclick = closeCreatorProfile;
  if(card && input){
    card.addEventListener("click", function(event){
      if(event.target && event.target.closest && event.target.closest("button, input, a")) return;
      input.focus();
    });
  }
  if(input){
    input.addEventListener("input", refreshCreatorProfileEntryState);
    input.addEventListener("change", function(){
      var entry = findCreatorEntry(this.value, getKnownCreatorDirectory());
      if(entry) this.value = entry.name;
      refreshCreatorProfileEntryState();
    });
    input.addEventListener("keydown", function(event){
      if(event.key === "Enter"){
        event.preventDefault();
        openCreatorProfileFromEntry();
      }
    });
  }
  refreshCreatorProfileEntryState();
}

function focusTourSchedule'''
text = regex_once(text, r'function setupCreatorProfile\(\)\{[\s\S]*?\n\}\n\nfunction focusTourSchedule', setup_profile, "replace setup profile")

# 5. Daily content index, rounded content cards and the leading add-content card.
stories_function = r'''function getTodayPublishedContentCount(items){
  var today = getTodayKey();
  return (Array.isArray(items) ? items : []).filter(function(report){
    var timestamp = getActivityTimestamp(report);
    return Number.isFinite(timestamp) && getVladivostokDateKey(new Date(timestamp)) === today;
  }).length;
}

function buildCreatorStoryAddCard(){
  return '<button type="button" id="cb-story-add-card" class="cb-story-card cb-story-add-card" aria-label="Добавить готовый контент"><span class="cb-story-add-plus" aria-hidden="true">+</span><span class="cb-story-add-copy"><strong>Добавить контент</strong><span>Опубликуйте готовую работу и появитесь в материалах мастерской.</span></span></button>';
}

function bindCreatorStoryAddCard(){
  var addCard = $("cb-story-add-card");
  if(addCard) addCard.onclick = focusContentSubmission;
}

function renderCreatorStories(){
  var track = $("cb-stories-track");
  var summaryTitle = $("cb-stories-summary-title");
  var summaryMeta = $("cb-stories-summary-meta");
  var prev = $("cb-stories-prev");
  var next = $("cb-stories-next");
  if(!track || !summaryTitle || !summaryMeta) return;

  var publishedItems = getPublishedContentItems();
  var todayCount = getTodayPublishedContentCount(publishedItems);
  var todayIndex = '<span class="cb-stories-today-index">+' + todayCount + ' сегодня</span>';
  creatorStoryItems = publishedItems.slice(0, 5);
  if(!creatorStoryItems.length){
    summaryTitle.innerHTML = "<strong>Свежих публикаций</strong> пока нет " + todayIndex;
    summaryMeta.textContent = "Пока нет опубликованных материалов";
    track.innerHTML = buildCreatorStoryAddCard();
    bindCreatorStoryAddCard();
    if(prev) prev.disabled = true;
    if(next) next.disabled = true;
    return;
  }

  var latest = creatorStoryItems[0];
  var count = creatorStoryItems.length;
  var freshness = count === 1 ? "свежая" : (count >= 2 && count <= 4 ? "свежие" : "свежих");
  summaryTitle.innerHTML = "<strong>" + count + " " + freshness + "</strong> " + pluralCount(count, "публикация", "публикации", "публикаций") + " " + todayIndex;
  summaryMeta.textContent = "Последняя: " + (getReportCreator(latest) || "креатор") + " · " + getContentPlatform(getReportLink(latest));

  var seen = readCreatorStorySeen();
  track.innerHTML = buildCreatorStoryAddCard() + creatorStoryItems.map(function(report, index){
    var creator = getReportCreator(report) || "креатор";
    var tour = getReportTour(report) || "Морское путешествие «Корсар»";
    var platform = getContentPlatform(getReportLink(report));
    var identity = getCreatorStoryIdentity(report);
    var seenClass = seen[identity] ? " is-seen" : "";
    var recent = isCreatorStoryRecent(report);
    return '<button type="button" class="cb-story-card is-tone-' + getCreatorStoryTone(index) + seenClass + '" data-story-index="' + index + '" aria-label="Открыть публикацию ' + escapeHtml(creator) + ': ' + escapeHtml(tour) + '">' +
      '<span class="cb-story-card-top"><span class="cb-story-index">' + String(index + 1).padStart(2, "0") + ' / ' + String(creatorStoryItems.length).padStart(2, "0") + '</span><span class="cb-story-platform">' + escapeHtml(platform) + '</span></span>' +
      '<span class="cb-story-card-main"><strong class="cb-story-creator">' + escapeHtml(creator) + '</strong><span class="cb-story-tour">' + escapeHtml(tour) + '</span></span>' +
      '<span class="cb-story-card-bottom"><span class="cb-story-date">' + escapeHtml(formatCreatorStoryDate(report)) + '</span>' + (recent ? '<span class="cb-story-new">Новое</span>' : '') + '</span>' +
    '</button>';
  }).join("");

  bindCreatorStoryAddCard();
  Array.prototype.forEach.call(track.querySelectorAll(".cb-story-card[data-story-index]"), function(card){
    card.onclick = function(){ openCreatorStory(Number(this.getAttribute("data-story-index")), this); };
  });
  if(prev) prev.disabled = creatorStoryItems.length < 2;
  if(next) next.disabled = creatorStoryItems.length < 2;
}

function renderCreatorStoryViewer'''
text = regex_once(text, r'function renderCreatorStories\(\)\{[\s\S]*?\n\}\n\nfunction renderCreatorStoryViewer', stories_function, "replace creator stories")

# 6. Keep the update log current.
text = replace_once(
    text,
    '  text: "Уточнены мини-ЛК, прогноз погоды, защита бронирований и локальная диагностика сайта."',
    '  text: "Обновлены личный кабинет, достижения креаторов, материалы и активные кнопки сайта."',
    "portal update text",
)

# 7. Extend permanent tests.
tests = replace_once(
    tests,
    '    sanitizeDiagnosticDetail: sanitizeDiagnosticDetail,\n    isPendingWriteConfirmed: isPendingWriteConfirmed,',
    '    sanitizeDiagnosticDetail: sanitizeDiagnosticDetail,\n    isPendingWriteConfirmed: isPendingWriteConfirmed,\n    getTodayPublishedContentCount: getTodayPublishedContentCount,\n    getCreatorProfileAchievements: getCreatorProfileAchievements,',
    "expose new test helpers",
)

new_tests = r'''

test("creator cabinet has close control, achievements and no duplicate metric cards", () => {
  assert.match(html, /id="cb-profile-entry-title">Открыть ЛК</);
  assert.match(html, /id="cb-profile-close"/);
  assert.match(script, /function closeCreatorProfile\(\)/);
  assert.match(script, /function getCreatorProfileAchievements\(data\)/);
  assert.doesNotMatch(script, /<div class="cb-profile-metrics is-compact">/);
  assert.match(html, /\.cb-profile-overview-copy h3[\s\S]*?white-space:\s*normal/);
});

test("creator achievement level follows actual progress", () => {
  const novice = api.getCreatorProfileAchievements({bookings: [{}], reports: [], uniqueCount: 1, visitRank: 3, uniqueRank: 3, contentRank: 0});
  assert.equal(novice[0].label, "Новичок");
  const advanced = api.getCreatorProfileAchievements({bookings: [{}, {}], reports: [{}], uniqueCount: 2, visitRank: 2, uniqueRank: 2, contentRank: 2});
  assert.equal(advanced[0].label, "Продвинутый");
  const guru = api.getCreatorProfileAchievements({bookings: Array(10).fill({}), reports: Array(5).fill({}), uniqueCount: api.TOTAL_UNIQUE_TOURS, visitRank: 1, uniqueRank: 1, contentRank: 1});
  assert.equal(guru[0].label, "Гуру");
  assert.ok(guru.some((item) => item.label === "Все маршруты"));
});

test("materials show today's index and leading add-content card", () => {
  assert.match(script, /cb-stories-today-index/);
  assert.match(script, /id="cb-story-add-card"/);
  assert.match(script, /buildCreatorStoryAddCard\(\) \+ creatorStoryItems/);
  const count = api.getTodayPublishedContentCount([
    {createdAt: "2026-07-24T03:00:00+10:00"},
    {createdAt: "2026-07-23T03:00:00+10:00"},
  ]);
  assert.equal(count, 1);
});

test("diagnostics are rendered below CREACLOUD", () => {
  assert.ok(html.indexOf('<footer id="creacloud"') < html.indexOf('id="cb-diagnostics"'));
});

test("active controls use rounded edges while card buttons keep a compact radius", () => {
  assert.match(html, /button:not\(:disabled\):not\(\[aria-disabled="true"\]\)/);
  assert.match(html, /\.cb-story-card[\s\S]*?border-radius:\s*22px/);
});
'''
tests = replace_once(tests, '\nconsole.log(`\\n${passed} site health tests passed.`);\n', new_tests + '\nconsole.log(`\\n${passed} site health tests passed.`);\n', "append feature tests")

index_path.write_text(text, encoding="utf-8")
test_path.write_text(tests, encoding="utf-8")
print("creator profile, materials and controls patch applied")
