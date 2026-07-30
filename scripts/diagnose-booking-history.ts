import fs from "node:fs";
import { buildWorkingState } from "../src/creacloud-data";

const raw = fs.readFileSync("/tmp/creacloud-working-base.js", "utf8").trim();
const match = raw.match(/^bookingHistoryAudit\((.*)\);?$/s);
if (!match) throw new Error("Рабочая база вернула некорректный JSONP");

const rows = JSON.parse(match[1]);
if (!Array.isArray(rows)) throw new Error("Рабочая база не вернула массив строк");

const state = buildWorkingState(rows);
const bookings = [...state.bookings].sort((a, b) =>
  a.date.localeCompare(b.date) || a.creator.localeCompare(b.creator, "ru"),
);
const today = "2026-07-30";
const past = bookings.filter((booking) => booking.date < today);
const currentAndFuture = bookings.filter((booking) => booking.date >= today);
const occupiedDates = new Set(bookings.map((booking) => booking.date));

console.log(`RAW_ROWS=${rows.length}`);
console.log(`PARSED_BOOKINGS=${bookings.length}`);
console.log(`PAST_BOOKINGS=${past.length}`);
console.log(`CURRENT_FUTURE_BOOKINGS=${currentAndFuture.length}`);
console.log(`OCCUPIED_DATES=${occupiedDates.size}`);
console.log(`CREATORS=${state.creators?.length ?? 0}`);
console.log(`FIRST_BOOKING=${bookings[0] ? `${bookings[0].date}|${bookings[0].creator}|${bookings[0].tourName}` : "none"}`);
console.log(`LAST_BOOKING=${bookings.at(-1) ? `${bookings.at(-1)!.date}|${bookings.at(-1)!.creator}|${bookings.at(-1)!.tourName}` : "none"}`);
console.log("LAST_12_BOOKINGS=");
for (const booking of bookings.slice(-12)) {
  console.log(`${booking.date}|${booking.creator}|${booking.tourName}`);
}

if (!bookings.length) {
  throw new Error("Сайт не распознал ни одной брони из рабочей базы");
}
