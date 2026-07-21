#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

INDEX = Path("index.html")

OLD = '''function getPublishedContentItems(){
  var seen = {};
  return reports.slice().reverse().filter(function(report){
    var link = getReportLink(report);
    var key = normalizeContentLink(link);
    var matchStatus = String((report && report.matchStatus) || "").trim();
    if(isDeletedCreator(getReportCreator(report))) return false;
    if(matchStatus && matchStatus !== "Есть запись") return false;
    if(!isValidContentLink(link) || seen[key]) return false;
    seen[key] = true;
    return true;
  });
}'''

NEW = '''function resolveHistoricalContentReport(report){
  var matchStatus = String((report && report.matchStatus) || "").trim();
  if(matchStatus !== "Запись не найдена") return report;

  var match = findReportBooking(getReportCreator(report), getReportTour(report));
  if(!match) return report;

  var resolved = Object.assign({}, report);
  resolved.date = normalizeDate(match.date);
  resolved.telegram = normalizeTelegram(match.telegram || getReportCreator(report));
  resolved.matchStatus = "Есть запись";
  return resolved;
}

function getPublishedContentItems(){
  var seen = {};
  return reports.slice().reverse().map(resolveHistoricalContentReport).filter(function(report){
    var link = getReportLink(report);
    var key = normalizeContentLink(link);
    var matchStatus = String((report && report.matchStatus) || "").trim();
    if(isDeletedCreator(getReportCreator(report))) return false;
    if(matchStatus && matchStatus !== "Есть запись" && matchStatus !== "Запись не найдена") return false;
    if(!isValidContentLink(link) || seen[key]) return false;
    seen[key] = true;
    return true;
  });
}'''


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if NEW in text:
        print("Исторические публикации уже подключены")
        return
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"Ожидался один блок публикаций, найдено: {count}")
    updated = text.replace(OLD, NEW, 1)

    required = (
        "function resolveHistoricalContentReport(report)",
        'matchStatus !== "Запись не найдена"',
        ".map(resolveHistoricalContentReport)",
        'matchStatus !== "Есть запись" && matchStatus !== "Запись не найдена"',
    )
    for token in required:
        if token not in updated:
            raise RuntimeError(f"Не применена проверка: {token}")

    # Критично: логика новых ссылок и дедупликации не меняется.
    unchanged_tokens = (
        "function hasContentDuplicate(link)",
        "if(hasContentDuplicate(link) || wasRecentlySubmitted(CONTENT_STORAGE_KEY, linkKey))",
        'setMessage("Такая ссылка уже добавлена.", true)',
        'type: "content_report"',
        'dedupeKey: "content:" + linkKey',
    )
    for token in unchanged_tokens:
        if token not in updated:
            raise RuntimeError(f"Повреждена логика новых ссылок: {token}")

    INDEX.write_text(updated, encoding="utf-8", newline="\n")
    print("Старые публикации со статусом «Запись не найдена» подключены")


if __name__ == "__main__":
    main()
