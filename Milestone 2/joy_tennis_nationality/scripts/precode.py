"""Phase 3, transformation 2: snapshot text -> structured, provisional codes.

Two steps, both run by this one script:

1. Keyword pass (fully automatic, transparent). For every selected item it
   scans snapshots/<id>.txt with the keyword lists below and records which
   frame lists matched (keyword_flags), plus keyword hints for identities,
   money and player voice. Output: data/precode_flags.csv

2. Merge pass. Reads data/coding_suggestions.csv (evidence notes and frame
   suggestions drafted by the AI assistant after reading each snapshot,
   all marked provisional) and joins everything with players.csv and
   snapshot_log.csv into data/tennis_nationality_dataset.csv.

The keyword flags are NOT the codes. They are a cheap first look that tells a
human reviewer where to read. The frame_primary / frame_secondary columns come
from the reading, and reviewed_by stays blank until Joy checks each row.

Run from the joy_tennis_nationality folder:
    python scripts/precode.py
"""

import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
SNAP = BASE / "snapshots"

# ---------------------------------------------------------------------------
# Keyword lists. Each entry is a regex matched against lowercased text.
# Stems are used on purpose (e.g. "финанс" catches финансовый, финансирование).
# English first, then Russian, then the odd Italian/French term for the few
# non English, non Russian items. Edit these lists, rerun, and the flags update.
# ---------------------------------------------------------------------------
FRAME_KEYWORDS = {
    # money, coaching, facilities offered by a federation
    "opportunity_funding": [
        r"\bfund(ing|ed|s)?\b", r"financial(ly)? support", r"\bmoney\b", r"\bresources\b",
        r"\bcoach(es|ing)?\b", r"training (conditions|facilities|base)", r"provided everything",
        r"\binvest(ed|ment)?\b", r"\bsponsor", r"\bpaid\b",
        r"финанс", r"деньг", r"поддержк", r"услови[яй] для", r"инвест", r"спонсор", r"бесплатно",
        r"soldi", r"finanzi", r"sostegno", r"argent", r"financ", r"soutien",
    ],
    # rational career move: rankings, wild cards, chances
    "pragmatic_career": [
        r"\bcareer\b", r"\branking", r"wild ?card", r"\bopportunit", r"\bchance",
        r"\bdecision\b", r"\bchoice\b", r"\bpractical", r"\bcompetition\b",
        r"карьер", r"рейтинг", r"уайлд-?кард", r"решени", r"шанс", r"возможност", r"конкуренц",
        r"carriera", r"carrière",
    ],
    # abandoning a nation, not belonging
    "loyalty_betrayal": [
        r"\bbetray", r"\btraitor", r"\bloyal", r"\babandon", r"\bdefect", r"turn(ed)? (his|her|their) back",
        r"\bdesert", r"\bunpatriotic",
        r"предател", r"предательств", r"измен", r"потер[яи]", r"отказ(ал|ыва)", r"патриот", r"родин[уеы]",
        r"tradi", r"trahi",
    ],
    # war, sanctions, neutral status, political pressure
    "politics_war": [
        r"\bwar\b", r"\binvasion\b", r"\bukrain", r"\bsanction", r"\bneutral", r"\bbann?(ed)?\b",
        r"\bflag\b", r"lukashenko", r"\bkremlin\b", r"\bputin\b", r"\bpolitic", r"\bkyiv\b",
        r"войн", r"украин", r"санкци", r"нейтральн", r"флаг", r"отстран", r"лукашенк", r"политик",
        r"вторжени", r"иноагент",
        r"guerra", r"guerre", r"neutr",
    ],
    # new nation framed as real home or identity
    "belonging_homecoming": [
        r"\bhome\b", r"\bproud\b", r"feel(s)? (kazakh|australian|georgian|at home)", r"\bbelong",
        r"new chapter", r"\bgrateful\b", r"\bwelcom", r"\bfamily\b", r"new homeland", r"\bsafe\b",
        r"горд", r"чувствую себя", r"благодар", r"нов(ая|ой|ую) родин", r"\bдом\b", r"как дома",
        r"casa", r"fier", r"chez (moi|elle|lui)",
    ],
    # nationality as bought, nominal, a passport of convenience
    "flag_of_convenience": [
        r"rent-a-russian", r"\bbought\b", r"\bimport(s|ed)?\b", r"\bpassport", r"convenience",
        r"naturali[sz]", r"\bmercenar", r"\brecruit", r"in order to play", r"to avoid", r"loophole",
        r"легионер", r"куп(ил|лен)", r"паспорт", r"натурализ", r"импорт", r"чтобы сыграть",
        r"mercenai", r"passaport",
    ],
}

IDENTITY_KEYWORDS = {
    "birthplace": [r"\bborn\b", r"birthplace", r"\bnative of\b", r"родил", r"уроженк", r"уроженец",
                   r"\bnata\b", r"\bnée?\b"],
    "citizenship": [r"citizen", r"passport", r"nationalit", r"гражданств", r"паспорт", r"cittadinanza",
                    r"nationalité"],
    "residence": [r"lives in", r"\blive[sd]? in\b", r"residen", r"based in", r"вид на жительство",
                  r"прожива", r"живет в", r"живёт в", r"переехал"],
    "training_base": [r"\btrain(s|ed|ing)? (in|at)\b", r"\bacademy\b", r"training base",
                      r"тренир(уется|овал)", r"академи", r"база"],
    "federation": [r"federation", r"\bktf\b", r"tennis australia", r"\bitf\b", r"федерац", r"\bфтк\b",
                   r"federazione", r"fédération"],
    "heritage": [r"\bfather\b", r"\bmother\b", r"\bparents\b", r"\broots\b", r"heritage", r"ethnic",
                 r"\bdescent\b", r"отец", r"\bмать\b", r"родител", r"корн", r"padre", r"père"],
}

