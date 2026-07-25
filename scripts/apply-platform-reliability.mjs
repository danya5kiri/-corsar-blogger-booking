import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";

async function load(path) {
  return readFile(path, "utf8");
}

async function save(path, content) {
  await writeFile(path, content, "utf8");
}

function replaceOnce(content, before, after, label) {
  const count = content.split(before).length - 1;
  assert.equal(count, 1, `${label}: expected one match, found ${count}`);
  return content.replace(before, after);
}

function replaceRegex(content, pattern, after, label) {
  const matches = content.match(new RegExp(pattern.source, pattern.flags.includes("g") ? pattern.flags : `${pattern.flags}g`)) ?? [];
  assert.equal(matches.length, 1, `${label}: expected one match, found ${matches.length}`);
  return content.replace(pattern, after);
}

const appPath = "src/creacloud-app.tsx";
const dataPath = "src/creacloud-data.ts";
const apiPath = "src/creacloud-api.ts";
const mainPath = "src/main.tsx";

let app = await load(appPath);
let data = await load(dataPath);
let api = await load(apiPath);
let main = await load(mainPath);

if (app.includes("PORTAL_TRANSITION_MIN_MS")) {
  console.log("Platform reliability patches are already applied.");
  process.exit(0);
}

app = replaceOnce(
  app,
  `const TEAM_DAILY_NOTICE_KEY = "creacloud-main-team-daily-notice-v3";\nconst RECENT_WRITE_TTL = 15 * 60 * 1000;\nconst AUTO_SYNC_INTERVAL_MS = 45 * 1000;\nconst AUTO_SYNC_MIN_GAP_MS = 5 * 1000;\nconst POST_WRITE_SYNC_DELAYS = [1800, 5200, 12_000] as const;`,
  `const TEAM_DAILY_NOTICE_KEY = "creacloud-main-team-daily-notice-v4";\nconst RECENT_WRITE_TTL = 15 * 60 * 1000;\nconst AUTO_SYNC_INTERVAL_MS = 30 * 1000;\nconst AUTO_SYNC_MIN_GAP_MS = 5 * 1000;\nconst WEATHER_REFRESH_INTERVAL_MS = 15 * 60 * 1000;\nconst WEATHER_REFRESH_MIN_GAP_MS = 60 * 1000;\nconst PORTAL_TRANSITION_MIN_MS = 720;\nconst PORTAL_DATA_WAIT_MS = 3_200;\nconst POST_WRITE_SYNC_DELAYS = [650, 1800, 5200, 12_000] as const;`,
  "sync and transition constants",
);

app = replaceOnce(
  app,
  `function completeWorkingState(next: WorkingState): WorkingState {\n  const creators = [\n    ...new Set(\n      [\n        ...(next.creators ?? []),\n        ...next.bookings.map((booking) => booking.creator),\n        ...next.content.map((item) => item.creator),\n      ]\n        .map(normalizeCreator)\n        .filter((creator) => creator && !isDeletedCreator(creator)),\n    ),\n  ].sort((a, b) => a.localeCompare(b, "ru"));\n  return { ...next, creators };\n}`,
  `function completeWorkingState(next: WorkingState): WorkingState {\n  const bookings = next.bookings.map((booking, index) => ({\n    ...booking,\n    sourceOrder: Number.isFinite(booking.sourceOrder)\n      ? booking.sourceOrder\n      : index,\n  }));\n  const content = next.content.map((item, index) => ({\n    ...item,\n    sourceOrder: Number.isFinite(item.sourceOrder)\n      ? item.sourceOrder\n      : bookings.length + index,\n  }));\n  const creators = [\n    ...new Set(\n      [\n        ...(next.creators ?? []),\n        ...bookings.map((booking) => booking.creator),\n        ...content.map((item) => item.creator),\n      ]\n        .map(normalizeCreator)\n        .filter((creator) => creator && !isDeletedCreator(creator)),\n    ),\n  ].sort((a, b) => a.localeCompare(b, "ru"));\n  return { ...next, bookings, content, creators };\n}\n\nfunction nextSourceOrder(state: WorkingState) {\n  return (\n    Math.max(\n      -1,\n      ...state.bookings.map((booking) => booking.sourceOrder ?? -1),\n      ...state.content.map((item) => item.sourceOrder ?? -1),\n    ) + 1\n  );\n}`,
  "working state completion",
);

