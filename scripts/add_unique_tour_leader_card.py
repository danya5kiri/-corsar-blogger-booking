#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = []

old_css = '''.cb-leaders-track .cb-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.68), transparent 34%),
    linear-gradient(135deg, #ffd66b 0%, #ffb09e 38%, #cbbdff 70%, #8ce8f4 100%);
  color: var(--cb-ink);
}
'''
new_css = '''.cb-leaders-track .cb-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.68), transparent 34%),
    linear-gradient(135deg, #ffd66b 0%, #ffb09e 38%, #cbbdff 70%, #8ce8f4 100%);
  color: var(--cb-ink);
}

.cb-leaders-track .cb-content-leader-card {
  background:
    radial-gradient(circle at 88% 10%, rgba(255,255,255,.72), transparent 35%),
    linear-gradient(135deg, #f8d5e7 0%, #e6d8ff 42%, #ffb9bf 72%, #ffd7a4 100%);
}

.cb-leaders-track .cb-unique-leader-card {
  background:
    radial-gradient(circle at 88% 10%, rgba(255,255,255,.72), transparent 35%),
    linear-gradient(135deg, #dff6ec 0%, #bceef1 38%, #9fd4ff 70%, #ded4ff 100%);
}
'''
replacements.append((old_css, new_css, "градиенты карточек"))

old_html = '''            <button type="button" id="cb-content-leader-card" class="cb-stat-card cb-leader-card cb-content-leader-card" aria-disabled="true" aria-label="Лидер по опубликованному контенту">
              <div class="cb-stat-label">Лидер по опубликованному контенту</div>
              <div id="cb-content-leader-name" class="cb-leader-name">—</div>
              <div id="cb-content-leader-count" class="cb-leader-visits">Загружаем публикации...</div>
              <span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>
            </button>
          </div>
'''
new_html = '''            <button type="button" id="cb-content-leader-card" class="cb-stat-card cb-leader-card cb-content-leader-card" aria-disabled="true" aria-label="Лидер по опубликованному контенту">
              <div class="cb-stat-label">Лидер по опубликованному контенту</div>
              <div id="cb-content-leader-name" class="cb-leader-name">—</div>
              <div id="cb-content-leader-count" class="cb-leader-visits">Загружаем публикации...</div>
              <span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>
            </button>
            <button type="button" id="cb-unique-leader-card" class="cb-stat-card cb-leader-card cb-unique-leader-card" aria-disabled="true" aria-label="Лидер по количеству уникальных туров">
              <div class="cb-stat-label">Лидер по количеству уникальных туров</div>
              <div id="cb-unique-leader-name" class="cb-leader-name">—</div>
              <div id="cb-unique-leader-count" class="cb-leader-visits">Загружаем охват программ...</div>
              <span id="cb-unique-leader-action" class="cb-leader-action" hidden>Смотреть расписание <span aria-hidden="true">↓</span></span>
            </button>
          </div>
'''
replacements.append((old_html, new_html, "третья карточка"))

old_labels = 'var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту"];'
new_labels = 'var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту", "По уникальным турам"];'
replacements.append((old_labels, new_labels, "подписи карусели"))

old_helpers = '''function renderTourVarietyStars(uniqueTours){
  var total = TOTAL_UNIQUE_TOURS;
  var filled = Math.max(0, Math.min(total, Number(uniqueTours) || 0));
  var stars = "";
  for(var i = 0; i < total; i++){
    stars += '<span class="cb-rank-coverage-star' + (i < filled ? ' is-filled' : '') + '" aria-hidden="true">★</span>';
  }
  return stars;
}

function renderAnalytics(){
'''
new_helpers = '''function renderTourVarietyStars(uniqueTours){
  var total = TOTAL_UNIQUE_TOURS;
  var filled = Math.max(0, Math.min(total, Number(uniqueTours) || 0));
  var stars = "";
  for(var i = 0; i < total; i++){
    stars += '<span class="cb-rank-coverage-star' + (i < filled ? ' is-filled' : '') + '" aria-hidden="true">★</span>';
  }
  return stars;
}

function focusTourSchedule(){
  var calendar = $("calendar");
  if(window.location.hash !== "#calendar") window.location.hash = "calendar";
  if(calendar) calendar.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderUniqueTourLeader(ranking){
  var leaderName = $("cb-unique-leader-name");
  var leaderCount = $("cb-unique-leader-count");
  var leaderCard = $("cb-unique-leader-card");
  var leaderAction = $("cb-unique-leader-action");
  if(!leaderName || !leaderCount || !leaderCard) return;

  var candidates = (Array.isArray(ranking) ? ranking : []).filter(function(item){
    return Number(item.uniqueTours) > 0;
  }).slice().sort(function(a, b){
    return b.uniqueTours - a.uniqueTours || b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  if(candidates.length){
    var leader = candidates[0];
    leaderName.textContent = leader.name;
    leaderCount.textContent = leader.uniqueTours + " " + pluralCount(leader.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") +
      " из " + TOTAL_UNIQUE_TOURS + " · " + leader.visits + " " + pluralCount(leader.visits, "поездка", "поездки", "поездок");
    leaderCard.setAttribute("data-creator", leader.name);
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Открыть расписание. Лидер по уникальным турам " + leader.name);
    leaderCard.onclick = focusTourSchedule;
    if(leaderAction) leaderAction.hidden = false;
  } else {
    leaderName.textContent = "Пока нет";
    leaderCount.textContent = "Первая уникальная программа определит лидера";
    leaderCard.removeAttribute("data-creator");
    leaderCard.setAttribute("aria-disabled", "true");
    leaderCard.setAttribute("aria-label", "Лидер по уникальным турам пока не определён");
    leaderCard.onclick = null;
    if(leaderAction) leaderAction.hidden = true;
  }
}

function renderAnalytics(){
'''
replacements.append((old_helpers, new_helpers, "логика лидера по уникальным турам"))

old_call = '''    if(leaderAction) leaderAction.hidden = true;
  }

  if(!ranking.length){
'''
new_call = '''    if(leaderAction) leaderAction.hidden = true;
  }

  renderUniqueTourLeader(ranking);

  if(!ranking.length){
'''
replacements.append((old_call, new_call, "обновление третьей карточки"))

for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось одно совпадение, найдено {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Третья карточка лидера добавлена")
