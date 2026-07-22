#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

if "function focusContentForm()" in text and ">Добавить контент <span aria-hidden=\"true\">↓</span></span>" in text:
    print("Патч уже применён")
    raise SystemExit(0)

replacements = [
    (
        '''.cb-leader-name {
  overflow: hidden;
  font-size: clamp(20px, 2.45vw, 34px);
  text-overflow: ellipsis;
  white-space: nowrap;
}''',
        '''.cb-leader-name {
  overflow: hidden;
  padding-bottom: .12em;
  font-size: clamp(20px, 2.45vw, 34px);
  line-height: 1.12;
  text-overflow: ellipsis;
  white-space: nowrap;
}'''
    ),
    (
        '''<span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>''',
        '''<span id="cb-content-leader-action" class="cb-leader-action" hidden>Добавить контент <span aria-hidden="true">↓</span></span>'''
    ),
    (
        '''function focusTourSchedule(){
  var calendar = $("calendar");
  if(window.location.hash !== "#calendar") window.location.hash = "calendar";
  if(calendar) calendar.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderUniqueTourLeader(ranking){''',
        '''function focusTourSchedule(){
  var calendar = $("calendar");
  if(window.location.hash !== "#calendar") window.location.hash = "calendar";
  if(calendar) calendar.scrollIntoView({behavior: "smooth", block: "start"});
}

function focusContentForm(){
  var content = $("content");
  if(window.location.hash !== "#content") window.location.hash = "content";
  if(content) content.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderUniqueTourLeader(ranking){'''
    ),
    (
        '''    leaderCard.setAttribute("data-creator", ranking[0].name);
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Показать опубликованные работы лидера по контенту " + ranking[0].name);
    leaderCard.onclick = function(){
      focusCreatorResults(this.getAttribute("data-creator"));
    };
    if(leaderAction) leaderAction.hidden = false;''',
        '''    leaderCard.removeAttribute("data-creator");
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Добавить контент и участвовать в рейтинге. Текущий лидер " + ranking[0].name);
    leaderCard.onclick = focusContentForm;
    if(leaderAction) leaderAction.hidden = false;'''
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Ожидалось одно совпадение, найдено {count}: {old[:80]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Патч применён")
