#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    text = text.replace(old, new, 1)


font_anchor = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">\n<style>'
font_replacement = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">\n<script src="creacloud-design.js"></script>\n<link rel="stylesheet" href="creacloud-redesign.css">\n<style>'
replace_once(font_anchor, font_replacement, "theme assets")

old_splash = '''<div id="cb-splash" class="cb-splash" role="status" aria-live="polite">
  <div class="cb-splash-inner">
    <div id="cb-loader-ring" class="cb-splash-mark"><span id="cb-loader-status" class="cb-splash-percent">0%</span></div>
    <div class="cb-splash-title">Творческая мастерская <strong>«Корсар»</strong></div>
    <div id="cb-loader-text" class="cb-splash-copy">Загружаем расписание...</div>
  </div>
</div>'''
new_splash = '''<div id="cb-splash" class="cb-splash" role="status" aria-live="polite">
  <div class="cb-splash-inner cb-splash-legacy">
    <div id="cb-loader-ring" class="cb-splash-mark"><span id="cb-loader-status" class="cb-splash-percent">0%</span></div>
    <div class="cb-splash-title">Творческая мастерская <strong>«Корсар»</strong></div>
    <div id="cb-loader-text" class="cb-splash-copy">Загружаем расписание...</div>
  </div>
  <div class="cb-splash-redesign">
    <div class="cb-splash-logo" aria-label="CREACLOUD">
      <strong class="cb-splash-logo-crea" aria-hidden="true">CREA</strong><span class="cb-splash-logo-cloud" aria-hidden="true">CLOUD</span>
    </div>
    <div class="cb-splash-subtitle">креаторская студия «Корсар»</div>
    <div class="cb-splash-pulse" aria-hidden="true"></div>
    <div class="cb-splash-phrase-frame"><span id="cb-loader-phrase" class="cb-splash-phrase">собираем креаторов</span></div>
    <span id="cb-loader-redesign-status" class="cb-visually-hidden">Загрузка сайта, 0%</span>
  </div>
</div>'''
replace_once(old_splash, new_splash, "splash markup")

old_loader = '''var loaderTimer = null;

function setLoader(percent, text, state){
  var card = $("cb-splash");
  var ring = $("cb-loader-ring");
  var status = $("cb-loader-status");
  var label = $("cb-loader-text");

  if(!card || !ring || !status || !label) return;

  var p = Math.max(0, Math.min(100, percent || 0));
  ring.style.setProperty("--progress", p);
  label.textContent = text || "Загружаем расписание...";
  status.textContent = p + "%";

  if(state === "success"){
    status.textContent = "✓";
  } else if(state === "error"){
    status.textContent = "!";
  }
}

function startLoader(){
  if(loaderTimer) clearInterval(loaderTimer);

  var p = 0;
  setLoader(0, "Загружаем расписание...", "");

  loaderTimer = setInterval(function(){
    p += p < 55 ? 7 : 3;
    if(p >= 92) p = 92;
    setLoader(p, p < 55 ? "Загружаем расписание..." : "Собираем рейтинг креаторов...", "");
  }, 145);
}

function finishLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Всё готово", "success");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
  }, 520);
}

function failLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Расписание временно недоступно", "error");
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
  }, 1100);
}'''
new_loader = '''var loaderTimer = null;

function getDesignTheme(){
  return window.CREACLOUD_THEME || null;
}

function setLoader(percent, text, state){
  var p = Math.max(0, Math.min(100, percent || 0));
  var theme = getDesignTheme();
  if(theme && typeof theme.updateSplash === "function") theme.updateSplash(p, text, state);

  var card = $("cb-splash");
  var ring = $("cb-loader-ring");
  var status = $("cb-loader-status");
  var label = $("cb-loader-text");

  if(!card || !ring || !status || !label) return;

  ring.style.setProperty("--progress", p);
  label.textContent = text || "Загружаем расписание...";
  status.textContent = p + "%";

  if(state === "success"){
    status.textContent = "✓";
  } else if(state === "error"){
    status.textContent = "!";
  }
}

function startLoader(){
  if(loaderTimer) clearInterval(loaderTimer);
  var theme = getDesignTheme();
  if(theme && typeof theme.startSplash === "function") theme.startSplash();

  var p = 0;
  setLoader(0, "Загружаем расписание...", "");

  loaderTimer = setInterval(function(){
    p += p < 55 ? 7 : 3;
    if(p >= 92) p = 92;
    setLoader(p, p < 55 ? "Загружаем расписание..." : "Собираем рейтинг креаторов...", "");
  }, 145);
}

function finishLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Всё готово", "success");
  var theme = getDesignTheme();
  if(theme && typeof theme.finishSplash === "function") theme.finishSplash(true);
  var delay = theme && typeof theme.getHideDelay === "function" ? theme.getHideDelay(true) : 520;
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
  }, delay);
}

function failLoader(text){
  if(loaderTimer) clearInterval(loaderTimer);
  setLoader(100, text || "Расписание временно недоступно", "error");
  var theme = getDesignTheme();
  if(theme && typeof theme.finishSplash === "function") theme.finishSplash(false);
  var delay = theme && typeof theme.getHideDelay === "function" ? theme.getHideDelay(false) : 1100;
  setTimeout(function(){
    var splash = $("cb-splash");
    if(splash) splash.classList.add("is-hidden");
    document.body.classList.remove("cb-lock-scroll");
  }, delay);
}'''
replace_once(old_loader, new_loader, "loader lifecycle")

path.write_text(text, encoding="utf-8")
print("CREACLOUD redesign integration applied")
