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
'''  background:
    radial-gradient(circle at 94% 10%, rgba(78, 203, 237, .20), transparent 19rem),
    radial-gradient(circle at 4% 96%, rgba(234, 90, 167, .12), transparent 18rem),
    linear-gradient(135deg, rgba(255,255,255,.96), rgba(246,243,255,.97) 55%, rgba(238,251,254,.97));''',
'''  background: #fff;''',
"белый фон блока историй",
)

profile_css = r'''

/* ===== Мини-ЛК креатора ===== */
.cb-profile-entry-card {
  position: relative;
  grid-column: 1 / -1;
  overflow: hidden;
  padding: 18px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: #fff;
  box-shadow: 0 12px 30px rgba(45, 50, 69, .07);
}

.cb-profile-entry-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--cb-blue), var(--cb-lilac-strong) 36%, var(--cb-cyan) 70%, var(--cb-coral));
}

.cb-profile-entry-copy {
  display: grid;
  gap: 5px;
}

.cb-profile-entry-copy strong {
  font-size: 20px;
  font-weight: 810;
  line-height: 1.08;
  letter-spacing: -.045em;
}

.cb-profile-entry-copy span:last-child {
  color: #737887;
  font-size: 9px;
  line-height: 1.45;
}

.cb-profile-entry-form {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  margin-top: 13px;
}

.cb-profile-entry-form input {
  min-width: 0;
  min-height: 43px;
  padding: 0 12px;
  border: 1px solid rgba(23, 23, 25, .12);
  border-radius: 0;
  outline: none;
  background: #f8f8fb;
  color: var(--cb-ink);
  font: inherit;
  font-size: 12px;
}

.cb-profile-entry-form input:focus {
  border-color: var(--cb-lilac-strong);
  box-shadow: 0 0 0 3px rgba(127, 103, 248, .11);
}

.cb-profile-entry-form button {
  min-height: 43px;
  padding: 0 14px;
  border: 1px solid rgba(23, 23, 25, .09);
  background: linear-gradient(105deg, #ffd66b, #ffb09e 42%, #cbbdff 72%, #8ce8f4);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 9px;
  font-weight: 840;
  letter-spacing: .055em;
  text-transform: uppercase;
  transition: transform .18s ease, box-shadow .18s ease;
}

.cb-profile-entry-form button:hover,
.cb-profile-entry-form button:focus-visible {
  transform: translateY(-1px);
  outline: 0;
  box-shadow: 0 10px 22px rgba(91, 82, 146, .16);
}

.cb-profile-entry-state {
  min-height: 16px;
  margin-top: 7px;
  color: #787d88;
  font-size: 8px;
  line-height: 1.35;
}

.cb-profile-entry-state.is-ready {
  color: #287866;
}

.cb-profile-entry-state.is-error {
  color: #a44b43;
}

.cb-profile-section {
  background: #fff;
}

.cb-profile-section::before {
  content: "";
  position: absolute;
  z-index: 0;
  top: 0;
  right: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--cb-blue), var(--cb-lilac-strong) 34%, var(--cb-cyan) 68%, var(--cb-coral));
}

.cb-profile-dashboard {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 14px;
}

.cb-profile-overview {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 20px;
  padding: 22px;
  border: 1px solid rgba(23, 23, 25, .08);
  background:
    radial-gradient(circle at 94% 8%, rgba(255,255,255,.76), transparent 34%),
    linear-gradient(125deg, #fff0ba 0%, #ffe1d7 38%, #e9e2ff 70%, #dff7fb 100%);
}

.cb-profile-overview-copy {
  display: grid;
  min-width: 0;
  gap: 7px;
}

.cb-profile-overview-copy small,
.cb-profile-block-label {
  color: #6e7480;
  font-size: 8px;
  font-weight: 840;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.cb-profile-overview-copy h3 {
  margin: 0;
  overflow: hidden;
  font-size: clamp(30px, 5vw, 52px);
  font-weight: 820;
  line-height: .98;
  letter-spacing: -.065em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-profile-overview-copy p {
  margin: 0;
  color: #646a76;
  font-size: 11px;
  line-height: 1.5;
}

.cb-profile-overview-score {
  display: flex;
  align-items: baseline;
  gap: 4px;
  font-size: clamp(42px, 7vw, 68px);
  font-weight: 320;
  line-height: 1;
  letter-spacing: -.07em;
}

.cb-profile-overview-score strong {
  font-weight: 820;
}

.cb-profile-overview-score small {
  color: #717683;
  font-size: 15px;
  font-weight: 760;
  letter-spacing: -.02em;
}

.cb-profile-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 9px;
}

.cb-profile-metric {
  min-height: 94px;
  padding: 16px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: #f7f7fa;
}

.cb-profile-metric:nth-child(2) {
  background: #f2efff;
}

.cb-profile-metric:nth-child(3) {
  background: #eaf8fa;
}

.cb-profile-metric strong {
  display: block;
  font-size: 28px;
  font-weight: 820;
  line-height: 1;
  letter-spacing: -.055em;
}

.cb-profile-metric span {
  display: block;
  margin-top: 8px;
  color: #747985;
  font-size: 8px;
  font-weight: 780;
  line-height: 1.35;
  letter-spacing: .055em;
  text-transform: uppercase;
}

.cb-profile-ranks {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.cb-profile-rank {
  display: grid;
  gap: 5px;
  padding: 13px 14px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: #fff;
}

.cb-profile-rank small {
  color: #808590;
  font-size: 7px;
  font-weight: 830;
  letter-spacing: .075em;
  text-transform: uppercase;
}

.cb-profile-rank strong {
  font-size: 15px;
  font-weight: 810;
  letter-spacing: -.025em;
}

.cb-profile-progress {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 17px 18px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: #fafafd;
}

.cb-profile-progress-copy {
  display: grid;
  gap: 5px;
}

.cb-profile-progress-copy strong {
  font-size: 18px;
  font-weight: 810;
  letter-spacing: -.035em;
}

.cb-profile-progress-copy span {
  color: #747985;
  font-size: 9px;
  line-height: 1.45;
}

.cb-profile-progress-stars {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 3px;
  white-space: nowrap;
}

.cb-profile-tour-columns,
.cb-profile-activity-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.cb-profile-tour-block,
.cb-profile-activity-card {
  padding: 17px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: #fff;
}

.cb-profile-tour-block.is-complete {
  background: #f2fbf7;
}

.cb-profile-tour-block.is-missing {
  background: #faf8ff;
}

.cb-profile-tour-list {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 11px;
}

.cb-profile-tour-chip {
  display: inline-flex;
  align-items: center;
  min-height: 29px;
  padding: 0 9px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: rgba(255,255,255,.76);
  color: #656b76;
  font-size: 8px;
  font-weight: 700;
  line-height: 1.25;
}

.cb-profile-tour-empty {
  margin-top: 10px;
  color: #777c87;
  font-size: 9px;
  line-height: 1.45;
}

.cb-profile-recommendation {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 20px;
  border: 1px solid rgba(23, 23, 25, .08);
  background:
    radial-gradient(circle at 94% 10%, rgba(255,255,255,.76), transparent 34%),
    linear-gradient(120deg, #e5fbf3 0%, #e8f8fd 43%, #eee8ff 72%, #fff0eb 100%);
}

.cb-profile-recommendation.is-complete {
  background: linear-gradient(120deg, #fff0ba, #ffe1d7 48%, #e9e2ff 100%);
}

.cb-profile-recommendation-copy {
  display: grid;
  min-width: 0;
  gap: 6px;
}

.cb-profile-recommendation-copy strong {
  font-size: 19px;
  font-weight: 820;
  line-height: 1.22;
  letter-spacing: -.04em;
}

.cb-profile-recommendation-copy span {
  color: #616875;
  font-size: 10px;
  line-height: 1.5;
}

.cb-profile-primary-action,
.cb-profile-action {
  min-height: 46px;
  padding: 0 15px;
  border: 1px solid rgba(23, 23, 25, .10);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .055em;
  text-transform: uppercase;
  transition: transform .18s ease, box-shadow .18s ease;
}

.cb-profile-primary-action {
  background: linear-gradient(105deg, #a9f0df, #8ce8f4 42%, #cbbdff 74%, #ffb09e);
}

.cb-profile-action {
  background: #fff;
}

.cb-profile-primary-action:hover,
.cb-profile-action:hover,
.cb-profile-primary-action:focus-visible,
.cb-profile-action:focus-visible {
  transform: translateY(-1px);
  outline: 0;
  box-shadow: 0 10px 24px rgba(74, 77, 106, .13);
}

.cb-profile-activity-card {
  display: grid;
  gap: 7px;
  min-height: 110px;
}

.cb-profile-activity-card strong {
  font-size: 15px;
  font-weight: 810;
  line-height: 1.3;
  letter-spacing: -.025em;
}

.cb-profile-activity-card span,
.cb-profile-activity-card a {
  color: #6c727e;
  font-size: 9px;
  line-height: 1.5;
}

.cb-profile-activity-card a {
  width: fit-content;
  color: var(--cb-blue);
  font-weight: 790;
  text-decoration: none;
}

.cb-profile-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

@media (max-width: 900px) {
  .cb-profile-entry-card {
    grid-column: 1 / -1;
  }

  .cb-profile-metrics,
  .cb-profile-ranks {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .cb-profile-entry-form,
  .cb-profile-overview,
  .cb-profile-progress,
  .cb-profile-recommendation {
    grid-template-columns: 1fr;
  }

  .cb-profile-entry-form button,
  .cb-profile-primary-action {
    width: 100%;
  }

  .cb-profile-overview {
    gap: 14px;
    padding: 18px;
  }

  .cb-profile-overview-score {
    font-size: 48px;
  }

  .cb-profile-metrics,
  .cb-profile-ranks,
  .cb-profile-tour-columns,
  .cb-profile-activity-grid {
    grid-template-columns: 1fr;
  }

  .cb-profile-progress-stars {
    justify-content: flex-start;
  }

  .cb-profile-recommendation {
    padding: 17px;
  }

  .cb-profile-action {
    flex: 1 1 100%;
  }
}
'''

