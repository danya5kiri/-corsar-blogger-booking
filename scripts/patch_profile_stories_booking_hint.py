#!/usr/bin/env python3
from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


def replace_regex(pattern: str, replacement: str, label: str) -> None:
    global text
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = updated


profile_entry = '''        <article class="cb-profile-entry-card" aria-labelledby="cb-profile-entry-title">
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
        </article>
'''

replace_once(profile_entry, "", "удаление карточки мини-ЛК из правой колонки")
hero_intro_anchor = '''        <div>
          <div class="cb-eyebrow">Творческая мастерская</div>
          <h1 class="cb-hero-title">Привет, <strong>креатор!</strong></h1>
          <p class="cb-hero-text">Выбирайте морское путешествие, создавайте живой контент о Владивостоке и возвращайтесь сюда, чтобы поделиться готовой публикацией.</p>
        </div>
'''
replace_once(hero_intro_anchor, hero_intro_anchor + profile_entry, "перенос карточки мини-ЛК в левую колонку")

profile_section = '''  <section id="creator-profile" class="cb-section cb-profile-section" hidden>
    <div class="cb-section-head">
      <div>
        <div class="cb-section-kicker">Персональный профиль</div>
        <h2 class="cb-section-title">Мини-ЛК <strong>креатора</strong></h2>
      </div>
      <p class="cb-section-note">Профиль формируется из действующих записей и опубликованных материалов. Отдельной регистрации или нового учёта нет.</p>
    </div>
    <div id="cb-profile-dashboard" class="cb-profile-dashboard" aria-live="polite"></div>
  </section>

'''
replace_once(profile_section, "", "удаление мини-ЛК из середины страницы")
footer_anchor = '  <footer id="creacloud" class="cb-footer">'
replace_once(footer_anchor, profile_section + footer_anchor, "перенос мини-ЛК перед CREACLOUD")

replace_once(
    '<strong id="cb-stories-summary-title" class="cb-stories-summary-title">Загружаем истории креаторов...</strong>',
    '<span id="cb-stories-summary-title" class="cb-stories-summary-title"><strong>Загружаем</strong> публикации...</span>',
    "разметка заголовка историй",
)

booking_tour_field = '''      <div class="cb-field" style="grid-column: 1 / -1;">
        <label for="cb-tour">Название тура</label>
        <select id="cb-tour"><option value="">Сначала выберите дату</option></select>
        <div class="cb-field-hint">Показаны только программы из актуального расписания на выбранную дату.</div>
      </div>
'''
booking_tour_field_new = booking_tour_field + '''      <details id="cb-booking-unique-hint" class="cb-booking-unique-hint" hidden>
        <summary><span>Новая категория на эту дату</span><span class="cb-booking-unique-toggle" aria-hidden="true">+</span></summary>
        <div class="cb-booking-unique-body">
          <div id="cb-booking-unique-copy" class="cb-booking-unique-copy"></div>
          <button type="button" id="cb-booking-unique-action">Выбрать рекомендованный тур</button>
        </div>
      </details>
'''
replace_once(booking_tour_field, booking_tour_field_new, "подсказка в форме бронирования")

