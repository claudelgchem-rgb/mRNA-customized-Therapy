#!/usr/bin/env python3
"""특허 원문(청구항 포함)을 독립 경로로 검증한다.

이 환경에서 patents.google.com 은 503 을 반환하고 Espacenet 은 403, Justia 는
Cloudflare 로 차단된다. FreePatentsOnline 은 접근 가능하므로 이를 대체 경로로 쓴다.
CLAUDE.md 규칙 1 에 따라 '왜 1차 경로가 불가했는지'와 '대체 경로'를 명시하기 위한 스크립트다.

FTO 판단에는 청구항 원문이 필수(M4 규칙)이므로, 청구항 1 을 실제로 가져와 저장한다.

출력: out/raw/patent_claims.json, out/raw/patent_claims.md
"""

import html
import json
import os
import re
import ssl
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "raw")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
CTX = ssl.create_default_context()

# 레이어별 핵심 특허. FTO 결론이 이 청구항들에 직접 걸린다.
TARGETS = [
    ("8278036",  "L3 변형뉴클레오사이드", "UPenn Kariko/Weissman 원천 (슈도우리딘)"),
    ("11389547", "L3 변형뉴클레오사이드", "UPenn 계속출원"),
    ("8835108",  "L3 변형뉴클레오사이드", "UPenn m5C 방법"),
    ("10small",  "", ""),  # 자리표시자 - 아래에서 필터링
]
TARGETS = [t for t in TARGETS if t[0].isdigit()]


def fetch(num, retries=3):
    url = f"https://www.freepatentsonline.com/{num}.html"
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
                return r.read().decode("utf-8", errors="replace"), url
        except Exception as e:
            if i == retries - 1:
                return None, f"{url} ({type(e).__name__})"
            time.sleep(3 * (i + 1))
    return None, url


def clean(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def parse(h):
    txt = re.sub(r"<(script|style).*?</\1>", "", h, flags=re.S)
    out = {}
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    if t:
        full = clean(t.group(1))
        out["title"] = full.split(" - ")[0].strip()
        if " - " in full:
            out["assignee_title"] = full.split(" - ", 1)[1].strip()
    for key, lab in (("filing_date", "Filing Date"), ("publication_date", "Publication Date"),
                     ("application_number", "Application Number"), ("assignee", "Assignee")):
        # 라벨은 HTML 주석(<!-- Filing Date -->)에도 나타나므로 첫 매치를 쓰면 '>' 를 잡는다.
        # 모든 매치 중 실제 값처럼 보이는(영숫자 포함) 첫 항목을 취한다.
        for m in re.finditer(re.escape(lab) + r"\s*:?\s*(?:</?[^>]+>\s*)*([^<]{1,120})", txt, re.S):
            v = clean(m.group(1)).strip(" :->-")
            if re.search(r"[0-9A-Za-z]", v):
                out[key] = v
                break
    m = (re.search(r"What is claimed is:(.{0,2000})", txt, re.S)
         or re.search(r"We claim:(.{0,2000})", txt, re.S)
         or re.search(r"claim(?:ed)?\s+is\s*:(.{0,2000})", txt, re.S | re.I))
    if m:
        body = clean(m.group(1))
        # 청구항 2 직전까지가 청구항 1
        c1 = re.split(r"\s2\.\s", body)[0]
        out["claim_1"] = c1.strip()[:1400]
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    results = []
    for num, layer, note in TARGETS:
        h, url = fetch(num)
        if not h:
            print(f"[실패] US{num} — {url}")
            results.append({"patent": f"US{num}", "layer": layer, "note": note,
                            "source_url": url, "error": "fetch_failed"})
            continue
        d = parse(h)
        d.update({"patent": f"US{num}", "layer": layer, "note": note, "source_url": url})
        results.append(d)
        print(f"[OK] US{num} · {d.get('title','?')[:70]}")
        print(f"     출원 {d.get('filing_date','?')} / 등록 {d.get('publication_date','?')} / {d.get('assignee','?')[:60]}")
        print(f"     청구항1: {d.get('claim_1','(추출 실패)')[:150]}...")
        time.sleep(2)

    json.dump(results, open(os.path.join(OUT, "patent_claims.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    lines = [
        "# 특허 청구항 원문 검증",
        "",
        "**1차 경로 불가 사유** — 이 실행 환경에서 `patents.google.com` 은 모든 요청에 HTTP 503,",
        "`worldwide.espacenet.com` 은 403, `patents.justia.com` 은 Cloudflare 차단을 반환했다.",
        "규칙 1(완수 규칙)에 따라 대체 경로로 FreePatentsOnline 원문을 사용했고, 아래 청구항은",
        "실제로 내려받은 텍스트다. M4 규칙(청구항 원문 없이 FTO 판단 금지)을 충족시키기 위한 근거다.",
        "",
    ]
    for d in results:
        lines += [f"## {d['patent']} — {d.get('note','')}", "",
                  f"- 레이어: {d.get('layer','')}",
                  f"- 명칭: {d.get('title','?')}",
                  f"- 양수인: {d.get('assignee') or d.get('assignee_title','?')}",
                  f"- 출원일: {d.get('filing_date','?')} · 등록일: {d.get('publication_date','?')}",
                  f"- 출처: {d.get('source_url','')}", "",
                  "**청구항 1 (원문 인용)**", "",
                  f"> {d.get('claim_1','(추출 실패)')}", ""]
    open(os.path.join(OUT, "patent_claims.md"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"\n[OK] {OUT}/patent_claims.md · {len(results)}건")


if __name__ == "__main__":
    sys.exit(main())
