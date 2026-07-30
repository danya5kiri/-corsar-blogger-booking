import { test, expect } from "@playwright/test";

// Regression coverage: archived calendar dates remain viewable but not bookable.
const bookingRows = [
  {
    date: "2026-07-27T07:00:00.000Z",
    telegram: "@older_creator",
    tour: "Барбекю на островах",
    status: "Новая заявка",
  },
  {
    date: "2026-08-05T07:00:00.000Z",
    telegram: "@katerinamanko.ru",
    tour: "Путешествие на остров Рикорда",
    status: "Новая заявка",
  },
  {
    date: "2026-08-06T07:00:00.000Z",
    telegram: "@mobile_creator_2",
    tour: "Путешествие на остров Русский",
    status: "Новая заявка",
  },
  {
    date: "2026-08-07T07:00:00.000Z",
    telegram: "@mobile_creator_3",
    tour: "Путешествие на остров Шкота",
    status: "Новая заявка",
  },
  {
    date: "2026-08-08T07:00:00.000Z",
    telegram: "@mobile_creator_4",
    tour: "Прогулка «Архипелаг»",
    status: "Новая заявка",
  },
];

const contentRows = Array.from({ length: 6 }, (_, index) => ({
  type: "content_report",
  telegram: `@content_creator_${index + 1}`,
  date: "2026-07-22T07:00:00.000Z",
  tour: "Вечерний круиз на яхте с саксофоном",
  link: `https://example.com/post-${index + 1}`,
  matchStatus: "Есть запись",
  createdAt: `2026-07-${String(20 + index).padStart(2, "0")}T10:00:00.000Z`,
}));

const workingRows = [...bookingRows, ...contentRows];
const creatorCount = new Set(
  workingRows.map((row) => row.telegram).filter(Boolean),
).size;

function weatherPayload() {
  const dates = Array.from({ length: 16 }, (_, index) => {
    const date = new Date(Date.UTC(2026, 6, 25 + index));
    return date.toISOString().slice(0, 10);
  });
  return {
    current: {
      time: "2026-07-25T14:00",
      temperature_2m: 22.4,
      weather_code: 2,
    },
    daily: {
      time: dates,
      weather_code: dates.map(() => 2),
      temperature_2m_max: dates.map((_, index) => 23 + (index % 3)),
      temperature_2m_min: dates.map((_, index) => 17 + (index % 2)),
    },
  };
}

async function closeModal(page) {
  const close = page.getByRole("button", {
    name: "Закрыть и вернуться на главную",
  });
  await expect(close).toBeVisible();
  await close.click();
}

async function assertNoHorizontalOverflow(page) {
  const dimensions = await page.evaluate(() => ({
    viewport: window.innerWidth,
    document: document.documentElement.scrollWidth,
    body: document.body.scrollWidth,
  }));
  expect(dimensions.document).toBeLessThanOrEqual(dimensions.viewport + 1);
  expect(dimensions.body).toBeLessThanOrEqual(dimensions.viewport + 1);
}

test.use({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 3,
});

test("mobile team entry, daily notice, creator search and sections", async ({
  page,
}) => {
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.route("**/script.google.com/macros/**", async (route) => {
    const request = route.request();
    if (request.method() !== "GET") {
      await route.fulfill({ status: 204, body: "" });
      return;
    }
    const url = new URL(request.url());
    const callback = url.searchParams.get("callback") || "creacloudCallback";
    await route.fulfill({
      status: 200,
      contentType: "application/javascript; charset=utf-8",
      body: `${callback}(${JSON.stringify(workingRows)});`,
    });
  });

  await page.route("**/api.open-meteo.com/**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(weatherPayload()),
    });
  });

  await page.goto("http://127.0.0.1:4173/vite-entry.html", {
    waitUntil: "domcontentloaded",
  });

  const teamButton = page.getByRole("button", { name: /Я уже в команде/ });
  await expect(teamButton).toBeVisible({ timeout: 10_000 });
  await assertNoHorizontalOverflow(page);

  await teamButton.click();
  const whiteLoader = page.locator(".splash--light");
  await expect(whiteLoader).toBeVisible();
  await expect(whiteLoader).toContainText("CREACLOUD");

  const noticeDialog = page.getByRole("dialog", {
    name: "Сводка мастерской",
  });
  await expect(noticeDialog).toBeVisible({ timeout: 8_000 });
  await expect(noticeDialog).toContainText("@katerinamanko.ru");
  await expect(noticeDialog).toContainText("Автообновление включено");
  await expect(noticeDialog.getByText("Обновить данные")).toHaveCount(0);
  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.getByRole("button", { name: /^ЛК$/ }).click();
  const profileDialog = page.getByRole("dialog", { name: "ЛК креатора" });
  await expect(profileDialog).toBeVisible();
  const creatorInput = profileDialog.getByRole("combobox", {
    name: "Ник креатора",
  });
  await creatorInput.click();
  const options = profileDialog.locator('[role="listbox"] [role="option"]');
  await expect(options).toHaveCount(creatorCount);
  await creatorInput.fill("katerina");
  await expect(
    profileDialog.getByRole("option", { name: "@katerinamanko.ru" }),
  ).toBeVisible();
  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.getByRole("button", { name: /^Бронь$/ }).click();
  const bookingDialog = page.getByRole("dialog", { name: "Выбрать тур" });
  await expect(bookingDialog).toBeVisible();
  await expect(bookingDialog.locator(".calendar-card")).toBeVisible();
  await expect(bookingDialog.locator(".selected-date-weather")).toBeVisible();
  await expect(bookingDialog).toContainText("Обновляется автоматически");

  const archivedDate = bookingDialog.getByRole("button", { name: /27 число/ });
  await expect(archivedDate).toBeEnabled();
  await archivedDate.click();
  await expect(bookingDialog).toContainText("История бронирований");
  await expect(bookingDialog).toContainText("Занято · @older_creator");
  await expect(
    bookingDialog.getByRole("button", { name: "Архивная дата" }),
  ).toBeDisabled();

  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.getByRole("button", { name: /^Контент$/ }).click();
  await expect(
    page.getByRole("dialog", { name: "Добавить контент" }),
  ).toBeVisible();
  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.locator(".tile--rating").click();
  await expect(
    page.getByRole("dialog", { name: "Рейтинг креаторов" }),
  ).toBeVisible();
  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.locator(".tile--metric").first().click();
  await expect(
    page.getByRole("dialog", { name: "Смотреть результаты" }),
  ).toBeVisible();
  await assertNoHorizontalOverflow(page);
  await closeModal(page);

  await page.reload({ waitUntil: "domcontentloaded" });
  await expect(teamButton).toBeVisible({ timeout: 10_000 });
  await teamButton.click();
  await expect(page.locator(".dashboard")).toBeVisible({ timeout: 8_000 });
  await expect(
    page.getByRole("dialog", { name: "Сводка мастерской" }),
  ).toHaveCount(0);
  await assertNoHorizontalOverflow(page);

  expect(pageErrors).toEqual([]);
});
