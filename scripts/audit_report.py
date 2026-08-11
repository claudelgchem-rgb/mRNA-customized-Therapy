#!/usr/bin/env python3
"""V 감사 1단계 — 보고서·원장의 기계 검증.

반려 조건 중 기계적으로 판정 가능한 항목을 전수 점검한다:
  1  근거 미부착 사실 문장
  2  인용-주장 불일치 후보 (보고서 수치가 원장 claim/quote 에 없음)
  4  '하' 등급 단독 근거의 단정형 서술
  5  존재하지 않는 rid
  9  record_type=estimate 를 [EST] 표기 없이 1차 근거처럼 사용

출력: out/raw/audit_mechanical.json
사람(V)이 판단해야 하는 항목은 'needs_human' 으로 분리한다.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")

# 사실 주장이 아닌 줄 — 근거 부착 의무에서 제외
SKIP = re.compile(
    r"^\s*$|^#{1,6}\s|^\|?\s*[-:]+\s*\|"          # 빈 줄·제목·표 구분선
    r"|^```|^>\s*\*\*|^\s*\|\s*항목\s*\|"          # 코드펜스·표 헤더
    r"|^\s*[-*]\s*\*\*[^:]+\*\*\s*$"               # 항목 라벨만
)
# 근거 없이도 허용되는 메타 문장(하니스 설명·구조 안내)
META = re.compile(
    r"본 보고서|본 조사|이 표|아래 표|위 표|다음과 같다|정리하면|요약하면|이 절에서"
    r"|도식 [①②③④]|범례|전거|근거는 다음|출처:|재현:|참조|§|부록|산출물|정지 조건"
    r"|판정한다|기술한다|다룬다|제시하지 않는다|적시한다|명시한다|구분한다|나열한다"
)
NUM = re.compile(r"\d")
CITE = re.compile(r"\[R\d{1,4}(?:\s*,\s*R\d{1,4})*\]|\[EST\]")


def rids_of(line):
    out = set(re.findall(r"R\d{1,4}", " ".join(re.findall(r"\[(R[^\]]*)\]", line))))
    return out


def main():
    ledger = {json.loads(l)["rid"]: json.loads(l)
              for l in open(os.path.join(OUT, "evidence_ledger.jsonl"), encoding="utf-8") if l.strip()}
    grades = {json.loads(l)["rid"]: json.loads(l)
              for l in open(os.path.join(OUT, "reliability_ledger.jsonl"), encoding="utf-8") if l.strip()}
    report = open(os.path.join(OUT, "INTX_report.md"), encoding="utf-8").read().split("\n")

    findings = {"uncited_factual": [], "dangling_rid": [], "low_grade_assertive": [],
                "estimate_as_primary": [], "number_not_in_source": [], "needs_human": []}

    # 마크다운은 한 문장을 여러 줄로 접는다. 줄 단위로 보면 인용이 뒤 줄에 있어 오탐이 폭증한다.
    # 연속된 비어있지 않은 줄을 하나의 논리 블록으로 합쳐 검사한다.
    blocks, buf, start, in_fence = [], [], 1, False
    for i, line in enumerate(report, 1):
        st = line.strip()
        if st.startswith("```"):
            in_fence = not in_fence
            if buf:
                blocks.append((start, " ".join(buf)))
                buf = []
            continue
        if in_fence:
            continue
        if not st or SKIP.match(line):
            if buf:
                blocks.append((start, " ".join(buf)))
                buf = []
            continue
        if st.lstrip().startswith("|"):          # 표 행은 행 단위가 곧 논리 단위
            blocks.append((i, st))
            continue
        if not buf:
            start = i
        buf.append(st)
    if buf:
        blocks.append((start, " ".join(buf)))

    for i, s in blocks:
        line = s

        cited = bool(CITE.search(line))
        rs = rids_of(line)

        # 5) 존재하지 않는 rid
        for r in rs:
            if r not in ledger:
                findings["dangling_rid"].append({"line": i, "rid": r, "text": s[:120]})

        # 1) 숫자를 담은 사실 문장인데 근거 없음
        if NUM.search(s) and not cited and not META.search(s):
            # 표 행이면 같은 행 안에 근거가 있는지 이미 확인됨
            findings["uncited_factual"].append({"line": i, "text": s[:160]})

        if not rs:
            continue

        # 4) '하' 등급 단독 근거 + 단정형
        if len(rs) == 1:
            r = next(iter(rs))
            rec, gr = ledger.get(r), grades.get(r, {})
            if rec and rec.get("reliability") == "하":
                hedged = re.search(r"가능|추정|시사|보인다|것으로|수 있|불명|미확인|주장|보도|한다고|일 수", s)
                if not hedged:
                    findings["low_grade_assertive"].append(
                        {"line": i, "rid": r, "text": s[:160],
                         "publisher": rec.get("publisher", "")[:60]})
            # 9) estimate 를 [EST] 없이 사용
            if gr.get("record_type") == "estimate" and "[EST]" not in line:
                findings["estimate_as_primary"].append(
                    {"line": i, "rid": r, "text": s[:160]})

        # 2) 보고서 숫자가 인용 rid 의 claim/quote/notes 에 존재하는지
        nums = set(re.findall(r"\d+(?:[.,]\d+)*", s))
        nums = {n for n in nums if len(n.replace(",", "").replace(".", "")) >= 2}
        if nums and rs:
            hay = " ".join(
                f"{ledger[r].get('claim','')} {ledger[r].get('quote_ko','')} "
                f"{ledger[r].get('notes','')} {ledger[r].get('title','')}"
                for r in rs if r in ledger)
            hay_digits = hay.replace(" ", "")
            miss = [n for n in nums
                    if n not in hay and n.replace(",", "") not in hay_digits.replace(",", "")]
            # 연도·rid 번호·퍼센트 반올림은 오탐이 많아 사람 확인 대상으로 분리
            miss = [n for n in miss if not re.fullmatch(r"(19|20)\d\d", n)]
            if miss:
                findings["needs_human"].append(
                    {"line": i, "rids": sorted(rs), "unmatched_numbers": miss[:6],
                     "text": s[:150]})

    os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
    json.dump(findings, open(os.path.join(OUT, "raw", "audit_mechanical.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=1)

    print("[V 기계 검증]")
    for k, v in findings.items():
        print(f"  {k:24s} {len(v):4d}")
    for k in ("dangling_rid", "low_grade_assertive", "estimate_as_primary"):
        for x in findings[k][:10]:
            print(f"    [{k}] L{x['line']} {x.get('rid','')} {x['text'][:100]}")
    print(f"\n  uncited_factual 상위 15건:")
    for x in findings["uncited_factual"][:15]:
        print(f"    L{x['line']}: {x['text'][:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
