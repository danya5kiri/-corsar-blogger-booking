#!/usr/bin/env python3
from pathlib import Path
import re

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if text.count(old) != 1:
        raise SystemExit(f"{label}: ожидалось одно совпадение, найдено {text.count(old)}")
    text = text.replace(old, new, 1)


def regex_once(pattern: str, replacement: str, label: str) -> None:
    global text
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: ожидалось одно совпадение, найдено {count}")


recent_css = r'''\.cb-recent-events \{.*?\.cb-activity-empty \{.*?\n\}\n\n(?=\.cb-link-button \{)'''
recent_css_new = '''.cb-recent-events {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .07);
  background: rgba(255, 255, 255, .38);
  color: var(--cb-ink);
  box-shadow: 0 10px 26px rgba(68, 78, 102, .045);
  backdrop-filter: blur(12px) saturate(112%);
  -webkit-backdrop-filter: blur(12px) saturate(112%);
}

.cb-recent-events::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 2px;
  background: linear-gradient(180deg, var(--cb-mint), var(--cb-cyan), var(--cb-lilac-strong));
  opacity: .48;
}

.cb-recent-events-desktop {
  max-width: 680px;
  margin: 18px 0 0;
}

.cb-recent-events-mobile {
  display: none;
}

.cb-activity-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 24px;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  margin: 0;
  padding: 9px 12px 9px 15px;
  cursor: pointer;
  list-style: none;
  user-select: none;
}

.cb-activity-head::-webkit-details-marker {
  display: none;
}

.cb-activity-title {
  overflow: hidden;
  font-size: 10px;
  font-weight: 820;
  letter-spacing: .065em;
  text-overflow: ellipsis;
  text-transform: uppercase;
  white-space: nowrap;
}

.cb-activity-live {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #6f7974;
  font-size: 7.5px;
  font-weight: 780;
  letter-spacing: .075em;
  text-transform: uppercase;
  white-space: nowrap;
}

.cb-activity-live::before {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #76bca5;
  box-shadow: 0 0 0 3px rgba(118, 188, 165, .10);
}

.cb-activity-toggle {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  color: #747985;
  font-size: 17px;
  font-weight: 420;
  transition: transform .2s ease, color .2s ease;
}

.cb-recent-events[open] .cb-activity-toggle {
  color: var(--cb-ink);
  transform: rotate(45deg);
}

.cb-activity-panel {
  padding: 0 12px 7px 15px;
  border-top: 1px solid rgba(23, 23, 25, .055);
}

.cb-activity-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.cb-activity-item {
  display: grid;
  grid-template-columns: 7px minmax(0, 1fr) auto;
  align-items: start;
  gap: 8px;
  padding: 6px 0;
  border-top: 1px solid rgba(23, 23, 25, .055);
}

.cb-activity-item:first-child {
  border-top: 0;
}

.cb-activity-dot {
  width: 6px;
  height: 6px;
  margin-top: 4px;
  border-radius: 50%;
  background: var(--cb-cyan);
  opacity: .72;
}

.cb-activity-item.is-creator .cb-activity-dot {
  background: #55b995;
}

.cb-activity-item.is-content .cb-activity-dot {
  background: var(--cb-rose);
}

.cb-activity-item.is-leader .cb-activity-dot {
  background: var(--cb-yellow);
  box-shadow: 0 0 0 2px rgba(255, 214, 107, .16);
}

.cb-activity-copy {
  min-width: 0;
  color: #666b77;
  font-size: 9.5px;
  line-height: 1.36;
}

.cb-activity-copy strong {
  color: var(--cb-ink);
  font-weight: 800;
}

.cb-activity-time {
  padding-top: 1px;
  color: #8b8f99;
  font-size: 7.5px;
  font-weight: 700;
  line-height: 1.35;
  white-space: nowrap;
}

.cb-activity-empty {
  padding: 11px 0 5px;
  color: var(--cb-muted);
  font-size: 9.5px;
  line-height: 1.4;
}

'''
regex_once(recent_css, recent_css_new, "стили ленты событий")

