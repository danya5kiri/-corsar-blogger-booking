import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";

const path = "src/creacloud-app.tsx";
let content = await readFile(path, "utf8");

if (content.includes("LEGACY_BOOKING_NOTICE_LIMIT")) {
  console.log("Recent-event policy is already applied.");
  process.exit(0);
}

const before = `function getRecentTourEvents(state: WorkingState) {
  const events: RecentTourEvent[] = [
    ...state.bookings.map((booking, index) => ({
      id: \`booking-\${booking.id}\`,
      kind: "booking" as const,
      creator: booking.creator,
      tourName: booking.tourName,
      date: booking.date,
      createdAt: booking.createdAt,
      sourceOrder: booking.sourceOrder ?? index,
    })),
    ...state.content.map((item, index) => ({
      id: \`content-\${item.id}\`,
      kind: "content" as const,
      creator: item.creator,
      tourName: item.tourName,
      date: item.date,
      createdAt: item.createdAt,
      sourceOrder: item.sourceOrder ?? state.bookings.length + index,
    })),
  ];

  return events
    .sort((a, b) => {
      if (a.sourceOrder !== b.sourceOrder) return b.sourceOrder - a.sourceOrder;
      const aTimestamp = Date.parse(a.createdAt);
      const bTimestamp = Date.parse(b.createdAt);
      if (Number.isFinite(aTimestamp) || Number.isFinite(bTimestamp)) {
        return (Number.isFinite(bTimestamp) ? bTimestamp : 0) -
          (Number.isFinite(aTimestamp) ? aTimestamp : 0);
      }
      return b.date.localeCompare(a.date);
    })
    .slice(0, 5);
}`;

const after = `const LEGACY_BOOKING_NOTICE_LIMIT = 4;
const DAILY_NOTICE_EVENT_LIMIT = 5;

function compareEventsWithinSource(a: RecentTourEvent, b: RecentTourEvent) {
  const aTimestamp = Date.parse(a.createdAt);
  const bTimestamp = Date.parse(b.createdAt);
  if (Number.isFinite(aTimestamp) && Number.isFinite(bTimestamp)) {
    return bTimestamp - aTimestamp;
  }
  if (a.sourceOrder !== b.sourceOrder) return b.sourceOrder - a.sourceOrder;
  return b.date.localeCompare(a.date);
}

function getRecentTourEvents(state: WorkingState) {
  const bookings: RecentTourEvent[] = state.bookings
    .map((booking, index) => ({
      id: \`booking-\${booking.id}\`,
      kind: "booking" as const,
      creator: booking.creator,
      tourName: booking.tourName,
      date: booking.date,
      createdAt: booking.createdAt,
      sourceOrder: booking.sourceOrder ?? index,
    }))
    .sort(compareEventsWithinSource);
  const content: RecentTourEvent[] = state.content
    .map((item, index) => ({
      id: \`content-\${item.id}\`,
      kind: "content" as const,
      creator: item.creator,
      tourName: item.tourName,
      date: item.date,
      createdAt: item.createdAt,
      sourceOrder: item.sourceOrder ?? index,
    }))
    .sort(compareEventsWithinSource);

  // Legacy booking rows do not contain a creation timestamp. The API returns
  // bookings and content as separate blocks, so their global array indexes are
  // not a shared timeline. Reserve four places for the newest booking rows so
  // season-critical applications never disappear behind content reports.
  const bookingLimit = content.length
    ? Math.min(LEGACY_BOOKING_NOTICE_LIMIT, bookings.length)
    : Math.min(DAILY_NOTICE_EVENT_LIMIT, bookings.length);
  const selected = [
    ...bookings.slice(0, bookingLimit),
    ...content.slice(0, DAILY_NOTICE_EVENT_LIMIT - bookingLimit),
  ];

  if (selected.length < DAILY_NOTICE_EVENT_LIMIT) {
    selected.push(
      ...bookings.slice(bookingLimit, DAILY_NOTICE_EVENT_LIMIT - selected.length),
    );
  }
  if (selected.length < DAILY_NOTICE_EVENT_LIMIT) {
    const selectedContent = new Set(
      selected.filter((event) => event.kind === "content").map((event) => event.id),
    );
    selected.push(
      ...content
        .filter((event) => !selectedContent.has(event.id))
        .slice(0, DAILY_NOTICE_EVENT_LIMIT - selected.length),
    );
  }

  return selected.slice(0, DAILY_NOTICE_EVENT_LIMIT);
}`;

assert.ok(content.includes(before), "Current recent-event function was not found");
content = content.replace(before, after);
await writeFile(path, content, "utf8");
console.log("Applied booking-priority daily notice policy.");
