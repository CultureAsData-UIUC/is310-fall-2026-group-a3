"""Check the CSV and generate a searchable collection page. Python 3 only."""
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parents[1]
STRANDS={'athlete_mobility':'soccer','nba_global':'basketball','f1_allegiance':'formula_1'}
FLAGS=['development','national_identity','audience_connection','competing_allegiance']
FIELDS=['item_id','strand','sport','record_label','source_date','date_basis','publisher','originator','provenance','subject','language','evidence_note',*FLAGS,'movement','inspected_scope','evidence_locator','access_method','accessed_date','source_url','review_status','reviewer','date_note']

def validate(rows,headers):
    errors=[]
    if headers!=FIELDS: errors.append('Column names or order differ from the codebook schema.')
    ids=set(); urls=set()
    allowed={'date_basis':{'published','updated','edited','not_displayed'},'provenance':{'institutional','independent'},'movement':{'relocation_discussed','domestic_pathway','not_established'},'inspected_scope':{'article_body','transcript_section','article_excerpt'},'access_method':{'original_page','indexed_text'},'review_status':{'provisional','student_verified'}}
    for rownum,row in enumerate(rows,2):
        prefix=f'Row {rownum} {row.get("item_id", "?")}: '
        if None in row or any(v is None for v in row.values()): errors.append(prefix+'Column count mismatch.')
        for field in FIELDS:
            if field not in {'source_date','reviewer','date_note'} and not (row.get(field) or '').strip(): errors.append(prefix+f'Missing {field}.')
        rid=row.get('item_id','')
        if not re.fullmatch(r'(?:SOC|NBA|F1)\d{3}',rid): errors.append(prefix+'Invalid ID.')
        if rid in ids: errors.append(prefix+'Duplicate ID.')
        ids.add(rid)
        try:
            url=urlsplit(row.get('source_url') or '')
            if url.scheme not in {'http','https'} or not url.netloc: raise ValueError()
            key=urlunsplit((url.scheme.lower(),url.netloc.lower().removeprefix('www.'),url.path.rstrip('/'),url.query,''))
            if key in urls: errors.append(prefix+'Duplicate source URL.')
            urls.add(key)
        except ValueError: errors.append(prefix+'Invalid source URL.')
        if row.get('strand') not in STRANDS or STRANDS.get(row.get('strand'))!=row.get('sport'): errors.append(prefix+'Strand and sport do not match.')
        for field in FLAGS:
            if row.get(field) not in {'yes','no','unclear'}: errors.append(prefix+f'Invalid {field}.')
        for field,values in allowed.items():
            if row.get(field) not in values: errors.append(prefix+f'Invalid {field}.')
        dates={}
        for field in ['source_date','accessed_date']:
            value=row.get(field) or ''
            if field=='source_date' and not value:
                if row.get('date_basis')!='not_displayed' or not row.get('date_note'): errors.append(prefix+'Blank date needs not_displayed basis and a note.')
                continue
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError()
                dates[field]=date.fromisoformat(value)
            except ValueError: errors.append(prefix+f'Invalid {field}.')
        if row.get('source_date') and row.get('date_basis')=='not_displayed': errors.append(prefix+'Date value conflicts with not_displayed basis.')
        if row.get('date_basis') in {'updated','edited'} and not row.get('date_note'): errors.append(prefix+'Changed date needs a note.')
        if 'source_date' in dates and not date(2017,1,1)<=dates['source_date']<=date(2026,10,22): errors.append(prefix+'Source date outside collection window.')
        if len(dates)==2 and dates['source_date']>dates['accessed_date']: errors.append(prefix+'Source date follows access date.')
        if row.get('review_status')=='student_verified' and not (row.get('reviewer') or '').strip(): errors.append(prefix+'Student verification needs a reviewer.')
    return errors

