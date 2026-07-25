const API_URL =
  "https://script.google.com/macros/s/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/exec";
const callback = "creacloudLiveAudit";
const response = await fetch(
  `${API_URL}?callback=${callback}&t=${Date.now()}`,
  { cache: "no-store" },
);
if (!response.ok) throw new Error(`Working base HTTP ${response.status}`);
const raw = (await response.text()).trim();
const match = raw.match(/^creacloudLiveAudit\((.*)\);?$/s);
if (!match) throw new Error("Working base did not return valid JSONP");
const rows = JSON.parse(match[1]);
if (!Array.isArray(rows)) throw new Error("Working base response is not an array");

const text = (value) => String(value ?? "").trim();
const creator = (row) =>
  text(row.telegram || row.creator || row.nickname || row.name)
    .toLowerCase()
    .replace(/\s+/g, "");
const summaries = rows.map((row, sourceIndex) => ({
  sourceIndex,
  type: text(row.type) || "booking",
  creator: creator(row),
  date: row.date,
  tour: row.tour,
  createdAt:
    row.createdAt || row.timestamp || row.submittedAt || row.created || "",
}));
const katerina = summaries.filter((row) =>
  JSON.stringify(row).toLowerCase().includes("katerinamanko"),
);
const contentRows = summaries.filter((row) => row.type === "content_report");
const withoutTimestamp = summaries.filter((row) => !row.createdAt);

console.log(
  JSON.stringify({
    total: summaries.length,
    bookingRows: summaries.length - contentRows.length,
    contentRows: contentRows.length,
    rowsWithoutTimestamp: withoutTimestamp.length,
    katerina,
    tail: summaries.slice(-12),
  }),
);
