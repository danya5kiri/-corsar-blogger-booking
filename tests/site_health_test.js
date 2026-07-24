#!/usr/bin/env node
"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const html = fs.readFileSync("index.html", "utf8");
let passed = 0;

function test(name, fn) {
  try {
    fn();
    passed += 1;
    console.log("✓", name);
  } catch (error) {
    console.error("✗", name);
    throw error;
  }
}

function extractInlineScript(source) {
  const matches = Array.from(source.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi));
  const inline = matches.map((match) => match[1]).filter((value) => value.trim());
  assert.ok(inline.length, "inline JavaScript not found");
  return inline[inline.length - 1];
}

function buildSandbox(script) {
  const fixedNow = new Date("2026-07-24T00:00:00+10:00").getTime();
  const NativeDate = Date;
  class FixedDate extends NativeDate {
    constructor(...args) {
      super(...(args.length ? args : [fixedNow]));
    }
    static now() {
      return fixedNow;
    }
  }

  const storage = new Map();
  const documentStub = {
    readyState: "loading",
    hidden: false,
    addEventListener() {},
    getElementById() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    createElement() {
      return {
        style: {},
        classList: { add() {}, remove() {}, toggle() {} },
        setAttribute() {},
        appendChild() {},
        removeChild() {},
        select() {},
        querySelectorAll() { return []; },
      };
    },
    execCommand() { return true; },
    body: {
      classList: { add() {}, remove() {}, toggle() {} },
      appendChild() {},
      removeChild() {},
    },
    fonts: { ready: Promise.resolve() },
  };

  const sandbox = {
    console,
    Date: FixedDate,
    Intl,
    URL,
    Math,
    JSON,
    Number,
    String,
    Boolean,
    Object,
    Array,
    RegExp,
    Promise,
    Error,
    TypeError,
    Map,
    Set,
    encodeURIComponent,
    decodeURIComponent,
    setTimeout() { return 0; },
    clearTimeout() {},
    setInterval() { return 0; },
    clearInterval() {},
    requestAnimationFrame(callback) { if (typeof callback === "function") callback(); return 0; },
    cancelAnimationFrame() {},
    AbortController,
    document: documentStub,
    navigator: {},
    location: { hash: "", href: "" },
    localStorage: {
      getItem(key) { return storage.has(key) ? storage.get(key) : null; },
      setItem(key, value) { storage.set(key, String(value)); },
      removeItem(key) { storage.delete(key); },
    },
    fetch() { return Promise.reject(new Error("network disabled in tests")); },
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  sandbox.window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  sandbox.window.addEventListener = () => {};
  sandbox.window.requestAnimationFrame = sandbox.requestAnimationFrame;

  const hook = `
  globalThis.__corsarTest = {
    CONFIG: CONFIG,
    CANONICAL_TOURS: CANONICAL_TOURS,
    TOURS_BY_DATE: TOURS_BY_DATE,
    TOTAL_UNIQUE_TOURS: TOTAL_UNIQUE_TOURS,
    normalizeTour: normalizeTour,
    canonicalTourName: canonicalTourName,
    getUniqueTourKey: getUniqueTourKey,
    bookingFingerprint: bookingFingerprint,
    bookingSlotFingerprint: bookingSlotFingerprint,
    resolveEffectiveBookings: resolveEffectiveBookings,
    hasBookingSlotConflict: hasBookingSlotConflict,
    isDateInSeason: isDateInSeason,
    isBookableDate: isBookableDate,
    getToursByDate: getToursByDate,
    isTourScheduledOnDate: isTourScheduledOnDate,
    isTransferableBookingForCreator: isTransferableBookingForCreator,
    findBookingUniqueAlternative: findBookingUniqueAlternative,
    buildWeatherForecastMap: buildWeatherForecastMap,
    getWeatherForecastTitle: getWeatherForecastTitle,
    sanitizeDiagnosticDetail: sanitizeDiagnosticDetail,
    isPendingWriteConfirmed: isPendingWriteConfirmed,
    setBookings: function(value){ bookings = Array.isArray(value) ? value : []; creatorDirectoryReady = true; },
    setReports: function(value){ reports = Array.isArray(value) ? value : []; },
    setTours: function(date, tours){ TOURS_BY_DATE[date] = tours.slice(); }
  };
`;

  const injected = script.replace(/\n\}\)\(\);\s*$/, hook + "\n})();");
  assert.notEqual(injected, script, "test hook injection failed");

  vm.createContext(sandbox);
  new vm.Script(injected, { filename: "index-inline.js" }).runInContext(sandbox);
  return sandbox.__corsarTest;
}