app = replaceRegex(
  app,
  /function Splash\(\{ hidden \}: \{ hidden: boolean \}\) \{[\s\S]*?\n\}\n\ntype InteractionAura/,
  `function Splash({\n  hidden,\n  light = false,\n}: {\n  hidden: boolean;\n  light?: boolean;\n}) {\n  const phrases = useMemo(\n    () =>\n      light\n        ? [\n            "обновляем рабочую базу",\n            "проверяем свободные места",\n            "готовим ежедневную сводку",\n          ]\n        : [\n            "собираем креаторов",\n            "вдохновляем креаторов",\n            "респектуем креаторам",\n          ],\n    [light],\n  );\n  const [phraseIndex, setPhraseIndex] = useState(0);\n  const [visibleChars, setVisibleChars] = useState(0);\n  const [erasing, setErasing] = useState(false);\n  const phrase = phrases[phraseIndex] ?? phrases[0];\n\n  useEffect(() => {\n    setPhraseIndex(0);\n    setVisibleChars(0);\n    setErasing(false);\n  }, [light]);\n\n  useEffect(() => {\n    const isComplete = visibleChars >= phrase.length;\n    const isEmpty = visibleChars <= 0;\n    const delay = erasing ? 38 : isComplete ? 620 : 64;\n    const timer = window.setTimeout(() => {\n      if (!erasing && isComplete) {\n        setErasing(true);\n        return;\n      }\n      if (erasing && isEmpty) {\n        setErasing(false);\n        setPhraseIndex((current) => (current + 1) % phrases.length);\n        return;\n      }\n      setVisibleChars((current) => current + (erasing ? -1 : 1));\n    }, delay);\n    return () => window.clearTimeout(timer);\n  }, [erasing, phrase.length, phrases.length, visibleChars]);\n\n  return (\n    <div\n      className={\`splash\${light ? " splash--light" : ""}\${\n        hidden ? " splash--hidden" : ""\n      }\`}\n      aria-hidden={hidden}\n      role="status"\n      aria-live="polite"\n    >\n      <div className="splash__stage">\n        <div className="splash__logo" aria-label="CREACLOUD">\n          <strong>CREA</strong>\n          <span>CLOUD</span>\n        </div>\n        <div className="splash__typing">\n          <span className="splash__pulse" aria-hidden="true" />\n          <p>{phrase.slice(0, visibleChars)}</p>\n          <span className="splash__caret" aria-hidden="true" />\n        </div>\n      </div>\n    </div>\n  );\n}\n\ntype InteractionAura`,
  "splash component",
);

app = replaceOnce(
  app,
  `function Welcome({ onEnter }: { onEnter: () => void }) {`,
  `function Welcome({\n  onEnter,\n  busy,\n}: {\n  onEnter: () => void;\n  busy: boolean;\n}) {`,
  "welcome props",
);

app = replaceOnce(
  app,
  `<button className="status-card status-card--team" onClick={onEnter}>\n            <span className="status-card__index">02</span>\n            <SplitTitle strong="Я уже" light="в команде" as="h2" />\n            <p>Открыть дашборд CREACLOUD</p>`,
  `<button\n            className="status-card status-card--team"\n            onClick={onEnter}\n            disabled={busy}\n            aria-busy={busy}\n          >\n            <span className="status-card__index">02</span>\n            <SplitTitle strong="Я уже" light="в команде" as="h2" />\n            <p>{busy ? "Обновляем данные площадки..." : "Открыть дашборд CREACLOUD"}</p>`,
  "team entry button",
);

