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


next_tour_css = r'''
/* ===== Персональный подбор следующего уникального тура ===== */
.cb-next-tour-shell {
  position: relative;
  margin-top: 22px;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .08);
  border-radius: 30px;
  background:
    radial-gradient(circle at 92% 8%, rgba(78, 203, 237, .22), transparent 20rem),
    radial-gradient(circle at 5% 94%, rgba(127, 103, 248, .15), transparent 19rem),
    linear-gradient(135deg, rgba(255,255,255,.98), rgba(241,250,248,.98) 50%, rgba(242,238,255,.98));
  box-shadow: 0 18px 58px rgba(28, 31, 41, .065);
}

.cb-next-tour-shell::before {
  content: "";
  position: absolute;
  z-index: 0;
  top: 0;
  right: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--cb-mint), var(--cb-cyan) 34%, var(--cb-lilac-strong) 68%, var(--cb-coral));
}

.cb-next-tour-summary {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 34px;
  align-items: center;
  gap: 18px;
  min-height: 94px;
  padding: 22px 26px;
  cursor: pointer;
  list-style: none;
  user-select: none;
}

.cb-next-tour-summary::-webkit-details-marker {
  display: none;
}

.cb-next-tour-summary-copy {
  display: grid;
  min-width: 0;
  gap: 5px;
}

.cb-next-tour-kicker {
  color: #747b87;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .105em;
  text-transform: uppercase;
}

.cb-next-tour-title {
  overflow: hidden;
  color: var(--cb-ink);
  font-size: clamp(20px, 2.5vw, 30px);
  font-weight: 760;
  line-height: 1.08;
  letter-spacing: -.045em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-next-tour-summary-meta {
  max-width: 350px;
  color: #737887;
  text-align: right;
  font-size: 10px;
  font-weight: 650;
  line-height: 1.45;
}

.cb-next-tour-toggle {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: rgba(255,255,255,.76);
  color: var(--cb-ink);
  font-size: 21px;
  line-height: 1;
  transition: transform .22s ease, background .22s ease;
}

.cb-next-tour-shell[open] .cb-next-tour-toggle {
  transform: rotate(45deg);
  background: var(--cb-ink);
  color: #fff;
}

.cb-next-tour-body {
  position: relative;
  z-index: 1;
  padding: 20px 26px 26px;
  border-top: 1px solid rgba(23, 23, 25, .07);
}

.cb-next-tour-picker {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 12px;
}

.cb-next-tour-field {
  display: grid;
  gap: 8px;
}

.cb-next-tour-field label {
  color: #666c78;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: .075em;
  text-transform: uppercase;
}

.cb-next-tour-field input {
  width: 100%;
  min-height: 48px;
  padding: 0 14px;
  border: 1px solid rgba(23, 23, 25, .12);
  border-radius: 0;
  outline: none;
  background: rgba(255,255,255,.82);
  color: var(--cb-ink);
  font: inherit;
  font-size: 14px;
  transition: border-color .18s ease, box-shadow .18s ease;
}

.cb-next-tour-field input:focus {
  border-color: var(--cb-lilac-strong);
  box-shadow: 0 0 0 3px rgba(127, 103, 248, .12);
}

.cb-next-tour-submit,
.cb-next-tour-book {
  min-height: 48px;
  padding: 0 18px;
  border: 1px solid rgba(23, 23, 25, .10);
  background: linear-gradient(105deg, #a9f0df, #8ce8f4 42%, #cbbdff 74%, #ffb09e);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  font-weight: 820;
  text-align: center;
  transition: transform .18s ease, box-shadow .18s ease;
}

.cb-next-tour-submit:hover,
.cb-next-tour-book:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(83, 89, 126, .14);
}

.cb-next-tour-result {
  margin-top: 16px;
}

.cb-next-tour-placeholder,
.cb-next-tour-error {
  padding: 18px;
  border: 1px dashed rgba(23, 23, 25, .14);
  background: rgba(255,255,255,.56);
  color: #707682;
  font-size: 11px;
  line-height: 1.55;
}

.cb-next-tour-error {
  border-style: solid;
  border-color: rgba(185, 64, 58, .18);
  background: rgba(255, 239, 236, .72);
  color: #8d4842;
}

.cb-next-tour-profile {
  display: grid;
  gap: 15px;
}

.cb-next-tour-progress {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
  padding: 17px 18px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: rgba(255,255,255,.66);
}

.cb-next-tour-progress-copy {
  display: grid;
  min-width: 0;
  gap: 4px;
}

.cb-next-tour-progress-copy small {
  color: #777d88;
  font-size: 8px;
  font-weight: 820;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-next-tour-progress-copy strong {
  overflow: hidden;
  font-size: clamp(22px, 4vw, 34px);
  font-weight: 790;
  line-height: 1;
  letter-spacing: -.055em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cb-next-tour-progress-copy span {
  color: #686f7b;
  font-size: 10px;
  line-height: 1.45;
}

.cb-next-tour-stars {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 3px;
  white-space: nowrap;
}

.cb-next-tour-missing {
  display: grid;
  gap: 9px;
}

.cb-next-tour-missing-label {
  color: #737985;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: .075em;
  text-transform: uppercase;
}

.cb-next-tour-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.cb-next-tour-chip {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 10px;
  border: 1px solid rgba(23, 23, 25, .09);
  background: rgba(255,255,255,.64);
  color: #676d79;
  font-size: 9px;
  font-weight: 690;
  line-height: 1.3;
}

.cb-next-tour-recommendation {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 18px;
  border: 1px solid rgba(23, 23, 25, .08);
  background:
    radial-gradient(circle at 94% 10%, rgba(255,255,255,.72), transparent 34%),
    linear-gradient(120deg, #e5fbf3 0%, #e8f8fd 43%, #eee8ff 72%, #fff0eb 100%);
}

.cb-next-tour-recommendation-copy {
  display: grid;
  min-width: 0;
  gap: 5px;
}

.cb-next-tour-recommendation-copy small {
  color: #6c7380;
  font-size: 8px;
  font-weight: 830;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.cb-next-tour-recommendation-copy strong {
  color: var(--cb-ink);
  font-size: 18px;
  font-weight: 810;
  line-height: 1.22;
  letter-spacing: -.035em;
}

.cb-next-tour-recommendation-copy span {
  color: #606875;
  font-size: 10px;
  line-height: 1.5;
}

.cb-next-tour-complete {
  padding: 22px;
  border: 1px solid rgba(23, 23, 25, .08);
  background: linear-gradient(120deg, #fff0ba, #ffe1d7 48%, #e9e2ff 100%);
}

.cb-next-tour-complete strong {
  display: block;
  font-size: clamp(22px, 4vw, 32px);
  font-weight: 810;
  letter-spacing: -.05em;
}

.cb-next-tour-complete span {
  display: block;
  margin-top: 7px;
  color: #676a75;
  font-size: 10px;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .cb-next-tour-summary {
    grid-template-columns: minmax(0, 1fr) 34px;
    gap: 10px;
    min-height: 82px;
    padding: 18px 20px;
  }

  .cb-next-tour-summary-meta {
    grid-column: 1 / -1;
    grid-row: 2;
    max-width: none;
    margin-top: -3px;
    text-align: left;
  }

  .cb-next-tour-toggle {
    grid-column: 2;
    grid-row: 1;
  }

  .cb-next-tour-body {
    padding: 18px 20px 20px;
  }
}

@media (max-width: 600px) {
  .cb-next-tour-shell {
    margin-top: 14px;
    border-radius: 22px;
  }

  .cb-next-tour-summary {
    min-height: 76px;
    padding: 16px;
  }

  .cb-next-tour-title {
    font-size: 19px;
  }

  .cb-next-tour-summary-meta {
    font-size: 9px;
  }

  .cb-next-tour-body {
    padding: 14px;
  }

  .cb-next-tour-picker,
  .cb-next-tour-progress,
  .cb-next-tour-recommendation {
    grid-template-columns: 1fr;
  }

  .cb-next-tour-submit,
  .cb-next-tour-book {
    width: 100%;
  }

  .cb-next-tour-stars {
    justify-content: flex-start;
  }

  .cb-next-tour-recommendation {
    gap: 14px;
  }
}
'''

