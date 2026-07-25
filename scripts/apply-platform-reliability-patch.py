from pathlib import Path
import re


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    next_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one regex match, found {count}")
    return next_text


# Preserve the source order returned by the shared base. It is the only reliable
# recency signal for legacy rows that do not contain a creation timestamp.
data_path = Path("src/creacloud-data.ts")
data = data_path.read_text()
if "sourceOrder?: number" not in data:
    data = replace_once(
        data,
        '  createdAt: string;\n};\n\nexport type ContentItem',
        '  createdAt: string;\n  sourceOrder?: number;\n};\n\nexport type ContentItem',
        "booking source order type",
    )
    data = replace_once(
        data,
        '  createdAt: string;\n};\n\nexport type WorkingState',
        '  createdAt: string;\n  sourceOrder?: number;\n};\n\nexport type WorkingState',
        "content source order type",
    )
    data = replace_once(
        data,
        '    .map((row) => {\n      const creator',
        '    .map((row) => {\n      const sourceOrder = prepared.indexOf(row);\n      const creator',
        "booking source order value",
    )
    data = replace_once(
        data,
        '    .map((row, index) => {\n      const creator',
        '    .map((row, index) => {\n      const sourceOrder = prepared.indexOf(row);\n      const creator',
        "content source order value",
    )
    created_at_pattern = '        createdAt: rowCreatedAt(row),\n      };'
    if data.count(created_at_pattern) != 2:
        raise RuntimeError("expected two working-state createdAt fields")
    data = data.replace(
        created_at_pattern,
        '        createdAt: rowCreatedAt(row),\n        sourceOrder,\n      };',
    )
data_path.write_text(data)


# New rows must always carry a timestamp, so future daily notifications do not
# depend on the historical fallback above.
api_path = Path("src/creacloud-api.ts")
api = api_path.read_text()
if 'createdAt: new Date().toISOString(),\n    dedupeKey,' not in api:
    api = replace_once(
        api,
        '    dedupeKey,\n    requestId: requestId(mode === "transfer" ? "transfer" : "booking"),',
        '    createdAt: new Date().toISOString(),\n    dedupeKey,\n    requestId: requestId(mode === "transfer" ? "transfer" : "booking"),',
        "booking timestamp",
    )
if 'createdAt: new Date().toISOString(),\n      dedupeKey,' not in api:
    api = replace_once(
        api,
        '      comment: `Удаление бронирования креатором [cancelBooking:${encodeURIComponent(source.sourceKey)}]`,\n      dedupeKey,',
        '      comment: `Удаление бронирования креатором [cancelBooking:${encodeURIComponent(source.sourceKey)}]`,\n      createdAt: new Date().toISOString(),\n      dedupeKey,',
        "cancellation timestamp",
    )
api = api.replace(
    '    createdAt: new Date().toLocaleString("ru-RU"),',
    '    createdAt: new Date().toISOString(),',
)
api = api.replace(
    '  const response = await fetch(url);',
    '  const response = await fetch(url, { cache: "no-store" });',
)
api_path.write_text(api)


