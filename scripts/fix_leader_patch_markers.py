#!/usr/bin/env python3
from pathlib import Path

path = Path("scripts/add_leader_alert_and_tour_variety.py")
text = path.read_text(encoding="utf-8")
old_rank = 'insert_before(".cb-rank-score {\\n", ranking_css, "стили уникальных туров")'
new_rank = 'insert_before("\\n.cb-rank-score {\\n", ranking_css, "стили уникальных туров")'
old_message = 'insert_before(".cb-message {\\n", leader_notice_css, "стили уведомления о лидере")'
new_message = 'insert_before("\\n.cb-message {\\n", leader_notice_css, "стили уведомления о лидере")'

if text.count(old_rank) != 1:
    raise RuntimeError("Не найден селектор рейтинга для уточнения")
if text.count(old_message) != 1:
    raise RuntimeError("Не найден селектор сообщения для уточнения")

text = text.replace(old_rank, new_rank, 1).replace(old_message, new_message, 1)
path.write_text(text, encoding="utf-8")
print("Селекторы патча уточнены")
