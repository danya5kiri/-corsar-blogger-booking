#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


replace_once(
'''html {
  scroll-behavior: smooth;
  background: var(--cb-canvas);
}''',
'''html {
  min-height: 100%;
  scroll-behavior: smooth;
  background: var(--cb-canvas);
}''',
"минимальная высота html",
)

replace_once(
'''body {
  margin: 0;
  min-width: 320px;''',
'''body {
  margin: 0;
  min-width: 320px;
  min-height: 100%;''',
"минимальная высота body",
)

replace_once(
'''body.cb-lock-scroll {
  overflow: hidden;
  height: 100vh;
  height: 100dvh;
  overscroll-behavior: none;
  touch-action: none;
}''',
'''body.cb-lock-scroll {
  overflow: hidden;
  min-height: 100%;
  overscroll-behavior: none;
  touch-action: none;
  background: #f7f7fb !important;
}

body.cb-lock-scroll::before {
  content: "";
  position: fixed;
  z-index: 2147483645;
  inset: -8px;
  pointer-events: none;
  background: #f7f7fb;
}''',
"защитный фон загрузки",
)

replace_once(
'''.cb-splash {
  position: fixed;
  z-index: 2147483647;
  inset: 0;
  display: grid;
  width: 100%;
  height: 100vh;
  height: 100dvh;
  min-height: 100svh;
  place-items: center;
  overflow: hidden;
  box-sizing: border-box;
  padding: max(24px, env(safe-area-inset-top)) 24px max(24px, env(safe-area-inset-bottom));
  background: #f7f7fb;
  isolation: isolate;
  overscroll-behavior: none;
  transition: opacity .55s ease, visibility .55s ease;
}''',
'''.cb-splash {
  position: fixed;
  z-index: 2147483647;
  inset: -8px;
  display: grid;
  place-items: center;
  overflow: hidden;
  box-sizing: border-box;
  padding: calc(max(24px, env(safe-area-inset-top)) + 8px) 32px calc(max(24px, env(safe-area-inset-bottom)) + 8px);
  background: #f7f7fb;
  isolation: isolate;
  overscroll-behavior: none;
  touch-action: none;
  transition: opacity .55s ease, visibility .55s ease;
}''',
"полноэкранный загрузчик без viewport height",
)

if text == original:
    raise RuntimeError("index.html не изменён")

path.write_text(text, encoding="utf-8")
print("mobile splash v2 patch applied")
