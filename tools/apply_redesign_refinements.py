#!/usr/bin/env python3
from pathlib import Path

INDEX = Path("index.html")
CSS = Path("creacloud-redesign.css")
TESTS = Path("tests/design_modes_test.js")

index = INDEX.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
tests = TESTS.read_text(encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


index = replace_once(
    index,
    '      <button type="button" id="cb-submit" class="cb-submit">Сформировать заявку в WhatsApp</button>',
    '      <div class="cb-booking-actions">\n'
    '        <button type="button" id="cb-submit" class="cb-submit">Сформировать заявку WhatsApp</button>\n'
    '        <button type="button" id="cb-call-submit" class="cb-booking-call" aria-label="Позвонить Ольге для записи">Позвонить для записи</button>\n'
    '      </div>',
    "booking action row",
)

index = replace_once(
    index,
    '<h2 class="cb-section-title">Мини-ЛК <strong>креатора</strong></h2>',
    '<h2 class="cb-section-title">ЛК <strong>креатора</strong></h2>',
    "creator cabinet title",
)

helper = '''function setBookingSubmitBusy(busy, busyText){
  setSubmitBusy("cb-submit", busy, busyText);
  setSubmitBusy("cb-call-submit", busy, busyText);
}

'''
if helper not in index:
    anchor = 'var messageTimer = null;\n'
    if index.count(anchor) != 1:
        raise SystemExit("booking busy helper anchor not found")
    index = index.replace(anchor, helper + anchor, 1)

if 'setSubmitBusy("cb-submit",' in index:
    index = index.replace('setSubmitBusy("cb-submit",', 'setBookingSubmitBusy(')

index = replace_once(
    index,
    'function submitBookingCancellation(tg, sourceFingerprint){\n',
    'function submitBookingCancellation(tg, sourceFingerprint, contactMode){\n'
    '  contactMode = contactMode === "call" ? "call" : "whatsapp";\n',
    "cancellation contact mode",
)

index = replace_once(
    index,
    'function submitBooking(){\n',
    'function submitBooking(contactMode){\n'
    '  contactMode = contactMode === "call" ? "call" : "whatsapp";\n',
    "booking contact mode",
)

index = replace_once(
    index,
    '    submitBookingCancellation(tg, sourceFingerprint);',
    '    submitBookingCancellation(tg, sourceFingerprint, contactMode);',
    "pass cancellation contact mode",
)

index = replace_once(
    index,
    '        operation: "cancel",\n',
    '        operation: "cancel",\n'
    '        contactChannel: contactMode === "call" ? "phone" : "whatsapp",\n',
    "cancellation contact channel",
)

index = replace_once(
    index,
    '        status: mode === "transfer" ? "Перенос" : "Новая заявка",\n',
    '        status: mode === "transfer" ? "Перенос" : "Новая заявка",\n'
    '        contactChannel: contactMode === "call" ? "phone" : "whatsapp",\n',
    "booking contact channel",
)

index = replace_once(
    index,
    '        var whatsappUrl = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);\n\n'
    '        setMessage("Бронь удалена. Место освобождено; открываем WhatsApp.", false);\n'
    '        setTimeout(function(){ window.location.href = whatsappUrl; }, 650);',
    '        var whatsappUrl = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);\n'
    '        var contactUrl = contactMode === "call" ? "tel:+" + CONFIG.WHATSAPP_NUMBER : whatsappUrl;\n\n'
    '        setMessage(contactMode === "call" ? "Бронь удалена. Место освобождено; звоним Ольге." : "Бронь удалена. Место освобождено; открываем WhatsApp.", false);\n'
    '        setTimeout(function(){ window.location.href = contactUrl; }, 650);',
    "cancellation contact redirect",
)

index = replace_once(
    index,
    '        var whatsappUrl = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);\n\n'
    '        setMessage(mode === "transfer" ? "Запись перенесена. Открываем WhatsApp для согласования." : "Заявка записана. Открываем WhatsApp для согласования.", false);\n'
    '        setTimeout(function(){ window.location.href = whatsappUrl; }, 650);',
    '        var whatsappUrl = "https://wa.me/" + CONFIG.WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);\n'
    '        var contactUrl = contactMode === "call" ? "tel:+" + CONFIG.WHATSAPP_NUMBER : whatsappUrl;\n'
    '        var successMessage = contactMode === "call"\n'
    '          ? (mode === "transfer" ? "Запись перенесена. Звоним Ольге для согласования." : "Заявка записана. Звоним Ольге для согласования.")\n'
    '          : (mode === "transfer" ? "Запись перенесена. Открываем WhatsApp для согласования." : "Заявка записана. Открываем WhatsApp для согласования.");\n\n'
    '        setMessage(successMessage, false);\n'
    '        setTimeout(function(){ window.location.href = contactUrl; }, 650);',
    "booking contact redirect",
)

index = replace_once(
    index,
    '  var submit = $("cb-submit");\n  var dateInput = $("cb-date");',
    '  var submit = $("cb-submit");\n  var callSubmit = $("cb-call-submit");\n  var dateInput = $("cb-date");',
    "call button init variable",
)

index = replace_once(
    index,
    '  if(submit) submit.onclick = submitBooking;\n  if(reportSubmit) reportSubmit.onclick = submitReport;',
    '  if(submit) submit.onclick = function(){ submitBooking("whatsapp"); };\n'
    '  if(callSubmit) callSubmit.onclick = function(){ submitBooking("call"); };\n'
    '  if(reportSubmit) reportSubmit.onclick = submitReport;',
    "call button binding",
)

nav_function = '''function setupRedesignNavigationBehavior(){
  if(document.documentElement.getAttribute("data-design") !== "redesign") return;
  var nav = document.querySelector(".cb-sticky-nav");
  if(!nav) return;

  var lastY = Math.max(0, window.scrollY || 0);
  var ticking = false;

  function showNavigation(){
    nav.classList.remove("is-scroll-hidden");
  }

  window.addEventListener("scroll", function(){
    if(ticking) return;
    ticking = true;
    window.requestAnimationFrame(function(){
      var currentY = Math.max(0, window.scrollY || 0);
      var delta = currentY - lastY;
      if(currentY < 96 || delta < -4){
        showNavigation();
      } else if(currentY > 150 && delta > 4){
        nav.classList.add("is-scroll-hidden");
      }
      lastY = currentY;
      ticking = false;
    });
  }, {passive: true});

  nav.addEventListener("focusin", showNavigation);
  nav.addEventListener("pointerenter", showNavigation);
  Array.prototype.forEach.call(nav.querySelectorAll("a"), function(link){
    link.addEventListener("click", showNavigation);
  });
}

'''
if nav_function not in index:
    anchor = 'function init(){\n'
    if index.count(anchor) != 1:
        raise SystemExit("init anchor not found")
    index = index.replace(anchor, nav_function + anchor, 1)

index = replace_once(
    index,
    '  setupStickyNav();\n  setupCreatorProfilePlacement();',
    '  setupStickyNav();\n  setupRedesignNavigationBehavior();\n  setupCreatorProfilePlacement();',
    "navigation behavior init",
)

css_marker = '/* ===== CREACLOUD refinements v2 ===== */'
if css_marker not in css:
    css += r'''

/* ===== CREACLOUD refinements v2 ===== */
html[data-design="redesign"] .cb-sticky-nav {
  border-color: rgba(21, 23, 20, .10);
  background: rgba(255, 255, 255, .82);
  box-shadow: 0 14px 36px rgba(31, 35, 28, .11);
  transition: transform .26s cubic-bezier(.22, 1, .36, 1), opacity .2s ease, background .2s ease;
}

html[data-design="redesign"] .cb-sticky-nav.is-scroll-hidden {
  opacity: 0;
  pointer-events: none;
  transform: translateY(calc(-100% - max(18px, env(safe-area-inset-top))));
}

html[data-design="redesign"] .cb-nav-brand,
html[data-design="redesign"] .cb-nav-links a {
  color: #151714;
}

html[data-design="redesign"] .cb-nav-links a:hover,
html[data-design="redesign"] .cb-nav-links a.is-active {
  background: var(--cc-lime);
  color: #11130f;
}

html[data-design="redesign"] .cb-hero {
  border-color: rgba(21, 23, 20, .08);
  background:
    radial-gradient(circle at 76% 2%, rgba(118, 87, 246, .14), transparent 28rem),
    radial-gradient(circle at 96% 82%, rgba(255, 122, 36, .12), transparent 24rem),
    radial-gradient(circle at 8% 96%, rgba(217, 255, 82, .18), transparent 26rem),
    linear-gradient(145deg, #ffffff 0%, #ffffff 64%, #f7f8f3 100%) !important;
  box-shadow: 0 24px 72px rgba(31, 35, 28, .10);
  color: #151714;
}

html[data-design="redesign"] .cb-hero-inner::before {
  background: rgba(118, 87, 246, .12);
}

html[data-design="redesign"] .cb-hero-inner::after {
  background: rgba(217, 255, 82, .18);
}

html[data-design="redesign"] .cb-hero-title,
html[data-design="redesign"] .cb-hero-title strong {
  color: #151714;
}

html[data-design="redesign"] .cb-hero-text {
  color: #5f645c;
}

html[data-design="redesign"] .cb-route-line {
  opacity: .94;
  filter: drop-shadow(0 5px 11px rgba(77, 64, 150, .24));
}

html[data-design="redesign"] .cb-route-line > path {
  stroke-width: 5.4px;
}

html[data-design="redesign"] #cb-route-gradient stop:nth-child(1) {
  stop-color: #7657f6;
}

html[data-design="redesign"] #cb-route-gradient stop:nth-child(2) {
  stop-color: #ff7a24;
}

html[data-design="redesign"] #cb-route-gradient stop:nth-child(3) {
  stop-color: #5d9b6f;
}

html[data-design="redesign"] #cb-route-gradient stop:nth-child(4) {
  stop-color: #292d28;
}

html[data-design="redesign"] .cb-route-stop {
  fill: #fff;
  filter: drop-shadow(0 3px 5px rgba(21, 23, 20, .20));
}

html[data-design="redesign"] .cb-route-ship {
  filter: drop-shadow(0 8px 13px rgba(65, 48, 126, .30));
}

html[data-design="redesign"] .cb-profile-entry-card,
html[data-design="redesign"] .cb-hero-stats > .cb-stat-card:first-child,
html[data-design="redesign"] .cb-hero-stats > .cb-stat-card:nth-child(2) {
  border-radius: 16px;
}

html[data-design="redesign"] .cb-profile-entry-card,
html[data-design="redesign"] .cb-profile-entry-card .cb-stat-label,
html[data-design="redesign"] .cb-profile-entry-copy,
html[data-design="redesign"] .cb-profile-entry-copy strong,
html[data-design="redesign"] .cb-profile-entry-copy span,
html[data-design="redesign"] .cb-profile-entry-state {
  color: #151714;
}

html[data-design="redesign"] .cb-recent-events {
  border-color: rgba(21, 23, 20, .10);
  border-radius: 999px;
  background: rgba(255, 255, 255, .76);
  color: #151714;
  box-shadow: 0 10px 26px rgba(31, 35, 28, .07);
}

html[data-design="redesign"] .cb-recent-events[open] {
  border-radius: 18px;
}

html[data-design="redesign"] .cb-recent-events .cb-activity-head,
html[data-design="redesign"] .cb-recent-events-desktop .cb-activity-head,
html[data-design="redesign"] .cb-recent-events-mobile .cb-activity-head {
  border-radius: 999px;
  background: rgba(255, 255, 255, .74);
  color: #151714;
}

html[data-design="redesign"] .cb-recent-events .cb-activity-panel,
html[data-design="redesign"] .cb-recent-events-mobile .cb-activity-panel {
  border-color: rgba(21, 23, 20, .09);
  border-radius: 16px;
  background: rgba(255, 255, 255, .97);
  color: #151714;
  box-shadow: 0 -14px 34px rgba(31, 35, 28, .11);
}

html[data-design="redesign"] .cb-activity-copy,
html[data-design="redesign"] .cb-activity-time,
html[data-design="redesign"] .cb-activity-empty,
html[data-design="redesign"] .cb-activity-live {
  color: #676c64;
}

html[data-design="redesign"] .cb-activity-copy strong {
  color: #151714;
}

html[data-design="redesign"] .cb-hero-stats > .cb-stat-card:first-child {
  background:
    radial-gradient(circle at 84% 10%, rgba(255, 255, 255, .88), transparent 35%),
    linear-gradient(145deg, #f4ffd1 0%, #e9f6cf 48%, #ffffff 100%);
  color: #151714;
  box-shadow: 0 16px 36px rgba(79, 96, 49, .13);
}

html[data-design="redesign"] .cb-weather-temp {
  width: fit-content;
  max-width: 100%;
  align-self: flex-start;
  justify-content: flex-start;
  gap: 8px;
}

html[data-design="redesign"] .cb-weather-number {
  flex: 0 0 auto;
}

html[data-design="redesign"] .cb-weather-temp .cb-weather-icon {
  width: 42px;
  height: 42px;
  margin: 0;
}

html[data-design="redesign"] .cb-leaders-controls {
  background: rgba(21, 23, 20, .06);
  color: #151714;
}

html[data-design="redesign"] .cb-leaders-current span,
html[data-design="redesign"] .cb-leaders-current strong {
  color: #62675f;
}

html[data-design="redesign"] .cb-leaders-track .cb-leader-card {
  border-radius: 14px;
}

html[data-design="redesign"] .cb-story-card,
html[data-design="redesign"] .cb-story-add-card {
  border-radius: 14px;
  overflow: hidden;
}

html[data-design="redesign"] .cb-story-add-copy {
  min-width: 0;
  padding-right: 8px;
}

html[data-design="redesign"] .cb-calendar-controls,
html[data-design="redesign"] .cb-calendar-card,
html[data-design="redesign"] .cb-details-card {
  border-radius: 14px;
}

html[data-design="redesign"] .cb-day {
  border-radius: 7px;
}

html[data-design="redesign"] .cb-ranking-section {
  background:
    radial-gradient(circle at 8% 6%, rgba(217, 255, 82, .22), transparent 24rem),
    radial-gradient(circle at 92% 10%, rgba(178, 151, 255, .42), transparent 26rem),
    radial-gradient(circle at 86% 88%, rgba(255, 157, 94, .34), transparent 24rem),
    linear-gradient(135deg, #6657b8 0%, #47526c 50%, #a75935 100%);
  color: #fff;
  box-shadow: 0 26px 76px rgba(62, 52, 92, .22);
}

html[data-design="redesign"] .cb-ranking-section .cb-section-title,
html[data-design="redesign"] .cb-ranking-section .cb-section-note {
  color: #fff;
}

html[data-design="redesign"] .cb-ranking-section .cb-section-note {
  color: rgba(255, 255, 255, .82);
}

html[data-design="redesign"] .cb-booking-actions {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(220px, .42fr);
  gap: 12px;
  margin-top: 8px;
}

html[data-design="redesign"] .cb-booking-actions .cb-submit,
html[data-design="redesign"] .cb-booking-call {
  grid-column: auto;
  width: 100%;
  min-height: 58px;
  margin: 0;
  padding: 0 20px;
  border: 0;
  border-radius: 999px;
  cursor: pointer;
  font: inherit;
  font-size: 14px;
  font-weight: 780;
}

html[data-design="redesign"] .cb-booking-call {
  background: #151714;
  color: #fff;
  box-shadow: 0 14px 30px rgba(21, 23, 20, .17);
}

html[data-design="redesign"] .cb-booking-call:hover,
html[data-design="redesign"] .cb-booking-call:focus-visible {
  background: #292d28;
  transform: translateY(-2px);
}

html[data-design="redesign"] .cb-booking-call:disabled {
  cursor: wait;
  filter: grayscale(.45);
  opacity: .46;
  transform: none;
}

html[data-design="redesign"] .cb-splash {
  display: grid;
  place-items: center;
}

html[data-design="redesign"] .cb-splash-redesign {
  width: 100%;
  max-width: 100%;
  min-height: 0;
  height: 100%;
  box-sizing: border-box;
  place-content: center;
  overflow: hidden;
}

html[data-design="redesign"] .cb-splash-logo {
  width: 100%;
  max-width: calc(100vw - 36px);
}

@media (max-width: 600px) {
  html[data-design="redesign"] .cb-splash {
    inset: 0;
    min-height: 100dvh;
    padding: max(18px, env(safe-area-inset-top)) 18px max(22px, env(safe-area-inset-bottom));
  }

  html[data-design="redesign"] .cb-splash-redesign {
    min-height: 0;
    height: calc(100dvh - max(18px, env(safe-area-inset-top)) - max(22px, env(safe-area-inset-bottom)));
  }

  html[data-design="redesign"] .cb-splash-logo {
    max-width: calc(100vw - 36px);
    font-size: clamp(38px, 15.4vw, 62px);
    letter-spacing: -.07em;
  }

  html[data-design="redesign"] .cb-splash-subtitle {
    max-width: min(280px, calc(100vw - 44px));
    margin-top: clamp(20px, 4vh, 30px);
    font-size: 15px;
  }

  html[data-design="redesign"] .cb-splash-pulse {
    margin-top: clamp(52px, 8vh, 70px);
  }

  html[data-design="redesign"] .cb-splash-phrase-frame {
    min-height: 34px;
    margin-top: 36px;
  }

  html[data-design="redesign"] .cb-leaders-track .cb-leader-card,
  html[data-design="redesign"] .cb-calendar-card,
  html[data-design="redesign"] .cb-details-card {
    border-radius: 14px;
  }

  html[data-design="redesign"] .cb-day {
    border-radius: 7px;
  }

  html[data-design="redesign"] .cb-booking-actions {
    grid-template-columns: 1fr;
  }
}
'''

extra_tests = r'''

test("refinements keep the hero light and improve compact card radii", () => {
  assert.match(themeCss, /CREACLOUD refinements v2/);
  assert.match(themeCss, /\.cb-hero\s*\{[\s\S]*linear-gradient\(145deg, #ffffff/);
  assert.match(themeCss, /\.cb-leaders-track \.cb-leader-card\s*\{\s*border-radius:\s*14px/);
  assert.match(themeCss, /\.cb-day\s*\{\s*border-radius:\s*7px/);
  assert.match(themeCss, /\.cb-recent-events \.cb-activity-head[\s\S]*border-radius:\s*999px/);
});


test("booking supports WhatsApp and phone confirmation through the same write flow", () => {
  assert.match(html, /id="cb-call-submit"/);
  assert.match(html, /Сформировать заявку WhatsApp/);
  assert.match(html, /Позвонить для записи/);
  assert.match(html, /submitBooking\("call"\)/);
  assert.match(html, /contactChannel:\s*contactMode === "call" \? "phone" : "whatsapp"/);
  assert.match(html, /tel:\+" \+ CONFIG\.WHATSAPP_NUMBER/);
});


test("creator cabinet title and scrolling navigation match the refinement brief", () => {
  assert.match(html, /<h2 class="cb-section-title">ЛК <strong>креатора<\/strong><\/h2>/);
  assert.match(html, /function setupRedesignNavigationBehavior\(\)/);
  assert.match(themeCss, /\.cb-sticky-nav\.is-scroll-hidden/);
  assert.match(themeCss, /background:\s*rgba\(255, 255, 255, \.82\)/);
});


test("mobile splash is constrained to the safe viewport", () => {
  assert.match(themeCss, /max-width:\s*calc\(100vw - 36px\)/);
  assert.match(themeCss, /font-size:\s*clamp\(38px, 15\.4vw, 62px\)/);
  assert.match(themeCss, /height:\s*calc\(100dvh - max\(18px, env\(safe-area-inset-top\)\) - max\(22px, env\(safe-area-inset-bottom\)\)\)/);
});
'''

if 'refinements keep the hero light and improve compact card radii' not in tests:
    marker = r'console.log(`\n${passed} design mode tests passed.`);'
    if tests.count(marker) != 1:
        raise SystemExit("design test footer not found")
    tests = tests.replace(marker, extra_tests + '\n' + marker, 1)

INDEX.write_text(index, encoding="utf-8")
CSS.write_text(css, encoding="utf-8")
TESTS.write_text(tests, encoding="utf-8")
print("CREACLOUD refinement patch applied")
