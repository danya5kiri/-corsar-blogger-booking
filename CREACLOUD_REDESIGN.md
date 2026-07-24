# CREACLOUD redesign

## Stable recovery point

The pre-redesign production version is preserved in the branch:

- branch: `pre-creacloud-redesign`
- commit: `2f48786259d0d70984770fe9a498655859bfaa83`

This branch contains the complete site immediately before the visual redesign.

## Central design switch

The only default-mode switch is at the top of `creacloud-design.js`:

```js
window.CREACLOUD_DESIGN_MODE = "redesign";
```

Allowed values:

- `legacy` — previous interface;
- `redesign` — refreshed CREACLOUD interface.

Changing this single value does not change the database, API, schedule, bookings, content, ratings, diagnostics or statistics.

## Preview without changing the default

A temporary mode can be opened through the URL query parameter:

- `?design=legacy`
- `?design=redesign`

The query parameter applies only to the current page address and does not write anything to the database or browser storage.

## Normal rollback

1. Open `creacloud-design.js`.
2. Change `"redesign"` to `"legacy"` in `window.CREACLOUD_DESIGN_MODE`.
3. Commit the one-line change.
4. Wait for GitHub Pages deployment and refresh the site.

The old visual layer is still stored in `index.html`. The redesign stylesheet is scoped to `html[data-design="redesign"]`, so legacy mode restores the previous palette, backgrounds, cards, buttons, widgets and loading screen without manually editing each component.

## Emergency full rollback

Move `main` back to the preserved branch `pre-creacloud-redesign`, or restore commit `2f48786259d0d70984770fe9a498655859bfaa83` through a reviewed pull request.

A database rollback is not required: both visual modes use the same current data and business logic.

## Files in the redesign layer

- `creacloud-design.js` — design flag, URL preview mode and splash phrase lifecycle;
- `creacloud-redesign.css` — scoped visual tokens and redesign overrides;
- `index.html` — unchanged product structure plus dual loading-screen markup and lifecycle hooks;
- `tests/design_modes_test.js` — checks both modes, section order and business-logic safeguards.

## Product invariants

The redesign must not change:

- section order and navigation;
- Apps Script API URL and payloads;
- calendar dates, states and weather data;
- booking, transfer and cancellation checks;
- content submission and matching;
- ranking formulas and eight unique-tour categories;
- results, creator profiles, notifications and diagnostics.
