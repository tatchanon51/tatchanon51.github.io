#!/usr/bin/env python3
"""Unit tests for Section 3 filter in KhonKaen report.
Run: python3 test_section3_filter.py
"""
import sys
import os

# Add the script directory to path so we can import generate_report
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Import the functions we want to test
from generate_report_27Jul2026 import extract_date, extract_venue, event_kw, all_forbidden

# Test counter
PASSED = 0
FAILED = 0

def test(name, fn):
    """Run a single test, print result."""
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

# ============================================================
# DATE PATTERN TESTS (Bug 2026-07-27: '1 – 5 สิงหาคม' ไม่ match)
# ============================================================

def test_date_1_5_singhm():
    """Bug 2026-07-27: '1 – 5 สิงหาคม' ไม่ match"""
    text = "📅 1 – 5 สิงหาคมนี้"
    result = extract_date(text)
    assert result == "1 – 5 สิงหาคม", f"Got: '{result}'"

def test_date_standard_with_year():
    """Standard pattern: '20 – 26 กรกฎาคม 2569' - regex catches end date"""
    text = "📅 20 – 26 กรกฎาคม 2569"
    result = extract_date(text)
    assert "กรกฎาคม 2569" in result, f"Got: '{result}'"

def test_date_short_month():
    """Short month: '25 ก.ค. 2569'"""
    text = "📅 25 ก.ค. 2569"
    result = extract_date(text)
    assert result == "25 ก.ค. 2569", f"Got: '{result}'"

def test_date_saturday():
    """Saturday pattern: 'วันเสาร์ที่ 25 ก.ค.'"""
    text = "งานวันเสาร์ที่ 25 ก.ค."
    result = extract_date(text)
    assert result == "วันเสาร์ที่ 25 ก.ค.", f"Got: '{result}'"

def test_date_wan_ni_last_day():
    """'วันนี้วันสุดท้าย'"""
    text = "BIG SALE วันนี้วันสุดท้าย"
    result = extract_date(text)
    assert result == "วันนี้วันสุดท้าย", f"Got: '{result}'"

def test_date_s_just_number():
    """'3 ส.ค.' (just day + month)"""
    text = "วันที่ 3 ส.ค. ที่เซ็นทรัล"
    result = extract_date(text)
    assert result, f"Got empty: '{result}'"

# ============================================================
# VENUE TESTS (Bug 2026-07-27: 'Lotus นครพนม' → wrong province)
# ============================================================

def test_venue_nakhonphanom_lotus():
    """Bug 2026-07-27: 'Lotus นครพนม' must NOT be 'โลตัส ขอนแก่น'"""
    text = "📍 Lotus's จังหวัดนครพนม"
    result = extract_venue(text)
    assert "นครพนม" in result, f"Should contain 'นครพนม', got: '{result}'"
    assert "ขอนแก่น" not in result, f"Should NOT contain 'ขอนแก่น', got: '{result}'"

def test_venue_khonkaen_central():
    """Default: 'เซ็นทรัล ขอนแก่น' ต้อง map ถูก"""
    text = "📍 เซ็นทรัล ขอนแก่น"
    result = extract_venue(text)
    assert result == "เซ็นทรัล ขอนแก่น", f"Got: '{result}'"

def test_venue_khonkaen_lotus():
    """Default: 'Lotus ขอนแก่น' ต้อง map เป็น 'โลตัส ขอนแก่น'"""
    text = "📍 Lotus ขอนแก่น"
    result = extract_venue(text)
    assert result == "โลตัส ขอนแก่น", f"Got: '{result}'"

def test_venue_udon_lotus():
    """Udon Thani: จังหวัดอื่นที่อยู่ใน context"""
    text = "📍 Lotus อุดรธานี"
    result = extract_venue(text)
    assert "อุดรธานี" in result, f"Should contain 'อุดรธานี', got: '{result}'"

def test_venue_showroom():
    """Default: 'โชว์รูม'"""
    text = "📍 โชว์รูม TOYOTA"
    result = extract_venue(text)
    assert result == "โชว์รูม", f"Got: '{result}'"

def test_venue_no_venue():
    """No venue detected → 'ไม่ระบุ'"""
    text = "มาพบกับงานรถยนต์"
    result = extract_venue(text)
    assert result == "ไม่ระบุ", f"Got: '{result}'"

# ============================================================
# EVENT KEYWORD TESTS
# ============================================================

def test_event_kw_samlap():
    """Added keyword: 'สัมผัส' (Geely 'สัมผัสคันจริง')"""
    text = "สัมผัสคันจริง GEELY EX2"
    text_lower = text.lower()
    assert any(k in text_lower for k in event_kw), "Should detect 'สัมผัส' as event keyword"

def test_event_kw_big_sale():
    """'big sale motor' event"""
    text = "BIG SALE MOTOR SHOW"
    text_lower = text.lower()
    assert any(k in text_lower for k in event_kw), "Should detect 'big sale motor'"

def test_event_kw_roadshow():
    """'roadshow' event"""
    text = "Roadshow GEELY"
    text_lower = text.lower()
    assert any(k in text_lower for k in event_kw), "Should detect 'roadshow'"

# ============================================================
# FORBIDDEN FILTER TESTS
# ============================================================

def test_forbidden_delivery():
    """Should reject 'ส่งมอบรถ' (delivery posts)"""
    text = "🎉 ขอแสดงความยินดี ส่งมอบรถ JAECOO คันแรก"
    assert any(k in text for k in all_forbidden), "Should detect 'ส่งมอบรถ' as forbidden"

def test_forbidden_service():
    """Should reject 'ศูนย์บริการ' (service posts)"""
    text = "ศูนย์บริการ Nissan ขอนแก่น เปิดให้บริการ"
    assert any(k in text for k in all_forbidden), "Should detect 'ศูนย์บริการ' as forbidden"

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("🚀 Running KhonKaen Section 3 Filter Tests...")
    print("=" * 60)
    
    # Date patterns
    print("\n📅 Date Patterns:")
    test("date_1_5_singhm", test_date_1_5_singhm)
    test("date_standard_with_year", test_date_standard_with_year)
    test("date_short_month", test_date_short_month)
    test("date_saturday", test_date_saturday)
    test("date_wan_ni_last_day", test_date_wan_ni_last_day)
    test("date_s_just_number", test_date_s_just_number)
    
    # Venue
    print("\n📍 Venue Detection:")
    test("venue_nakhonphanom_lotus", test_venue_nakhonphanom_lotus)
    test("venue_khonkaen_central", test_venue_khonkaen_central)
    test("venue_khonkaen_lotus", test_venue_khonkaen_lotus)
    test("venue_udon_lotus", test_venue_udon_lotus)
    test("venue_showroom", test_venue_showroom)
    test("venue_no_venue", test_venue_no_venue)
    
    # Event keywords
    print("\n🔑 Event Keywords:")
    test("event_kw_samlap", test_event_kw_samlap)
    test("event_kw_big_sale", test_event_kw_big_sale)
    test("event_kw_roadshow", test_event_kw_roadshow)
    
    # Forbidden filter
    print("\n🚫 Forbidden Filter:")
    test("forbidden_delivery", test_forbidden_delivery)
    test("forbidden_service", test_forbidden_service)
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {PASSED} passed, {FAILED} failed")
    print("=" * 60)
    
    if FAILED > 0:
        print("❌ Some tests FAILED — fix code before pushing!")
        sys.exit(1)
    else:
        print("✅ All tests PASSED — safe to push!")
        sys.exit(0)
