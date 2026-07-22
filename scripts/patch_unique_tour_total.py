#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: ожидалось 1 совпадение, найдено {count}")
    text = text.replace(old, new, 1)


replace_once(
    'var TOTAL_UNIQUE_TOURS = 5;',
    '''var TOTAL_UNIQUE_TOURS = (function(){
  var seen = Object.create(null);
  CANONICAL_TOURS.forEach(function(tour){
    var key = getUniqueTourKey(tour);
    if(key) seen[key] = true;
  });
  return Object.keys(seen).length;
})();''',
    "динамический максимум уникальных туров",
)

replace_once(
    '''function normalizeTour(v){
  return canonicalTourName(v).toLowerCase().replace(/\\s+/g, " ");
}''',
    '''function normalizeTour(v){
  return canonicalTourName(v).toLowerCase().replace(/\\s+/g, " ");
}

function getUniqueTourKey(v){
  var canonical = canonicalTourName(v);
  if(!canonical) return "";
  if(canonical === CANONICAL_TOURS[1] || canonical === CANONICAL_TOURS[8]) return "вечерняя программа";
  return normalizeTour(canonical);
}''',
    "единый ключ вечерних программ",
)

replace_once(
    'var key = normalizeTour(booking.tour);',
    'var key = getUniqueTourKey(booking.tour);',
    "ключ уникальности рейтинга",
)
replace_once(
    'var tourKey = normalizeTour(booking.tour);',
    'var tourKey = getUniqueTourKey(booking.tour);',
    "ключ уникальности смены лидера",
)

path.write_text(text, encoding="utf-8")
