#!/usr/bin/env python3
from pathlib import Path

INDEX = Path("index.html")
CSS = Path("creacloud-redesign.css")
TESTS = Path("tests/design_modes_test.js")

index = INDEX.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
tests = TESTS.read_text(encoding="utf-8")

# Keep the WhatsApp contact unchanged, but make the phone destination explicit.
if 'CALL_PHONE_NUMBER: "79149753285"' not in index:
    anchor = 'WHATSAPP_NUMBER: "79149753285"'
    if index.count(anchor) != 1:
        raise SystemExit(f"WhatsApp config anchor: expected 1, found {index.count(anchor)}")
    replacement = 'WHATSAPP_NUMBER: "79149753285",\n  CALL_PHONE_NUMBER: "79149753285"'
    index = index.replace(anchor, replacement, 1)

old_call = 'contactMode === "call" ? "tel:+" + CONFIG.WHATSAPP_NUMBER : whatsappUrl'
new_call = 'contactMode === "call" ? "tel:+" + CONFIG.CALL_PHONE_NUMBER : whatsappUrl'
if old_call in index:
    count = index.count(old_call)
    if count != 2:
        raise SystemExit(f"call destination anchors: expected 2, found {count}")
    index = index.replace(old_call, new_call)
if index.count(new_call) != 2:
    raise SystemExit(f"explicit call destinations: expected 2, found {index.count(new_call)}")

marker = "/* ===== CREACLOUD screenshot corrections v3 ===== */"
css_patch = r'''

/* ===== CREACLOUD screenshot corrections v3 ===== */
/* Match the leader-card silhouette to the compact season dashboard. */
html[data-design="redesign"] #corsar-blogger-booking .cb-leaders-track .cb-leader-card {
  border-radius: 16px !important;
  overflow: hidden;
}

/* The activity control should not have a decorative stripe attached to its left edge. */
html[data-design="redesign"] #corsar-blogger-booking .cb-recent-events::before {
  content: none !important;
  display: none !important;
}

/* Restore the original rectangular calendar-day geometry. */
html[data-design="redesign"] #corsar-blogger-booking button.cb-day {
  border-radius: 0 !important;
}

@media (min-width: 901px) {
  /* Keep the main weather icon directly beside the temperature. */
  html[data-design="redesign"] #corsar-blogger-booking .cb-weather-temp {
    display: inline-flex !important;
    width: max-content !important;
    max-width: 100%;
    align-self: flex-start;
    justify-content: flex-start !important;
  }

  html[data-design="redesign"] #corsar-blogger-booking .cb-weather-temp > .cb-weather-icon {
    position: static !important;
    margin: 0 0 0 2px !important;
    transform: none !important;
  }

  /* On wide calendar cells, place the forecast beside the day number, not at the far edge. */
  html[data-design="redesign"] #corsar-blogger-booking .cb-day-weather {
    top: 5px;
    right: auto !important;
    left: calc(50% + 10px);
  }

  html[data-design="redesign"] #corsar-blogger-booking .cb-day-weather .cb-weather-icon {
    width: 14px;
    height: 14px;
  }
}
'''
if marker not in css:
    css = css.rstrip() + css_patch + "\n"

if 'screenshot corrections keep requested desktop geometry' not in tests:
    footer = 'console.log(`\\n${passed} design mode tests passed.`);'
    if tests.count(footer) != 1:
        raise SystemExit("design test footer not found")
    extra = r'''

test("screenshot corrections keep requested desktop geometry", () => {
  assert.match(themeCss, /CREACLOUD screenshot corrections v3/);
  assert.match(themeCss, /\.cb-leaders-track \.cb-leader-card[\s\S]*border-radius:\s*16px !important/);
  assert.match(themeCss, /\.cb-recent-events::before[\s\S]*display:\s*none !important/);
  assert.match(themeCss, /button\.cb-day[\s\S]*border-radius:\s*0 !important/);
  assert.match(themeCss, /@media \(min-width: 901px\)[\s\S]*\.cb-day-weather[\s\S]*left:\s*calc\(50% \+ 10px\)/);
});


test("phone confirmation uses Olga's explicit call number", () => {
  assert.match(html, /CALL_PHONE_NUMBER:\s*"79149753285"/);
  const calls = html.match(/contactMode === "call" \? "tel:\+" \+ CONFIG\.CALL_PHONE_NUMBER : whatsappUrl/g) || [];
  assert.equal(calls.length, 2);
});
'''
    tests = tests.replace(footer, extra + "\n" + footer, 1)

INDEX.write_text(index, encoding="utf-8")
CSS.write_text(css, encoding="utf-8")
TESTS.write_text(tests, encoding="utf-8")
print("Screenshot corrections applied")
