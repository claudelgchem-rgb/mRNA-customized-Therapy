#!/usr/bin/env python3
"""INTX 근거 카드 UI 렌더러.

out/evidence_ledger.jsonl  ->  out/INTX_evidence.html

단일 파일 self-contained HTML. 외부 리소스 의존 없음.
- 등급(상/중/하)·모듈(M1-M7)·에이전트·출처유형별 필터
- 전문 검색
- #R042 앵커로 보고서에서 딥링크 가능
"""

import html
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(ROOT, "out", "evidence_ledger.jsonl")
OUT = os.path.join(ROOT, "out", "INTX_evidence.html")

GRADE_ORDER = {"상": 0, "중": 1, "하": 2}

SOURCE_LABEL = {
    "peer_reviewed": "peer-reviewed 원논문",
    "regulatory": "규제기관 문서",
    "registry": "임상시험 등록정보",
    "company_filing": "기업 공시",
    "company_pr": "기업 보도자료",
    "conference_abstract": "학회 초록·발표",
    "patent": "특허 원문",
    "trade_press": "산업지 취재",
    "secondary": "2차 요약",
}

MODULE_LABEL = {
    "M1": "M1 기술스택",
    "M2": "M2 임상근거",
    "M3": "M3 제조·CMC",
    "M4": "M4 특허·FTO",
    "M5": "M5 시장·경제성",
    "M6": "M6 정책·리스크",
    "M7": "M7 종합판정",
}


def rid_key(rid):
    try:
        return int(str(rid).lstrip("Rr") or 0)
    except ValueError:
        return 10**9


def load(path):
    rows, bad = [], []
    if not os.path.exists(path):
        sys.exit(f"[FATAL] 근거 원장이 없습니다: {path}")
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                bad.append((i, str(exc)))
    if bad:
        print(f"[WARN] 파싱 실패 {len(bad)}줄: {bad[:5]}", file=sys.stderr)
    return rows


def esc(v):
    return html.escape(str(v if v is not None else ""), quote=True)


def card(r):
    rid = r.get("rid", "R???")
    grade = r.get("reliability") or r.get("reliability_self") or "미등급"
    module = r.get("module", "")
    agent = r.get("agent", "")
    stype = r.get("source_type", "")
    url = r.get("url", "")
    conflicts = r.get("conflicts_with") or []

    link = (
        f'<a class="src-url" href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>'
        if str(url).startswith("http")
        else f'<span class="src-url none">{esc(url) or "URL 미확보"}</span>'
    )

    conflict_html = ""
    if conflicts:
        chips = " ".join(
            f'<a class="conflict" href="#{esc(c)}">{esc(c)}</a>' for c in conflicts
        )
        conflict_html = f'<div class="row"><span class="k">충돌 근거</span><span class="v">{chips}</span></div>'

    def row(k, v, cls=""):
        if not v:
            return ""
        return f'<div class="row"><span class="k">{esc(k)}</span><span class="v {cls}">{esc(v)}</span></div>'

    haystack = " ".join(
        str(r.get(f, "")) for f in
        ("rid", "claim", "title", "publisher", "quote_ko", "notes", "locator",
         "reliability_rationale", "url", "agent", "module")
    ).lower()

    return f"""
<article class="card" id="{esc(rid)}"
         data-grade="{esc(grade)}" data-module="{esc(module)}"
         data-agent="{esc(agent)}" data-stype="{esc(stype)}"
         data-q="{esc(haystack)}">
  <header class="card-head">
    <a class="rid" href="#{esc(rid)}">{esc(rid)}</a>
    <span class="badge g-{esc(grade)}">{esc(grade)}</span>
    <span class="badge mod">{esc(MODULE_LABEL.get(module, module))}</span>
    <span class="badge agent">{esc(agent)}</span>
    <span class="badge stype">{esc(SOURCE_LABEL.get(stype, stype))}</span>
  </header>
  <p class="claim">{esc(r.get('claim'))}</p>
  <div class="meta">
    {row('출처', r.get('title'))}
    {row('발행처', r.get('publisher'))}
    {row('발행일', r.get('published') or '미상')}
    {row('위치', r.get('locator'))}
    <div class="row"><span class="k">URL</span><span class="v">{link}</span></div>
    {row('원문 요지', r.get('quote_ko'), 'quote')}
    {row('등급 사유', r.get('reliability_rationale'))}
    {row('등급 조정', r.get('downgrade_reason'), 'warn')}
    {row('주의사항', r.get('notes'), 'warn')}
    {conflict_html}
  </div>
</article>"""