css_anchor = '''

@media (max-width: 900px) {
  #corsar-blogger-booking {
'''
css_addition = r'''

/* ===== Уточнение мини-ЛК, историй и рекомендации при записи ===== */
.cb-stories-summary-title {
  font-weight: 300;
}

.cb-stories-summary-title strong {
  font-weight: 820;
}

.cb-profile-metrics.is-compact {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.cb-booking-unique-hint[hidden] {
  display: none;
}

.cb-booking-unique-hint {
  grid-column: 1 / -1;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .09);
  background: linear-gradient(110deg, rgba(229, 251, 243, .82), rgba(232, 248, 253, .84) 45%, rgba(238, 232, 255, .82));
}

.cb-booking-unique-hint summary {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 28px;
  align-items: center;
  gap: 12px;
  min-height: 44px;
  padding: 10px 13px;
  color: #52606a;
  cursor: pointer;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: .065em;
  list-style: none;
  text-transform: uppercase;
}

.cb-booking-unique-hint summary::-webkit-details-marker {
  display: none;
}

.cb-booking-unique-toggle {
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border: 1px solid rgba(23, 23, 25, .10);
  border-radius: 50%;
  background: rgba(255, 255, 255, .72);
  color: var(--cb-ink);
  font-size: 17px;
  font-weight: 420;
  transition: transform .2s ease;
}

.cb-booking-unique-hint[open] .cb-booking-unique-toggle {
  transform: rotate(45deg);
}

.cb-booking-unique-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  padding: 12px 13px 14px;
  border-top: 1px solid rgba(23, 23, 25, .07);
}

.cb-booking-unique-copy {
  color: #626b76;
  font-size: 10px;
  line-height: 1.5;
}

.cb-booking-unique-copy strong {
  color: var(--cb-ink);
  font-weight: 810;
}

#cb-booking-unique-action {
  min-height: 42px;
  padding: 0 13px;
  border: 1px solid rgba(23, 23, 25, .10);
  background: rgba(255, 255, 255, .82);
  color: var(--cb-ink);
  cursor: pointer;
  font: inherit;
  font-size: 9px;
  font-weight: 830;
  letter-spacing: .045em;
  text-transform: uppercase;
  transition: transform .18s ease, box-shadow .18s ease;
}

#cb-booking-unique-action:hover,
#cb-booking-unique-action:focus-visible {
  transform: translateY(-1px);
  outline: 0;
  box-shadow: 0 10px 22px rgba(77, 111, 122, .13);
}

@media (min-width: 901px) {
  .cb-profile-entry-card.is-desktop-placement {
    display: grid;
    grid-template-columns: minmax(190px, .9fr) minmax(280px, 1.1fr);
    grid-template-rows: auto auto;
    align-items: center;
    gap: 8px 18px;
    width: var(--cb-events-desktop-width, 100%);
    max-width: 100%;
    min-height: 154px;
    margin: auto 0 10px;
    padding: 18px;
  }

  .cb-profile-entry-card.is-desktop-placement .cb-profile-entry-copy {
    grid-row: 1 / span 2;
  }

  .cb-profile-entry-card.is-desktop-placement .cb-profile-entry-form {
    grid-column: 2;
    margin-top: 0;
  }

  .cb-profile-entry-card.is-desktop-placement .cb-profile-entry-state {
    grid-column: 2;
    margin-top: -2px;
  }

  .cb-profile-entry-card.is-desktop-placement + .cb-recent-events-desktop {
    margin: 0;
  }
}

@media (max-width: 600px) {
  .cb-profile-metrics.is-compact,
  .cb-booking-unique-body {
    grid-template-columns: 1fr;
  }

  #cb-booking-unique-action {
    width: 100%;
  }
}
'''
replace_once(css_anchor, css_addition + css_anchor, "добавление адаптивных стилей")

replace_regex(
    r'''function syncDesktopRecentEventsWidth\(\)\{.*?\n\}\n\nfunction setupDesktopRecentEventsWidth\(\)\{''',
    '''function syncDesktopRecentEventsWidth(){
  var events = $("cb-recent-events-desktop");
  var profile = document.querySelector(".cb-profile-entry-card");
  var actions = document.querySelector(".cb-hero-actions");
  if(!events || !actions) return;

  var desktop = !window.matchMedia || window.matchMedia("(min-width: 901px)").matches;
  if(!desktop){
    events.style.removeProperty("--cb-events-desktop-width");
    if(profile) profile.style.removeProperty("--cb-events-desktop-width");
    return;
  }

  var buttons = actions.querySelectorAll(".cb-link-button");
  if(!buttons.length) return;

  var left = Infinity;
  var right = -Infinity;
  Array.prototype.forEach.call(buttons, function(button){
    var rect = button.getBoundingClientRect();
    left = Math.min(left, rect.left);
    right = Math.max(right, rect.right);
  });

  var width = Math.ceil(right - left);
  if(width > 0){
    var value = Math.min(width, actions.clientWidth) + "px";
    events.style.setProperty("--cb-events-desktop-width", value);
    if(profile) profile.style.setProperty("--cb-events-desktop-width", value);
  }
}

function setupDesktopRecentEventsWidth(){''',
    "синхронизация ширины событий и входа в мини-ЛК",
)

