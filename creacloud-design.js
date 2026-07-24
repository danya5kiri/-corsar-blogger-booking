/* CREACLOUD visual mode.
 * Change only this value to switch the default interface:
 * "legacy"   — previous site design
 * "redesign" — refreshed CREACLOUD design
 */
window.CREACLOUD_DESIGN_MODE = "redesign";

(function(){
  "use strict";

  var allowed = {legacy: true, redesign: true};
  var requested = "";
  try {
    requested = new URLSearchParams(window.location.search).get("design") || "";
  } catch(e) {}

  var configured = allowed[window.CREACLOUD_DESIGN_MODE] ? window.CREACLOUD_DESIGN_MODE : "legacy";
  var mode = allowed[requested] ? requested : configured;
  document.documentElement.setAttribute("data-design", mode);

  var themeMeta = document.querySelector('meta[name="theme-color"]');
  if(themeMeta) themeMeta.setAttribute("content", mode === "redesign" ? "#151714" : "#171719");

  var phrases = [
    "собираем креаторов",
    "смотрим туры",
    "рейтингуем креаторов",
    "респектуем креаторам"
  ];
  var phraseIndex = 0;
  var phraseTimer = null;
  var phraseSwapTimer = null;

  function getPhraseElement(){
    return document.getElementById("cb-loader-phrase");
  }

  function setPhrase(value, immediate){
    var element = getPhraseElement();
    if(!element) return;
    if(phraseSwapTimer){
      clearTimeout(phraseSwapTimer);
      phraseSwapTimer = null;
    }
    if(immediate){
      element.classList.remove("is-changing");
      element.textContent = value;
      return;
    }
    element.classList.add("is-changing");
    phraseSwapTimer = setTimeout(function(){
      element.textContent = value;
      element.classList.remove("is-changing");
      phraseSwapTimer = null;
    }, 170);
  }

  function stopSplashCycle(){
    if(phraseTimer){
      clearInterval(phraseTimer);
      phraseTimer = null;
    }
    if(phraseSwapTimer){
      clearTimeout(phraseSwapTimer);
      phraseSwapTimer = null;
    }
  }

  function startSplash(){
    if(mode !== "redesign") return;
    stopSplashCycle();
    phraseIndex = 0;
    setPhrase(phrases[phraseIndex], true);
    phraseTimer = setInterval(function(){
      phraseIndex = (phraseIndex + 1) % phrases.length;
      setPhrase(phrases[phraseIndex], false);
    }, 1040);
  }

  function updateSplash(percent, text, state){
    var status = document.getElementById("cb-loader-redesign-status");
    if(!status) return;
    var value = Math.max(0, Math.min(100, Number(percent) || 0));
    status.textContent = (state === "error" ? "Ошибка загрузки. " : "") + (text || "Загрузка сайта") + ", " + value + "%";
  }

  function finishSplash(success){
    if(mode !== "redesign") return;
    stopSplashCycle();
    setPhrase(success ? "респектуем креаторам" : "проверяем соединение", true);
  }

  function getHideDelay(success){
    if(mode === "redesign") return 0;
    return success ? 520 : 1100;
  }

  window.CREACLOUD_THEME = Object.freeze({
    mode: mode,
    phrases: phrases.slice(),
    startSplash: startSplash,
    updateSplash: updateSplash,
    finishSplash: finishSplash,
    getHideDelay: getHideDelay
  });
})();
