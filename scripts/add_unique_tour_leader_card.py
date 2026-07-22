#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось одно совпадение, найдено {count}")
    text = text.replace(old, new, 1)


replace_once(
''' .cb-leaders-track .cb-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.68), transparent 34%),
    linear-gradient(135deg, #ffd66b 0%, #ffb09e 38%, #cbbdff 70%, #8ce8f4 100%);
  color: var(--cb-ink);
}
'''.lstrip(),
''' .cb-leaders-track .cb-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.68), transparent 34%),
    linear-gradient(135deg, #ffd66b 0%, #ffb09e 38%, #cbbdff 70%, #8ce8f4 100%);
  color: var(--cb-ink);
}

.cb-leaders-track .cb-content-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.72), transparent 34%),
    linear-gradient(135deg, #f2dcff 0%, #d5c8ff 36%, #f4b7d4 68%, #bcecf6 100%);
}

.cb-leaders-track .cb-unique-leader-card {
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.72), transparent 34%),
    linear-gradient(135deg, #dff6ec 0%, #bcebd8 34%, #9edfec 67%, #d9ceff 100%);
}
'''.lstrip(),
"градиенты карточек лидеров",
)

replace_once(
'''            <button type="button" id="cb-content-leader-card" class="cb-stat-card cb-leader-card cb-content-leader-card" aria-disabled="true" aria-label="Лидер по опубликованному контенту">
              <div class="cb-stat-label">Лидер по опубликованному контенту</div>
              <div id="cb-content-leader-name" class="cb-leader-name">—</div>
              <div id="cb-content-leader-count" class="cb-leader-visits">Загружаем публикации...</div>
              <span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>
            </button>
''',
'''            <button type="button" id="cb-content-leader-card" class="cb-stat-card cb-leader-card cb-content-leader-card" aria-disabled="true" aria-label="Лидер по опубликованному контенту">
              <div class="cb-stat-label">Лидер по опубликованному контенту</div>
              <div id="cb-content-leader-name" class="cb-leader-name">—</div>
              <div id="cb-content-leader-count" class="cb-leader-visits">Загружаем публикации...</div>
              <span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>
            </button>
            <button type="button" id="cb-unique-leader-card" class="cb-stat-card cb-leader-card cb-unique-leader-card" aria-disabled="true" aria-label="Лидер по количеству уникальных туров">
              <div class="cb-stat-label">Лидер по количеству уникальных туров</div>
              <div id="cb-unique-leader-name" class="cb-leader-name">—</div>
              <div id="cb-unique-leader-count" class="cb-leader-visits">Считаем уникальные туры...</div>
              <span id="cb-unique-leader-action" class="cb-leader-action" hidden>Смотреть расписание <span aria-hidden="true">↓</span></span>
            </button>
''',
"третья карточка лидера",
)

replace_once(
'var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту"];',
'var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту", "По уникальным турам"];',
"подписи карусели лидеров",
)

replace_once(
'''function escapeHtml(v){
''',
'''function focusTourSchedule(){
  var calendar = $("calendar");
  if(!calendar) return;
  calendar.scrollIntoView({behavior: "smooth", block: "start"});
  try { history.replaceState(null, "", "#calendar"); } catch(e) {}
}

function escapeHtml(v){
''',
"переход к расписанию",
)

replace_once(
'''function renderAnalytics(){
''',
'''function renderUniqueTourLeader(ranking){
  var leaderName = $("cb-unique-leader-name");
  var leaderCount = $("cb-unique-leader-count");
  var leaderCard = $("cb-unique-leader-card");
  var leaderAction = $("cb-unique-leader-action");
  if(!leaderName || !leaderCount || !leaderCard) return;

  var uniqueRanking = (ranking || []).slice().sort(function(a, b){
    return b.uniqueTours - a.uniqueTours || b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });
  var leader = uniqueRanking[0];

  if(leader && leader.uniqueTours > 0){
    leaderName.textContent = leader.name;
    leaderCount.textContent = leader.uniqueTours + " " + pluralCount(leader.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") + " из " + TOTAL_UNIQUE_TOURS + " · первое место";
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Перейти к расписанию. Лидер по уникальным турам " + leader.name);
    leaderCard.onclick = focusTourSchedule;
    if(leaderAction) leaderAction.hidden = false;
  } else {
    leaderName.textContent = "Пока нет";
    leaderCount.textContent = "Первая уникальная программа определит лидера";
    leaderCard.setAttribute("aria-disabled", "true");
    leaderCard.setAttribute("aria-label", "Лидер по уникальным турам пока не определён");
    leaderCard.onclick = null;
    if(leaderAction) leaderAction.hidden = true;
  }
}

function renderAnalytics(){
''',
"расчёт лидера по уникальным турам",
)

replace_once(
'''  var ranking = Object.keys(users).map(function(tg){
    return {name: tg, visits: users[tg], uniqueTours: Math.min(getCreatorTourVariety(tg), TOTAL_UNIQUE_TOURS)};
  }).sort(function(a, b){
    return b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  var leaderName = $("cb-leader-name");
''',
'''  var ranking = Object.keys(users).map(function(tg){
    return {name: tg, visits: users[tg], uniqueTours: Math.min(getCreatorTourVariety(tg), TOTAL_UNIQUE_TOURS)};
  }).sort(function(a, b){
    return b.visits - a.visits || a.name.localeCompare(b.name, "ru");
  });

  renderUniqueTourLeader(ranking);

  var leaderName = $("cb-leader-name");
''',
"подключение третьего лидера",
)

path.write_text(text, encoding="utf-8")
