#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


replace_once(
'''  --cb-mint: #dff6ec;
  --cb-line: #e3e5eb;
}''',
'''  --cb-mint: #dff6ec;
  --cb-line: #e3e5eb;
  --cb-visual-center-y: 50svh;
  --cb-visual-bottom-gap: 0px;
}''',
"переменные visual viewport",
)

replace_once(
'''.cb-splash-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}''',
'''.cb-splash-inner {
  position: fixed;
  z-index: 1;
  top: var(--cb-visual-center-y, 50svh);
  left: 50%;
  display: flex;
  width: min(680px, calc(100vw - 48px));
  flex-direction: column;
  align-items: center;
  text-align: center;
  transform: translate(-50%, -50%);
}''',
"центрирование загрузчика",
)

replace_once(
'''.cb-recent-events {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .07);
  background: rgba(255, 255, 255, .38);
  color: var(--cb-ink);
  box-shadow: 0 10px 26px rgba(68, 78, 102, .045);
  backdrop-filter: blur(12px) saturate(112%);
  -webkit-backdrop-filter: blur(12px) saturate(112%);
}''',
'''.cb-recent-events {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(23, 23, 25, .07);
  background: linear-gradient(112deg, rgba(250, 250, 252, .72), rgba(221, 225, 232, .46) 58%, rgba(255, 255, 255, .56));
  color: var(--cb-ink);
  box-shadow: 0 10px 26px rgba(68, 78, 102, .045);
  backdrop-filter: blur(12px) saturate(108%);
  -webkit-backdrop-filter: blur(12px) saturate(108%);
}''',
"серый прозрачный градиент событий",
)

replace_once(
'''.cb-recent-events-desktop {
  max-width: 680px;
  margin: 18px 0 0;
}

.cb-recent-events-mobile {
  display: none;
}''',
'''.cb-recent-events-desktop {
  z-index: 12;
  max-width: 680px;
  margin: auto 0 0;
  overflow: visible;
}

.cb-recent-events-mobile {
  display: none;
}

@media (min-width: 901px) {
  .cb-hero-actions {
    margin-top: 10px;
  }

  .cb-recent-events-desktop .cb-activity-head {
    position: relative;
    z-index: 2;
    background: linear-gradient(112deg, rgba(250, 250, 252, .82), rgba(221, 225, 232, .56) 58%, rgba(255, 255, 255, .68));
    backdrop-filter: blur(14px) saturate(105%);
    -webkit-backdrop-filter: blur(14px) saturate(105%);
  }

  .cb-recent-events-desktop .cb-activity-panel {
    position: absolute;
    z-index: 1;
    right: -1px;
    bottom: calc(100% + 7px);
    left: -1px;
    max-height: 270px;
    overflow: auto;
    padding: 8px 12px 7px 15px;
    border: 1px solid rgba(23, 23, 25, .08);
    background: linear-gradient(145deg, rgba(250, 250, 252, .96), rgba(226, 230, 237, .91) 58%, rgba(255, 255, 255, .94));
    box-shadow: 0 -16px 38px rgba(52, 58, 72, .12);
    backdrop-filter: blur(18px) saturate(108%);
    -webkit-backdrop-filter: blur(18px) saturate(108%);
  }
}''',
"положение и раскрытие событий на десктопе",
)

replace_once(
'''@media (max-width: 600px) {
  .cb-topbar {''',
'''@media (max-width: 600px) {
  .cb-message {
    right: auto;
    bottom: calc(var(--cb-visual-bottom-gap, 0px) + 14px);
    left: 14px;
    width: auto;
    max-width: min(300px, calc(100vw - 28px));
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.42;
    transform: translate(-8px, 10px);
  }

  .cb-message.is-visible {
    transform: translate(0, 0);
  }

  .cb-topbar {''',
"нижний левый toast на смартфоне",
)

replace_once(
'''function $(id){ return document.getElementById(id); }
function pad(n){ return String(n).padStart(2,"0"); }
function makeDate(y,m,d){ return y + "-" + pad(m+1) + "-" + pad(d); }

function setupStickyNav(){''',
'''function $(id){ return document.getElementById(id); }
function pad(n){ return String(n).padStart(2,"0"); }
function makeDate(y,m,d){ return y + "-" + pad(m+1) + "-" + pad(d); }

function syncVisualViewportMetrics(){
  var viewport = window.visualViewport;
  var height = viewport && Number.isFinite(viewport.height) ? viewport.height : window.innerHeight;
  var offsetTop = viewport && Number.isFinite(viewport.offsetTop) ? viewport.offsetTop : 0;
  var layoutHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  var centerY = Math.max(0, offsetTop + height / 2);
  var bottomGap = Math.max(0, layoutHeight - offsetTop - height);

  document.documentElement.style.setProperty("--cb-visual-center-y", Math.round(centerY) + "px");
  document.documentElement.style.setProperty("--cb-visual-bottom-gap", Math.round(bottomGap) + "px");
}

function setupVisualViewportMetrics(){
  syncVisualViewportMetrics();
  window.addEventListener("resize", syncVisualViewportMetrics, {passive: true});
  window.addEventListener("orientationchange", function(){
    setTimeout(syncVisualViewportMetrics, 80);
  }, {passive: true});

  if(window.visualViewport){
    window.visualViewport.addEventListener("resize", syncVisualViewportMetrics, {passive: true});
    window.visualViewport.addEventListener("scroll", syncVisualViewportMetrics, {passive: true});
  }
}

function setupStickyNav(){''',
"расчёт видимой области Safari",
)

replace_once(
'''function init(){
  if(!$("corsar-blogger-booking")) return;

  updateSeasonCounter();''',
'''function init(){
  if(!$("corsar-blogger-booking")) return;

  setupVisualViewportMetrics();
  updateSeasonCounter();''',
"запуск visual viewport",
)

if text == original:
    raise RuntimeError("изменения не применились")

path.write_text(text, encoding="utf-8")
print("patch applied")
