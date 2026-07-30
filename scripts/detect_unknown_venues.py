#!/usr/bin/env python3
"""Unknown venue detector — scans report HTML for 'ไม่ระบุ' venues.
Usage:
  python3 detect_unknown_venues.py <report.html> [--alert]
"""
import sys
import re
import os
import json
from datetime import datetime

UNKNOWN_LOG = "/Users/tatchanon/.hermes/profiles/office-shirm/.hermes/cron/unknown_venues.json"


def scan_html(html_path):
    """Scan HTML for 'ไม่ระบุ' venues in Section 4 (Roadshow)."""
    if not os.path.exists(html_path):
        return []

    with open(html_path) as f:
        c = f.read()

    # Section 4 (Roadshow)
    sec_start = c.find('🎪 กิจกรรม Roadshow')
    sec_end = c.find('📊 ตารางสรุปคู่แข่ง', sec_start)
    if sec_start == -1 or sec_end == -1:
        return []

    section = c[sec_start:sec_end]
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', section, re.DOTALL)

    unknowns = []
    for row in rows[1:]:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if cells and len(cells) >= 4:
            venue = re.sub(r'<[^>]+>', ' ', cells[4]).strip()
            if 'ไม่ระบุ' in venue or not venue:
                # Get the post text snippet
                text_snippet = re.sub(r'<[^>]+>', ' ', cells[2]).strip()[:150]
                brand = re.sub(r'<[^>]+>', ' ', cells[0]).strip()
                unknowns.append({
                    'brand': brand,
                    'text': text_snippet,
                    'venue': venue or '(empty)'
                })
    return unknowns


def log_unknowns(unknowns, source):
    """Save unknowns to JSON log for weekly review."""
    if not unknowns:
        return 0

    existing = []
    if os.path.exists(UNKNOWN_LOG):
        try:
            with open(UNKNOWN_LOG) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing = []

    entry = {
        'timestamp': datetime.now().isoformat(),
        'source': source,
        'count': len(unknowns),
        'unknowns': unknowns
    }
    existing.append(entry)

    # Keep only last 20 entries
    existing = existing[-20:]

    with open(UNKNOWN_LOG, 'w') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return len(unknowns)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_unknown_venues.py <report.html>")
        sys.exit(1)

    html_path = sys.argv[1]
    unknowns = scan_html(html_path)

    if unknowns:
        print(f"⚠️ Found {len(unknowns)} 'ไม่ระบุ' venues in {html_path}:")
        for u in unknowns:
            print(f"  • {u['brand']:20} | text: {u['text'][:80]}")

        n = log_unknowns(unknowns, html_path)
        print(f"📝 Logged to {UNKNOWN_LOG}")
    else:
        print(f"✅ No unknown venues in {html_path}")