replace_once(
"\n@media (max-width: 900px) {\n  #corsar-blogger-booking {",
profile_css + "\n\n@media (max-width: 900px) {\n  #corsar-blogger-booking {",
"стили мини-ЛК",
)

profile_entry_html = r'''
        <article class="cb-profile-entry-card" aria-labelledby="cb-profile-entry-title">
          <div class="cb-profile-entry-copy">
            <span class="cb-stat-label">Профиль креатора</span>
            <strong id="cb-profile-entry-title">Откройте мини-ЛК</strong>
            <span>Поездки, уникальные программы, публикации, места в рейтингах и персональная рекомендация.</span>
          </div>
          <div class="cb-profile-entry-form">
            <input id="cb-profile-entry-input" list="cb-profile-creators" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Введите @username" aria-label="Ник креатора для открытия профиля">
            <datalist id="cb-profile-creators"></datalist>
            <button type="button" id="cb-profile-entry-submit">Открыть профиль</button>
          </div>
          <div id="cb-profile-entry-state" class="cb-profile-entry-state" aria-live="polite">Данные будут найдены в действующей базе сайта.</div>
        </article>'''

replace_once(
'''        </div>
      </div>

      <svg class="cb-route-line"''',
'''        </div>
''' + profile_entry_html + '''
      </div>

      <svg class="cb-route-line"''',
"вход в мини-ЛК на главной",
)

