from pathlib import Path


app_path = Path("src/creacloud-app.tsx")
app = app_path.read_text(encoding="utf-8")

app = app.replace(
    "const WEATHER_REFRESH_INTERVAL_MS = 15 * 60 * 1000;",
    "const WEATHER_REFRESH_INTERVAL_MS = 10 * 60 * 1000;",
)
app = app.replace(
    "Проверяем погоду каждые 15 минут",
    "Проверяем погоду каждые 10 минут",
)

old_initial = '''    const dataRequest = refreshWorkingDataRef.current({ force: true });

    const weatherRequest = refreshWeatherRef.current({ force: true });

    Promise.allSettled([dataRequest, weatherRequest]).then(() => {
      const remaining = Math.max(0, 1450 - (Date.now() - startedAt));
      window.setTimeout(() => {
        if (!cancelled) setLoading(false);
      }, remaining);
    });

    return () => {
      cancelled = true;
    };'''
new_initial = '''    void refreshWorkingDataRef.current({ force: true });
    void refreshWeatherRef.current({ force: true });

    const remaining = Math.max(0, 950 - (Date.now() - startedAt));
    const splashTimer = window.setTimeout(() => {
      if (!cancelled) setLoading(false);
    }, remaining);

    return () => {
      cancelled = true;
      window.clearTimeout(splashTimer);
    };'''
if old_initial in app:
    app = app.replace(old_initial, new_initial, 1)

old_disabled = '''            cell.date > SEASON_END ||
            scheduled.length === 0;'''
new_disabled = '''            cell.date > SEASON_END ||
            scheduled.length === 0 ||
            occupied === scheduled.length;'''
if old_disabled in app:
    app = app.replace(old_disabled, new_disabled, 1)

app_path.write_text(app, encoding="utf-8")

verify_path = Path("scripts/verify-site.mjs")
verify = verify_path.read_text(encoding="utf-8")
anchor = "assert.match(app, /POST_WRITE_SYNC_DELAYS/);"
additions = '''assert.match(app, /WEATHER_REFRESH_INTERVAL_MS = 10 \\* 60 \\* 1000/);
assert.match(app, /occupied === scheduled.length/);
assert.match(app, /PORTAL_TRANSITION_MIN_MS/);'''
if additions not in verify:
    if anchor not in verify:
        raise RuntimeError("Verification anchor was not found")
    verify = verify.replace(anchor, f"{anchor}\n{additions}", 1)
verify_path.write_text(verify, encoding="utf-8")

print("Final CREACLOUD refinements applied")