app = replaceRegex(
  app,
  /type RecentTourEvent = \{[\s\S]*?\n\}\n\nfunction NoticesPanel/,
  `type RecentTourEvent = {\n  id: string;\n  kind: "booking" | "content";\n  creator: string;\n  tourName: string;\n  date: string;\n  createdAt: string;\n  sourceOrder: number;\n};\n\nfunction getRecentTourEvents(state: WorkingState) {\n  const events: RecentTourEvent[] = [\n    ...state.bookings.map((booking, index) => ({\n      id: \`booking-\${booking.id}\`,\n      kind: "booking" as const,\n      creator: booking.creator,\n      tourName: booking.tourName,\n      date: booking.date,\n      createdAt: booking.createdAt,\n      sourceOrder: booking.sourceOrder ?? index,\n    })),\n    ...state.content.map((item, index) => ({\n      id: \`content-\${item.id}\`,\n      kind: "content" as const,\n      creator: item.creator,\n      tourName: item.tourName,\n      date: item.date,\n      createdAt: item.createdAt,\n      sourceOrder: item.sourceOrder ?? state.bookings.length + index,\n    })),\n  ];\n\n  return events\n    .sort((a, b) => {\n      if (a.sourceOrder !== b.sourceOrder) return b.sourceOrder - a.sourceOrder;\n      const aTimestamp = Date.parse(a.createdAt);\n      const bTimestamp = Date.parse(b.createdAt);\n      if (Number.isFinite(aTimestamp) || Number.isFinite(bTimestamp)) {\n        return (Number.isFinite(bTimestamp) ? bTimestamp : 0) -\n          (Number.isFinite(aTimestamp) ? aTimestamp : 0);\n      }\n      return b.date.localeCompare(a.date);\n    })\n    .slice(0, 5);\n}\n\nfunction NoticesPanel`,
  "recent events ordering",
);

app = replaceOnce(
  app,
  `  const [loading, setLoading] = useState(true);\n  const [entered, setEntered] = useState(false);`,
  `  const [loading, setLoading] = useState(true);\n  const [portalLoading, setPortalLoading] = useState(false);\n  const [entered, setEntered] = useState(false);`,
  "portal loading state",
);

app = replaceOnce(
  app,
  `  const cacheSavedAtRef = useRef(0);\n  const reconciliationTimersRef = useRef<number[]>([]);`,
  `  const cacheSavedAtRef = useRef(0);\n  const reconciliationTimersRef = useRef<number[]>([]);\n  const weatherInFlightRef = useRef<Promise<void> | null>(null);\n  const lastWeatherStartedAtRef = useRef(0);`,
  "weather refs",
);

app = replaceOnce(
  app,
  `  function clearReconciliationTimers() {`,
  `  async function refreshWeather({\n    force = false,\n  }: {\n    force?: boolean;\n  } = {}) {\n    if (weatherInFlightRef.current) return weatherInFlightRef.current;\n    const now = nowTimestamp();\n    if (\n      !force &&\n      now - lastWeatherStartedAtRef.current < WEATHER_REFRESH_MIN_GAP_MS\n    ) {\n      return;\n    }\n\n    lastWeatherStartedAtRef.current = now;\n    const request = fetchVladivostokWeather()\n      .then((next) => {\n        setWeather(next.current);\n        setWeatherForecast(next.forecast);\n      })\n      .catch(() => {\n        // Keep the last successful weather snapshot.\n      })\n      .finally(() => {\n        if (weatherInFlightRef.current === request) {\n          weatherInFlightRef.current = null;\n        }\n      });\n    weatherInFlightRef.current = request;\n    return request;\n  }\n\n  function clearReconciliationTimers() {`,
  "weather refresh function",
);