profile_section_html = r'''

  <section id="creator-profile" class="cb-section cb-profile-section" hidden>
    <div class="cb-section-head">
      <div>
        <div class="cb-section-kicker">Персональный профиль</div>
        <h2 class="cb-section-title">Мини-ЛК <strong>креатора</strong></h2>
      </div>
      <p class="cb-section-note">Профиль формируется из действующих записей и опубликованных материалов. Отдельной регистрации или нового учёта нет.</p>
    </div>
    <div id="cb-profile-dashboard" class="cb-profile-dashboard" aria-live="polite"></div>
  </section>'''

replace_once(
'''    <div id="cb-analytics" class="cb-analytics-card"></div>
  </section>

  <section id="results"''',
'''    <div id="cb-analytics" class="cb-analytics-card"></div>
  </section>''' + profile_section_html + '''

  <section id="results"''',
"секция мини-ЛК",
)

replace_once(
'''var creatorStoryRestoreFocus = null;
var weatherLastRequestedAt = 0;''',
'''var creatorStoryRestoreFocus = null;
var activeCreatorProfile = "";
var currentCreatorProfileRecommendation = null;
var weatherLastRequestedAt = 0;''',
"состояние мини-ЛК",
)

replace_once(
'''  fillCreatorDatalist("cb-booking-creators", bookingDirectory);
  fillCreatorDatalist("cb-report-creators", reportDirectory);''',
'''  fillCreatorDatalist("cb-booking-creators", bookingDirectory);
  fillCreatorDatalist("cb-report-creators", reportDirectory);
  fillCreatorDatalist("cb-profile-creators", bookingDirectory);
  refreshCreatorProfileEntryState();''',
"список креаторов мини-ЛК",
)

