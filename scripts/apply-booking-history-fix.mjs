import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";

const appPath = "src/creacloud-app.tsx";
const cssPath = "src/globals.css";
const testPath = "tests/mobile-platform.spec.mjs";

let app = await readFile(appPath, "utf8");
let css = await readFile(cssPath, "utf8");
let test = await readFile(testPath, "utf8");

function replaceOnce(source, before, after, label) {
  assert.ok(source.includes(before), `Не найден фрагмент: ${label}`);
  const next = source.replace(before, after);
  assert.notEqual(next, source, `Не применено изменение: ${label}`);
  return next;
}

app = replaceOnce(
  app,
  `          const disabled =\n            cell.date < BOOKING_START ||\n            cell.date < DEMO_TODAY ||\n            cell.date > SEASON_END ||\n            scheduled.length === 0;`,
  `          const disabled =\n            cell.date < BOOKING_START ||\n            cell.date > SEASON_END ||\n            scheduled.length === 0;`,
  "прошедшие даты доступны для просмотра",
);

app = replaceOnce(
  app,
  `                selectedDate === cell.date ? "is-selected" : "",\n                scheduled.length ? "has-tours" : "",`,
  `                selectedDate === cell.date ? "is-selected" : "",\n                cell.date < DEMO_TODAY ? "is-past" : "",\n                scheduled.length ? "has-tours" : "",`,
  "класс архивной даты",
);

app = replaceOnce(
  app,
  `  const schedule = SCHEDULE[selectedDate] ?? [];\n  const selectedWeather: WeatherDay | undefined = forecast[selectedDate];`,
  `  const schedule = SCHEDULE[selectedDate] ?? [];\n  const isHistoricalDate = selectedDate < DEMO_TODAY;\n  const selectedWeather: WeatherDay | undefined = forecast[selectedDate];`,
  "признак архивной даты",
);

app = replaceOnce(
  app,
  `            <small>{view === "transfer" ? "Новая дата" : "Выбранная дата"}</small>`,
  `            <small>\n              {view === "transfer"\n                ? "Новая дата"\n                : isHistoricalDate\n                  ? "История бронирований"\n                  : "Выбранная дата"}\n            </small>`,
  "заголовок истории бронирований",
);

app = replaceOnce(
  app,
  `                disabled={Boolean(occupant)}`,
  `                disabled={Boolean(occupant) || isHistoricalDate}`,
  "запрет бронирования прошедшего тура",
);

app = replaceOnce(
  app,
  `                  <small>{occupant ? \`Занято · \${occupant.creator}\` : "Свободно"}</small>`,
  `                  <small>\n                    {occupant\n                      ? \`Занято · \${occupant.creator}\`\n                      : isHistoricalDate\n                        ? "Нет записи"\n                        : "Свободно"}\n                  </small>`,
  "подпись архивного тура",
);

app = replaceOnce(
  app,
  `          <button\n            className="primary-button"\n            disabled={busy}\n            onClick={() => onSubmit("whatsapp")}\n          >\n            {busy\n              ? "Сохраняем..."`,
  `          <button\n            className="primary-button"\n            disabled={busy || isHistoricalDate}\n            onClick={() => onSubmit("whatsapp")}\n          >\n            {isHistoricalDate\n              ? "Архивная дата"\n              : busy\n                ? "Сохраняем..."`,
  "кнопка архивной даты",
);

app = replaceOnce(
  app,
  `          <button\n            className="booking-call-button"\n            disabled={busy}\n            onClick={() => onSubmit("call")}`,
  `          <button\n            className="booking-call-button"\n            disabled={busy || isHistoricalDate}\n            onClick={() => onSubmit("call")}`,
  "запрет звонка для архивной даты",
);

css = replaceOnce(
  css,
  `.calendar-grid > button.is-selected {\n  background: var(--lime);\n  font-weight: 800;\n}`,
  `.calendar-grid > button.is-past {\n  background: rgba(21, 23, 20, 0.045);\n  color: rgba(21, 23, 20, 0.58);\n}\n\n.calendar-grid > button.is-past i {\n  background: rgba(118, 87, 246, 0.5);\n}\n\n.calendar-grid > button.is-selected {\n  background: var(--lime);\n  color: var(--ink);\n  font-weight: 800;\n}`,
  "оформление архивных дат",
);

test = replaceOnce(
  test,
  `  await expect(bookingDialog).toContainText("Обновляется автоматически");\n  await assertNoHorizontalOverflow(page);\n  await closeModal(page);`,
  `  await expect(bookingDialog).toContainText("Обновляется автоматически");\n\n  const archivedDate = bookingDialog.getByRole("button", { name: /27 число/ });\n  await expect(archivedDate).toBeEnabled();\n  await archivedDate.click();\n  await expect(bookingDialog).toContainText("История бронирований");\n  await expect(bookingDialog).toContainText("Занято · @older_creator");\n  await expect(\n    bookingDialog.getByRole("button", { name: "Архивная дата" }),\n  ).toBeDisabled();\n\n  await assertNoHorizontalOverflow(page);\n  await closeModal(page);`,
  "мобильная проверка истории бронирований",
);

await Promise.all([
  writeFile(appPath, app),
  writeFile(cssPath, css),
  writeFile(testPath, test),
]);

console.log("История бронирований восстановлена без изменения данных и правил записи.");
