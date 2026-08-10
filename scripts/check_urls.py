#!/usr/bin/env python3
"""근거 원장의 모든 URL 도달 가능성을 검증한다.

V 감사 반려 조건 5("존재하지 않는 URL")를 기계적으로 잡아내기 위한 사전 검사.
결과는 out/raw/url_check.json 에 저장되어 R 에이전트의 강등 판단 입력이 된다.

주의: 403/406 은 봇 차단인 경우가 많아 '접근불가'와 '부존재'를 구분한다.
"""

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "out", "evidence_ledger.jsonl")
OUT = os.path.join(ROOT, "out", "raw", "url_check.json")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
CTX = ssl.create_default_context()


def probe(url, timeout=25):
    if not str(url).startswith("http"):
        return {"status": "no_url", "code": None}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/json,*/*",
            })
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return {"status": "ok", "code": r.getcode()}
        except urllib.error.HTTPError as e:
            # 405 = HEAD 미지원 → GET 재시도. 403/406 = 봇 차단(부존재 아님)
            if e.code == 405 and method == "HEAD":
                continue
            if e.code in (401, 403, 406, 429):
                return {"status": "blocked", "code": e.code}
            return {"status": "http_error", "code": e.code}
        except Exception as e:
            if method == "GET":
                return {"status": "error", "code": None, "err": type(e).__name__}
            continue
    return {"status": "error", "code": None}


def main():
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    urls = sorted({r.get("url", "") for r in rows if r.get("url")})
    print(f"고유 URL {len(urls)}건 검사 중...")

    results = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        for url, res in zip(urls, ex.map(probe, urls)):
            results[url] = res

    by = {}
    for r in rows:
        by[r["rid"]] = results.get(r.get("url", ""), {"status": "no_url", "code": None})

    from collections import Counter
    c = Counter(v["status"] for v in results.values())
    bad = {u: v for u, v in results.items() if v["status"] in ("http_error", "error", "no_url")}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"by_url": results, "by_rid": by}, open(OUT, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"[OK] {OUT}")
    print(f"     URL 상태: {dict(c)}")
    print(f"     도달 불가(부존재 의심) {len(bad)}건 — R 에이전트 강등 검토 대상")
    for u, v in list(bad.items())[:25]:
        rids = [r["rid"] for r in rows if r.get("url") == u]
        print(f"       [{v.get('code') or v['status']}] {','.join(rids[:4])} {u[:88]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