app = replaceOnce(
  app,
  `  const refreshWorkingDataRef = useRef(refreshWorkingData);\n\n  useEffect(() => {\n    refreshWorkingDataRef.current = refreshWorkingData;\n  });`,
  `  const refreshWorkingDataRef = useRef(refreshWorkingData);\n  const refreshWeatherRef = useRef(refreshWeather);\n\n  useEffect(() => {\n    refreshWorkingDataRef.current = refreshWorkingData;\n    refreshWeatherRef.current = refreshWeather;\n  });`,
  "refresh refs",
);

app = replaceOnce(
  app,
  `    window.addEventListener("focus", synchronizeVisiblePage);\n    window.addEventListener("online", synchronizeVisiblePage);\n    window.addEventListener("storage", onStorage);`,
  `    window.addEventListener("focus", synchronizeVisiblePage);\n    window.addEventListener("online", synchronizeVisiblePage);\n    window.addEventListener("pageshow", synchronizeVisiblePage);\n    window.addEventListener("storage", onStorage);`,
  "pageshow sync listener",
);

app = replaceOnce(
  app,
  `      window.removeEventListener("focus", synchronizeVisiblePage);\n      window.removeEventListener("online", synchronizeVisiblePage);\n      window.removeEventListener("storage", onStorage);`,
  `      window.removeEventListener("focus", synchronizeVisiblePage);\n      window.removeEventListener("online", synchronizeVisiblePage);\n      window.removeEventListener("pageshow", synchronizeVisiblePage);\n      window.removeEventListener("storage", onStorage);`,
  "pageshow sync cleanup",
);

app = replaceOnce(
  app,
  `  useEffect(() => {\n    let cancelled = false;\n    const startedAt = Date.now();`,
  `  useEffect(() => {\n    const synchronizeWeather = () => {\n      if (document.visibilityState === "visible") {\n        void refreshWeatherRef.current();\n      }\n    };\n    const interval = window.setInterval(\n      synchronizeWeather,\n      WEATHER_REFRESH_INTERVAL_MS,\n    );\n    window.addEventListener("focus", synchronizeWeather);\n    window.addEventListener("online", synchronizeWeather);\n    window.addEventListener("pageshow", synchronizeWeather);\n    document.addEventListener("visibilitychange", synchronizeWeather);\n    return () => {\n      window.clearInterval(interval);\n      window.removeEventListener("focus", synchronizeWeather);\n      window.removeEventListener("online", synchronizeWeather);\n      window.removeEventListener("pageshow", synchronizeWeather);\n      document.removeEventListener("visibilitychange", synchronizeWeather);\n    };\n  }, []);\n\n  useEffect(() => {\n    let cancelled = false;\n    const startedAt = Date.now();`,
  "automatic weather synchronization",
);

app = replaceRegex(
  app,
  /    const weatherRequest = fetchVladivostokWeather\(\)[\s\S]*?      \}\);/,
  `    const weatherRequest = refreshWeatherRef.current({ force: true });`,
  "initial weather request",
);

app = replaceRegex(
  app,
  /  function enterTeamPortal\(\) \{[\s\S]*?\n  \}\n\n  function openBooking/,
  `  async function enterTeamPortal() {\n    if (portalLoading) return;\n    const startedAt = Date.now();\n    let showDailyNotice = true;\n    try {\n      showDailyNotice =\n        window.localStorage.getItem(TEAM_DAILY_NOTICE_KEY) !== DEMO_TODAY;\n    } catch {\n      // The notification remains available when browser storage is unavailable.\n    }\n\n    setPortalLoading(true);\n    const synchronization = Promise.allSettled([\n      refreshWorkingData({ force: true }),\n      refreshWeather({ force: true }),\n    ]);\n    await Promise.race([\n      synchronization,\n      new Promise((resolve) => window.setTimeout(resolve, PORTAL_DATA_WAIT_MS)),\n    ]);\n    const remaining = Math.max(\n      0,\n      PORTAL_TRANSITION_MIN_MS - (Date.now() - startedAt),\n    );\n    if (remaining) {\n      await new Promise((resolve) => window.setTimeout(resolve, remaining));\n    }\n\n    setEntered(true);\n    if (showDailyNotice) {\n      setPanel("notices");\n      try {\n        window.localStorage.setItem(TEAM_DAILY_NOTICE_KEY, DEMO_TODAY);\n      } catch {\n        // Opening the notice must not depend on local storage.\n      }\n    } else {\n      setPanel(null);\n    }\n    window.requestAnimationFrame(() => setPortalLoading(false));\n  }\n\n  function openBooking`,
  "team portal entry",
);