placement_anchor = '''function setupDesktopRecentEventsWidth(){
  syncDesktopRecentEventsWidth();
  window.addEventListener("resize", function(){
    window.requestAnimationFrame(syncDesktopRecentEventsWidth);
  }, {passive: true});

  if(document.fonts && document.fonts.ready){
    document.fonts.ready.then(syncDesktopRecentEventsWidth).catch(function(){});
  }
}
'''
placement_addition = placement_anchor + '''
function placeCreatorProfileEntry(){
  var card = document.querySelector(".cb-profile-entry-card");
  var heroCopy = document.querySelector(".cb-hero-copy");
  var heroStats = document.querySelector(".cb-hero-stats");
  var desktopEvents = $("cb-recent-events-desktop");
  var leaders = document.querySelector(".cb-leaders-carousel");
  if(!card || !heroCopy || !heroStats || !desktopEvents || !leaders) return;

  var desktop = !window.matchMedia || window.matchMedia("(min-width: 901px)").matches;
  if(desktop){
    if(card.parentNode !== heroCopy || card.nextElementSibling !== desktopEvents){
      heroCopy.insertBefore(card, desktopEvents);
    }
    card.classList.add("is-desktop-placement");
  } else {
    if(card.parentNode !== heroStats || card.previousElementSibling !== leaders){
      heroStats.insertBefore(card, leaders.nextSibling);
    }
    card.classList.remove("is-desktop-placement");
  }
  syncDesktopRecentEventsWidth();
}

function setupCreatorProfilePlacement(){
  placeCreatorProfileEntry();
  window.addEventListener("resize", function(){
    window.requestAnimationFrame(placeCreatorProfileEntry);
  }, {passive: true});
}
'''
replace_once(placement_anchor, placement_addition, "адаптивное размещение входа в мини-ЛК")

replace_once(
    '''var PORTAL_UPDATES = [{
  date: "2026-07-22",
  text: "Обновлены мобильный календарь, блок обратной связи CREACLOUD и ежедневная сводка портала."
}];''',
    '''var PORTAL_UPDATES = [{
  date: "2026-07-24",
  text: "Уточнены мини-ЛК, пять свежих публикаций и персональная рекомендация при бронировании."
}, {
  date: "2026-07-22",
  text: "Обновлены мобильный календарь, блок обратной связи CREACLOUD и ежедневная сводка портала."
}];''',
    "обновление сводки портала",
)