replace_once(
    "/* ===== Истории креаторов ===== */",
    next_tour_css + "\n\n/* ===== Истории креаторов ===== */",
    "CSS персонального подбора",
)

next_tour_html = r'''
  <details id="cb-next-tour" class="cb-next-tour-shell">
    <summary class="cb-next-tour-summary">
      <span class="cb-next-tour-summary-copy">
        <span class="cb-next-tour-kicker">Персональный маршрут</span>
        <strong class="cb-next-tour-title">Какой тур посетить следующим</strong>
      </span>
      <span id="cb-next-tour-summary-meta" class="cb-next-tour-summary-meta">Подберём новую уникальную программу по вашему нику и свободным окнам.</span>
      <span class="cb-next-tour-toggle" aria-hidden="true">+</span>
    </summary>
    <div class="cb-next-tour-body">
      <div class="cb-next-tour-picker">
        <div class="cb-next-tour-field">
          <label for="cb-next-tour-creator">Ник креатора</label>
          <input id="cb-next-tour-creator" list="cb-next-tour-creators" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="Начните вводить @username">
          <datalist id="cb-next-tour-creators"></datalist>
        </div>
        <button type="button" id="cb-next-tour-submit" class="cb-next-tour-submit">Подобрать следующий тур</button>
      </div>
      <div id="cb-next-tour-result" class="cb-next-tour-result" aria-live="polite">
        <div class="cb-next-tour-placeholder">Выберите существующий ник. Покажем прогресс из 8 уникальных категорий, ещё не закрытые программы и ближайшее свободное окно.</div>
      </div>
    </div>
  </details>

'''