MONEY_KEYWORDS = FRAME_KEYWORDS["opportunity_funding"][:10] + [
    r"\$\d", r"\bdollars?\b", r"\bprize money\b", r"деньг", r"финанс", r"долл", r"soldi", r"argent"]

# player voice: a quote mark near a speech verb. Crude on purpose; the reader decides.
VOICE_PATTERN = re.compile(
    r"([\"“”«»].{10,}?[\"“”«»]).{0,80}?\b(said|says|told|added|explained|wrote|posted|"
    r"сказал|сказала|заявил|заявила|признал|признала|отметил|отметила|рассказал|рассказала|"
    r"ha detto|a déclaré)\b"
    r"|\b(said|says|told|explained)\b.{0,10}?[\"“”«]",
    re.IGNORECASE | re.DOTALL,
)

COMPILED = {k: [re.compile(p) for p in v] for k, v in FRAME_KEYWORDS.items()}
COMPILED_ID = {k: [re.compile(p) for p in v] for k, v in IDENTITY_KEYWORDS.items()}
COMPILED_MONEY = [re.compile(p) for p in MONEY_KEYWORDS]


def hits(text, patterns):
    return sum(len(p.findall(text)) for p in patterns)


def keyword_pass(selected):
    rows = []
    for cid in selected:
        path = SNAP / f"{cid}.txt"
        text = path.read_text(encoding="utf-8").lower() if path.exists() else ""
        frame_hits = {k: hits(text, v) for k, v in COMPILED.items()}
        # a frame is flagged when it has 2+ keyword hits; one stray "flag" is noise
        flags = [k for k, n in sorted(frame_hits.items(), key=lambda x: -x[1]) if n >= 2]
        ids = [k for k, v in COMPILED_ID.items() if hits(text, v) >= 1]
        rows.append({
            "candidate_id": cid,
            "keyword_flags": "|".join(flags),
            **{f"hits_{k}": n for k, n in frame_hits.items()},
            "kw_identities": "|".join(ids),
            "kw_money": "yes" if hits(text, COMPILED_MONEY) else "no",
            "kw_quote": "yes" if VOICE_PATTERN.search(text) else "no",
        })
    with (DATA / "precode_flags.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return {r["candidate_id"]: r for r in rows}


def read_csv(path, key=None):
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {r[key]: r for r in rows} if key else rows


def iso_date(raw):
    """trafilatura gives YYYY-MM-DD already; anything else is left blank."""
    return raw if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw or "") else ""


DATASET_FIELDS = [
    "item_id", "player", "from_nation", "to_nation", "switch_year", "outlet", "outlet_country",
    "url", "pub_date", "access_date", "item_type", "language", "snapshot_sha256", "evidence_note",
    "frame_primary", "frame_secondary", "identities_mentioned", "money_mentioned", "player_voice",
    "keyword_flags", "uncertainty_note", "reviewed_by",
]


def main():
    suggestions = read_csv(DATA / "coding_suggestions.csv")
    selected = [s["candidate_id"] for s in suggestions]
    flags = keyword_pass(selected)
    print(f"keyword pass: {len(flags)} items -> data/precode_flags.csv")

    cands = read_csv(DATA / "candidates.csv", "candidate_id")
    snaps = read_csv(DATA / "snapshot_log.csv", "candidate_id")
    players = read_csv(DATA / "players.csv", "player")

    # rows Joy already reviewed are kept exactly as he left them, so rerunning
    # this script never overwrites human coding with AI suggestions
    dataset_path = DATA / "tennis_nationality_dataset.csv"
    reviewed = {}
    if dataset_path.exists():
        for r in read_csv(dataset_path):
            if r.get("reviewed_by", "").strip():
                reviewed[r["url"]] = r

    out = []
    for n, s in enumerate(suggestions, 1):
        url = cands[s["candidate_id"]]["url"]
        if url in reviewed:
            kept = dict(reviewed[url], item_id=f"TEN{n:03d}")
            out.append(kept)
            continue
        cid = s["candidate_id"]
        c, snap, p = cands[cid], snaps[cid], players[s["player_canonical"]]
        out.append({
            "item_id": f"TEN{n:03d}",
            "player": s["player_as_written"],
            "from_nation": p["from_nation"],
            "to_nation": p["to_nation"],
            "switch_year": p["switch_year"],
            "outlet": c["outlet"],
            "outlet_country": c["outlet_country"],
            "url": c["url"],
            # a date read off the page by hand beats the metadata guess;
            # "unknown" means the metadata date is clearly wrong, so leave it blank
            "pub_date": "" if s.get("pub_date_override") == "unknown"
                        else s.get("pub_date_override") or iso_date(snap["meta_pub_date"]),
            "access_date": snap["access_date"],
            "item_type": s["item_type"],
            "language": c["language"],
            "snapshot_sha256": snap["snapshot_sha256"],
            "evidence_note": s["evidence_note"],
            "frame_primary": s["frame_primary"],
            "frame_secondary": s["frame_secondary"],
            "identities_mentioned": s["identities_mentioned"],
            "money_mentioned": s["money_mentioned"],
            "player_voice": s["player_voice"],
            "keyword_flags": flags[cid]["keyword_flags"],
            "uncertainty_note": s["uncertainty_note"],
            "reviewed_by": "",  # only Joy fills this in
        })

    with (DATA / "tennis_nationality_dataset.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=DATASET_FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"merge pass: {len(out)} rows -> data/tennis_nationality_dataset.csv")


if __name__ == "__main__":
    main()