unique_key_anchor = '''function getUniqueTourKey(v){
  var canonical = canonicalTourName(v);
  if(!canonical) return "";
  if(canonical === CANONICAL_TOURS[1] || canonical === CANONICAL_TOURS[8]) return "вечерняя программа";
  return normalizeTour(canonical);
}
'''
unique_hint_logic = unique_key_anchor + '''
var bookingUniqueSuggestion = null;

function hideBookingUniqueHint(){
  var hint = $("cb-booking-unique-hint");
  bookingUniqueSuggestion = null;
  if(!hint) return;
  hint.hidden = true;
  hint.open = false;
}

function findBookingUniqueAlternative(creator, date, selectedTour){
  var entry = findCreatorEntry(creator, getKnownCreatorDirectory());
  if(!entry || !date || !selectedTour || !isBookableDate(date)) return null;

  var selectedKey = getUniqueTourKey(selectedTour);
  if(!selectedKey) return null;
  var visited = getCreatorProfileUniqueSet(entry.name);
  if(!visited[selectedKey]) return null;

  var tours = getToursByDate(date);
  for(var i = 0; i < tours.length; i++){
    var tour = tours[i];
    var key = getUniqueTourKey(tour);
    if(!key || visited[key] || normalizeTour(tour) === normalizeTour(selectedTour) || hasBookingSlotConflict(date, tour)) continue;
    return {creator: entry.name, date: date, tour: canonicalTourName(tour), key: key};
  }
  return null;
}

function updateBookingUniqueHint(){
  var hint = $("cb-booking-unique-hint");
  var copy = $("cb-booking-unique-copy");
  var action = $("cb-booking-unique-action");
  var input = $("cb-telegram");
  var select = $("cb-tour");
  var mode = $("cb-booking-mode");
  if(!hint || !copy || !action || !input || !select){
    bookingUniqueSuggestion = null;
    return;
  }

  if(mode && mode.value !== "new"){
    hideBookingUniqueHint();
    return;
  }

  var suggestion = findBookingUniqueAlternative(input.value, getFormDate(), select.value);
  if(!suggestion){
    hideBookingUniqueHint();
    return;
  }

  bookingUniqueSuggestion = suggestion;
  copy.innerHTML = 'Вы уже выбирали <strong>' + escapeHtml(canonicalTourName(select.value)) + '</strong>. На эту же дату свободна новая для вас программа: <strong>' + escapeHtml(suggestion.tour) + '</strong>.';
  action.textContent = "Выбрать рекомендованный тур";
  hint.hidden = false;
  hint.open = true;
}

function selectBookingUniqueSuggestion(){
  var suggestion = bookingUniqueSuggestion;
  var select = $("cb-tour");
  if(!suggestion || !select || normalizeDate(suggestion.date) !== getFormDate()){
    updateBookingUniqueHint();
    return;
  }

  var selected = false;
  Array.prototype.some.call(select.options, function(option){
    if(!option.disabled && normalizeTour(option.value) === normalizeTour(suggestion.tour)){
      select.value = option.value;
      selected = true;
      return true;
    }
    return false;
  });

  if(!selected){
    updateBookingUniqueHint();
    setMessage("Рекомендованный тур уже недоступен. Выберите другое свободное окно.", true);
    return;
  }

  hideBookingUniqueHint();
  setMessage("Выбран новый для вашего профиля тур: <b>" + escapeHtml(suggestion.tour) + "</b>.", false);
}
'''
replace_once(unique_key_anchor, unique_hint_logic, "логика персональной подсказки")

