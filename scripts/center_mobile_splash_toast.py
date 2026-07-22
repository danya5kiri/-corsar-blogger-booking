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
'''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#171719">''',
'''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#171719">
<script>
(function(){
  function syncCorsarVisualViewport(){
    var viewport = window.visualViewport;
    var height = viewport ? viewport.height : window.innerHeight;
    var top = viewport ? viewport.offsetTop : 0;
    if(!Number.isFinite(height) || height <= 0) return;
    document.documentElement.style.setProperty("--cb-visual-height", Math.ceil(height) + "px");
    document.documentElement.style.setProperty("--cb-visual-top", Math.max(0, Math.floor(top || 0)) + "px");
  }
  syncCorsarVisualViewport();
  window.addEventListener("resize", syncCorsarVisualViewport, {passive:true});
  if(window.visualViewport){
    window.visualViewport.addEventListener("resize", syncCorsarVisualViewport, {passive:true});
    window.visualViewport.addEventListener("scroll", syncCorsarVisualViewport, {passive:true});
  }
})();
</script>''',
"ранняя синхронизация видимой области",
)

replace_once(
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
'''.cb-splash {
  position: fixed;
  z-index: 2147483647;
  top: calc(var(--cb-visual-top, 0px) - 8px);
  right: -8px;
  bottom: auto;
  left: -8px;
  display: grid;
  height: calc(var(--cb-visual-height, 100vh) + 16px);
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
"центрирование загрузчика по visual viewport",
)

replace_once(
'''  .cb-day-num + .cb-day-count {
    margin-top: 1px;
  }

  .cb-weekly-push {''',
'''  .cb-day-num + .cb-day-count {
    margin-top: 1px;
  }

  .cb-message {
    right: auto;
    bottom: max(14px, env(safe-area-inset-bottom));
    left: max(12px, env(safe-area-inset-left));
    width: auto;
    max-width: min(310px, calc(100vw - 28px));
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.45;
    text-align: left;
    transform: translate(-8px, 8px);
  }

  .cb-message.is-visible {
    transform: translate(0, 0);
  }

  .cb-weekly-push {''',
"мобильное положение служебных уведомлений",
)

if text == original:
    raise RuntimeError("index.html не изменён")

path.write_text(text, encoding="utf-8")
print("mobile splash and toast patch applied")
