#!/usr/bin/env python3
"""out/evidence/*.jsonl 을 out/evidence_ledger.jsonl 로 병합·검증한다.

- rid 중복 검출 (에이전트별 rid 블록 침범 포함)
- 스키마 필수 필드 검증
- reliability_ledger.jsonl 이 있으면 최종 등급을 머지
- URL 중복(동일 URL + 동일 claim) 탐지 후 리포트
"""

import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "out", "evidence")
LEDGER = os.path.join(ROOT, "out", "evidence_ledger.jsonl")
GRADES = os.path.join(ROOT, "out", "reliability_ledger.jsonl")

BLOCKS = {
    "O": (1, 99),
    "A1": (100, 199), "A2": (200, 299), "A3": (300, 399), "A4": (400, 499),
    "A5": (500, 599), "B1": (600, 699), "B2": (700, 799), "C1": (800, 899),
    "C2": (900, 999), "C3": (1000, 1099), "D1": (1100, 1199),
    "D2": (1200, 1299), "D3": (1300, 1399),
}
REQUIRED = ("rid", "claim", "module", "agent", "source_type", "title", "publisher", "url")


def rid_num(rid):
    m = re.match(r"^R(\d+)$", str(rid or ""))
    return int(m.group(1)) if m else None


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.jsonl")))
    if not files:
        sys.exit(f"[FATAL] 근거 파일이 없습니다: {SRC}/*.jsonl")

    rows, problems = [], []
    seen_rid = {}

    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as fh:
            for ln, line in enumerate(fh, 1):
                line = line.strip().rstrip(",")
                if not line or line.startswith("//"):
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError as exc:
                    problems.append(f"{name}:{ln} JSON 파싱 실패 — {exc}")
                    continue
                if not isinstance(r, dict):
                    problems.append(f"{name}:{ln} object 가 아님")
                    continue

                missing = [f for f in REQUIRED if not r.get(f)]
                if missing:
                    problems.append(f"{name}:{ln} rid={r.get('rid')} 필수필드 누락 {missing}")

                rid = r.get("rid")
                n = rid_num(rid)
                if n is None:
                    problems.append(f"{name}:{ln} rid 형식 오류 '{rid}'")
                else:
                    lo, hi = BLOCKS.get(name, (None, None))
                    if lo is not None and not (lo <= n <= hi):
                        problems.append(f"{name}:{ln} rid {rid} 가 배정 블록 R{lo}-R{hi} 밖")
                    if rid in seen_rid:
                        problems.append(f"{name}:{ln} rid {rid} 중복 (이미 {seen_rid[rid]})")
                    else:
                        seen_rid[rid] = f"{name}:{ln}"

                r.setdefault("agent", name)
                rows.append(r)

    # 최종 등급 머지
    if os.path.exists(GRADES):
        gmap = {}
        with open(GRADES, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    g = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if g.get("rid"):
                    gmap[g["rid"]] = g
        hit = 0
        for r in rows:
            g = gmap.get(r.get("rid"))
            if g:
                hit += 1
                r["reliability"] = g.get("reliability") or r.get("reliability_self")
                for f in ("reliability_rationale", "downgrade_reason", "verified_by"):
                    if g.get(f):
                        r[f] = g[f]
        print(f"[R] 등급 머지 {hit}/{len(rows)}건")
        if hit < len(rows):
            ungraded = [r["rid"] for r in rows if not r.get("reliability")][:20]
            problems.append(f"R 미등급 {len(rows)-hit}건 (정지조건 위반). 예: {ungraded}")
    else:
        print("[R] reliability_ledger.jsonl 없음 — self 등급을 임시 사용")

    for r in rows:
        r.setdefault("reliability", r.get("reliability_self"))

    # 동일 URL+동일 주장 중복
    bykey = defaultdict(list)
    for r in rows:
        bykey[(r.get("url"), (r.get("claim") or "")[:60])].append(r.get("rid"))
    dup = {k: v for k, v in bykey.items() if len(v) > 1}
    if dup:
        print(f"[중복 후보] 동일 URL+유사 주장 {len(dup)}쌍: "
              f"{[v for v in list(dup.values())[:5]]}")

    rows.sort(key=lambda r: (rid_num(r.get("rid")) or 10**9))
    with open(LEDGER, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    g = Counter(r.get("reliability") or "미등급" for r in rows)
    m = Counter(r.get("module") or "?" for r in rows)
    a = Counter(r.get("agent") or "?" for r in rows)
    total = len(rows)
    print(f"\n[OK] {LEDGER}")
    print(f"     근거 {total}건 / 파일 {len(files)}개")
    print(f"     등급: {dict(sorted(g.items()))}"
          f"  (상 비중 {100.0*g.get('상',0)/total:.1f}%)" if total else "")
    print(f"     모듈: {dict(sorted(m.items()))}")
    print(f"     에이전트: {dict(sorted(a.items()))}")

    if problems:
        print(f"\n[문제 {len(problems)}건]")
        for p in problems[:40]:
            print("  -", p)
        if len(problems) > 40:
            print(f"  ... 외 {len(problems)-40}건")
    else:
        print("\n[검증] 문제 없음")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