app_path = Path("src/creacloud-app.tsx")
app = app_path.read_text()
if "PORTAL_LOAD_TIMEOUT_MS" not in app:
    app = replace_once(
        app,
        '  getTour,\n  isDeletedCreator,',
        '  getTour,\n  getTodayKey,\n  isDeletedCreator,',
        "today key import",
    )
    app = replace_once(
        app,
        'const RECENT_WRITE_TTL = 15 * 60 * 1000;\nconst AUTO_SYNC_INTERVAL_MS = 45 * 1000;\nconst AUTO_SYNC_MIN_GAP_MS = 5 * 1000;\nconst POST_WRITE_SYNC_DELAYS = [1800, 5200, 12_000] as const;',
        'const RECENT_WRITE_TTL = 15 * 60 * 1000;\nconst AUTO_SYNC_INTERVAL_MS = 30 * 1000;\nconst AUTO_SYNC_MIN_GAP_MS = 5 * 1000;\nconst WEATHER_SYNC_INTERVAL_MS = 10 * 60 * 1000;\nconst WEATHER_SYNC_MIN_GAP_MS = 2 * 60 * 1000;\nconst PORTAL_LOAD_TIMEOUT_MS = 5_500;\nconst PORTAL_LOAD_MIN_MS = 700;\nconst WRITE_CONFIRM_DELAYS = [650, 1_200, 2_400, 4_000] as const;\nconst POST_WRITE_SYNC_DELAYS = [1800, 5200, 12_000] as const;',
        "sync constants",
    )
    app = replace_once(
        app,
        'function nowTimestamp() {\n  return Date.now();\n}\n',
        'function nowTimestamp() {\n  return Date.now();\n}\n\nfunction delay(milliseconds: number) {\n  return new Promise<void>((resolve) => window.setTimeout(resolve, milliseconds));\n}\n',
        "delay helper",
    )
    app = replace_once(
        app,
        'type InteractionAura = {',
        '''function PortalLoadingScreen({ visible }: { visible: boolean }) {
  if (!visible) return null;
  return (
    <div className="portal-loading" role="status" aria-live="polite">
      <div className="portal-loading__stage">
        <div className="portal-loading__logo" aria-label="CREACLOUD">
          <strong>CREA</strong>
          <span>CLOUD</span>
        </div>
        <div className="portal-loading__status">
          <span aria-hidden="true" />
          <p>обновляем рабочую базу</p>
        </div>
        <small>Подготавливаем актуальный дашборд и уведомления</small>
      </div>
    </div>
  );
}

type InteractionAura = {''',
        "portal loader component",
    )

    app = regex_once(
        app,
        r'type RecentTourEvent = \{.*?function getRecentTourEvents\(state: WorkingState\) \{.*?\n\}',
        '''type RecentTourEvent = {
  id: string;
  kind: "booking" | "content";
  creator: string;
  tourName: string;
  date: string;
  createdAt: string;
  sourceOrder: number;
};

function getRecentTourEvents(state: WorkingState) {
  const events: RecentTourEvent[] = [
    ...state.bookings.map((booking, index) => ({
      id: `booking-${booking.id}`,
      kind: "booking" as const,
      creator: booking.creator,
      tourName: booking.tourName,
      date: booking.date,
      createdAt: booking.createdAt,
      sourceOrder: booking.sourceOrder ?? index,
    })),
    ...state.content.map((item, index) => ({
      id: `content-${item.id}`,
      kind: "content" as const,
      creator: item.creator,
      tourName: item.tourName,
      date: item.date,
      createdAt: item.createdAt,
      sourceOrder: item.sourceOrder ?? Number.MAX_SAFE_INTEGER - index,
    })),
  ];

  return events
    .sort((a, b) => {
      const aTimestamp = Date.parse(a.createdAt);
      const bTimestamp = Date.parse(b.createdAt);
      if (Number.isFinite(aTimestamp) && Number.isFinite(bTimestamp)) {
        return bTimestamp - aTimestamp || b.sourceOrder - a.sourceOrder;
      }
      return b.sourceOrder - a.sourceOrder || b.date.localeCompare(a.date);
    })
    .slice(0, 5);
}''',
        "recent event ordering",
    )

    app = replace_once(
        app,
        '  const [loading, setLoading] = useState(true);\n  const [entered, setEntered] = useState(false);',
        '  const [loading, setLoading] = useState(true);\n  const [portalLoading, setPortalLoading] = useState(false);\n  const [entered, setEntered] = useState(false);',
        "portal loading state",
    )
    app = replace_once(
        app,
        '  const lastSyncStartedAtRef = useRef(0);\n  const cacheSavedAtRef = useRef(0);',
        '  const lastSyncStartedAtRef = useRef(0);\n  const weatherInFlightRef = useRef<Promise<VladivostokWeather | null> | null>(null);\n  const lastWeatherSyncStartedAtRef = useRef(0);\n  const cacheSavedAtRef = useRef(0);',
        "weather refs",
    )
    # Import the weather response type used by the in-flight reference.
    app = replace_once(
        app,
        '  WeatherSummary,\n} from "./creacloud-api";',
        '  WeatherSummary,\n  VladivostokWeather,\n} from "./creacloud-api";',
        "weather type import",
    )

    app = replace_once(
        app,
        '  function clearReconciliationTimers() {',
        '''  async function refreshWeatherData({
    force = false,
  }: {
    force?: boolean;
  } = {}) {
    if (weatherInFlightRef.current) return weatherInFlightRef.current;
    const now = nowTimestamp();
    if (
      !force &&
      now - lastWeatherSyncStartedAtRef.current < WEATHER_SYNC_MIN_GAP_MS
    ) {
      return null;
    }
    lastWeatherSyncStartedAtRef.current = now;
    const request: Promise<VladivostokWeather | null> = fetchVladivostokWeather()
      .then((next) => {
        setWeather(next.current);
        setWeatherForecast(next.forecast);
        return next;
      })
      .catch(() => null)
      .finally(() => {
        if (weatherInFlightRef.current === request) {
          weatherInFlightRef.current = null;
        }
      });
    weatherInFlightRef.current = request;
    return request;
  }

  function clearReconciliationTimers() {''',
        "weather refresh function",
    )
    app = replace_once(
        app,
        '  const refreshWorkingDataRef = useRef(refreshWorkingData);\n\n  useEffect(() => {\n    refreshWorkingDataRef.current = refreshWorkingData;\n  });',
        '  const refreshWorkingDataRef = useRef(refreshWorkingData);\n  const refreshWeatherDataRef = useRef(refreshWeatherData);\n\n  useEffect(() => {\n    refreshWorkingDataRef.current = refreshWorkingData;\n    refreshWeatherDataRef.current = refreshWeatherData;\n  });',
        "refresh refs",
    )
    app = replace_once(
        app,
        '  }, []);\n\n  useEffect(() => {\n    let cancelled = false;\n    const startedAt = Date.now();',
        '''  }, []);

  useEffect(() => {
    const synchronizeVisibleWeather = () => {
      if (document.visibilityState === "visible") {
        void refreshWeatherDataRef.current();
      }
    };
    const onVisibilityChange = () => synchronizeVisibleWeather();
    const interval = window.setInterval(
      synchronizeVisibleWeather,
      WEATHER_SYNC_INTERVAL_MS,
    );
    window.addEventListener("focus", synchronizeVisibleWeather);
    window.addEventListener("online", synchronizeVisibleWeather);
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => {
      window.clearInterval(interval);
      window.removeEventListener("focus", synchronizeVisibleWeather);
      window.removeEventListener("online", synchronizeVisibleWeather);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    const startedAt = Date.now();''',
        "weather auto refresh effect",
    )
    app = regex_once(
        app,
        r'    const dataRequest = refreshWorkingDataRef\.current\(\{ force: true \}\);.*?    return \(\) => \{\n      cancelled = true;\n    \};',
        '''    void refreshWorkingDataRef.current({ force: true });
    void refreshWeatherDataRef.current({ force: true });

    const remaining = Math.max(0, 900 - (Date.now() - startedAt));
    const splashTimer = window.setTimeout(() => {
      if (!cancelled) setLoading(false);
    }, remaining);

    return () => {
      cancelled = true;
      window.clearTimeout(splashTimer);
    };''',
        "non-blocking initial load",
    )
    app = regex_once(
        app,
        r'  function enterTeamPortal\(\) \{.*?\n  \}\n\n  function openBooking',
        '''  async function enterTeamPortal() {
    const startedAt = Date.now();
    const todayKey = getTodayKey();
    let showDailyNotice = true;
    try {
      showDailyNotice =
        window.localStorage.getItem(TEAM_DAILY_NOTICE_KEY) !== todayKey;
    } catch {
      // The notification remains available when browser storage is unavailable.
    }

    setPortalLoading(true);
    setEntered(true);
    void refreshWeatherData({ force: true });
    const dataRequest = refreshWorkingData({ force: true });
    await Promise.race([dataRequest, delay(PORTAL_LOAD_TIMEOUT_MS)]);
    const remaining = Math.max(0, PORTAL_LOAD_MIN_MS - (Date.now() - startedAt));
    if (remaining) await delay(remaining);

    if (showDailyNotice) {
      setPanel("notices");
      try {
        window.localStorage.setItem(TEAM_DAILY_NOTICE_KEY, todayKey);
      } catch {
        // The next visit can show the daily notification again.
      }
    }
    setPortalLoading(false);
  }

  function openBooking''',
        "team entry flow",
    )
    app = replace_once(
        app,
        '  async function submitBooking(contactMode: ContactMode) {',
        '''  async function confirmWorkingMutation(
    predicate: (next: WorkingState) => boolean,
  ) {
    for (const wait of WRITE_CONFIRM_DELAYS) {
      await delay(wait);
      const next = await fetchWorkingState();
      if (predicate(next)) return next;
    }
    throw new Error("Рабочая база не подтвердила изменение вовремя.");
  }

  async function submitBooking(contactMode: ContactMode) {''',
        "write confirmation helper",
    )
    app = replace_once(
        app,
        '      saveCachedState({ ...latest, bookings: nextBookings });\n      setDataStatus("live");',
        '''      saveCachedState({ ...latest, bookings: nextBookings });
      const confirmed = await confirmWorkingMutation((next) => {
        const targetExists = next.bookings.some(
          (booking) => booking.sourceKey === targetKey,
        );
        const sourceRemoved =
          !source ||
          !next.bookings.some(
            (booking) => booking.sourceKey === source.sourceKey,
          );
        return targetExists && sourceRemoved;
      });
      saveCachedState(confirmed);
      setDataStatus("live");''',
        "booking confirmation",
    )
    app = replace_once(
        app,
        '      saveCachedState({\n        ...latest,\n        bookings: latest.bookings.filter(\n          (booking) => booking.sourceKey !== source.sourceKey,\n        ),\n      });\n      setDataStatus("live");',
        '''      saveCachedState({
        ...latest,
        bookings: latest.bookings.filter(
          (booking) => booking.sourceKey !== source.sourceKey,
        ),
      });
      const confirmed = await confirmWorkingMutation(
        (next) =>
          !next.bookings.some(
            (booking) => booking.sourceKey === source.sourceKey,
          ),
      );
      saveCachedState(confirmed);
      setDataStatus("live");''',
        "cancellation confirmation",
    )
    app = replace_once(
        app,
        '      saveCachedState({\n        ...latest,\n        content: [optimistic, ...latest.content],\n      });\n      setDataStatus("live");',
        '''      saveCachedState({
        ...latest,
        content: [optimistic, ...latest.content],
      });
      const confirmed = await confirmWorkingMutation((next) =>
        next.content.some(
          (item) => normalizeContentLink(item.link) === linkKey,
        ),
      );
      saveCachedState(confirmed);
      setDataStatus("live");''',
        "content confirmation",
    )
    app = replace_once(
        app,
        '            scheduled.length === 0;',
        '            scheduled.length === 0 ||\n            occupied === scheduled.length;',
        "disable full calendar dates",
    )
    app = replace_once(
        app,
        '      <Splash hidden={!loading} />',
        '      <Splash hidden={!loading} />\n      <PortalLoadingScreen visible={portalLoading} />',
        "portal loader render",
    )