replace_regex(
    r'''function renderCreatorOptions\(\)\{.*?\n\}\n\nfunction setupCreatorIdentityInputs\(\)\{.*?\n\}\n\nfunction normalizeTour''',
    '''function renderCreatorOptions(){
  var bookingDirectory = getKnownCreatorDirectory();
  var reportTour = $("cb-report-tour") ? String($("cb-report-tour").value || "").trim() : "";
  var reportDirectory = getReportCreatorDirectory(reportTour);

  fillCreatorDatalist("cb-booking-creators", bookingDirectory);
  fillCreatorDatalist("cb-report-creators", reportDirectory);
  fillCreatorDatalist("cb-profile-creators", bookingDirectory);
  refreshCreatorProfileEntryState();
  setCreatorIdentityState("cb-telegram", "cb-booking-creator-state", bookingDirectory, "booking");
  setCreatorIdentityState("cb-report-telegram", "cb-report-creator-state", reportDirectory, "report");
  renderTransferOptions();
  updateBookingUniqueHint();
}

function setupCreatorIdentityInputs(){
  var bookingInput = $("cb-telegram");
  var bookingTour = $("cb-tour");
  var reportInput = $("cb-report-telegram");
  var reportTour = $("cb-report-tour");

  function updateBookingIdentity(){
    var directory = getKnownCreatorDirectory();
    setCreatorIdentityState("cb-telegram", "cb-booking-creator-state", directory, "booking");
    renderTransferOptions();
    updateBookingUniqueHint();
  }

  function updateReportIdentity(){
    var tour = reportTour ? String(reportTour.value || "").trim() : "";
    var directory = getReportCreatorDirectory(tour);
    fillCreatorDatalist("cb-report-creators", directory);
    setCreatorIdentityState("cb-report-telegram", "cb-report-creator-state", directory, "report");
  }

  if(bookingInput){
    bookingInput.addEventListener("input", updateBookingIdentity);
    bookingInput.addEventListener("change", function(){
      var entry = setCreatorIdentityState("cb-telegram", "cb-booking-creator-state", getKnownCreatorDirectory(), "booking");
      if(entry) bookingInput.value = entry.name;
      renderTransferOptions();
      updateBookingUniqueHint();
    });
  }

  if(bookingTour) bookingTour.addEventListener("change", updateBookingUniqueHint);

  if(reportInput){
    reportInput.addEventListener("input", updateReportIdentity);
    reportInput.addEventListener("change", function(){
      var tour = reportTour ? String(reportTour.value || "").trim() : "";
      var entry = setCreatorIdentityState("cb-report-telegram", "cb-report-creator-state", getReportCreatorDirectory(tour), "report");
      if(entry) reportInput.value = entry.name;
    });
  }

  if(reportTour) reportTour.addEventListener("change", updateReportIdentity);
  var bookingMode = $("cb-booking-mode");
  if(bookingMode) bookingMode.addEventListener("change", function(){
    renderTransferOptions();
    updateBookingUniqueHint();
  });
  var bookingHintAction = $("cb-booking-unique-action");
  if(bookingHintAction) bookingHintAction.addEventListener("click", selectBookingUniqueSuggestion);
  renderCreatorOptions();
}

function normalizeTour''',
    "обновление обработчиков формы",
)

replace_once(
    '''  appendGroup("Туры по календарю", scheduledTours);
}
''',
    '''  appendGroup("Туры по календарю", scheduledTours);
  updateBookingUniqueHint();
}
''',
    "обновление подсказки после отрисовки туров",
)

replace_once(
    '''      renderTransferOptions();
      setMessage("Выбраны <b>" + formatDateRu(date) + "</b> и тур <b>" + escapeHtml(canonicalTourName(chosenTour)) + "</b>. Укажите ник креатора.", false);
''',
    '''      renderTransferOptions();
      updateBookingUniqueHint();
      setMessage("Выбраны <b>" + formatDateRu(date) + "</b> и тур <b>" + escapeHtml(canonicalTourName(chosenTour)) + "</b>. Укажите ник креатора.", false);
''',
    "подсказка после выбора тура из календаря",
)

replace_regex(
    r'''function renderCreatorStories\(\)\{.*?\n\}\n\nfunction renderCreatorStoryViewer''',
    '''function renderCreatorStories(){
  var track = $("cb-stories-track");
  var summaryTitle = $("cb-stories-summary-title");
  var summaryMeta = $("cb-stories-summary-meta");
  var prev = $("cb-stories-prev");
  var next = $("cb-stories-next");
  if(!track || !summaryTitle || !summaryMeta) return;

  creatorStoryItems = getPublishedContentItems().slice(0, 5);
  if(!creatorStoryItems.length){
    summaryTitle.innerHTML = "<strong>Свежих публикаций</strong> пока нет";
    summaryMeta.textContent = "Пока нет опубликованных материалов";
    track.innerHTML = '<div class="cb-stories-empty">Публикации появятся после добавления первой готовой работы.</div>';
    if(prev) prev.disabled = true;
    if(next) next.disabled = true;
    return;
  }

  var latest = creatorStoryItems[0];
  var count = creatorStoryItems.length;
  var freshness = count === 1 ? "свежая" : (count >= 2 && count <= 4 ? "свежие" : "свежих");
  summaryTitle.innerHTML = "<strong>" + count + " " + freshness + "</strong> " + pluralCount(count, "публикация", "публикации", "публикаций");
  summaryMeta.textContent = "Последняя: " + (getReportCreator(latest) || "креатор") + " · " + getContentPlatform(getReportLink(latest));

  var seen = readCreatorStorySeen();
  track.innerHTML = creatorStoryItems.map(function(report, index){
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

  Array.prototype.forEach.call(track.querySelectorAll(".cb-story-card"), function(card){
    card.onclick = function(){ openCreatorStory(Number(this.getAttribute("data-story-index")), this); };
  });
  if(prev) prev.disabled = creatorStoryItems.length < 2;
  if(next) next.disabled = creatorStoryItems.length < 2;
}

function renderCreatorStoryViewer''',
    "пять свежих публикаций",
)

