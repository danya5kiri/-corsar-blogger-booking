#!/usr/bin/env python3
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://script.google.com/macros/s/AKfycbyRUzCwCTkj4TzURMsYfCZGVRrZnxoeoqTzz76w3n9qz-JlU4ji2i3e1xYQr4CymGsf8Q/exec"
TARGET = "https://www.instagram.com/reel/DaJ47gkItzE/?igsh=Z3ZjajVrNjhmZ2Fz"
OUT = Path("duplicate-check-result.json")


def normalize(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urllib.parse.urlsplit(raw)
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query = [(k, v) for k, v in query if k.lower() not in {"igsh", "igshid", "si", "feature", "share"} and not k.lower().startswith("utm_")]
    path = parsed.path.rstrip("/") or "/"
    netloc = host + ((":" + str(parsed.port)) if parsed.port else "")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), netloc, path, urllib.parse.urlencode(sorted(query)), "")).lower()


def main():
    callback = "duplicateCheckCallback"
    url = API_URL + "?callback=" + callback + "&t=1"
    req = urllib.request.Request(url, headers={"User-Agent": "CorsarDuplicateCheck/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        text = response.read().decode("utf-8-sig")

    match = re.match(r"^\s*" + re.escape(callback) + r"\((.*)\)\s*;?\s*$", text, re.S)
    payload = json.loads(match.group(1) if match else text)
    rows = payload if isinstance(payload, list) else []
    target_key = normalize(TARGET)
    matches = []
    for index, item in enumerate(rows):
        if not isinstance(item, dict):
            continue
        link = item.get("link") or item.get("url") or item.get("contentUrl") or ""
        if normalize(link) == target_key:
            matches.append({
                "index": index,
                "type": item.get("type"),
                "telegram": item.get("telegram") or item.get("creator") or item.get("nickname") or item.get("name"),
                "date": item.get("date"),
                "tour": item.get("tour") or item.get("tourName"),
                "link": link,
                "matchStatus": item.get("matchStatus"),
                "createdAt": item.get("createdAt"),
                "dedupeKey": item.get("dedupeKey"),
            })

    OUT.write_text(json.dumps({
        "target": TARGET,
        "normalizedTarget": target_key,
        "totalRows": len(rows),
        "matchCount": len(matches),
        "matches": matches,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