result_tones = '''
.cb-creator-group.is-result-tone-1::before {
  background: linear-gradient(90deg, #ffd66b, #ffb09e, #ded4ff);
}

.cb-creator-group.is-result-tone-2::before {
  background: linear-gradient(90deg, #8ce8f4, #cbbdff, #4ecbed);
}

.cb-creator-group.is-result-tone-3::before {
  background: linear-gradient(90deg, #ffb09e, #f3eaff, #dff6ec);
}

.cb-creator-group.is-result-tone-4::before {
  background: linear-gradient(90deg, #dff6ec, #8ce8f4, #ded4ff);
}

.cb-creator-group.is-result-tone-5::before {
  background: linear-gradient(90deg, #ded4ff, #f6dff0, #fff1e7);
}

.cb-creator-group.is-result-top-1 .cb-creator-summary {
  background: linear-gradient(100deg, rgba(255, 226, 138, .58), rgba(255, 186, 167, .42), rgba(222, 212, 255, .45));
}

.cb-creator-group.is-result-top-2 .cb-creator-summary {
  background: linear-gradient(100deg, rgba(223, 247, 251, .66), rgba(216, 208, 255, .52), rgba(244, 237, 255, .48));
}

.cb-creator-group.is-result-top-3 .cb-creator-summary {
  background: linear-gradient(100deg, rgba(255, 226, 215, .62), rgba(243, 234, 255, .50), rgba(226, 248, 242, .52));
}

.cb-creator-group.is-result-tone-4 .cb-creator-summary {
  background: rgba(233, 248, 251, .46);
}

.cb-creator-group.is-result-tone-5 .cb-creator-summary {
  background: rgba(243, 239, 255, .48);
}

.cb-creator-group.is-result-top-1 .cb-creator-index,
.cb-creator-group.is-result-top-2 .cb-creator-index,
.cb-creator-group.is-result-top-3 .cb-creator-index {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(23, 23, 25, .12);
  background: rgba(255, 255, 255, .62);
  color: var(--cb-ink);
  font-weight: 840;
}

.cb-creator-group.is-result-top-1 .cb-creator-index {
  border-color: var(--cb-ink);
  background: var(--cb-ink);
  color: #fff;
}

'''
replace_once('.cb-creator-group[open] {', result_tones + '.cb-creator-group[open] {', "цветовые группы результатов")

replace_once(
'''        <div id="cb-recent-events-desktop" class="cb-recent-events cb-recent-events-desktop" aria-live="polite">
          <div class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span></div>
          <div class="cb-activity-empty">Загружаем последние события...</div>
        </div>''',
'''        <details id="cb-recent-events-desktop" class="cb-recent-events cb-recent-events-desktop">
          <summary class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span><span class="cb-activity-toggle" aria-hidden="true">+</span></summary>
          <div class="cb-activity-panel" aria-live="polite"><div class="cb-activity-empty">Загружаем последние события...</div></div>
        </details>''',
"desktop-блок событий",
)

replace_once(
'''        <div id="cb-recent-events-mobile" class="cb-recent-events cb-recent-events-mobile" aria-live="polite">
          <div class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span></div>
          <div class="cb-activity-empty">Загружаем последние события...</div>
        </div>''',
'''        <details id="cb-recent-events-mobile" class="cb-recent-events cb-recent-events-mobile">
          <summary class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">активность</span><span class="cb-activity-toggle" aria-hidden="true">+</span></summary>
          <div class="cb-activity-panel" aria-live="polite"><div class="cb-activity-empty">Загружаем последние события...</div></div>
        </details>''',
"mobile-блок событий",
)

replace_once(
'var resultsCreatorFilter = "";\nvar rankingExpanded = false;',
'var resultsCreatorFilter = "";\nvar resultsExpanded = false;\nvar rankingExpanded = false;',
"состояние списка результатов",
)

