#!/usr/bin/env python3
"""Unit tests for Section 3 filter in Ubon report.
Run: python3 test_section3_filter.py
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from generate_report import extract_date, extract_venue, event_kw, all_forbidden

PASSED = 0
FAILED = 0

def test(name, fn):
    global PASSED, FAILED
    try:
        fn()
        print(f"  ✅ PASS: {name}")
        PASSED += 1
    except AssertionError as e:
        print(f"  ❌ FAIL: {name}")
        print(f"     {e}")
        FAILED += 1
    except Exception as e:
        print(f"  💥 ERROR: {name}: {e}")
        FAILED += 1

# DATE TESTS
def test_date_1_5_singhm():
    text = "📅 1 – 5 สิงหาคมนี้"
    result = extract_date(text)
    assert result == "1 – 5 สิงหาคม", f"Got: '{result}'"

def test_date_wan_ni_last_day():
    text = "BIG SALE วันนี้วันสุดท้าย"
    result = extract_date(text)
    assert result == "วันนี้วันสุดท้าย", f"Got: '{result}'"

def test_date_with_year():
    text = "📅 25 กรกฎาคม 2569"
    result = extract_date(text)
    assert "กรกฎาคม 2569" in result, f"Got: '{result}'"

# VENUE TESTS
def test_venue_ubon_central():
    text = "📍 เซ็นทรัล อุบล"
    result = extract_venue(text)
    assert "เซ็นทรัล" in result, f"Got: '{result}'"

def test_venue_sisaket():
    text = "📍 ปั๊มน้ำมันเชลล์ ถนนเลี่ยงเมือง จ.ศรีสะเกษ"
    result = extract_venue(text)
    assert "ศรีสะเกษ" in result, f"Got: '{result}'"

def test_venue_amnat():
    text = "📍 Big C Place อำนาจเจริญ"
    result = extract_venue(text)
    assert "อำนาจเจริญ" in result, f"Got: '{result}'"

def test_venue_yasothon():
    text = "📍 ตลาดนัดบ้านปลาขาว จ.ยโสธร"
    result = extract_venue(text)
    assert "ยโสธร" in result, f"Got: '{result}'"

# EVENT KEYWORDS
def test_event_kw_samlap():
    text = "สัมผัสรถยนต์ไฟฟ้ารุ่นใหม่"
    text_lower = text.lower()
    assert any(k in text_lower for k in event_kw)

def test_event_kw_big_sale():
    text = "BIG SALE MOTOR SHOW"
    text_lower = text.lower()
    assert any(k in text_lower for k in event_kw)

# FORBIDDEN
def test_forbidden_delivery():
    text = "ส่งมอบรถ Nissan ใหม่"
    assert any(k in text for k in all_forbidden)

if __name__ == "__main__":
    print("🚀 Running Ubon Section 3 Filter Tests...")
    print("=" * 60)
    
    print("\n📅 Date Patterns:")
    test("date_1_5_singhm", test_date_1_5_singhm)
    test("date_wan_ni_last_day", test_date_wan_ni_last_day)
    test("date_with_year", test_date_with_year)
    
    print("\n📍 Venue Detection:")
    test("venue_ubon_central", test_venue_ubon_central)
    test("venue_sisaket", test_venue_sisaket)
    test("venue_amnat", test_venue_amnat)
    test("venue_yasothon", test_venue_yasothon)
    
    print("\n🔑 Event Keywords:")
    test("event_kw_samlap", test_event_kw_samlap)
    test("event_kw_big_sale", test_event_kw_big_sale)
    
    print("\n🚫 Forbidden Filter:")
    test("forbidden_delivery", test_forbidden_delivery)
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {PASSED} passed, {FAILED} failed")
    
    if FAILED > 0:
        sys.exit(1)
    else:
        print("✅ All tests PASSED!")
        sys.exit(0)