def main():
    rows = load(LEDGER)
    if not rows:
        sys.exit("[FATAL] 근거가 0건입니다.")

    # rid 중복 검출
    dupes = [rid for rid, n in Counter(r.get("rid") for r in rows).items() if n > 1]
    if dupes:
        print(f"[WARN] 중복 rid {len(dupes)}건: {dupes[:10]}", file=sys.stderr)

    rows.sort(key=lambda r: rid_key(r.get("rid")))

    g = Counter(r.get("reliability") or r.get("reliability_self") or "미등급" for r in rows)
    mods = Counter(r.get("module", "") for r in rows)
    agents = sorted({r.get("agent", "") for r in rows if r.get("agent")})
    stypes = Counter(r.get("source_type", "") for r in rows)
    total = len(rows)
    hi_pct = 100.0 * g.get("상", 0) / total if total else 0.0

    def opts(counter, labelmap=None):
        items = sorted(counter.items(), key=lambda kv: kv[0])
        return "".join(
            f'<option value="{esc(k)}">{esc((labelmap or {}).get(k, k))} ({v})</option>'
            for k, v in items if k
        )

    cards = "\n".join(card(r) for r in rows)

    stat_rows = "".join(
        f'<div class="stat"><b class="g-{esc(k)}">{v}</b><span>{esc(k)} 등급</span>'
        f'<span class="pct">{100.0*v/total:.1f}%</span></div>'
        for k, v in sorted(g.items(), key=lambda kv: GRADE_ORDER.get(kv[0], 9))
    )

    doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>INTX 근거 카드 — 개인맞춤형 mRNA 항암치료제</title>
