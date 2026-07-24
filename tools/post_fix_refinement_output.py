#!/usr/bin/env python3
from pathlib import Path

index_path = Path("index.html")
tests_path = Path("tests/design_modes_test.js")
index = index_path.read_text(encoding="utf-8")
tests = tests_path.read_text(encoding="utf-8")

old_signature = '''function submitBooking(contactMode){
  contactMode = contactMode === "call" ? "call" : "whatsapp";
'''
new_signature = '''var bookingContactMode = "whatsapp";

function submitBooking(){
  var contactMode = bookingContactMode === "call" ? "call" : "whatsapp";
  bookingContactMode = "whatsapp";
'''
if new_signature not in index:
    if index.count(old_signature) != 1:
        raise SystemExit("generated submitBooking signature not found")
    index = index.replace(old_signature, new_signature, 1)

old_binding = '''  if(submit) submit.onclick = function(){ submitBooking("whatsapp"); };
  if(callSubmit) callSubmit.onclick = function(){ submitBooking("call"); };
'''
new_binding = '''  if(submit) submit.onclick = function(){ bookingContactMode = "whatsapp"; submitBooking(); };
  if(callSubmit) callSubmit.onclick = function(){ bookingContactMode = "call"; submitBooking(); };
'''
if new_binding not in index:
    if index.count(old_binding) != 1:
        raise SystemExit("generated booking bindings not found")
    index = index.replace(old_binding, new_binding, 1)

tests = tests.replace(
    '  assert.match(html, /submitBooking\\("call"\\)/);',
    '  assert.match(html, /bookingContactMode = "call"; submitBooking\\(\\)/);',
)

index_path.write_text(index, encoding="utf-8")
tests_path.write_text(tests, encoding="utf-8")
print("refinement output keeps the original submitBooking signature")
