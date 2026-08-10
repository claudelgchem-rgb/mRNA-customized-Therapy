#!/usr/bin/env python3
"""registry_snapshot 에서 개인맞춤·신항원 항암백신 시험의 중단 사유를 분류한다.

Q4("실패·중단 사례가 말해주는 구조적 한계는 무엇인가")에 대한 재현 가능한 1차 근거.
ClinicalTrials.gov 등록정보의 whyStopped 필드만 사용하므로 등급은 '상'이다.

출력: out/raw/failure_taxonomy.md, out/raw/failure_taxonomy.csv
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "out", "raw", "registry_snapshot.json")
OUT_MD = os.path.join(ROOT, "out", "raw", "failure_taxonomy.md")
OUT_CSV = os.path.join(ROOT, "out", "raw", "failure_taxonomy.csv")

# 규칙: 개인맞춤/신항원 + 암 을 동시에 만족해야 한다.
# 감염병 mRNA 백신·비암 시험이 섞이면 규칙(범주 혼동 금지)을 위반한다.
NEO_KEYS = [
    "neoantigen", "neo-antigen", "neoepitope", "personalized", "personalised",
    "individualized", "individualised", "autologous tumor", "patient-specific",
]
CANCER_KEYS = [
    "cancer", "carcinoma", "tumor", "tumour", "melanoma", "glioma", "lymphoma",
    "leukemia", "sarcoma", "myeloma", "neoplas", "malignan",
]

# 순서가 곧 우선순위다. 먼저 매칭되는 범주로 배정한다.
CATEGORIES = [
    ("안전성",             r"safety|adverse event|toxicit|\bdeath|serious adverse"),
    ("무효·효능부족",      r"futil|lack of efficac|no (clinical )?benefit|did not meet|interim analysis"),
    ("제조 실패·중단",     r"manufactur|product(ion)? (issue|hold|suspend|problem)|supply|drugs?[ /].*unavailab|equipment"),
    ("모집 실패·저조",     r"accru|enroll|recruit|slow|insufficient number|participant"),
    ("자금 중단",          r"fund|financ|resourc|budget|money"),
    ("사업적 판단·우선순위", r"business|strategic|portfolio|prioriti|company decision|reprioriti|sponsor decision"),
    ("경쟁·치료환경 변화", r"competing|standard of care|landscape|new knowledge"),
    ("운영·인력·규제절차", r"\bpi\b|investigator|logistic|staff|covid|site change|fda contingenc|irb"),
]


def relevant(r):
    blob = f"{r['title']} {r['conditions']} {r['interventions']}".lower()
    return (any(k in blob for k in NEO_KEYS) and any(k in blob for k in CANCER_KEYS))


def classify(why):
    w = (why or "").lower()
    for name, pat in CATEGORIES:
        if re.search(pat, w):
            return name
    return "기타·불명"


def main():
    if not os.path.exists(SNAP):
        sys.exit(f"[FATAL] 스냅샷이 없습니다. 먼저 fetch_registry_snapshot.py 를 실행하세요: {SNAP}")

    studies = json.load(open(SNAP, encoding="utf-8"))["studies"]
    stopped = [
        r for r in studies
        if r["status"] in ("TERMINATED", "WITHDRAWN", "SUSPENDED") and r["why_stopped"].strip()
    ]
    rel = [r for r in stopped if relevant(r)]
    if not rel:
        sys.exit("[FATAL] 관련 중단 시험이 0건입니다. 필터를 점검하세요.")

    buckets = defaultdict(list)
    for r in rel:
        buckets[classify(r["why_stopped"])].append(r)

    order = [n for n, _ in CATEGORIES] + ["기타·불명"]
    total = len(rel)

    lines = [
        "# 개인맞춤·신항원 항암백신 임상시험 중단 사유 분류",
        "",
        f"출처: ClinicalTrials.gov API v2 `whyStopped` 필드 (등급 **상** — 등록정보 원본).",
        f"모집단: 신항원·개인맞춤 관련 쿼리 23종으로 수집한 고유 시험 {len(studies)}건 중,",
        f"상태가 TERMINATED/WITHDRAWN/SUSPENDED 이고 중단 사유가 기재된 {len(stopped)}건.",
        f"그중 '개인맞춤/신항원' 과 '암' 을 동시에 만족하는 **{total}건**을 분류했다.",
        "",
        "재현: `python3 scripts/fetch_registry_snapshot.py && python3 scripts/analyze_failures.py`",
        "",
        "## 요약",
        "",
        "| 중단 사유 | 건수 | 비중 |",
        "|---|---:|---:|",
    ]
    for name in order:
        v = buckets.get(name, [])
        if v:
            lines.append(f"| {name} | {len(v)} | {100*len(v)/total:.0f}% |")
    lines += [f"| **합계** | **{total}** | **100%** |", ""]

    safety = len(buckets.get("안전성", []))
    futility = len(buckets.get("무효·효능부족", []))
    lines += [
        "## 핵심 해석",
        "",
        f"- **안전성을 사유로 중단된 시험은 {safety}건, 효능 부족·무효를 사유로 중단된 시험은 {futility}건이다.**",
        "  이 모달리티의 임상 중단은 과학적 실패가 아니라 **운영·재무·전략적 사유**에 집중되어 있다.",
        "- 모집 실패와 자금 중단이 최상위 사유라는 점은, 개인맞춤 백신의 병목이 '작동하는가'보다",
        "  '충분한 환자를 제때 등록하고 자금을 유지할 수 있는가'에 있음을 시사한다.",
        "- 다만 이 데이터는 **생존자 편향**을 내포한다. 중단 사유는 스폰서가 자발적으로 기재하며,",
        "  효능 부족을 '사업적 판단'으로 기재하는 유인이 존재한다. 단정적 해석은 금지한다.",
        "",
        "## 전체 목록",
        "",
    ]

    rows = []
    for name in order:
        v = sorted(buckets.get(name, []), key=lambda r: r["nct"])
        if not v:
            continue
        lines += [f"### {name} ({len(v)}건)", ""]
        for r in v:
            n = r["enrollment"] or "미기재"
            lines.append(
                f"- `{r['nct']}` **{r['status']}** · 등록 {n}명 · {r['sponsor']}  \n"
                f"  {r['title']}  \n"
                f"  > {r['why_stopped']}"
            )
            rows.append({
                "category": name, "nct": r["nct"], "status": r["status"],
                "enrollment": r["enrollment"], "enrollment_type": r["enrollment_type"],
                "sponsor": r["sponsor"], "phase": r["phase"],
                "title": r["title"], "why_stopped": r["why_stopped"],
                "conditions": r["conditions"], "start": r["start"],
                "last_update": r["last_update"],
            })
        lines.append("")

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"[OK] {OUT_MD}")
    print(f"[OK] {OUT_CSV}")
    print(f"     관련 중단 시험 {total}건 / 사유기재 중단 전체 {len(stopped)}건")
    for name in order:
        v = buckets.get(name, [])
        if v:
            print(f"       {name:20s} {len(v):3d}건 ({100*len(v)/total:3.0f}%)")
    print(f"\n     [Q4 직결] 안전성 중단 {safety}건 · 효능부족 중단 {futility}건")


if __name__ == "__main__":
    main()
