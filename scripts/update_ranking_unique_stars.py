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


old_css = '''.cb-rank-coverage-dots {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.cb-rank-coverage-dot {
  width: 7px;
  height: 7px;
  border: 1px solid rgba(23, 23, 25, .12);
  border-radius: 50%;
  background: rgba(255,255,255,.54);
}

.cb-rank-coverage-dot.is-filled {
  border-color: transparent;
  background: linear-gradient(135deg, var(--cb-blue), var(--cb-cyan) 54%, var(--cb-lilac-strong));
  box-shadow: 0 0 0 2px rgba(78, 203, 237, .09);
}

.cb-rank-row.is-top-1 .cb-rank-coverage-dot.is-filled {
  background: linear-gradient(135deg, #ff9e67, #7f67f8 58%, #4ecbed);
}
'''
new_css = '''.cb-rank-coverage-stars {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
}

.cb-rank-coverage-star {
  color: #c8cbd2;
  font-size: 15px;
  line-height: 1;
}

.cb-rank-coverage-star.is-filled {
  color: #f4b91f;
  text-shadow: 0 1px 0 rgba(132, 91, 0, .18);
}

.cb-rank-row.is-top-1 .cb-rank-coverage-star.is-filled {
  color: #efa900;
}
'''
replace_once(old_css, new_css, "стили звёзд")

replace_once('''.cb-rank-coverage-copy strong {
  color: var(--cb-ink);
  font-size: 11px;
  font-weight: 840;
}
''', '''.cb-rank-coverage-copy strong {
  color: #666b76;
  font-size: 11px;
  font-weight: 840;
}
''', "серый текст охвата")

replace_once('''  .cb-rank-coverage-dot {
    width: 6px;
    height: 6px;
  }
''', '''  .cb-rank-coverage-star {
    font-size: 14px;
  }
''', "мобильный размер звёзд")

replace_once('''var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту"];
''', '''var LEADER_CARD_LABELS = ["По количеству туров", "По опубликованному контенту"];
var TOTAL_UNIQUE_TOURS = 5;
''', "общее количество уникальных туров")

old_function = '''function renderTourVarietyDots(uniqueTours, visits){
  var ratio = visits > 0 ? Math.max(0, Math.min(1, uniqueTours / visits)) : 0;
  var filled = uniqueTours > 0 ? Math.max(1, Math.round(ratio * 5)) : 0;
  var dots = "";
  for(var i = 0; i < 5; i++){
    dots += '<span class="cb-rank-coverage-dot' + (i < filled ? ' is-filled' : '') + '"></span>';
  }
  return dots;
}
'''
new_function = '''function renderTourVarietyStars(uniqueTours){
  var total = TOTAL_UNIQUE_TOURS;
  var filled = Math.max(0, Math.min(total, Number(uniqueTours) || 0));
  var stars = "";
  for(var i = 0; i < total; i++){
    stars += '<span class="cb-rank-coverage-star' + (i < filled ? ' is-filled' : '') + '" aria-hidden="true">★</span>';
  }
  return stars;
}
'''
replace_once(old_function, new_function, "функция звёзд")

replace_once('''    return {name: tg, visits: users[tg], uniqueTours: getCreatorTourVariety(tg)};
''', '''    return {name: tg, visits: users[tg], uniqueTours: Math.min(getCreatorTourVariety(tg), TOTAL_UNIQUE_TOURS)};
''', "ограничение уникальных туров")

old_variety = '''    var varietyText = item.uniqueTours + " " + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") +
      " из " + item.visits + " " + pluralCount(item.visits, "поездки", "поездок", "поездок");
'''
new_variety = '''    var varietyText = item.uniqueTours + " " + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") +
      " из " + TOTAL_UNIQUE_TOURS + " доступных уникальных туров";
'''
replace_once(old_variety, new_variety, "текст уникальных туров")

old_markup = '''          '<span class="cb-rank-coverage-copy"><strong>' + item.uniqueTours + '</strong> ' + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") + ' из ' + item.visits + '</span>' +
          '<span class="cb-rank-coverage-dots" aria-hidden="true">' + renderTourVarietyDots(item.uniqueTours, item.visits) + '</span>' +
'''
new_markup = '''          '<span class="cb-rank-coverage-copy"><strong>' + item.uniqueTours + '</strong> ' + pluralCount(item.uniqueTours, "уникальный тур", "уникальных тура", "уникальных туров") + ' из ' + TOTAL_UNIQUE_TOURS + '</span>' +
          '<span class="cb-rank-coverage-stars" aria-label="Пройдено ' + item.uniqueTours + ' из ' + TOTAL_UNIQUE_TOURS + ' уникальных туров">' + renderTourVarietyStars(item.uniqueTours) + '</span>' +
'''
replace_once(old_markup, new_markup, "разметка звёзд")

if text == original:
    raise RuntimeError("index.html не изменился")

path.write_text(text, encoding="utf-8")
print("Показатель уникальных туров переведён на пять жёлтых звёзд")
