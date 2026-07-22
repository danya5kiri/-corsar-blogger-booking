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


old_buttons = '''.cb-link-button-booking {
  border-color: transparent;
  background: linear-gradient(105deg, var(--cb-coral) 0%, #ffad58 52%, var(--cb-yellow) 100%);
  color: #fff;
  box-shadow: 0 12px 28px rgba(255, 143, 118, .24);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-booking:hover,
.cb-link-button-booking:focus-visible {
  border-color: transparent;
  color: #fff;
  filter: saturate(1.06) brightness(1.02);
  box-shadow: 0 16px 32px rgba(255, 143, 118, .30);
}

.cb-link-button-content {
  border-color: rgba(23, 23, 25, .16);
  background: #fff;
  color: var(--cb-ink);
  box-shadow: 0 12px 26px rgba(42, 45, 59, .10);
}

.cb-link-button-content:hover,
.cb-link-button-content:focus-visible {
  border-color: rgba(23, 23, 25, .28);
  background: #fff;
  color: var(--cb-ink);
  box-shadow: 0 16px 30px rgba(42, 45, 59, .15);
}

.cb-link-button-chat {
  border-color: transparent;
  background: linear-gradient(105deg, var(--cb-blue) 0%, var(--cb-cyan) 66%, #8ce8f4 100%);
  color: #fff;
  box-shadow: 0 12px 28px rgba(37, 88, 200, .22);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-chat:hover,
.cb-link-button-chat:focus-visible {
  border-color: transparent;
  color: #fff;
  filter: saturate(1.08) brightness(1.03);
  box-shadow: 0 16px 32px rgba(37, 88, 200, .28);
}
'''

new_buttons = '''.cb-link-button-booking {
  border-color: transparent;
  background:
    radial-gradient(circle at 88% 10%, rgba(255,255,255,.72), transparent 35%),
    linear-gradient(135deg, #f8d5e7 0%, #e6d8ff 42%, #ffb9bf 72%, #ffd7a4 100%);
  color: var(--cb-ink);
  box-shadow: 0 12px 28px rgba(178, 118, 170, .18);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-booking:hover,
.cb-link-button-booking:focus-visible {
  border-color: transparent;
  color: var(--cb-ink);
  filter: saturate(1.06) brightness(1.02);
  box-shadow: 0 16px 32px rgba(178, 118, 170, .25);
}

.cb-link-button-content {
  border-color: transparent;
  background:
    radial-gradient(circle at 88% 10%, rgba(255,255,255,.72), transparent 35%),
    linear-gradient(135deg, #dff6ec 0%, #bceef1 38%, #9fd4ff 70%, #ded4ff 100%);
  color: var(--cb-ink);
  box-shadow: 0 12px 28px rgba(77, 151, 181, .17);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-content:hover,
.cb-link-button-content:focus-visible {
  border-color: transparent;
  color: var(--cb-ink);
  filter: saturate(1.06) brightness(1.02);
  box-shadow: 0 16px 32px rgba(77, 151, 181, .24);
}

.cb-link-button-chat {
  border-color: transparent;
  background:
    radial-gradient(circle at 90% 8%, rgba(255,255,255,.68), transparent 34%),
    linear-gradient(135deg, #ffd66b 0%, #ffb09e 38%, #cbbdff 70%, #8ce8f4 100%);
  color: var(--cb-ink);
  box-shadow: 0 12px 28px rgba(127, 103, 248, .18);
  transition: transform .2s ease, background .2s ease, color .2s ease, box-shadow .2s ease, filter .2s ease;
}

.cb-link-button-chat:hover,
.cb-link-button-chat:focus-visible {
  border-color: transparent;
  color: var(--cb-ink);
  filter: saturate(1.06) brightness(1.02);
  box-shadow: 0 16px 32px rgba(127, 103, 248, .25);
}
'''
replace_once(old_buttons, new_buttons, "градиенты главных кнопок")

old_name_css = '''.cb-leader-card .cb-leader-name {
  flex: 0 0 auto;
  margin-top: 9px;
  font-size: clamp(19px, 2.15vw, 30px);
}
'''
new_name_css = '''.cb-leader-card .cb-leader-name {
  flex: 0 0 auto;
  min-height: 1.18em;
  margin-top: 9px;
  padding-bottom: .14em;
  box-sizing: content-box;
  font-size: clamp(19px, 2.15vw, 30px);
  line-height: 1.14;
}
'''
replace_once(old_name_css, new_name_css, "нижний запас ника лидера")

replace_once(
    '<span id="cb-content-leader-action" class="cb-leader-action" hidden>Смотреть работы <span aria-hidden="true">↓</span></span>',
    '<span id="cb-content-leader-action" class="cb-leader-action" hidden>Добавить контент <span aria-hidden="true">↓</span></span>',
    "текст действия контент-лидера",
)

old_focus = '''function focusTourSchedule(){
  var calendar = $("calendar");
  if(window.location.hash !== "#calendar") window.location.hash = "calendar";
  if(calendar) calendar.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderUniqueTourLeader(ranking){
'''
new_focus = '''function focusTourSchedule(){
  var calendar = $("calendar");
  if(window.location.hash !== "#calendar") window.location.hash = "calendar";
  if(calendar) calendar.scrollIntoView({behavior: "smooth", block: "start"});
}

function focusContentSubmission(){
  var content = $("content");
  if(window.location.hash !== "#content") window.location.hash = "content";
  if(content) content.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderUniqueTourLeader(ranking){
'''
replace_once(old_focus, new_focus, "переход к форме контента")

old_content_action = '''    leaderCard.setAttribute("data-creator", ranking[0].name);
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Показать опубликованные работы лидера по контенту " + ranking[0].name);
    leaderCard.onclick = function(){
      focusCreatorResults(this.getAttribute("data-creator"));
    };
    if(leaderAction) leaderAction.hidden = false;
'''
new_content_action = '''    leaderCard.setAttribute("data-creator", ranking[0].name);
    leaderCard.setAttribute("aria-disabled", "false");
    leaderCard.setAttribute("aria-label", "Добавить контент и участвовать в рейтинге. Текущий лидер " + ranking[0].name);
    leaderCard.onclick = focusContentSubmission;
    if(leaderAction) leaderAction.hidden = false;
'''
replace_once(old_content_action, new_content_action, "действие карточки контент-лидера")

replace_once(
    'var WEATHER_REFRESH_INTERVAL = 12 * 60 * 60 * 1000;',
    'var WEATHER_REFRESH_INTERVAL = 3 * 60 * 60 * 1000;',
    "интервал обновления погоды",
)

path.write_text(text, encoding="utf-8")
print("Патч применён")