app_path.write_text(app)


css_path = Path("src/globals.css")
css = css_path.read_text()
if ".portal-loading" not in css:
    css = replace_once(
        css,
        '.welcome {',
        '''.portal-loading {
  position: fixed;
  z-index: 130;
  inset: 0;
  display: grid;
  min-height: 100dvh;
  padding: max(28px, env(safe-area-inset-top)) 24px max(34px, env(safe-area-inset-bottom));
  place-items: center;
  overflow: hidden;
  background:
    radial-gradient(circle at 12% 8%, rgba(217, 255, 82, 0.32), transparent 28rem),
    radial-gradient(circle at 90% 88%, rgba(118, 87, 246, 0.12), transparent 26rem),
    #ffffff;
  color: var(--ink);
  text-align: center;
}

.portal-loading__stage {
  display: grid;
  width: min(100%, 420px);
  justify-items: center;
  gap: 22px;
}

.portal-loading__logo {
  display: flex;
  align-items: baseline;
  color: #070807;
  font-size: clamp(46px, 13vw, 82px);
  line-height: 0.88;
  letter-spacing: -0.095em;
  white-space: nowrap;
}

.portal-loading__logo strong {
  font-weight: 800;
}

.portal-loading__logo span {
  font-weight: 300;
}

.portal-loading__status {
  display: flex;
  min-height: 32px;
  align-items: center;
  justify-content: center;
  gap: 11px;
}

.portal-loading__status > span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--lime);
  box-shadow:
    0 0 0 7px rgba(217, 255, 82, 0.24),
    0 0 28px rgba(118, 87, 246, 0.28);
  animation: portal-loading-pulse 1.15s ease-in-out infinite;
}

.portal-loading__status p {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
}

.portal-loading small {
  max-width: 290px;
  color: var(--muted);
  font-size: 9px;
  line-height: 1.55;
}

.welcome {''',
        "portal loader styles",
    )
    css += '''

@keyframes portal-loading-pulse {
  0%,
  100% {
    opacity: 0.58;
    transform: scale(0.82);
  }
  50% {
    opacity: 1;
    transform: scale(1.12);
  }
}
'''
css_path.write_text(css)


test_path = Path("scripts/verify-site.mjs")
test = test_path.read_text()
if "PORTAL_LOAD_TIMEOUT_MS" not in test:
    test = replace_once(
        test,
        'assert.match(app, /TEAM_DAILY_NOTICE_KEY/);',
        '''assert.match(app, /TEAM_DAILY_NOTICE_KEY/);
assert.match(app, /PORTAL_LOAD_TIMEOUT_MS/);
assert.match(app, /PortalLoadingScreen/);
assert.match(app, /WEATHER_SYNC_INTERVAL_MS/);
assert.match(app, /confirmWorkingMutation/);
assert.match(app, /occupied === scheduled.length/);
assert.match(data, /sourceOrder\?: number/);
assert.match(api, /createdAt: new Date\(\)\.toISOString\(\)/);''',
        "reliability assertions",
    )
test_path.write_text(test)

print("Platform reliability patch applied")