app = replaceOnce(
  app,
  `        {selectedWeather && (\n          <div className="selected-date-weather" aria-label="Прогноз погоды">\n            <span className="selected-date-weather__icon" aria-hidden="true">\n              {selectedWeather.icon}\n            </span>\n            <div>\n              <strong>{selectedWeather.label}</strong>\n              <span>\n                {selectedWeather.temperatureMin}…{selectedWeather.temperatureMax}\n              </span>\n            </div>\n            <small>Владивосток</small>\n          </div>\n        )}`,
  `        {selectedWeather ? (\n          <div className="selected-date-weather" aria-label="Прогноз погоды">\n            <span className="selected-date-weather__icon" aria-hidden="true">\n              {selectedWeather.icon}\n            </span>\n            <div>\n              <strong>{selectedWeather.label}</strong>\n              <span>\n                {selectedWeather.temperatureMin}…{selectedWeather.temperatureMax}\n              </span>\n            </div>\n            <small>Обновляется автоматически</small>\n          </div>\n        ) : (\n          <div\n            className="selected-date-weather is-pending"\n            aria-label="Прогноз пока недоступен"\n          >\n            <span className="selected-date-weather__icon" aria-hidden="true">\n              ◌\n            </span>\n            <div>\n              <strong>Прогноз появится ближе к дате</strong>\n              <span>Проверяем погоду каждые 15 минут</span>\n            </div>\n            <small>Владивосток</small>\n          </div>\n        )}`,
  "weather fallback in booking",
);

app = replaceOnce(
  app,
  `        status: "active",\n        createdAt: new Date().toISOString(),`,
  `        status: "active",\n        createdAt: new Date().toISOString(),\n        sourceOrder: nextSourceOrder(latest),`,
  "optimistic booking order",
);

app = replaceOnce(
  app,
  `        content: [optimistic, ...latest.content],`,
  `        content: [\n          { ...optimistic, sourceOrder: nextSourceOrder(latest) },\n          ...latest.content,\n        ],`,
  "optimistic content order",
);

app = replaceOnce(
  app,
  `      <Splash hidden={!loading} />\n      {!loading && !entered ? (\n        <Welcome onEnter={enterTeamPortal} />`,
  `      <Splash hidden={!loading && !portalLoading} light={portalLoading} />\n      {!loading && !entered ? (\n        <Welcome onEnter={enterTeamPortal} busy={portalLoading} />`,
  "render transition splash",
);

data = replaceOnce(
  data,
  `  status: "active";\n  createdAt: string;`,
  `  status: "active";\n  createdAt: string;\n  sourceOrder?: number;`,
  "booking source order type",
);

data = replaceOnce(
  data,
  `  link: string;\n  createdAt: string;`,
  `  link: string;\n  createdAt: string;\n  sourceOrder?: number;`,
  "content source order type",
);

