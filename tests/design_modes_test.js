const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const html = fs.readFileSync("index.html", "utf8");
const themeJs = fs.readFileSync("creacloud-design.js", "utf8");
const themeCss = fs.readFileSync("creacloud-redesign.css", "utf8");

let passed = 0;
function test(name, fn){
  try {
    fn();
    passed += 1;
    console.log(`✓ ${name}`);
  } catch(error){
    console.error(`✗ ${name}`);
    throw error;
  }
}

function evaluateTheme(search){
  const root = {mode: ""};
  const meta = {content: "", setAttribute(name, value){ if(name === "content") this.content = value; }};
  const context = {
    window: {location: {search}},
    document: {
      documentElement: {setAttribute(name, value){ if(name === "data-design") root.mode = value; }},
      querySelector(selector){ return selector === 'meta[name="theme-color"]' ? meta : null; },
      getElementById(){ return null; }
    },
    URLSearchParams,
    setInterval(){ return 1; },
    clearInterval(){},
    setTimeout(){ return 1; },
    clearTimeout(){},
    Object
  };
  context.window.window = context.window;
  vm.createContext(context);
  vm.runInContext(themeJs, context);
  return {mode: root.mode, meta: meta.content, theme: context.window.CREACLOUD_THEME, configured: context.window.CREACLOUD_DESIGN_MODE};
}

const sectionIds = ["home", "calendar", "booking", "content", "ranking", "results", "creator-profile"];


test("default design is controlled by one explicit feature flag", () => {
  assert.match(themeJs, /window\.CREACLOUD_DESIGN_MODE\s*=\s*"redesign"/);
  const result = evaluateTheme("");
  assert.equal(result.configured, "redesign");
  assert.equal(result.mode, "redesign");
});


test("legacy and redesign can both be selected without changing HTML", () => {
  const legacy = evaluateTheme("?design=legacy");
  const redesign = evaluateTheme("?design=redesign");
  assert.equal(legacy.mode, "legacy");
  assert.equal(redesign.mode, "redesign");
  assert.equal(legacy.theme.getHideDelay(true), 520);
  assert.equal(legacy.theme.getHideDelay(false), 1100);
  assert.equal(redesign.theme.getHideDelay(true), 0);
  assert.equal(redesign.theme.getHideDelay(false), 0);
});


