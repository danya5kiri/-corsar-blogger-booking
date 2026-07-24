const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");

const baseUrl = process.env.SITE_URL || "http://127.0.0.1:4173";
const outputDir = path.resolve("artifacts/refinement-smoke");
fs.mkdirSync(outputDir, { recursive: true });

function weatherPayload(){
  const dates = [];
  const start = Date.UTC(2026, 6, 20);
  for(let i = 0; i < 16; i++) dates.push(new Date(start + i * 86400000).toISOString().slice(0, 10));
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

function rgbaIsLight(value){
  const values = String(value || "").match(/[\d.]+/g) || [];
  return values.length >= 3 && Number(values[0]) > 230 && Number(values[1]) > 230 && Number(values[2]) > 230;
}

async function preparePage(browser, mode, viewport){
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: "no-preference" });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
  page.on("console", message => {
    if(message.type() !== "error") return;
    const text = message.text();
    if(/Failed to load resource|ERR_FAILED|fonts\.(googleapis|gstatic)/i.test(text)) return;
    errors.push(`console: ${text}`);
  });

  let firstJsonp = true;
  await page.route("**/script.google.com/**", async route => {
    const request = route.request();
    if(request.method() !== "GET"){
      await new Promise(resolve => setTimeout(resolve, 180));
      await route.fulfill({ status: 204, body: "" });
      return;
    }
    const url = new URL(request.url());
    const callback = url.searchParams.get("callback") || "callback";
    if(firstJsonp){
      firstJsonp = false;
      await new Promise(resolve => setTimeout(resolve, 900));
    }
    await route.fulfill({ status: 200, contentType: "application/javascript; charset=utf-8", body: `${callback}([]);` });
  });
  await page.route("**/api.open-meteo.com/**", route => route.fulfill({
    status: 200,
    contentType: "application/json; charset=utf-8",
    body: JSON.stringify(weatherPayload())
  }));
  await page.route("**/fonts.googleapis.com/**", route => route.fulfill({ status: 200, contentType: "text/css", body: "" }));
  await page.route("**/fonts.gstatic.com/**", route => route.fulfill({ status: 204, body: "" }));

  await page.goto(`${baseUrl}/index.html?design=${mode}`, { waitUntil: "domcontentloaded" });
  return { context, page, errors };
}

async function inspectInitialSplash(page, mode, viewport, name){
  await page.waitForSelector("#cb-splash:not(.is-hidden)");
  await page.waitForTimeout(120);
  const result = await page.evaluate(() => {
    const splash = document.getElementById("cb-splash");
    const legacy = document.querySelector(".cb-splash-legacy");
    const redesign = document.querySelector(".cb-splash-redesign");
    const logo = document.querySelector(".cb-splash-logo");
    function rect(element){
      if(!element) return null;
      const value = element.getBoundingClientRect();
      return { left: value.left, right: value.right, top: value.top, bottom: value.bottom, width: value.width, height: value.height, centerX: value.left + value.width / 2, centerY: value.top + value.height / 2 };
    }
    return {
      viewport: { width: document.documentElement.clientWidth, height: window.innerHeight },
      splash: rect(splash),
      logo: rect(logo),
      legacyVisible: legacy ? getComputedStyle(legacy).display !== "none" : false,
      redesignVisible: redesign ? getComputedStyle(redesign).display !== "none" : false
    };
  });

  if(mode === "redesign"){
    if(!result.redesignVisible || result.legacyVisible) throw new Error(`${name}: redesign splash visibility is incorrect`);
    if(!result.logo) throw new Error(`${name}: redesign logo is missing`);
    if(result.logo.left < -1 || result.logo.right > viewport.width + 1) throw new Error(`${name}: splash logo leaves viewport ${JSON.stringify(result.logo)}`);
    if(Math.abs(result.logo.centerX - viewport.width / 2) > 3) throw new Error(`${name}: splash logo is not centered`);
    if(result.splash.top < -1 || result.splash.bottom > viewport.height + 1) throw new Error(`${name}: splash leaves safe viewport`);
  } else if(!result.legacyVisible || result.redesignVisible){
    throw new Error(`${name}: legacy splash visibility is incorrect`);
  }

  await page.screenshot({ path: path.join(outputDir, `${name}-splash.png`), fullPage: false });
}