replace_regex(
    r'''function renderCreatorProfile\(\)\{.*?\n\}\n\nfunction selectCreatorProfileTourOption''',
    '''function renderCreatorProfile(){
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
  var remainingUnique = Math.max(0, TOTAL_UNIQUE_TOURS - data.uniqueCount);
  currentCreatorProfileRecommendation = data.recommendation;
  section.hidden = false;

  dashboard.innerHTML = '<div class="cb-profile-overview"><div class="cb-profile-overview-copy"><small>Профиль сезона</small><h3>' + escapeHtml(data.creator) + '</h3><p>' + data.bookings.length + ' ' + pluralCount(data.bookings.length, "поездка", "поездки", "поездок") + ' в учёте · ' + data.reports.length + ' ' + pluralCount(data.reports.length, "публикация", "публикации", "публикаций") + '.</p></div><div class="cb-profile-overview-score"><strong>' + data.uniqueCount + '</strong><small>/ ' + TOTAL_UNIQUE_TOURS + '</small></div></div>' +
    '<div class="cb-profile-metrics is-compact"><div class="cb-profile-metric"><strong>' + data.uniqueCount + '/' + TOTAL_UNIQUE_TOURS + '</strong><span>Уникальных туров посещено</span></div><div class="cb-profile-metric"><strong>' + remainingUnique + '</strong><span>Уникальных туров ещё не посещено</span></div></div>' +
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

function selectCreatorProfileTourOption''',
    "упрощение мини-ЛК",
)

replace_once(
    '''  setupStickyNav();
  setupDesktopRecentEventsWidth();
  setupLeadersCarousel();
''',
    '''  setupStickyNav();
  setupCreatorProfilePlacement();
  setupDesktopRecentEventsWidth();
  setupLeadersCarousel();
''',
    "инициализация размещения мини-ЛК",
)

replace_once(
    '''      renderCalendar();
      renderDetails(this.value);
      if(this.value) setMessage("Выбрано: <b>" + formatDateRu(this.value) + "</b>. Теперь выберите тур.", false);
''',
    '''      renderCalendar();
      renderDetails(this.value);
      updateBookingUniqueHint();
      if(this.value) setMessage("Выбрано: <b>" + formatDateRu(this.value) + "</b>. Теперь выберите тур.", false);
''',
    "подсказка после смены даты",
)

# Контрольные проверки до записи.
assert text.count('id="cb-profile-entry-input"') == 1
assert text.count('id="creator-profile"') == 1
assert text.index('id="creator-profile"') > text.index('id="results"')
assert text.index('id="creator-profile"') < text.index('id="creacloud"')
assert 'slice(0, 5)' in text
assert 'slice(0, 10)' not in text
assert 'cb-booking-unique-hint' in text
assert 'findBookingUniqueAlternative' in text
assert 'setupCreatorProfilePlacement' in text
assert 'cb-profile-view-works' not in re.search(r'function renderCreatorProfile\(\)\{.*?\n\}', text, re.S).group(0)
assert 'cb-profile-change' not in re.search(r'function renderCreatorProfile\(\)\{.*?\n\}', text, re.S).group(0)
assert 'window.visualViewport' not in text
assert 'document.body.style.position' not in text
assert 'body.cb-push-open' not in text

path.write_text(text, encoding="utf-8")
print("Патч интерфейса профиля применён")