test("redesign stylesheet is isolated from legacy styles", () => {
  assert.match(themeCss, /html\[data-design="redesign"\]/);
  assert.match(themeCss, /--cc-lime:\s*#d9ff52/);
  assert.match(themeCss, /\.cb-splash-redesign\s*\{\s*display:\s*none/);
  assert.doesNotMatch(themeCss, /(^|\n)body\s*\{/);
  assert.doesNotMatch(themeCss, /(^|\n)\.cb-section\s*\{/);
});


test("both loading screens remain available", () => {
  assert.match(html, /class="cb-splash-inner cb-splash-legacy"/);
  assert.match(html, /class="cb-splash-redesign"/);
  assert.match(html, /cb-splash-logo-crea/);
  assert.match(html, /cb-splash-logo-cloud/);
  assert.match(html, /креаторская студия «Корсар»/);
  assert.match(html, /id="cb-loader-phrase"/);
});


test("loader phrases and reduced motion are implemented", () => {
  const result = evaluateTheme("?design=redesign");
  assert.deepEqual(Array.from(result.theme.phrases), [
    "собираем креаторов",
    "смотрим туры",
    "рейтингуем креаторов",
    "респектуем креаторам"
  ]);
  assert.match(themeCss, /\.9s cubic-bezier\(\.22, 1, \.36, 1\)/);
  assert.match(themeCss, /@media \(prefers-reduced-motion: reduce\)/);
  assert.match(themeCss, /min-height:\s*100dvh/);
});


test("loader lifecycle uses the theme without artificial redesign delay", () => {
  assert.match(html, /function getDesignTheme\(\)/);
  assert.match(html, /theme\.startSplash\(\)/);
  assert.match(html, /theme\.finishSplash\(true\)/);
  assert.match(html, /theme\.finishSplash\(false\)/);
  assert.match(html, /theme\.getHideDelay\(true\)/);
});


test("main information architecture and navigation remain unchanged", () => {
  let last = -1;
  sectionIds.forEach((id) => {
    const position = html.indexOf(`id="${id}"`);
    assert.ok(position > last, `${id} must keep its position`);
    last = position;
  });
  ["Главная", "Календарь", "Запись", "Контент", "Рейтинг", "Итоги"].forEach((label) => {
    assert.ok(html.includes(`>${label}</a>`), label);
  });
});


test("business logic and data sources remain present", () => {
  assert.match(html, /AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/);
  [
    "function renderCalendar()",
    "function submitBooking()",
    "function submitReport()",
    "function renderAnalytics()",
    "function renderResults()",
    "function renderCreatorProfile()",
    "function loadData()",
    "TOTAL_UNIQUE_TOURS"
  ].forEach((marker) => assert.ok(html.includes(marker), marker));
});


test("calendar states keep separate tour, booking and disabled semantics", () => {
  assert.match(themeCss, /\.cb-day\.has-tours/);
  assert.match(themeCss, /\.cb-day\.busy/);
  assert.match(themeCss, /\.cb-day\.selected/);
  assert.match(themeCss, /\.cb-day\.is-disabled/);
  assert.match(themeCss, /#eee9ff/);
  assert.match(themeCss, /#fff0e5/);
});


test("mobile and desktop redesign breakpoints are explicit", () => {
  assert.match(themeCss, /@media \(max-width: 900px\)/);
  assert.match(themeCss, /@media \(max-width: 600px\)/);
  assert.match(themeCss, /env\(safe-area-inset-top\)/);
  assert.match(themeCss, /env\(safe-area-inset-bottom\)/);
});


test("redesign keeps white content surfaces and a limited dark contrast section", () => {
  assert.match(themeCss, /\.cb-section\.cb-calendar-shell[\s\S]*linear-gradient\(145deg, #fff/);
  assert.match(themeCss, /\.cb-section\.cb-form-card[\s\S]*linear-gradient\(145deg, #fff/);
  assert.match(themeCss, /\.cb-ranking-section[\s\S]*linear-gradient\(145deg, #242721/);
});



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
  assert.match(html, /bookingContactMode = "call"; submitBooking\(\)/);
  assert.match(html, /contactChannel:\s*contactMode === "call" \? "phone" : "whatsapp"/);
  assert.match(html, /tel:\+" \+ CONFIG\.CALL_PHONE_NUMBER/);
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



test("booking busy helper never calls itself", () => {
  const match = html.match(/function setBookingSubmitBusy\(busy, busyText\)\{([\s\S]*?)\n\}/);
  assert.ok(match, "setBookingSubmitBusy helper");
  assert.doesNotMatch(match[1], /setBookingSubmitBusy\s*\(/);
  assert.match(match[1], /setSubmitBusy\("cb-submit", busy, busyText\)/);
  assert.match(match[1], /setSubmitBusy\("cb-call-submit", busy, busyText\)/);
});



test("publication add card overrides the global pill-button radius", () => {
  assert.match(themeCss, /button\.cb-story-add-card,[\s\S]*border-radius:\s*14px !important/);
});



test("screenshot corrections keep requested desktop geometry", () => {
  assert.match(themeCss, /CREACLOUD screenshot corrections v3/);
  assert.match(themeCss, /\.cb-leaders-track \.cb-leader-card[\s\S]*border-radius:\s*16px !important/);
  assert.match(themeCss, /\.cb-recent-events::before[\s\S]*display:\s*none !important/);
  assert.match(themeCss, /button\.cb-day[\s\S]*border-radius:\s*0 !important/);
  assert.match(themeCss, /@media \(min-width: 901px\)[\s\S]*\.cb-day-weather[\s\S]*left:\s*calc\(50% \+ 10px\)/);
});


test("phone confirmation uses Olga's explicit call number", () => {
  assert.match(html, /CALL_PHONE_NUMBER:\s*"79149753285"/);
  const calls = html.match(/contactMode === "call" \? "tel:\+" \+ CONFIG\.CALL_PHONE_NUMBER : whatsappUrl/g) || [];
  assert.equal(calls.length, 2);
});

console.log(`\n${passed} design mode tests passed.`);
