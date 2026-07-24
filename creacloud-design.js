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
  var profileNoticeTimer = null;

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

  function syncMobileProfileEntry(){
    if(mode !== "redesign") return;
    var profile = document.querySelector(".cb-profile-entry-card");
    var stats = document.querySelector(".cb-hero-stats");
    var copy = document.querySelector(".cb-hero-copy");
    var events = document.getElementById("cb-recent-events-desktop");
    if(!profile || !stats || !copy) return;

    if(window.matchMedia("(max-width: 900px)").matches){
      if(profile.parentNode !== stats || profile !== stats.firstElementChild){
        stats.insertBefore(profile, stats.firstElementChild);
      }
    } else if(events && (profile.parentNode !== copy || profile.nextElementSibling !== events)){
      copy.insertBefore(profile, events);
    }
  }

  function normalizeProfileNick(value){
    return String(value || "").trim().toLowerCase().replace(/^@+/, "");
  }

  function showProfileBookingRequired(){
    var text = "ЛК открывается после первого бронирования.";
    var state = document.getElementById("cb-profile-entry-state");
    if(state){
      state.textContent = text;
      state.classList.remove("is-ready");
      state.classList.add("is-error");
    }

    var message = document.getElementById("cb-message");
    if(message){
      if(profileNoticeTimer) clearTimeout(profileNoticeTimer);
      message.textContent = text;
      message.classList.remove("error");
      message.classList.add("is-visible");
      profileNoticeTimer = setTimeout(function(){
        message.classList.remove("is-visible");
        profileNoticeTimer = null;
      }, 3200);
    }
  }

  function blockUnknownProfileOpen(event){
    var input = document.getElementById("cb-profile-entry-input");
    var list = document.getElementById("cb-profile-creators");
    if(!input || !list) return;

    var requestedNick = normalizeProfileNick(input.value);
    if(!requestedNick) return;

    var options = Array.prototype.slice.call(list.querySelectorAll("option"));
    if(!options.length) return;

    var exists = options.some(function(option){
      return normalizeProfileNick(option.value) === requestedNick;
    });
    if(exists) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    showProfileBookingRequired();
  }

  function initProfileEntry(){
    syncMobileProfileEntry();
    var media = window.matchMedia("(max-width: 900px)");
    if(media.addEventListener) media.addEventListener("change", syncMobileProfileEntry);
    else if(media.addListener) media.addListener(syncMobileProfileEntry);

    var button = document.getElementById("cb-profile-entry-submit");
    var input = document.getElementById("cb-profile-entry-input");
    if(button) button.addEventListener("click", blockUnknownProfileOpen, true);
    if(input){
      input.addEventListener("keydown", function(event){
        if(event.key === "Enter") blockUnknownProfileOpen(event);
      }, true);
    }
  }

  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", initProfileEntry, {once: true});
  else initProfileEntry();

  window.CREACLOUD_THEME = Object.freeze({
    mode: mode,
    phrases: phrases.slice(),
    startSplash: startSplash,
    updateSplash: updateSplash,
    finishSplash: finishSplash,
    getHideDelay: getHideDelay
  });
})();