replace_once(
    '  <section id="results" class="cb-section cb-results-section">',
    next_tour_html + '  <section id="results" class="cb-section cb-results-section">',
    "HTML блока перед итогами",
)

replace_once(
    '  fillCreatorDatalist("cb-booking-creators", bookingDirectory);\n  fillCreatorDatalist("cb-report-creators", reportDirectory);',
    '  fillCreatorDatalist("cb-booking-creators", bookingDirectory);\n  fillCreatorDatalist("cb-report-creators", reportDirectory);\n  fillCreatorDatalist("cb-next-tour-creators", bookingDirectory);',
    "список ников для персонального подбора",
)

next_tour_js = r'''
function getUniqueTourCategoryLabel(key, fallback){
  if(key === "вечерняя программа") return "Вечерняя программа";
  return canonicalTourName(fallback) || String(fallback || "");
}

function getUniqueTourCategories(){
  var seen = Object.create(null);
  var categories = [];
  CANONICAL_TOURS.forEach(function(tour){
    var key = getUniqueTourKey(tour);
    if(!key || seen[key]) return;
    seen[key] = true;
    categories.push({key: key, label: getUniqueTourCategoryLabel(key, tour)});
  });
  return categories;
}

function getCreatorUniqueTourMap(creator){
  var normalized = normalizeTelegram(creator);
  var seen = Object.create(null);
  bookings.forEach(function(booking){
    if(isInactiveBooking(booking) || isExcludedTour(booking.tour)) return;
    if(normalizeTelegram(booking.telegram) !== normalized) return;
    var key = getUniqueTourKey(booking.tour);
    if(key) seen[key] = true;
  });
  return seen;
}

function findNextUniqueTourSlot(missingKeys){
  var allowed = Object.create(null);
  (missingKeys || []).forEach(function(key){ if(key) allowed[key] = true; });
  var today = getTodayKey();
  var dates = Object.keys(TOURS_BY_DATE).sort();

  for(var d = 0; d < dates.length; d++){
    var date = dates[d];
    if(date < today || !isDateInSeason(date) || !isBookableDate(date)) continue;
    var tours = getToursByDate(date);

    for(var t = 0; t < tours.length; t++){
      var tour = tours[t];
      var key = getUniqueTourKey(tour);
      if(!key || !allowed[key]) continue;
      if(isExcludedTour(tour) || isKnownScheduleExclusion(date, tour) || hasBookingSlotConflict(date, tour)) continue;
      return {
        date: date,
        tour: tour,
        key: key,
        label: getUniqueTourCategoryLabel(key, tour)
      };
    }
  }

  return null;
}

function focusNextTourBooking(recommendation, creator){
  if(!recommendation) return;
  if(hasBookingSlotConflict(recommendation.date, recommendation.tour)){
    renderNextTourGuide();
    setMessage("Это окно уже занято. Подбираем следующее свободное предложение.", true);
    return;
  }

  var bookingInput = $("cb-telegram");
  var bookingMode = $("cb-booking-mode");
  var tourSelect = $("cb-tour");
  if(bookingInput) bookingInput.value = creator;
  if(bookingMode) bookingMode.value = "new";

  setFormDate(recommendation.date);
  renderTours(recommendation.date);
  tourSelect = $("cb-tour");
  if(tourSelect){
    var options = Array.prototype.slice.call(tourSelect.options || []);
    var match = options.filter(function(option){
      return normalizeTour(option.value) === normalizeTour(recommendation.tour);
    })[0];
    if(match) tourSelect.value = match.value;
  }

  renderCalendar();
  renderDetails(recommendation.date);
  renderCreatorOptions();

  var bookingSection = $("booking");
  if(window.location.hash !== "#booking") window.location.hash = "booking";
  if(bookingSection) bookingSection.scrollIntoView({behavior: "smooth", block: "start"});
  setMessage("Дата и новый уникальный тур подставлены в форму бронирования.", false);
}

function renderNextTourGuide(){
  var input = $("cb-next-tour-creator");
  var result = $("cb-next-tour-result");
  var summaryMeta = $("cb-next-tour-summary-meta");
  if(!input || !result || !summaryMeta) return;

  if(!creatorDirectoryReady){
    summaryMeta.textContent = "Загружаем данные креаторов и свободные окна...";
    result.innerHTML = '<div class="cb-next-tour-placeholder">Собираем персональную рекомендацию после загрузки расписания.</div>';
    return;
  }

  var rawCreator = String(input.value || "").trim();
  if(!rawCreator){
    summaryMeta.textContent = "Подберём новую уникальную программу по вашему нику и свободным окнам.";
    result.innerHTML = '<div class="cb-next-tour-placeholder">Выберите существующий ник. Покажем прогресс из ' + TOTAL_UNIQUE_TOURS + ' уникальных категорий, ещё не закрытые программы и ближайшее свободное окно.</div>';
    return;
  }

  var directory = getKnownCreatorDirectory();
  var entry = findCreatorEntry(rawCreator, directory);
  if(!entry){
    summaryMeta.textContent = "Ник не найден в действующей базе записей";
    result.innerHTML = '<div class="cb-next-tour-error">Такого креатора пока нет в системе. Выберите ник из подсказок или сначала оформите запись на тур.</div>';
    return;
  }

  var creator = entry.name;
  input.value = creator;
  var categories = getUniqueTourCategories();
  var visited = getCreatorUniqueTourMap(creator);
  var missing = categories.filter(function(category){ return !visited[category.key]; });
  var uniqueCount = Math.min(categories.length - missing.length, TOTAL_UNIQUE_TOURS);
  var remaining = Math.max(0, TOTAL_UNIQUE_TOURS - uniqueCount);
  summaryMeta.textContent = creator + " · " + uniqueCount + " из " + TOTAL_UNIQUE_TOURS + " уникальных туров";

  var progressMarkup = '<div class="cb-next-tour-progress">' +
    '<span class="cb-next-tour-progress-copy"><small>Ваш маршрут сезона</small><strong>' + escapeHtml(creator) + '</strong>' +
    '<span>' + uniqueCount + ' из ' + TOTAL_UNIQUE_TOURS + ' уникальных категорий · осталось ' + remaining + '</span></span>' +
    '<span class="cb-next-tour-stars" aria-label="Закрыто ' + uniqueCount + ' из ' + TOTAL_UNIQUE_TOURS + ' уникальных туров">' + renderTourVarietyStars(uniqueCount) + '</span>' +
  '</div>';

  if(!missing.length){
    result.innerHTML = '<div class="cb-next-tour-profile">' + progressMarkup +
      '<div class="cb-next-tour-complete"><strong>Все уникальные туры закрыты</strong><span>В вашей статистике собраны все ' + TOTAL_UNIQUE_TOURS + ' категории сезона. Повторные поездки продолжат увеличивать общий счёт, но уникальный охват уже максимальный.</span></div>' +
    '</div>';
    return;
  }

  var chips = missing.map(function(category){
    return '<span class="cb-next-tour-chip">' + escapeHtml(category.label) + '</span>';
  }).join("");
  var missingMarkup = '<div class="cb-next-tour-missing"><span class="cb-next-tour-missing-label">Ещё не закрыты</span><div class="cb-next-tour-chips">' + chips + '</div></div>';
  var recommendation = findNextUniqueTourSlot(missing.map(function(category){ return category.key; }));

  if(!recommendation){
    result.innerHTML = '<div class="cb-next-tour-profile">' + progressMarkup + missingMarkup +
      '<div class="cb-next-tour-placeholder">Для оставшихся категорий сейчас нет свободного будущего окна. Расписание и занятость могут измениться — проверяйте календарь.</div>' +
      '<button type="button" id="cb-next-tour-calendar" class="cb-next-tour-book">Смотреть календарь</button>' +
    '</div>';
    var calendarButton = $("cb-next-tour-calendar");
    if(calendarButton) calendarButton.onclick = focusTourSchedule;
    return;
  }

  result.innerHTML = '<div class="cb-next-tour-profile">' + progressMarkup + missingMarkup +
    '<div class="cb-next-tour-recommendation">' +
      '<span class="cb-next-tour-recommendation-copy"><small>Ближайшее свободное окно · ' + escapeHtml(recommendation.label) + '</small>' +
      '<strong>' + escapeHtml(canonicalTourName(recommendation.tour)) + '</strong>' +
      '<span>' + escapeHtml(formatDateRu(recommendation.date)) + ' · программа ещё не учтена в вашей уникальной статистике</span></span>' +
      '<button type="button" id="cb-next-tour-book" class="cb-next-tour-book">Выбрать этот тур</button>' +
    '</div>' +
  '</div>';

  var bookButton = $("cb-next-tour-book");
  if(bookButton) bookButton.onclick = function(){ focusNextTourBooking(recommendation, creator); };
}

function setupNextTourGuide(){
  var input = $("cb-next-tour-creator");
  var submit = $("cb-next-tour-submit");
  var details = $("cb-next-tour");
  if(submit) submit.onclick = renderNextTourGuide;
  if(input){
    input.addEventListener("change", renderNextTourGuide);
    input.addEventListener("keydown", function(event){
      if(event.key !== "Enter") return;
      event.preventDefault();
      renderNextTourGuide();
    });
  }
  if(details) details.addEventListener("toggle", function(){
    if(details.open) renderNextTourGuide();
  });
}

'''

