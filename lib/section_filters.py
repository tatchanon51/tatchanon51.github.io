# Shared filters for Nissan weekly reports — Phase 2A
# 2026-07-27

import re

# === Section 3/4/5 Filters (shared) ===

VENUE_MARKERS = ['📍', '📌', '🚩', '🏛️', '🏪', '🏢']
ADDRESS_HINTS = ['โชว์รูม', 'ถนน', 'ข้าง', 'ใกล้', 'ติด', 'ริม', 'ซอย']

DATE_PATTERNS = [
    # === July (ก.ค.) ===
    r'วันที่\s*\d{1,2}\s*-\s*\d{1,2}\s*ก\.?ค\.?',
    r'วันที่\s*\d{1,2}\s*กรกฎาคม\s*2569',
    r'วันที่\s*\d{1,2}\s*ก\.?ค\.?\s*2569',
    r'\d{1,2}\s*-\s*\d{1,2}\s*ก\.?ค\.?\s*2569',
    r'\d{1,2}\s*-\s*\d{1,2}\s*กรกฎาคม\s*2569',
    r'\d{1,2}\s*-\s*\d{1,2}\s*ก\.?ค\.?',
    r'วันเสาร์ที่\s*\d{1,2}\s*ก\.?ค\.?',
    # === August (ส.ค.) — Added 2026-07-27 ===
    r'\d{1,2}\s*[-–]\s*\d{1,2}\s*ส\.?ค\.?',
    r'\d{1,2}\s*[-–]\s*\d{1,2}\s*สิงหาคม',
    r'\d{1,2}\s*ส\.?ค\.?\s*2569',
    r'\d{1,2}\s*สิงหาคม\s*2569',
    r'\d{1,2}\s*สิงหาคม',
    r'\d{1,2}\s*ส\.?ค\.?',
    # === Common ===
    r'เริ่มแล้ววันนี้',
    r'วันนี้วันสุดท้าย',
    r'\d{1,2}\s*ก\.?ค\.?\s*2569',
    r'\d{1,2}\s*กรกฎาคม\s*2569',
]

EVENT_KW = [
    # Original 7
    'บูธ', 'motor show', 'roadshow', 'พบกับ', 'on tour', 'big sale motor', 'ทดลองขับ',
    # Expanded 2026-07-27
    'สัมผัส', 'เปิดตัว', 'ฉลอง', 'วันนี้', 'ร่วมงาน', 'พร้อมพบ', 'เตรียมพบ', 'งาน',
    'event', 'mini smile day', 'big day', 'มอเตอร์โชว์', 'test drive',
    'เที่ยวงาน', 'เชิญชวน', 'ถึงเวลา', 'road show', 'celebration', 'โชว์',
    'เปิดให้บริการ', 'โปรโมชั่น', 'แคมเปญ', 'เปิดจอง',
]

FORBIDDEN = [
    'ส่งมอบรถ', 'ยินดีด้วย', 'เข้าสู่ครอบครัว', 'รับเป็นเจ้าของ',
    'ขอแสดงความยินดี', 'ศูนย์บริการ', 'เช็คระยะ', 'เปลี่ยนถ่ายน้ำมัน',
    'บริการหลังการขาย', 'ตรวจเช็ค', 'ยอดขายอันดับ', 'ฉลองยอดขาย',
    'รับสมัคร', 'สมัครงาน', 'อบรม', 'งานวัด', 'งานบุญ', 'เปรียบเทียบ',
]

# Smart Venue Normalizer (Phase 2A)
VENUE_NORMALIZER = [
    # === Central Ubon (English/Thai variants) ===
    (r'(?:เซ็นทรัล|เซ็ทรัล|Central|central).*?(?:อุบล|อุบลฯ|Ubon|ubn|อุบลราชธานี)', 'เซ็นทรัล อุบล'),
    # === Central KhonKaen ===
    (r'(?:เซ็นทรัล|เซ็ทรัล|Central|central).*?(?:ขอนแก่น|Khon ?Kaen)', 'เซ็นทรัล ขอนแก่น'),
    # === Big C Ubon ===
    (r'(?:บิ๊กซี|BIG ?C|Big ?C).*?(?:อุบล|อุบลฯ|Ubon|ubn|อุบลราชธานี)', 'BIG C อุบล'),
    # === Big C KhonKaen ===
    (r'(?:บิ๊กซี|BIG ?C|Big ?C).*?(?:ขอนแก่น|Khon ?Kaen)', 'BIG C ขอนแก่น'),
    # === Lotus Ubon ===
    (r'(?:โลตัส|Lotus).*?(?:อุบล|อุบลฯ|Ubon|ubn|อุบลราชธานี)', 'โลตัส อุบล'),
    # === Lotus KhonKaen ===
    (r'(?:โลตัส|Lotus).*?(?:ขอนแก่น|Khon ?Kaen)', 'โลตัส ขอนแก่น'),
    # === Generic English fallback ===
    (r'Central\s+Ubon', 'เซ็นทรัล อุบล'),
    (r'Central\s+Khon ?Kaen', 'เซ็นทรัล ขอนแก่น'),
]


def extract_date(text):
    """Extract Thai date from text. Returns first matching date string or ''."""
    for pat in DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            return m.group(0).strip()
    return ''


def extract_venue(text, venue_map=None):
    """📍-marker aware venue extraction with Smart Normalizer + venue_map fallback.
    venue_map=None → use module-level venue_map if available, else rely on VENUE_NORMALIZER.
    Returns normalized venue name or 'ไม่ระบุ'.
    """
    if venue_map is None:
        venue_map = globals().get('venue_map', [])

    # Step 1: Find marker lines
    marker_lines = []
    for marker in VENUE_MARKERS:
        pattern = re.escape(marker) + r'\s*([^\n' + ''.join(re.escape(m) for m in VENUE_MARKERS) + r']+)'
        for m in re.finditer(pattern, text):
            marker_lines.append(m.group(1).strip())

    # Step 2: Filter out address lines
    candidates = [l for l in marker_lines if not any(h in l for h in ADDRESS_HINTS)]
    if not candidates:
        candidates = marker_lines

    # Step 3: VENUE_NORMALIZER (smart patterns)
    for line in candidates:
        for pattern, normalized in VENUE_NORMALIZER:
            if re.search(pattern, line):
                return normalized

    # Step 4: venue_map fallback (legacy)
    for line in candidates:
        for k, v in venue_map:
            if k in line:
                return v

    return 'ไม่ระบุ'


def is_event_post(text):
    """Check if post should be in Section 3/4/5 (Roadshow)."""
    text_lower = text.lower()
    if any(k in text for k in FORBIDDEN):
        return False
    if not any(k in text_lower for k in EVENT_KW):
        return False
    return True
