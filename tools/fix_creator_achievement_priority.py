#!/usr/bin/env python3
from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = '''  if(data && data.visitRank === 1 && trips > 0) achievements.push({label: "Лидер поездок", icon: "01"});
  if(data && data.uniqueRank === 1 && unique > 0) achievements.push({label: "Исследователь сезона", icon: "◎"});
  if(data && data.contentRank === 1 && materials > 0) achievements.push({label: "Автор сезона", icon: "✦"});
  if(unique >= TOTAL_UNIQUE_TOURS) achievements.push({label: "Все маршруты", icon: "✓"});
  else if(materials >= 3) achievements.push({label: "Контент-мейкер", icon: "+"});
  else if(trips >= 3) achievements.push({label: "Постоянный участник", icon: "∞"});
'''
new = '''  if(unique >= TOTAL_UNIQUE_TOURS) achievements.push({label: "Все маршруты", icon: "✓"});
  else if(materials >= 3) achievements.push({label: "Контент-мейкер", icon: "+"});
  else if(trips >= 3) achievements.push({label: "Постоянный участник", icon: "∞"});
  if(data && data.visitRank === 1 && trips > 0) achievements.push({label: "Лидер поездок", icon: "01"});
  if(data && data.uniqueRank === 1 && unique > 0) achievements.push({label: "Исследователь сезона", icon: "◎"});
  if(data && data.contentRank === 1 && materials > 0) achievements.push({label: "Автор сезона", icon: "✦"});
'''
if text.count(old) != 1:
    raise SystemExit(f"achievement order block: expected 1 occurrence, got {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("achievement priority fixed")
