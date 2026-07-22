#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

if "function setupDesktopRecentEventsWidth()" in text and "var LEADER_AUTO_INTERVAL = 5000;" in text:
    print("Патч уже применён")
    raise SystemExit(0)

replacements = []

old_css = '''.cb-recent-events-desktop {
  z-index: 12;
  max-width: 680px;
  margin: auto 0 0;
  overflow: visible;
}
'''
new_css = '''.cb-recent-events-desktop {
  z-index: 12;
  width: var(--cb-events-desktop-width, 100%);
  max-width: 100%;
  margin: auto 0 0;
  overflow: visible;
}
'''
replacements.append((old_css, new_css, "desktop width css"))

old_globals = '''var calendarScrollTicking = false;
var leaderScrollTicking = false;
var leaderCardPosition = 0;
var calendarMonthPosition = (function(){
'''
new_globals = '''var calendarScrollTicking = false;
var leaderScrollTicking = false;
var leaderCardPosition = 0;
var leaderAutoTimer = null;
var LEADER_AUTO_INTERVAL = 5000;
var calendarMonthPosition = (function(){
'''
replacements.append((old_globals, new_globals, "autoplay globals"))

old_before_wrap = '''function wrapLeaderCardPosition(position){
'''
new_before_wrap = '''function syncDesktopRecentEventsWidth(){
  var events = $("cb-recent-events-desktop");
  var actions = document.querySelector(".cb-hero-actions");
  if(!events || !actions) return;

  var desktop = !window.matchMedia || window.matchMedia("(min-width: 901px)").matches;
  if(!desktop){
    events.style.removeProperty("--cb-events-desktop-width");
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
    events.style.setProperty("--cb-events-desktop-width", Math.min(width, actions.clientWidth) + "px");
  }
}

function setupDesktopRecentEventsWidth(){
  syncDesktopRecentEventsWidth();
  window.addEventListener("resize", function(){
    window.requestAnimationFrame(syncDesktopRecentEventsWidth);
  }, {passive: true});

  if(document.fonts && document.fonts.ready){
    document.fonts.ready.then(syncDesktopRecentEventsWidth).catch(function(){});
  }
}

function shouldAutoPlayLeaders(){
  var root = $("cb-leaders-track");
  if(!root || document.hidden) return false;
  if(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return false;
  return root.querySelectorAll(".cb-leader-card").length > 1;
}

function stopLeaderAutoPlay(){
  if(leaderAutoTimer){
    clearTimeout(leaderAutoTimer);
    leaderAutoTimer = null;
  }
}

function scheduleLeaderAutoPlay(){
  stopLeaderAutoPlay();
  if(!shouldAutoPlayLeaders()) return;
  leaderAutoTimer = setTimeout(function(){
    setLeaderCardPosition(leaderCardPosition + 1, true);
    scheduleLeaderAutoPlay();
  }, LEADER_AUTO_INTERVAL);
}

function wrapLeaderCardPosition(position){
'''
replacements.append((old_before_wrap, new_before_wrap, "helpers"))

old_setup = '''function setupLeadersCarousel(){
  var root = $("cb-leaders-track");
  var prev = $("cb-leaders-prev");
  var next = $("cb-leaders-next");
  if(!root) return;

  if(prev) prev.onclick = function(){
    setLeaderCardPosition(leaderCardPosition - 1, true);
  };

  if(next) next.onclick = function(){
    setLeaderCardPosition(leaderCardPosition + 1, true);
  };

  root.addEventListener("scroll", function(){
    if(leaderScrollTicking) return;
    leaderScrollTicking = true;
    window.requestAnimationFrame(function(){
      leaderScrollTicking = false;
      var cards = root.querySelectorAll(".cb-leader-card");
      if(!cards.length) return;

      var nearest = 0;
      var nearestDistance = Infinity;
      Array.prototype.forEach.call(cards, function(card, index){
        var distance = Math.abs(card.offsetLeft - root.scrollLeft);
        if(distance < nearestDistance){
          nearestDistance = distance;
          nearest = index;
        }
      });

      if(nearest !== leaderCardPosition){
        leaderCardPosition = nearest;
        updateLeaderControls();
      }
    });
  }, {passive: true});

  window.addEventListener("resize", function(){
    window.requestAnimationFrame(function(){
      scrollLeadersToPosition(false);
    });
  }, {passive: true});

  scrollLeadersToPosition(false);
}
'''
new_setup = '''function setupLeadersCarousel(){
  var root = $("cb-leaders-track");
  var prev = $("cb-leaders-prev");
  var next = $("cb-leaders-next");
  if(!root) return;

  if(prev) prev.onclick = function(){
    setLeaderCardPosition(leaderCardPosition - 1, true);
    scheduleLeaderAutoPlay();
  };

  if(next) next.onclick = function(){
    setLeaderCardPosition(leaderCardPosition + 1, true);
    scheduleLeaderAutoPlay();
  };

  root.addEventListener("scroll", function(){
    if(leaderScrollTicking) return;
    leaderScrollTicking = true;
    window.requestAnimationFrame(function(){
      leaderScrollTicking = false;
      var cards = root.querySelectorAll(".cb-leader-card");
      if(!cards.length) return;

      var nearest = 0;
      var nearestDistance = Infinity;
      Array.prototype.forEach.call(cards, function(card, index){
        var distance = Math.abs(card.offsetLeft - root.scrollLeft);
        if(distance < nearestDistance){
          nearestDistance = distance;
          nearest = index;
        }
      });

      if(nearest !== leaderCardPosition){
        leaderCardPosition = nearest;
        updateLeaderControls();
      }
    });
  }, {passive: true});

  root.addEventListener("pointerenter", stopLeaderAutoPlay);
  root.addEventListener("pointerleave", scheduleLeaderAutoPlay);
  root.addEventListener("pointerdown", stopLeaderAutoPlay, {passive: true});
  root.addEventListener("pointerup", scheduleLeaderAutoPlay, {passive: true});
  root.addEventListener("pointercancel", scheduleLeaderAutoPlay, {passive: true});
  root.addEventListener("focusin", stopLeaderAutoPlay);
  root.addEventListener("focusout", function(){
    setTimeout(function(){
      if(!root.contains(document.activeElement)) scheduleLeaderAutoPlay();
    }, 0);
  });

  document.addEventListener("visibilitychange", function(){
    if(document.hidden) stopLeaderAutoPlay();
    else scheduleLeaderAutoPlay();
  });

  window.addEventListener("resize", function(){
    window.requestAnimationFrame(function(){
      scrollLeadersToPosition(false);
    });
  }, {passive: true});

  scrollLeadersToPosition(false);
  scheduleLeaderAutoPlay();
}
'''
replacements.append((old_setup, new_setup, "carousel setup"))

old_init = '''  setupWeatherRefresh();
  setupStickyNav();
  setupLeadersCarousel();
'''
new_init = '''  setupWeatherRefresh();
  setupStickyNav();
  setupDesktopRecentEventsWidth();
  setupLeadersCarousel();
'''
replacements.append((old_init, new_init, "init"))

for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось одно совпадение, найдено {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Патч применён")