const script = extractInlineScript(html);

// Parse the production script before any semantic tests.
test("JavaScript parses", () => {
  new vm.Script(script, { filename: "index-inline.js" });
});

test("HTML ids are unique", () => {
  const staticMarkup = html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/gi, "");
  const ids = Array.from(staticMarkup.matchAll(/\sid="([^"]+)"/g), (match) => match[1]);
  const seen = new Set();
  const duplicates = [];
  ids.forEach((id) => {
    if (seen.has(id)) duplicates.push(id);
    seen.add(id);
  });
  assert.deepEqual(duplicates, []);
});

test("weather uses explicit Best Match for 16 days", () => {
  assert.match(script, /models=best_match/);
  assert.match(script, /forecast_days=16/);
  assert.match(script, /WEATHER_REFRESH_INTERVAL = 3 \* 60 \* 60 \* 1000/);
  assert.doesNotMatch(script, /isWeatherDateInActiveMonth/);
  assert.doesNotMatch(script, /weatherActiveMonthKey/);
});

test("calendar displays every received forecast regardless of month", () => {
  assert.match(script, /var forecast = active \? getWeatherForecast\(date\) : null;/);
});

test("mobile regression guards remain intact", () => {
  assert.doesNotMatch(script, /window\.visualViewport/);
  assert.doesNotMatch(script, /document\.body\.style\.position\s*=\s*["']fixed["']/);
});

test("diagnostics container and privacy copy exist", () => {
  assert.match(html, /id="cb-diagnostics"/);
  assert.match(html, /не отправляется автоматически/);
  assert.match(script, /function setupDiagnostics\(\)/);
  assert.match(script, /function reconcilePendingWrites\(\)/);
});

const api = buildSandbox(script);

test("season retains eight unique categories", () => {
  assert.equal(api.TOTAL_UNIQUE_TOURS, 8);
  assert.equal(
    api.getUniqueTourKey(api.CANONICAL_TOURS[1]),
    api.getUniqueTourKey(api.CANONICAL_TOURS[8]),
    "two evening programmes must share one category"
  );
});

test("all static schedule dates are inside the season", () => {
  Object.entries(api.TOURS_BY_DATE).forEach(([date, tours]) => {
    assert.equal(api.isDateInSeason(date), true, date);
    assert.ok(Array.isArray(tours), date);
  });
});

test("forecast map keeps dates across July and August", () => {
  const map = api.buildWeatherForecastMap({
    time: ["2026-07-31", "2026-08-01"],
    weather_code: [1, 61],
    temperature_2m_max: [25, 23],
    temperature_2m_min: [18, 17],
    apparent_temperature_max: [26, 24],
    precipitation_probability_max: [20, 70],
    wind_speed_10m_max: [16, 21],
    wind_gusts_10m_max: [27, 35],
  });
  assert.ok(map["2026-07-31"]);
  assert.ok(map["2026-08-01"]);
  assert.equal(map["2026-08-01"].gust, 35);
  assert.equal(api.getWeatherForecastTitle("2026-08-05"), "Предварительный прогноз");
});

test("transfer removes the source and keeps the target", () => {
  const source = { date: "2026-08-10", telegram: "@alpha", tour: api.CANONICAL_TOURS[0] };
  const sourceKey = api.bookingFingerprint(source.date, source.telegram, source.tour);
  const target = {
    date: "2026-08-11",
    telegram: "@alpha",
    tour: api.CANONICAL_TOURS[2],
    operation: "transfer",
    transferFromKey: sourceKey,
  };
  const result = api.resolveEffectiveBookings([source, target]);
  assert.equal(result.length, 1);
  assert.equal(result[0].date, target.date);
  assert.equal(result[0].tour, target.tour);
});

test("cancellation removes an existing booking", () => {
  const booking = { date: "2026-08-12", telegram: "@beta", tour: api.CANONICAL_TOURS[3] };
  const cancellation = {
    date: booking.date,
    telegram: booking.telegram,
    tour: booking.tour,
    operation: "cancel",
    cancelBookingKey: api.bookingFingerprint(booking.date, booking.telegram, booking.tour),
  };
  assert.deepEqual(api.resolveEffectiveBookings([booking, cancellation]), []);
});

test("a new booking after an older cancellation survives", () => {
  const booking = { date: "2026-08-13", telegram: "@gamma", tour: api.CANONICAL_TOURS[4] };
  const cancellation = {
    operation: "cancel",
    cancelBookingKey: api.bookingFingerprint(booking.date, booking.telegram, booking.tour),
  };
  const result = api.resolveEffectiveBookings([cancellation, booking]);
  assert.equal(result.length, 1);
  assert.equal(result[0].telegram, booking.telegram);
});

test("slot conflict recognises canonical aliases", () => {
  api.setBookings([{ date: "2026-08-14", telegram: "@delta", tour: "Отдых на катере 32ft с рыбалкой" }]);
  assert.equal(api.hasBookingSlotConflict("2026-08-14", api.CANONICAL_TOURS[4]), true);
});

test("past bookings cannot be transferred or cancelled", () => {
  const future = { date: "2026-08-15", telegram: "@epsilon", tour: api.CANONICAL_TOURS[0] };
  const past = { date: "2026-07-23", telegram: "@epsilon", tour: api.CANONICAL_TOURS[0] };
  assert.equal(api.isTransferableBookingForCreator(future, "@epsilon"), true);
  assert.equal(api.isTransferableBookingForCreator(past, "@epsilon"), false);
  assert.equal(api.isTransferableBookingForCreator(future, "@other"), false);
});

test("tour must belong to the selected date", () => {
  const date = Object.keys(api.TOURS_BY_DATE).sort().find((value) => value >= "2026-07-24");
  assert.ok(date);
  const tour = api.TOURS_BY_DATE[date][0];
  assert.equal(api.isTourScheduledOnDate(date, tour), true);
  assert.equal(api.isTourScheduledOnDate(date, "Несуществующий тур"), false);
});

test("unique recommendation appears only for a free unvisited category", () => {
  const date = "2026-08-16";
  const visited = api.CANONICAL_TOURS[0];
  const newTour = api.CANONICAL_TOURS[2];
  api.setTours(date, [visited, newTour]);
  api.setBookings([{ date: "2026-07-24", telegram: "@zeta", tour: visited }]);
  const suggestion = api.findBookingUniqueAlternative("@zeta", date, visited);
  assert.ok(suggestion);
  assert.equal(api.normalizeTour(suggestion.tour), api.normalizeTour(newTour));

  api.setBookings([
    { date: "2026-07-24", telegram: "@zeta", tour: visited },
    { date, telegram: "@occupied", tour: newTour },
  ]);
  assert.equal(api.findBookingUniqueAlternative("@zeta", date, visited), null);
});

test("pending opaque POST is confirmed from reloaded data", () => {
  const booking = { date: "2026-08-17", telegram: "@eta", tour: api.CANONICAL_TOURS[3] };
  const key = api.bookingFingerprint(booking.date, booking.telegram, booking.tour);
  api.setBookings([booking]);
  assert.equal(api.isPendingWriteConfirmed({ kind: "booking", targetKey: key }), true);
  assert.equal(api.isPendingWriteConfirmed({ kind: "cancel", sourceKey: key }), false);
  api.setBookings([]);
  assert.equal(api.isPendingWriteConfirmed({ kind: "cancel", sourceKey: key }), true);
});

test("diagnostic details remove user identifiers", () => {
  const value = api.sanitizeDiagnosticDetail("Ошибка для @private_user, +7 999 123-45-67, https://example.com/private");
  assert.doesNotMatch(value, /private_user/);
  assert.doesNotMatch(value, /999/);
  assert.doesNotMatch(value, /example\.com/);
});

console.log(`\n${passed} site health tests passed.`);
