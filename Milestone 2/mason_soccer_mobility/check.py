import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


accounts = read("accounts.csv")
for field in ("item_id", "source_url"):
    if len({row[field] for row in accounts}) != len(accounts):
        raise ValueError(f"Duplicate {field}")
by_id = {row["item_id"]: row for row in accounts}
for row in accounts:
    for field in ("source_url", "evidence_note", "evidence_locator", "basis", "pathway", "frame"):
        if not row[field].strip():
            raise ValueError(f"{row['item_id']} missing {field}")
    for field in ("source_date", "accessed_date"):
        date.fromisoformat(row[field])
for match in read("audit.csv"):
    for item in match["account_ids"].split("|"):
        if by_id[item]["subject"] != match["player"]:
            raise ValueError(f"Player mismatch for {item}")
    if date.fromisoformat(match["announcement_date"]) > date.fromisoformat(match["league_transfer_date"]):
        raise ValueError("Check the transfer chronology")
print(f"{len(accounts)} accounts")
for producer, count in Counter(row["provenance"] for row in accounts).items():
    print(f"{producer}: {count}")