async function inspectLoadedPage(page, mode, viewport, name){
  await page.waitForFunction(() => !document.body.classList.contains("cb-lock-scroll"), null, { timeout: 15000 });
  await page.waitForSelector("#cb-splash.is-hidden", { timeout: 15000 });
  await page.waitForTimeout(350);

  const result = await page.evaluate(() => {
    const ids = ["home", "calendar", "booking", "content", "ranking", "results", "creator-profile", "creacloud"];
    const viewportWidth = document.documentElement.clientWidth;
    const elements = ids.map(id => document.getElementById(id));
    const rect = element => {
      if(!element) return null;
      const value = element.getBoundingClientRect();
      return { left: value.left, right: value.right, top: value.top, bottom: value.bottom, width: value.width, height: value.height };
    };
    const nav = document.querySelector(".cb-sticky-nav");
    const activeNav = document.querySelector(".cb-nav-links a.is-active");
    const hero = document.querySelector(".cb-hero");
    const title = document.querySelector(".cb-hero-title");
    const weatherCard = document.querySelector(".cb-hero-stats > .cb-stat-card:first-child");
    const weatherTemp = document.querySelector(".cb-weather-temp");
    const weatherNumber = document.querySelector(".cb-weather-number");
    const weatherIcon = weatherTemp && weatherTemp.querySelector(".cb-weather-icon");
    const leader = document.querySelector(".cb-leaders-track .cb-leader-card");
    const eventsHead = document.querySelector(".cb-recent-events .cb-activity-head");
    const storyAdd = document.querySelector(".cb-story-add-card");
    const day = document.querySelector(".cb-day");
    const bookingActions = document.querySelector(".cb-booking-actions");
    const whatsapp = document.getElementById("cb-submit");
    const call = document.getElementById("cb-call-submit");
    const heading = document.querySelector("#creator-profile .cb-section-title");
    const overflow = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - viewportWidth;
    const outOfBounds = elements.filter(Boolean).map(element => ({ id: element.id, ...rect(element) })).filter(item => item.left < -2 || item.right > viewportWidth + 2);
    return {
      design: document.documentElement.getAttribute("data-design"),
      missing: ids.filter((id, index) => !elements[index]),
      overflow,
      outOfBounds,
      navBackground: nav ? getComputedStyle(nav).backgroundColor : "",
      navColor: nav ? getComputedStyle(nav).color : "",
      activeBackground: activeNav ? getComputedStyle(activeNav).backgroundColor : "",
      heroBackground: hero ? getComputedStyle(hero).backgroundImage : "",
      heroColor: hero ? getComputedStyle(hero).color : "",
      titleColor: title ? getComputedStyle(title).color : "",
      weatherBackground: weatherCard ? getComputedStyle(weatherCard).backgroundImage : "",
      weatherCard: rect(weatherCard),
      weatherTemp: rect(weatherTemp),
      weatherNumber: rect(weatherNumber),
      weatherIcon: rect(weatherIcon),
      leaderRadius: leader ? getComputedStyle(leader).borderRadius : "",
      eventRadius: eventsHead ? getComputedStyle(eventsHead).borderRadius : "",
      storyRadius: storyAdd ? getComputedStyle(storyAdd).borderRadius : "missing",
      dayRadius: day ? getComputedStyle(day).borderRadius : "",
      bookingActions: rect(bookingActions),
      whatsapp: rect(whatsapp),
      call: rect(call),
      heading: heading ? heading.textContent.trim().replace(/\s+/g, " ") : "",
      navLabels: Array.from(document.querySelectorAll(".cb-nav-links a")).map(a => a.textContent.trim())
    };
  });

  if(result.design !== mode) throw new Error(`${name}: mode ${result.design} instead of ${mode}`);
  if(result.missing.length) throw new Error(`${name}: missing ${result.missing.join(", ")}`);
  if(result.overflow > 2) throw new Error(`${name}: horizontal overflow ${result.overflow}px`);
  if(result.outOfBounds.length) throw new Error(`${name}: sections out of bounds ${JSON.stringify(result.outOfBounds)}`);
  if(JSON.stringify(result.navLabels) !== JSON.stringify(["Главная", "Календарь", "Запись", "Контент", "Рейтинг", "Итоги"])) throw new Error(`${name}: navigation changed`);

  if(mode === "redesign"){
    if(!rgbaIsLight(result.navBackground)) throw new Error(`${name}: navigation is not light ${result.navBackground}`);
    if(!/217, 255, 82/.test(result.activeBackground)) throw new Error(`${name}: active navigation is not lime ${result.activeBackground}`);
    if(!/rgb\(21, 23, 20\)/.test(result.titleColor)) throw new Error(`${name}: hero title is not dark ${result.titleColor}`);
    if(!/#ffffff|rgb\(255, 255, 255\)/i.test(result.heroBackground) && !/linear-gradient/.test(result.heroBackground)) throw new Error(`${name}: hero background is missing`);
    if(!/244, 255, 209|#f4ffd1/i.test(result.weatherBackground)) throw new Error(`${name}: weather card is not light ${result.weatherBackground}`);
    if(result.leaderRadius !== "14px") throw new Error(`${name}: leader radius ${result.leaderRadius}`);
    if(result.dayRadius !== "7px") throw new Error(`${name}: day radius ${result.dayRadius}`);
    if(result.storyRadius !== "14px") throw new Error(`${name}: story add radius ${result.storyRadius}`);
    if(result.heading !== "ЛК креатора") throw new Error(`${name}: creator cabinet heading ${result.heading}`);
    if(!result.weatherCard || !result.weatherIcon || result.weatherIcon.right > result.weatherCard.right - 10) throw new Error(`${name}: weather icon leaves card`);
    if(result.weatherNumber && result.weatherIcon.left - result.weatherNumber.right > 24) throw new Error(`${name}: weather icon is too far from temperature`);
    if(!result.whatsapp || !result.call) throw new Error(`${name}: booking action buttons are missing`);
    const sameRow = Math.abs(result.whatsapp.top - result.call.top) < 3;
    if(viewport.width > 900 && !sameRow) throw new Error(`${name}: desktop booking buttons are not on one row`);
    if(viewport.width <= 600 && sameRow) throw new Error(`${name}: mobile booking buttons should stack`);

    await page.evaluate(() => window.scrollTo(0, Math.min(document.body.scrollHeight - window.innerHeight, 1700)));
    await page.waitForTimeout(300);
    const hidden = await page.locator(".cb-sticky-nav").evaluate(nav => nav.classList.contains("is-scroll-hidden"));
    if(!hidden) throw new Error(`${name}: navigation does not hide on downward scroll`);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    const visibleAgain = await page.locator(".cb-sticky-nav").evaluate(nav => !nav.classList.contains("is-scroll-hidden"));
    if(!visibleAgain) throw new Error(`${name}: navigation does not return on upward scroll`);
  }

  await page.screenshot({ path: path.join(outputDir, `${name}.png`), fullPage: true });
  console.log(`✓ ${name}: ${mode}, ${viewport.width}x${viewport.height}, no overflow`);
}

async function runCase(browser, mode, viewport, name){
  const { context, page, errors } = await preparePage(browser, mode, viewport);
  try {
    await inspectInitialSplash(page, mode, viewport, name);
    await inspectLoadedPage(page, mode, viewport, name);
    if(errors.length) throw new Error(`${name}: browser errors: ${errors.join(" | ")}`);
  } finally {
    await context.close();
  }
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