recent_function = r'''function renderRecentCreatorEvents\(\)\{.*?\n\}\n\n(?=function renderSeasonMetrics\(\))'''
recent_function_new = '''function renderRecentCreatorEvents(){
  var roots = [$("cb-recent-events-desktop"), $("cb-recent-events-mobile")].filter(Boolean);
  if(!roots.length) return;

  var events = creatorDirectoryReady ? buildRecentCreatorEvents() : [];
  var activityLabel = events.length
    ? events.length + " " + pluralCount(events.length, "событие", "события", "событий")
    : "активность";
  var body = '<summary class="cb-activity-head"><span class="cb-activity-title">Последние события креаторов</span><span class="cb-activity-live">' + escapeHtml(activityLabel) + '</span><span class="cb-activity-toggle" aria-hidden="true">+</span></summary><div class="cb-activity-panel" aria-live="polite">';

  if(!creatorDirectoryReady){
    body += '<div class="cb-activity-empty">Загружаем последние события...</div>';
  } else if(!events.length){
    body += '<div class="cb-activity-empty">События появятся после первой брони или публикации.</div>';
  } else {
    body += '<ol class="cb-activity-list">' + events.map(function(event){
      return '<li class="cb-activity-item is-' + escapeHtml(event.kind) + '">' +
        '<span class="cb-activity-dot" aria-hidden="true"></span>' +
        '<span class="cb-activity-copy">' + event.copy + '</span>' +
        '<time class="cb-activity-time">' + escapeHtml(event.time) + '</time>' +
      '</li>';
    }).join("") + '</ol>';
  }

  body += '</div>';
  roots.forEach(function(root){ root.innerHTML = body; });
}

'''
regex_once(recent_function, recent_function_new, "рендер сворачиваемой ленты")

