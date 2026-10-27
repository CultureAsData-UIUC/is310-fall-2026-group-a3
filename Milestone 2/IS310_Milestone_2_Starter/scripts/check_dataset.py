"""Validate the group CSV and build a local HTML collection report.

Run with Python 3. Standard library only. This checks structure, not truth.
"""
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
STRANDS = {"athlete_mobility": "soccer", "nba_global": "basketball", "f1_allegiance": "formula_1"}
FLAGS = ("development", "national_identity", "audience_connection", "competing_allegiance")
FIELDS = ["item_id", "strand", "sport", "record_label", "source_url", "publisher", "originator", "provenance", "published_date", "accessed_date", "subject", "language", "inspected_scope", "evidence_locator", "evidence_note", *FLAGS, "movement", "review_status", "reviewer"]


def canonical_url(value):
    parts = urlsplit(value)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), parts.query, ""))


def build_report():
    errors = []
    with (ROOT / "data" / "pilot_dataset.csv").open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        headers = reader.fieldnames or []
        rows = list(reader)
    if headers != FIELDS:
        errors.append("CSV header must match the fields in codebook.md in their documented order.")
    ids, urls = set(), set()
    for line, row in enumerate(rows, 2):
        prefix = f"Row {line} ({row.get('item_id', '?')}): "
        if None in row or any(value is None for value in row.values()):
            errors.append(prefix + "column count does not match header")
        for field in FIELDS:
            if field != "reviewer" and not str(row.get(field) or "").strip():
                errors.append(prefix + f"missing {field}")
        item_id = row.get("item_id", "")
        if not re.fullmatch(r"(?:SOC|NBA|F1)\d{3}", item_id):
            errors.append(prefix + "unexpected item ID format")
        if item_id in ids:
            errors.append(prefix + "duplicate item ID")
        ids.add(item_id)
        url = row.get("source_url") or ""
        try:
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("expected an HTTP or HTTPS URL")
            normalized = canonical_url(url)
            if normalized in urls:
                errors.append(prefix + "duplicate source URL")
            urls.add(normalized)
        except ValueError:
            errors.append(prefix + "invalid source URL")
        if STRANDS.get(row.get("strand")) != row.get("sport"):
            errors.append(prefix + "strand and sport do not match")
        for flag in FLAGS:
            if row.get(flag) not in {"yes", "no", "unclear"}:
                errors.append(prefix + f"invalid {flag}")
        allowed = {
            "provenance": {"institutional", "independent"},
            "movement": {"relocation_discussed", "domestic_pathway", "not_established"},
            "review_status": {"provisional", "student_verified"},
            "inspected_scope": {"article_body", "transcript_section"},
        }
        for field, values in allowed.items():
            if row.get(field) not in values:
                errors.append(prefix + f"invalid {field}")
        dates = {}
        for field in ("published_date", "accessed_date"):
            try:
                value = row.get(field) or ""
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError()
                dates[field] = date.fromisoformat(value)
            except ValueError:
                errors.append(prefix + f"invalid {field}")
        if "published_date" in dates and not date(2017, 1, 1) <= dates["published_date"] <= date(2026, 10, 22):
            errors.append(prefix + "publication is outside the proposed collection window")
        if len(dates) == 2 and dates["published_date"] > dates["accessed_date"]:
            errors.append(prefix + "publication date follows access date")
        if row.get("review_status") == "student_verified" and not (row.get("reviewer") or "").strip():
            errors.append(prefix + "student verification requires a named reviewer")
    counts = Counter(row.get("strand") for row in rows)
    provisional = sum(row.get("review_status") != "student_verified" for row in rows)
    report = {
        "record_count": len(rows), "proposed_target": 75,
        "remaining_to_target": max(75 - len(rows), 0),
        "by_strand": {strand: counts[strand] for strand in STRANDS},
        "remaining_by_strand": {strand: max(25 - counts[strand], 0) for strand in STRANDS},
        "awaiting_student_review": provisional, "structural_errors": errors,
        "note": "Counts describe this selected corpus. Passing checks does not verify facts or interpretation."
    }
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "quality_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    esc = lambda value: html.escape(str(value or ""), quote=True)
    cards = []
    for row in rows:
        url = row.get("source_url") or ""
        try:
            safe_url = url if urlsplit(url).scheme in {"http", "https"} else ""
        except ValueError:
            safe_url = ""
        labels = "; ".join(f"{key.replace('_', ' ')}: {row.get(key)}" for key in FLAGS)
        cards.append(f'<article><h2>{esc(row.get("item_id"))} {esc(row.get("record_label"))}</h2>'
                     f'<p>{esc(row.get("strand"))} | {esc(row.get("published_date"))} | {esc(row.get("review_status"))}</p>'
                     f'<p>{esc(row.get("evidence_note"))}</p><p><strong>Evidence location:</strong> {esc(row.get("evidence_locator"))}</p>'
                     f'<p>{esc(labels)}</p><a href="{esc(safe_url)}" rel="noreferrer">Read original source</a></article>')
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>IS310 group collection report</title><style>body{max-width:900px;margin:40px auto;padding:0 24px;font:17px/1.6 system-ui;color:#17202a;background:#f6f8fa}h1{line-height:1.2}article{background:white;padding:24px;margin:20px 0;border:1px solid #ccd3db;border-radius:8px}h2{font-size:21px}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#174ea6}</style>'
            '<h1>Sports media and national identity across borders</h1>'
            f'<p><strong>{len(rows)} of 75 proposed items</strong> | {provisional} awaiting student review | {len(errors)} structural errors</p>'
            '<p>This pilot documents a collection method. It does not establish findings about sports audiences or migration.</p>'
            '<details><summary>Quality report</summary><pre>' + esc(json.dumps(report, indent=2)) + '</pre></details>'
            + ''.join(cards) + '</html>')
    (report_dir / "collection_report.html").write_text(page, encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(build_report())