data = replaceRegex(
  data,
  /export function normalizeDate\(value: unknown\) \{[\s\S]*?\n\}/,
  `export function normalizeDate(value: unknown) {\n  if (!value) return "";\n  const text = String(value).trim();\n  const explicitDate = text.match(/^(\\d{4}-\\d{2}-\\d{2})(?:T|\\s|$)/);\n  if (explicitDate) return explicitDate[1];\n\n  const parsed = new Date(text);\n  if (Number.isNaN(parsed.getTime())) return text;\n  try {\n    const parts = new Intl.DateTimeFormat("en-CA", {\n      timeZone: "Asia/Vladivostok",\n      year: "numeric",\n      month: "2-digit",\n      day: "2-digit",\n    }).formatToParts(parsed);\n    const values = Object.fromEntries(\n      parts.map((part) => [part.type, part.value]),\n    );\n    return \`\${values.year}-\${values.month}-\${values.day}\`;\n  } catch {\n    return [\n      parsed.getFullYear(),\n      String(parsed.getMonth() + 1).padStart(2, "0"),\n      String(parsed.getDate()).padStart(2, "0"),\n    ].join("-");\n  }\n}`,
  "timezone-safe date normalization",
);

data = replaceOnce(
  data,
  `    row.nickname,\n    row.previousTelegram,`,
  `    row.nickname,\n    row.username,\n    row.handle,\n    row.login,\n    row.telegramNick,\n    row.previousTelegram,`,
  "creator candidate fields",
);

data = replaceOnce(
  data,
  `  const creators = [\n    ...new Set(`,
  `  const sourceOrder = new Map(\n    prepared.map((row, index) => [row, index] as const),\n  );\n  const creators = [\n    ...new Set(`,
  "source order map",
);

data = replaceOnce(
  data,
  `        status: "active" as const,\n        createdAt: rowCreatedAt(row),`,
  `        status: "active" as const,\n        createdAt: rowCreatedAt(row),\n        sourceOrder: sourceOrder.get(row) ?? -1,`,
  "booking source order value",
);

data = replaceOnce(
  data,
  `        link,\n        createdAt: rowCreatedAt(row),`,
  `        link,\n        createdAt: rowCreatedAt(row),\n        sourceOrder: sourceOrder.get(row) ?? -1,`,
  "content source order value",
);

api = replaceOnce(
  api,
  `  await fetch(API_URL, {\n    method: "POST",\n    mode: "no-cors",\n    body: JSON.stringify(payload),\n  });`,
  `  await fetch(API_URL, {\n    method: "POST",\n    mode: "no-cors",\n    cache: "no-store",\n    keepalive: true,\n    headers: {\n      "Content-Type": "text/plain;charset=UTF-8",\n    },\n    body: JSON.stringify(payload),\n  });`,
  "reliable working payload request",
);

api = replaceOnce(
  api,
  `    date,\n    telegram: creator,\n    tour: tourName,`,
  `    date,\n    telegram: creator,\n    tour: tourName,\n    createdAt: new Date().toISOString(),`,
  "booking timestamp",
);

api = replaceOnce(
  api,
  `      status: "Отмена",\n      operation: "cancel",`,
  `      status: "Отмена",\n      operation: "cancel",\n      createdAt: new Date().toISOString(),`,
  "cancellation timestamp",
);

api = replaceOnce(
  api,
  `    createdAt: new Date().toLocaleString("ru-RU"),`,
  `    createdAt: new Date().toISOString(),`,
  "content timestamp",
);

api = replaceOnce(
  api,
  `  url.searchParams.set("timezone", "Asia/Vladivostok");\n  const response = await fetch(url);`,
  `  url.searchParams.set("timezone", "Asia/Vladivostok");\n  url.searchParams.set("_", String(Date.now()));\n  const response = await fetch(url, { cache: "no-store" });`,
  "weather cache bypass",
);

main = replaceOnce(
  main,
  `import "./globals.css";`,
  `import "./globals.css";\nimport "./reliability.css";`,
  "reliability stylesheet import",
);

await Promise.all([
  save(appPath, app),
  save(dataPath, data),
  save(apiPath, api),
  save(mainPath, main),
]);

console.log("Applied CREACLOUD platform reliability patches.");