def main():
    with (ROOT/'data/sports_media_dataset.csv').open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f); headers=reader.fieldnames; rows=list(reader)
    errors=validate(rows,headers)
    counts=Counter(r['strand'] for r in rows)
    warnings=[]
    if len(rows)!=75: warnings.append(f'{len(rows)} records present against a proposed target of 75.')
    for s in STRANDS:
        if counts[s]!=25: warnings.append(f'{s} has {counts[s]} items against the proposed 25.')
    missing=[r['item_id'] for r in rows if not r['source_date']]
    indexed=[r['item_id'] for r in rows if r['access_method']=='indexed_text']
    unreviewed=[r['item_id'] for r in rows if r['review_status']!='student_verified']
    if missing: warnings.append(f'{len(missing)} source dates were not displayed; verify before time-based analysis.')
    if indexed: warnings.append(f'{len(indexed)} records use indexed text rather than readable original-page text.')
    if unreviewed: warnings.append(f'{len(unreviewed)} records await student review.')
    provenance={s:dict(Counter(r['provenance'] for r in rows if r['strand']==s)) for s in STRANDS}
    for s in STRANDS:
        if provenance[s].get('independent',0)<10: warnings.append(f'{s} has fewer than the proposed ten independent reporting items.')
    report={'record_count':len(rows),'by_strand':dict(counts),'unique_source_urls':len(set(r['source_url'] for r in rows)),'provenance_by_strand':provenance,'access_methods':dict(Counter(r['access_method'] for r in rows)),'dates_not_displayed':missing,'indexed_text_records':indexed,'awaiting_student_review':len(unreviewed),'structural_errors':errors,'review_warnings':warnings,'limitation':'Checks cover structure, not factual accuracy or interpretation. Same-event stories are not independent observations.'}
    out=ROOT/'reports'; out.mkdir(exist_ok=True)
    (out/'quality_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    data=json.dumps(rows,ensure_ascii=False).replace('<','\\u003c')
    template='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>IS310 sports media dataset</title><style>
    *{box-sizing:border-box}body{margin:0;background:#f3f5f8;color:#202a35;font:16px/1.55 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:38px 24px}h1{font-size:34px;line-height:1.15;max-width:760px}p{max-width:900px}.muted{color:#566575}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.stat{background:#fff;border:1px solid #dae0e6;padding:12px 20px;border-radius:8px}.stat b{font-size:23px;display:block}.controls{display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:0;background:#f3f5f8;padding:14px 0;border-bottom:1px solid #d5dde4}input,select,button{font:inherit;border:1px solid #aebbc7;border-radius:5px;padding:9px;background:white}input{flex:1;min-width:220px}article{background:white;border:1px solid #dbe1e7;border-radius:8px;margin:18px 0;padding:22px}h2{font-size:21px;margin:6px 0}article p{margin:10px 0}.tag{font-size:13px;color:#42566b}.codes{font-size:14px;background:#f4f6f8;padding:12px}a{color:#1358a2}details{font-size:14px;margin:12px 0}.review{color:#875400}footer{margin-top:28px;font-size:14px}</style><main>
    <p class="muted">IS310 · Mason, Drew, and Bob · Collection prepared October 22, 2026</p><h1>Sports media and national identity across borders</h1>
    <p>75 article and transcript records covering development and mobility, international NBA players, and Formula 1 allegiance. Codes describe the recorded text. They do not establish causal effects or represent all fan opinion.</p>
    <div class="stats"><div class="stat"><b>25</b>Soccer</div><div class="stat"><b>25</b>NBA</div><div class="stat"><b>25</b>Formula 1</div></div>
    <p class="review">All codes await student review. Some records use indexed excerpts; three source dates were not displayed. Open each source to verify the evidence before submission.</p>
    <div class="controls"><input id="query" aria-label="Search records" placeholder="Search athlete, source, evidence, or ID"><select id="strand" aria-label="Filter strand"><option value="">All topics</option><option value="athlete_mobility">Soccer development and mobility</option><option value="nba_global">International NBA players</option><option value="f1_allegiance">Formula 1 allegiance</option></select><select id="access" aria-label="Filter source access"><option value="">All access methods</option><option value="original_page">Original page text</option><option value="indexed_text">Indexed text</option></select><button id="reset">Reset</button></div><p id="count" class="muted"></p><section id="records"></section><footer>Full coding definitions are in codebook.md. Source labels abbreviate original headlines. This page reads the saved collection; rerun the Python program after changing the CSV.</footer></main><script>
    const rows=__DATA__;const esc=x=>String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    function draw(){const q=document.getElementById('query').value.toLowerCase(),s=document.getElementById('strand').value,a=document.getElementById('access').value;const show=rows.filter(r=>(!s||r.strand===s)&&(!a||r.access_method===a)&&Object.values(r).join(' ').toLowerCase().includes(q));document.getElementById('count').textContent=show.length+' of '+rows.length+' records';document.getElementById('records').innerHTML=show.map(r=>`<article><div class="tag">${esc(r.item_id)} · ${esc(r.strand.replaceAll('_',' '))} · ${esc(r.subject)}</div><h2>${esc(r.record_label)}</h2><p class="muted">${esc(r.publisher)} · ${esc(r.source_date||'Date not displayed')} · ${esc(r.date_basis)}</p><p>${esc(r.evidence_note)}</p><div class="codes">Development: ${esc(r.development)} · National identity: ${esc(r.national_identity)} · Audience connection: ${esc(r.audience_connection)} · Competing allegiance: ${esc(r.competing_allegiance)}<br>Movement: ${esc(r.movement.replaceAll('_',' '))}</div><details><summary>Evidence and review details</summary><p>Location: ${esc(r.evidence_locator)}<br>Scope: ${esc(r.inspected_scope)}<br>Access: ${esc(r.access_method)} on ${esc(r.accessed_date)}<br>Originator: ${esc(r.originator)} (${esc(r.provenance)})<br>Review: ${esc(r.review_status)}${r.date_note?'<br>Date note: '+esc(r.date_note):''}</p></details><a href="${esc(r.source_url)}" target="_blank" rel="noopener noreferrer">Read source</a></article>`).join('');}document.querySelectorAll('input,select').forEach(x=>x.addEventListener('input',draw));document.getElementById('reset').onclick=()=>{document.querySelectorAll('input,select').forEach(x=>x.value='');draw()};draw();</script></html>'''
    template=template.replace('75 article and transcript records',f'{len(rows)} article and transcript records')
    template=template.replace('<b>25</b>Soccer',f'<b>{counts["athlete_mobility"]}</b>Soccer').replace('<b>25</b>NBA',f'<b>{counts["nba_global"]}</b>NBA').replace('<b>25</b>Formula 1',f'<b>{counts["f1_allegiance"]}</b>Formula 1')
    template=template.replace('All codes await student review. Some records use indexed excerpts; three source dates were not displayed. Open each source to verify the evidence before submission.',f'{len(unreviewed)} records await student review; {len(indexed)} use indexed excerpts; {len(missing)} source dates were not displayed. Open each source to verify the evidence before submission.')
    (out/'collection_report.html').write_text(template.replace('__DATA__',data),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return 1 if errors else 0

if __name__=='__main__': sys.exit(main())
