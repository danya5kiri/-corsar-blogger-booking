const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");

const baseUrl = process.env.SITE_URL || "http://127.0.0.1:4173";
const outputDir = path.resolve("artifacts/redesign-smoke");
fs.mkdirSync(outputDir, { recursive: true });

function weatherPayload(){
  const dates = [];
  const start = new Date();
  for(let i = 0; i < 16; i++){
    const date = new Date(start.getTime() + i * 86400000);
    dates.push(date.toISOString().slice(0, 10));
  }
  return {
    daily: {
      time: dates,
      weather_code: dates.map((_, i) => i % 4 === 0 ? 61 : 1),
      temperature_2m_max: dates.map((_, i) => 24 + (i % 3)),
      temperature_2m_min: dates.map((_, i) => 18 + (i % 2)),
      apparent_temperature_max: dates.map((_, i) => 25 + (i % 3)),
      precipitation_probability_max: dates.map((_, i) => i % 4 === 0 ? 55 : 12),
      wind_speed_10m_max: dates.map(() => 18),
      wind_gusts_10m_max: dates.map(() => 29)
    }
  };
}

async function runCase(browser, mode, viewport, name){
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: "no-preference" });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
  page.on("console", message => {
    const value = message.text();
    if(message.type() === "error" && !/Failed to load resource:\s*net::ERR_FAILED/i.test(value)) errors.push(`console: ${value}`);
  });

  await page.route("**/script.google.com/**", async route => {
    const url = new URL(route.request().url());
    const callback = url.searchParams.get("callback") || "callback";
    await route.fulfill({ status: 200, contentType: "application/javascript; charset=utf-8", body: `${callback}([]);` });
  });
  await page.route("**/api.open-meteo.com/**", route => route.fulfill({
    status: 200,
    contentType: "application/json; charset=utf-8",
    body: JSON.stringify(weatherPayload())
  }));
  await page.route("**/fonts.googleapis.com/**", route => route.abort());
  await page.route("**/fonts.gstatic.com/**", route => route.abort());

  await page.goto(`${baseUrl}/index.html?design=${mode}`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => !document.body.classList.contains("cb-lock-scroll"), null, { timeout: 15000 });
  await page.waitForSelector("#cb-splash.is-hidden", { timeout: 15000 });
  await page.waitForTimeout(500);

  const result = await page.evaluate(() => {
    const ids = ["home", "calendar", "booking", "content", "ranking", "results", "creator-profile", "creacloud"];
    const elements = ids.map(id => document.getElementById(id));
    const viewportWidth = document.documentElement.clientWidth;
    const overflow = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - viewportWidth;
    const outOfBounds = elements.filter(Boolean).map(el => {
      const rect = el.getBoundingClientRect();
      return { id: el.id, left: rect.left, right: rect.right, width: rect.width };
    }).filter(item => item.left < -2 || item.right > viewportWidth + 2);
    return {
      design: document.documentElement.getAttribute("data-design"),
      missing: ids.filter((id, index) => !elements[index]),
      overflow,
      outOfBounds,
      navLabels: Array.from(document.querySelectorAll(".cb-nav-links a")).map(a => a.textContent.trim()),
      splashLegacyVisible: getComputedStyle(document.querySelector(".cb-splash-legacy")).display !== "none",
      splashRedesignVisible: getComputedStyle(document.querySelector(".cb-splash-redesign")).display !== "none"
    };
  });

  if(result.design !== mode) throw new Error(`${name}: mode ${result.design} instead of ${mode}`);
  if(result.missing.length) throw new Error(`${name}: missing ${result.missing.join(", ")}`);
  if(result.overflow > 2) throw new Error(`${name}: horizontal overflow ${result.overflow}px`);
  if(result.outOfBounds.length) throw new Error(`${name}: sections out of bounds ${JSON.stringify(result.outOfBounds)}`);
  const expectedNav = ["Главная", "Календарь", "Запись", "Контент", "Рейтинг", "Итоги"];
  if(JSON.stringify(result.navLabels) !== JSON.stringify(expectedNav)) throw new Error(`${name}: navigation changed`);
  if(mode === "legacy" && (!result.splashLegacyVisible || result.splashRedesignVisible)) throw new Error(`${name}: incorrect legacy splash`);
  if(mode === "redesign" && (result.splashLegacyVisible || !result.splashRedesignVisible)) throw new Error(`${name}: incorrect redesign splash`);
  if(errors.length) throw new Error(`${name}: browser errors: ${errors.join(" | ")}`);

  await page.screenshot({ path: path.join(outputDir, `${name}.png`), fullPage: true });
  console.log(`✓ ${name}: ${mode}, ${viewport.width}x${viewport.height}, no overflow`);
  await context.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    await runCase(browser, "legacy", { width: 390, height: 844 }, "mobile-legacy");
    await runCase(browser, "redesign", { width: 390, height: 844 }, "mobile-redesign");
    await runCase(browser, "legacy", { width: 1440, height: 1000 }, "desktop-legacy");
    await runCase(browser, "redesign", { width: 1440, height: 1000 }, "desktop-redesign");
  } finally {
    await browser.close();
  }
})();
