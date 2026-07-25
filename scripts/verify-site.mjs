import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const assetNames = await readdir("dist/assets");
const cssAsset = assetNames.find((name) => name.endsWith(".css"));
assert.ok(cssAsset, "Собранный CSS-файл не найден");

const [html, builtCss, css, reliabilityCss, app, api, data, main, schedule] =
  await Promise.all([
    readFile("dist/index.html", "utf8"),
    readFile(`dist/assets/${cssAsset}`, "utf8"),
    readFile("src/globals.css", "utf8"),
    readFile("src/reliability.css", "utf8"),
    readFile("src/creacloud-app.tsx", "utf8"),
    readFile("src/creacloud-api.ts", "utf8"),
    readFile("src/creacloud-data.ts", "utf8"),
    readFile("src/main.tsx", "utf8"),
    readFile("src/creacloud-schedule.ts", "utf8"),
  ]);

assert.match(html, /\/-corsar-blogger-booking\/assets\//);
assert.match(
  builtCss,
  /\/-corsar-blogger-booking\/fonts\/montserrat-400\.ttf/,
);
assert.doesNotMatch(
  [html, css, reliabilityCss, app, api].join("\n"),
  /\/Test-1\/|creacloudTest1|creacloud-portal-/,
);

assert.match(
  data,
  /https:\/\/script\.google\.com\/macros\/s\/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q\/exec/,
);
assert.match(app, /ЛК открывается после первого бронирования/);
assert.match(app, /createBookingPayload/);
assert.match(app, /createCancellationPayload/);
assert.match(app, /createContentPayload/);
assert.match(app, /TEAM_DAILY_NOTICE_KEY/);
assert.match(app, /TEAM_DAILY_NOTICE_KEY = "creacloud-main-team-daily-notice-v4"/);
assert.match(api, /fetchVladivostokWeather/);
assert.match(api, /cache: "no-store"/);
assert.match(api, /keepalive: true/);
assert.match(api, /createdAt: new Date\(\)\.toISOString\(\)/);
assert.match(data, /creatorCandidatesFromRow/);
assert.match(data, /row\.username/);
assert.match(data, /row\.telegramNick/);
assert.match(data, /return \{ bookings, content, creators \}/);
assert.match(data, /sourceOrder: sourceOrder\.get\(row\)/);
assert.match(app, /AUTO_SYNC_INTERVAL_MS = 30 \* 1000/);
assert.match(app, /WEATHER_REFRESH_INTERVAL_MS = 15 \* 60 \* 1000/);
assert.match(app, /PORTAL_TRANSITION_MIN_MS/);
assert.match(app, /PORTAL_DATA_WAIT_MS/);
assert.match(app, /LEGACY_BOOKING_NOTICE_LIMIT = 4/);
assert.match(app, /DAILY_NOTICE_EVENT_LIMIT = 5/);
assert.match(app, /syncInFlightRef/);
assert.match(app, /weatherInFlightRef/);
assert.match(app, /mutationEpochRef/);
assert.match(app, /POST_WRITE_SYNC_DELAYS/);
assert.match(app, /visibilitychange/);
assert.match(app, /addEventListener\("online"/);
assert.match(app, /addEventListener\("pageshow"/);
assert.match(app, /addEventListener\("storage"/);
assert.match(app, /role="combobox"/);
assert.match(app, /role="listbox"/);
assert.match(app, /splash--light/);
assert.match(reliabilityCss, /\.splash--light/);
assert.match(reliabilityCss, /font-size: 16px !important/);
assert.match(main, /import "\.\/reliability\.css"/);
assert.doesNotMatch(app, /creators\.slice\(/);
assert.doesNotMatch(app, /Обновить данные/);

const dates = schedule.match(/^\s*"2026-\d{2}-\d{2}":/gm) ?? [];
const slots =
  schedule.match(
    /"(?:barbecue|saxophone|ricorda|russkiy|fishing|shkota|archipelago|askold|captain)"/g,
  ) ?? [];
assert.equal(dates.length, 186);
assert.equal(slots.length, 583);

console.log("✓ Основной адрес и локальные ресурсы настроены");
console.log("✓ Рабочий API и пользовательские сценарии сохранены");
console.log("✓ Автосинхронизация и полный поиск ников защищены от регрессий");
console.log("✓ Белый переход, уведомления и погода защищены от регрессий");
console.log("✓ Расписание сохранено: 186 дат, 583 окна");