profile_js = r'''
function getCreatorProfileUniqueCatalog(){
  var seen = Object.create(null);
  var result = [];
  CANONICAL_TOURS.forEach(function(tour){
    if(isExcludedTour(tour)) return;
    var key = getUniqueTourKey(tour);
    if(!key || seen[key]) return;
    seen[key] = true;
    result.push({
      key: key,
      label: key === "вечерняя программа" ? "Вечерняя программа" : canonicalTourName(tour)
    });
  });
  return result;
}

function getCreatorProfileBookings(creator){
  var key = normalizeTelegram(creator);
  return bookings.filter(function(booking){
    return !isInactiveBooking(booking) && !isDeletedCreator(booking.telegram) && normalizeTelegram(booking.telegram) === key;
  });
}

function getCreatorProfileReports(creator){
  var key = normalizeTelegram(creator);
  return getPublishedContentItems().filter(function(report){
    return getReportCreator(report) === key;
  }).sort(function(a, b){
    return getActivitySortValue(b, reports.indexOf(b)) - getActivitySortValue(a, reports.indexOf(a));
  });
}

function getCreatorProfileUniqueSet(creator){
  var seen = Object.create(null);
  getCreatorProfileBookings(creator).forEach(function(booking){
    if(isExcludedTour(booking.tour)) return;
    var key = getUniqueTourKey(booking.tour);
    if(key) seen[key] = true;
  });
  return seen;
}

function getCreatorProfileRankings(){
  var visits = Object.create(null);
  bookings.forEach(function(booking){
    if(isInactiveBooking(booking)) return;
    var creator = normalizeTelegram(booking.telegram);
    if(!creator || isDeletedCreator(creator)) return;
    visits[creator] = (visits[creator] || 0) + 1;
  });

  var visitRanking = Object.keys(visits).map(function(name){
    return {name: name, visits: visits[name], uniqueTours: Math.min(getCreatorTourVariety(name), TOTAL_UNIQUE_TOURS)};
  }).sort(function(a, b){
    return b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  var uniqueRanking = visitRanking.slice().sort(function(a, b){
    return b.uniqueTours - a.uniqueTours || b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  var contentTotals = Object.create(null);
  getPublishedContentItems().forEach(function(report){
    var creator = getReportCreator(report);
    if(!creator || isDeletedCreator(creator)) return;
    contentTotals[creator] = (contentTotals[creator] || 0) + 1;
  });
  var contentRanking = Object.keys(contentTotals).map(function(name){
    return {name: name, materials: contentTotals[name]};
  }).sort(function(a, b){
    return b.materials - a.materials || a.name.localeCompare(b.name, "ru");
  });

  return {visits: visitRanking, unique: uniqueRanking, content: contentRanking};
}

function getCreatorProfileRankPosition(items, creator){
  var key = normalizeTelegram(creator);
  for(var i = 0; i < items.length; i++){
    if(items[i].name === key) return i + 1;
  }
  return 0;
}

function formatCreatorProfileRank(position){
  return position ? position + " место" : "нет позиции";
}

function findCreatorProfileRecommendation(creator, visited){
  var dates = Object.keys(TOURS_BY_DATE).sort();
  for(var i = 0; i < dates.length; i++){
    var date = dates[i];
    if(!isBookableDate(date)) continue;
    var tours = getToursByDate(date);
    for(var j = 0; j < tours.length; j++){
      var tour = tours[j];
      var key = getUniqueTourKey(tour);
      if(!key || visited[key] || hasBookingSlotConflict(date, tour)) continue;
      return {date: date, tour: canonicalTourName(tour), key: key};
    }
  }
  return null;
}

function getCreatorProfileData(creator){
  var key = normalizeTelegram(creator);
  var creatorBookings = getCreatorProfileBookings(key);
  var creatorReports = getCreatorProfileReports(key);
  var catalog = getCreatorProfileUniqueCatalog();
  var visited = getCreatorProfileUniqueSet(key);
  var completedTours = catalog.filter(function(item){ return !!visited[item.key]; });
  var missingTours = catalog.filter(function(item){ return !visited[item.key]; });
  var upcomingBookings = creatorBookings.filter(function(booking){
    var date = normalizeDate(booking.date);
    return isDateInSeason(date) && date >= getTodayKey();
  }).sort(function(a, b){
    return normalizeDate(a.date).localeCompare(normalizeDate(b.date)) || normalizeTour(a.tour).localeCompare(normalizeTour(b.tour), "ru");
  });
  var rankings = getCreatorProfileRankings();

  return {
    creator: key,
    bookings: creatorBookings,
    reports: creatorReports,
    uniqueCount: completedTours.length,
    completedTours: completedTours,
    missingTours: missingTours,
    upcomingBookings: upcomingBookings,
    nextBooking: upcomingBookings[0] || null,
    lastReport: creatorReports[0] || null,
    recommendation: findCreatorProfileRecommendation(key, visited),
    visitRank: getCreatorProfileRankPosition(rankings.visits, key),
    uniqueRank: getCreatorProfileRankPosition(rankings.unique, key),
    contentRank: getCreatorProfileRankPosition(rankings.content, key)
  };
}

function renderCreatorProfileTourChips(items){
  if(!items.length) return '<div class="cb-profile-tour-empty">Список пока пуст.</div>';
  return '<div class="cb-profile-tour-list">' + items.map(function(item){
    return '<span class="cb-profile-tour-chip">' + escapeHtml(item.label) + '</span>';
  }).join("") + '</div>';
}

function buildCreatorProfileRecommendation(data){
  if(data.uniqueCount >= TOTAL_UNIQUE_TOURS){
    return '<div class="cb-profile-recommendation is-complete"><div class="cb-profile-recommendation-copy"><small class="cb-profile-block-label">Все категории закрыты</small><strong>Пройдены все ' + TOTAL_UNIQUE_TOURS + ' уникальных туров</strong><span>Можно повторять любимые программы, продолжать набирать поездки и добавлять новые публикации.</span></div></div>';
  }
  if(data.recommendation){
    return '<div class="cb-profile-recommendation"><div class="cb-profile-recommendation-copy"><small class="cb-profile-block-label">Следующий уникальный тур</small><strong>' + escapeHtml(data.recommendation.tour) + '</strong><span>Ближайшее свободное окно: ' + escapeHtml(formatDateRu(data.recommendation.date)) + '. Эта категория ещё не учитывалась в вашем профиле.</span></div><button type="button" id="cb-profile-book-next" class="cb-profile-primary-action">Записаться</button></div>';
  }
  return '<div class="cb-profile-recommendation"><div class="cb-profile-recommendation-copy"><small class="cb-profile-block-label">Следующий уникальный тур</small><strong>Свободное окно пока не найдено</strong><span>В текущем расписании нет свободной непройденной программы. Профиль автоматически пересчитается при изменении данных.</span></div></div>';
}

function buildCreatorProfileActivity(data){
  var nextBooking = data.nextBooking
    ? '<strong>' + escapeHtml(formatDateRu(normalizeDate(data.nextBooking.date))) + '</strong><span>' + escapeHtml(canonicalTourName(data.nextBooking.tour)) + '</span>'
    : '<strong>Нет будущих записей</strong><span>Новая бронь появится здесь после оформления.</span>';

  var lastMaterial = data.lastReport
    ? '<strong>' + escapeHtml(getReportTour(data.lastReport) || "Материал сезона") + '</strong><span>' + escapeHtml(getContentPlatform(getReportLink(data.lastReport))) + ' · ' + escapeHtml(formatCreatorStoryDate(data.lastReport)) + '</span><a href="' + escapeHtml(getReportLink(data.lastReport)) + '" target="_blank" rel="noopener noreferrer">Открыть публикацию ↗</a>'
    : '<strong>Публикаций пока нет</strong><span>Добавленная работа сразу появится в профиле и рейтинге контента.</span>';

  return '<div class="cb-profile-activity-grid"><article class="cb-profile-activity-card"><small class="cb-profile-block-label">Ближайшая бронь</small>' + nextBooking + '</article><article class="cb-profile-activity-card"><small class="cb-profile-block-label">Последний материал</small>' + lastMaterial + '</article></div>';
}

function renderCreatorProfile(){
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

  dashboard.innerHTML = '<div class="cb-profile-overview"><div class="cb-profile-overview-copy"><small>Профиль сезона</small><h3>' + escapeHtml(data.creator) + '</h3><p>Данные собраны из действующих записей и опубликованных работ без отдельной регистрации.</p></div><div class="cb-profile-overview-score"><strong>' + data.uniqueCount + '</strong><small>/ ' + TOTAL_UNIQUE_TOURS + '</small></div></div>' +
    '<div class="cb-profile-metrics"><div class="cb-profile-metric"><strong>' + data.bookings.length + '</strong><span>' + pluralCount(data.bookings.length, "поездка в учёте", "поездки в учёте", "поездок в учёте") + '</span></div><div class="cb-profile-metric"><strong>' + data.uniqueCount + '/' + TOTAL_UNIQUE_TOURS + '</strong><span>Уникальные программы</span></div><div class="cb-profile-metric"><strong>' + data.reports.length + '</strong><span>' + pluralCount(data.reports.length, "опубликованная работа", "опубликованные работы", "опубликованных работ") + '</span></div></div>' +
    '<div class="cb-profile-ranks"><div class="cb-profile-rank"><small>По количеству туров</small><strong>' + formatCreatorProfileRank(data.visitRank) + '</strong></div><div class="cb-profile-rank"><small>По уникальным турам</small><strong>' + formatCreatorProfileRank(data.uniqueRank) + '</strong></div><div class="cb-profile-rank"><small>По контенту</small><strong>' + formatCreatorProfileRank(data.contentRank) + '</strong></div></div>' +
    '<div class="cb-profile-progress"><div class="cb-profile-progress-copy"><small class="cb-profile-block-label">Охват программ</small><strong>' + data.uniqueCount + ' ' + pluralCount(data.uniqueCount, "уникальный тур", "уникальных тура", "уникальных туров") + ' из ' + TOTAL_UNIQUE_TOURS + '</strong><span>Две вечерние программы учитываются как одна категория; двухдневные туры в уникальность не входят.</span></div><div class="cb-profile-progress-stars" aria-label="Пройдено ' + data.uniqueCount + ' из ' + TOTAL_UNIQUE_TOURS + ' уникальных туров">' + renderTourVarietyStars(data.uniqueCount) + '</div></div>' +
    '<div class="cb-profile-tour-columns"><article class="cb-profile-tour-block is-complete"><small class="cb-profile-block-label">Уже учтено</small>' + renderCreatorProfileTourChips(data.completedTours) + '</article><article class="cb-profile-tour-block is-missing"><small class="cb-profile-block-label">Ещё не посещено</small>' + renderCreatorProfileTourChips(data.missingTours) + '</article></div>' +
    buildCreatorProfileRecommendation(data) + buildCreatorProfileActivity(data) +
    '<div class="cb-profile-actions">' + (data.upcomingBookings.length ? '<button type="button" id="cb-profile-manage" class="cb-profile-action">Управлять бронями</button>' : '') + (data.bookings.length ? '<button type="button" id="cb-profile-add-content" class="cb-profile-action">Добавить контент</button>' : '') + (data.reports.length ? '<button type="button" id="cb-profile-view-works" class="cb-profile-action">Смотреть мои работы</button>' : '') + '<button type="button" id="cb-profile-change" class="cb-profile-action">Сменить профиль</button></div>';

  var bookNext = $("cb-profile-book-next");
  var manage = $("cb-profile-manage");
  var addContent = $("cb-profile-add-content");
  var viewWorks = $("cb-profile-view-works");
  var change = $("cb-profile-change");
  if(bookNext) bookNext.onclick = prefillCreatorProfileRecommendation;
  if(manage) manage.onclick = openCreatorProfileBookingManagement;
  if(addContent) addContent.onclick = openCreatorProfileContentForm;
  if(viewWorks) viewWorks.onclick = function(){ focusCreatorResults(activeCreatorProfile); };
  if(change) change.onclick = function(){
    var input = $("cb-profile-entry-input");
    if(input){
      input.focus();
      input.select();
      var home = $("home");
      if(home) home.scrollIntoView({behavior: "smooth", block: "start"});
    }
  };
}

function selectCreatorProfileTourOption(tour){
  var select = $("cb-tour");
  if(!select) return;
  var key = normalizeTour(tour);
  Array.prototype.some.call(select.options, function(option){
    if(!option.disabled && normalizeTour(option.value) === key){
      select.value = option.value;
      return true;
    }
    return false;
  });
}

function prefillCreatorProfileRecommendation(){
  if(!activeCreatorProfile || !currentCreatorProfileRecommendation) return;
  var recommendation = currentCreatorProfileRecommendation;
  var bookingInput = $("cb-telegram");
  var mode = $("cb-booking-mode");
  if(bookingInput) bookingInput.value = activeCreatorProfile;
  if(mode) mode.value = "new";
  setFormDate(recommendation.date);
  renderTours(recommendation.date);
  selectCreatorProfileTourOption(recommendation.tour);
  renderCreatorOptions();
  renderCalendar();
  renderDetails(recommendation.date);
  renderTransferOptions();
  setMessage("Подготовлены <b>" + formatDateRu(recommendation.date) + "</b> и тур <b>" + escapeHtml(recommendation.tour) + "</b>. Проверьте данные и сформируйте заявку.", false);
  var bookingSection = $("booking");
  if(bookingSection) bookingSection.scrollIntoView({behavior: "smooth", block: "start"});
}

function openCreatorProfileBookingManagement(){
  if(!activeCreatorProfile) return;
  var input = $("cb-telegram");
  var mode = $("cb-booking-mode");
  if(input) input.value = activeCreatorProfile;
  if(mode) mode.value = "transfer";
  renderCreatorOptions();
  renderTransferOptions();
  setMessage("Профиль подставлен. Выберите перенос или удаление своей активной брони.", false);
  var bookingSection = $("booking");
  if(bookingSection) bookingSection.scrollIntoView({behavior: "smooth", block: "start"});
}

function openCreatorProfileContentForm(){
  if(!activeCreatorProfile) return;
  var input = $("cb-report-telegram");
  if(input) input.value = activeCreatorProfile;
  renderCreatorOptions();
  setMessage("Ник подставлен. Выберите посещённый тур и добавьте ссылку на готовую работу.", false);
  var contentSection = $("content");
  if(contentSection) contentSection.scrollIntoView({behavior: "smooth", block: "start"});
}

function setCreatorProfileEntryState(message, type){
  var state = $("cb-profile-entry-state");
  if(!state) return;
  state.className = "cb-profile-entry-state" + (type ? " is-" + type : "");
  state.textContent = message || "";
}

function refreshCreatorProfileEntryState(){
  var input = $("cb-profile-entry-input");
  if(!input) return;
  var raw = String(input.value || "").trim();
  if(!raw){
    setCreatorProfileEntryState(creatorDirectoryReady ? "Введите ник из подсказок, чтобы открыть профиль." : "Загружаем базу креаторов...", "");
    return;
  }
  if(!creatorDirectoryReady){
    setCreatorProfileEntryState("Данные ещё загружаются.", "");
    return;
  }
  var entry = findCreatorEntry(raw, getKnownCreatorDirectory());
  if(entry){
    setCreatorProfileEntryState("Найден профиль " + entry.name + ".", "ready");
  } else {
    setCreatorProfileEntryState("Ник не найден в действующей базе записей и материалов.", "error");
  }
}

function openCreatorProfileFromEntry(){
  var input = $("cb-profile-entry-input");
  if(!input) return;
  if(!creatorDirectoryReady){
    setCreatorProfileEntryState("Дождитесь завершения загрузки данных.", "error");
    return;
  }
  var entry = findCreatorEntry(input.value, getKnownCreatorDirectory());
  if(!entry){
    setCreatorProfileEntryState("Выберите существующий ник из подсказок.", "error");
    return;
  }
  input.value = entry.name;
  activeCreatorProfile = entry.name;
  setCreatorProfileEntryState("Открыт профиль " + entry.name + ".", "ready");
  renderCreatorProfile();
  var section = $("creator-profile");
  if(section) section.scrollIntoView({behavior: "smooth", block: "start"});
}

function setupCreatorProfile(){
  var input = $("cb-profile-entry-input");
  var submit = $("cb-profile-entry-submit");
  if(submit) submit.onclick = openCreatorProfileFromEntry;
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

'''

replace_once(
"function focusTourSchedule(){",
profile_js + "function focusTourSchedule(){",
"логика мини-ЛК",
)

replace_once(
'''  renderAnalytics();
  renderResults();
  renderCreatorStories();''',
'''  renderAnalytics();
  renderResults();
  renderCreatorProfile();
  renderCreatorStories();''',
"обновление мини-ЛК вместе с данными",
)

replace_once(
'''        renderResults();
        renderCreatorOptions();
        renderCreatorStories();
        renderRecentCreatorEvents();''',
'''        renderResults();
        renderCreatorOptions();
        renderCreatorStories();
        renderCreatorProfile();
        renderRecentCreatorEvents();''',
"обновление профиля после публикации",
)

replace_once(
'''  setupCreatorIdentityInputs();
  setupCreatorStories();
  setupCompactNotice();''',
'''  setupCreatorIdentityInputs();
  setupCreatorProfile();
  setupCreatorStories();
  setupCompactNotice();''',
"инициализация мини-ЛК",
)

path.write_text(text, encoding="utf-8")