results_function = r'''function renderResults\(\)\{.*?\n\}\n\n(?=function fetchRemoteRows\(timeoutMs\))'''
results_function_new = '''function renderResults(){
  var root = $("cb-results");
  if(!root) return;

  renderContentLeader();

  var select = $("cb-results-filter");
  var summary = $("cb-results-summary");

  var items = getPublishedContentItems();

  var groupsByCreator = {};
  items.forEach(function(report){
    var creator = getReportCreator(report);
    var key = creator || "__corsar_creator__";
    if(!groupsByCreator[key]){
      groupsByCreator[key] = {
        key: key,
        creator: creator || "участник «Корсар»",
        items: []
      };
    }
    groupsByCreator[key].items.push(report);
  });

  var groups = Object.keys(groupsByCreator).map(function(key){
    return groupsByCreator[key];
  }).sort(function(a, b){
    return b.items.length - a.items.length || a.creator.localeCompare(b.creator, "ru");
  });

  groups.forEach(function(group, index){
    group.rank = index + 1;
  });

  if(select){
    var options = '<option value="">Все креаторы</option>' + groups.map(function(group){
      return '<option value="' + escapeHtml(group.key) + '">' + escapeHtml(group.creator) + ' · ' + group.items.length + '</option>';
    }).join("");

    if(resultsCreatorFilter && !groupsByCreator[resultsCreatorFilter]){
      options += '<option value="' + escapeHtml(resultsCreatorFilter) + '">' + escapeHtml(resultsCreatorFilter) + ' · пока без работ</option>';
    }

    select.innerHTML = options;
    select.value = resultsCreatorFilter;
    select.onchange = function(){
      resultsCreatorFilter = this.value;
      resultsExpanded = false;
      renderResults();
    };
  }

  if(!items.length){
    if(summary) summary.textContent = "Опубликованных материалов пока нет";
    root.innerHTML = '<div class="cb-results-empty">Пока здесь нет опубликованных материалов.<br>Первое готовое видео появится сразу после отправки формы выше.</div>';
    return;
  }

  var visibleGroups = resultsCreatorFilter ? groups.filter(function(group){
    return group.key === resultsCreatorFilter;
  }) : groups;

  if(summary){
    var visibleMaterialCount = visibleGroups.reduce(function(total, group){ return total + group.items.length; }, 0);
    summary.textContent = visibleGroups.length + " " + pluralCount(visibleGroups.length, "креатор", "креатора", "креаторов") +
      " · " + visibleMaterialCount + " " + pluralCount(visibleMaterialCount, "материал", "материала", "материалов");
  }

  if(!visibleGroups.length){
    root.innerHTML = '<div class="cb-results-empty">У <b>' + escapeHtml(resultsCreatorFilter) + '</b> пока нет опубликованных работ.' +
      '<button type="button" id="cb-results-reset" class="cb-results-reset">Показать всех креаторов</button></div>';
    var reset = $("cb-results-reset");
    if(reset) reset.onclick = function(){
      resultsCreatorFilter = "";
      resultsExpanded = false;
      renderResults();
    };
    return;
  }

  var groupsToRender = resultsCreatorFilter || resultsExpanded ? visibleGroups : visibleGroups.slice(0, 5);
  var markup = groupsToRender.map(function(group){
    var materials = group.items.map(function(report, materialIndex){
      var link = getReportLink(report);
      var tour = getReportTour(report) || "Морское путешествие «Корсар»";
      var date = normalizeDate(report.date);
      var dateText = /^\\d{4}-\\d{2}-\\d{2}$/.test(date) ? formatDateRu(date) : "";
      var platform = getContentPlatform(link);

      return '<li class="cb-creator-material">' +
        '<a class="cb-material-link" href="' + escapeHtml(link) + '" target="_blank" rel="noopener noreferrer" aria-label="Открыть ' + escapeHtml(platform) + ': ' + escapeHtml(tour) + '">' +
          '<span class="cb-material-index">' + String(materialIndex + 1).padStart(2, "0") + '</span>' +
          '<span class="cb-material-copy">' +
            '<span class="cb-material-platform">' + escapeHtml(platform) + '</span>' +
            '<strong class="cb-material-tour">' + escapeHtml(tour) + '</strong>' +
          '</span>' +
          '<span class="cb-material-date">' + escapeHtml(dateText) + '</span>' +
          '<span class="cb-material-open">Открыть ↗</span>' +
        '</a>' +
      '</li>';
    }).join("");

    var tone = ((group.rank - 1) % 5) + 1;
    var topClass = group.rank <= 3 ? ' is-result-top-' + group.rank : '';
    return '<details id="' + getCreatorGroupId(group.key) + '" class="cb-creator-group is-result-tone-' + tone + topClass + '" data-creator="' + escapeHtml(group.key) + '">' +
      '<summary class="cb-creator-summary">' +
        '<span class="cb-creator-index">' + String(group.rank).padStart(2, "0") + '</span>' +
        '<span class="cb-creator-name">' + escapeHtml(group.creator) + '</span>' +
        '<span class="cb-creator-count">' + group.items.length + " " + pluralCount(group.items.length, "работа", "работы", "работ") + '</span>' +
        '<span class="cb-creator-chevron" aria-hidden="true">+</span>' +
      '</summary>' +
      '<ol class="cb-creator-materials">' + materials + '</ol>' +
    '</details>';
  }).join("");

  if(!resultsCreatorFilter && visibleGroups.length > 5){
    markup += '<button type="button" id="cb-results-toggle" class="cb-ranking-toggle cb-results-toggle" aria-expanded="' + (resultsExpanded ? 'true' : 'false') + '">' +
      (resultsExpanded ? 'Свернуть до 5 мест' : 'Показать все') +
    '</button>';
  }

  root.innerHTML = markup;

  var toggle = $("cb-results-toggle");
  if(toggle){
    toggle.onclick = function(){
      resultsExpanded = !resultsExpanded;
      renderResults();
    };
  }
}

'''
regex_once(results_function, results_function_new, "топ-5 результатов")

if text == original:
    raise SystemExit("Изменения не внесены")

PATH.write_text(text, encoding="utf-8")
print("Компактная лента и топ-5 результатов применены")
