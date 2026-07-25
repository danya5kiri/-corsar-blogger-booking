import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const assetNames = await readdir("dist/assets");
const cssAsset = assetNames.find((name) => name.endsWith(".css"));
assert.ok(cssAsset, "Собранный CSS-файл не найден");

const [html, builtCss, css, app, api, data, schedule] = await Promise.all([
  readFile("dist/index.html", "utf8"),
  readFile(`dist/assets/${cssAsset}`, "utf8"),
  readFile("src/globals.css", "utf8"),
  readFile("src/creacloud-app.tsx", "utf8"),
  readFile("src/creacloud-api.ts", "utf8"),
  readFile("src/creacloud-data.ts", "utf8"),
  readFile("src/creacloud-schedule.ts", "utf8"),
]);

assert.match(html, /\/-corsar-blogger-booking\/assets\//);
assert.match(
  builtCss,
  /\/-corsar-blogger-booking\/fonts\/montserrat-400\.ttf/,
);
assert.doesNotMatch(
  [html, css, app, api].join("\n"),
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
assert.match(api, /fetchVladivostokWeather/);

const dates = schedule.match(/^\s*"2026-\d{2}-\d{2}":/gm) ?? [];
const slots =
  schedule.match(
    /"(?:barbecue|saxophone|ricorda|russkiy|fishing|shkota|archipelago|askold|captain)"/g,
  ) ?? [];
assert.equal(dates.length, 186);
assert.equal(slots.length, 583);

console.log("✓ Основной адрес и локальные ресурсы настроены");
console.log("✓ Рабочий API и пользовательские сценарии сохранены");
console.log("✓ Расписание сохранено: 186 дат, 583 окна");