<style>
  :root {{
    --bg:#f6f7f9; --fg:#16191d; --mut:#5c6570; --line:#dfe3e8; --card:#fff;
    --hi:#0f7b3f; --hib:#e6f4ec; --mid:#8a6100; --midb:#fdf3dd; --lo:#a32020; --lob:#fbe9e9;
    --accent:#1d4ed8;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0f1216; --fg:#e7eaee; --mut:#9aa4b0; --line:#2a3138; --card:#171b21;
      --hi:#5fd08d; --hib:#122b1d; --mid:#e8bf5a; --midb:#2e2512; --lo:#f08a8a; --lob:#331616;
      --accent:#7ea6ff; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg); font-size:15px; line-height:1.6;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",
    "Malgun Gothic",sans-serif; }}
  header.top {{ padding:28px 20px 18px; border-bottom:1px solid var(--line); background:var(--card); }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:0 20px; }}
  h1 {{ font-size:22px; margin:0 0 4px; letter-spacing:-.01em; }}
  .sub {{ color:var(--mut); font-size:13px; margin:0; }}
  .stats {{ display:flex; flex-wrap:wrap; gap:10px; margin:16px 0 0; }}
  .stat {{ background:var(--bg); border:1px solid var(--line); border-radius:10px;
    padding:8px 14px; display:flex; align-items:baseline; gap:8px; }}
  .stat b {{ font-size:19px; }}
  .stat span {{ font-size:12px; color:var(--mut); }}
  .stat .pct {{ font-variant-numeric:tabular-nums; }}
  .g-상 {{ color:var(--hi); }} .g-중 {{ color:var(--mid); }} .g-하 {{ color:var(--lo); }}
  .controls {{ position:sticky; top:0; z-index:10; background:var(--card);
    border-bottom:1px solid var(--line); padding:12px 20px; }}
  .controls .wrap {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; }}
  input[type=search], select {{ font:inherit; font-size:13px; padding:7px 10px;
    border:1px solid var(--line); border-radius:8px; background:var(--bg); color:var(--fg); }}
  input[type=search] {{ flex:1 1 240px; min-width:180px; }}
  #count {{ font-size:12px; color:var(--mut); margin-left:auto; white-space:nowrap; }}
  button.reset {{ font:inherit; font-size:13px; padding:7px 12px; border:1px solid var(--line);
    border-radius:8px; background:var(--bg); color:var(--fg); cursor:pointer; }}
  main {{ padding:20px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px;
    padding:16px 18px; margin:0 0 12px; scroll-margin-top:76px; }}
  .card:target {{ outline:2px solid var(--accent); }}
  .card-head {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; margin-bottom:8px; }}
  .rid {{ font-weight:700; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
    color:var(--accent); text-decoration:none; font-size:14px; }}
  .badge {{ font-size:11px; padding:2px 8px; border-radius:99px; border:1px solid var(--line);
    color:var(--mut); white-space:nowrap; }}
  .badge.g-상 {{ background:var(--hib); color:var(--hi); border-color:transparent; font-weight:700; }}
  .badge.g-중 {{ background:var(--midb); color:var(--mid); border-color:transparent; font-weight:700; }}
  .badge.g-하 {{ background:var(--lob); color:var(--lo); border-color:transparent; font-weight:700; }}
  .claim {{ margin:0 0 12px; font-weight:600; font-size:15px; }}
  .meta {{ border-top:1px dashed var(--line); padding-top:10px; }}
  .row {{ display:flex; gap:10px; font-size:13px; padding:2px 0; }}
  .row .k {{ flex:0 0 76px; color:var(--mut); }}
  .row .v {{ flex:1 1 auto; min-width:0; overflow-wrap:anywhere; }}
  .row .v.quote {{ color:var(--mut); font-style:italic; }}
  .row .v.warn {{ color:var(--lo); }}
  .src-url {{ color:var(--accent); }}
  .src-url.none {{ color:var(--mut); }}
  .conflict {{ display:inline-block; font-family:ui-monospace,monospace; font-size:12px;
    padding:1px 6px; border-radius:6px; background:var(--lob); color:var(--lo); text-decoration:none; }}
  .hidden {{ display:none; }}
  .empty {{ text-align:center; color:var(--mut); padding:40px 0; }}
  footer {{ color:var(--mut); font-size:12px; padding:24px 20px 48px; }}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <h1>INTX 근거 카드 — mRNA 개인맞춤형 항암치료제</h1>
  <p class="sub">총 <b>{total}</b>건의 근거. 규칙 3(신뢰도 독립 검증)에 따라 R 에이전트가 등급화.
     <b>상</b> 등급 비중 <b>{hi_pct:.1f}%</b>. 보고서의 [R###] 태그는 이 페이지의 앵커와 연결됨.</p>
  <div class="stats">{stat_rows}
    <div class="stat"><b>{len(mods)}</b><span>모듈</span></div>
    <div class="stat"><b>{len(agents)}</b><span>조사 에이전트</span></div>
  </div>
</div></header>

<div class="controls"><div class="wrap">
  <input type="search" id="q" placeholder="검색 — 주장·출처·발행처·주의사항 전문 검색" autocomplete="off">
  <select id="fg"><option value="">전체 등급</option>{opts(g)}</select>
  <select id="fm"><option value="">전체 모듈</option>{opts(mods, MODULE_LABEL)}</select>
  <select id="fa"><option value="">전체 에이전트</option>{''.join(f'<option value="{esc(a)}">{esc(a)}</option>' for a in agents)}</select>
  <select id="fs"><option value="">전체 출처유형</option>{opts(stypes, SOURCE_LABEL)}</select>
  <button class="reset" id="reset">초기화</button>
  <span id="count"></span>
</div></div>

<main><div class="wrap">
{cards}
<p class="empty hidden" id="empty">조건에 맞는 근거가 없습니다.</p>
</div></main>

<footer><div class="wrap">
  INTX harness · 근거 원장 <code>evidence_ledger.jsonl</code> 로부터 자동 생성 ·
  등급 기준: 상 = peer-reviewed·공시·규제문서·등록정보·등록특허 / 중 = 학회초록·보도자료·1차취재 산업지 / 하 = 2차요약·시장조사 요약본
</div></footer>

<script>
(function () {{
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var q = document.getElementById('q'), fg = document.getElementById('fg'),
      fm = document.getElementById('fm'), fa = document.getElementById('fa'),
      fs = document.getElementById('fs'), count = document.getElementById('count'),
      empty = document.getElementById('empty');

  function apply() {{
    var t = q.value.trim().toLowerCase(),
        vg = fg.value, vm = fm.value, va = fa.value, vs = fs.value, n = 0;
    for (var i = 0; i < cards.length; i++) {{
      var c = cards[i];
      var ok = (!vg || c.dataset.grade === vg)
            && (!vm || c.dataset.module === vm)
            && (!va || c.dataset.agent === va)
            && (!vs || c.dataset.stype === vs)
            && (!t || c.dataset.q.indexOf(t) !== -1);
      c.classList.toggle('hidden', !ok);
      if (ok) n++;
    }}
    count.textContent = n + ' / ' + cards.length + ' 건';
    empty.classList.toggle('hidden', n !== 0);
  }}

  [q, fg, fm, fa, fs].forEach(function (el) {{
    el.addEventListener('input', apply);
    el.addEventListener('change', apply);
  }});
  document.getElementById('reset').addEventListener('click', function () {{
    q.value = ''; fg.value = ''; fm.value = ''; fa.value = ''; fs.value = ''; apply();
  }});
  apply();

  // 해시로 들어온 카드는 필터에 가려지지 않도록 초기화 후 스크롤
  if (location.hash) {{
    var el = document.querySelector(location.hash);
    if (el) {{ el.classList.remove('hidden'); el.scrollIntoView(); }}
  }}
}})();
</script>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)

    print(f"[OK] {OUT}")
    print(f"     근거 {total}건 | 상 {g.get('상',0)} ({hi_pct:.1f}%) "
          f"중 {g.get('중',0)} 하 {g.get('하',0)} 미등급 {g.get('미등급',0)}")
    print(f"     모듈 {dict(sorted(mods.items()))}")
    if dupes:
        print(f"     [주의] 중복 rid {len(dupes)}건")


if __name__ == "__main__":
    main()