replace_once(
    "function getCreatorGroupId(creator){",
    next_tour_js + "function getCreatorGroupId(creator){",
    "JavaScript персонального подбора",
)

replace_once(
    "  renderAnalytics();\n  renderResults();\n  renderCreatorStories();",
    "  renderAnalytics();\n  renderNextTourGuide();\n  renderResults();\n  renderCreatorStories();",
    "обновление персонального подбора вместе с данными",
)

replace_once(
    "  setupCreatorStories();\n  setupCompactNotice();",
    "  setupCreatorStories();\n  setupNextTourGuide();\n  setupCompactNotice();",
    "инициализация персонального подбора",
)

replace_once(
    '''var PORTAL_UPDATES = [{
  date: "2026-07-22",
  text: "Обновлены мобильный календарь, блок обратной связи CREACLOUD и ежедневная сводка портала."
}];''',
    '''var PORTAL_UPDATES = [{
  date: "2026-07-22",
  text: "Обновлены мобильный календарь, блок обратной связи CREACLOUD и ежедневная сводка портала."
}, {
  date: "2026-07-24",
  text: "Добавлен персональный подбор следующего уникального тура по нику и свободным окнам."
}];''',
    "обновление ежедневной сводки портала",
)

path.write_text(text, encoding="utf-8")
