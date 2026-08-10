#!/usr/bin/env python3
"""R 에이전트 1단계 — 규칙 기반 독립 등급화.

CLAUDE.md 규칙 3의 등급 기준을 기계적으로 적용한다. 조사 에이전트가 붙인
`reliability_self` 는 **입력으로 쓰지 않는다**. 출처 유형·발행처·URL 도달성만 본다.
그래야 '조사 에이전트와 분리된 등급화'라는 규칙 3의 취지가 지켜진다.

산출: out/reliability_ledger.jsonl  (전 rid 100% 등급)
      out/raw/grading_review.json   (self 등급과 불일치하거나 판단이 필요한 항목 → R 에이전트 검토용)
"""

import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "out", "evidence_ledger.jsonl")
URLCHK = os.path.join(ROOT, "out", "raw", "url_check.json")
OUT = os.path.join(ROOT, "out", "reliability_ledger.jsonl")
REVIEW = os.path.join(ROOT, "out", "raw", "grading_review.json")

BASE = {
    "peer_reviewed": ("상", "peer-reviewed 원논문"),
    "regulatory": ("상", "규제기관 문서(FDA/EMA/MFDS 등)"),
    "registry": ("상", "임상시험 등록정보 원본"),
    "company_filing": ("상", "기업 공시(10-K/20-F/8-K/IR)"),
    "patent": ("상", "특허 원문"),
    "conference_abstract": ("중", "학회 초록·발표"),
    "company_pr": ("중", "기업 보도자료"),
    "trade_press": ("중", "1차 취재 기반 산업지"),
    "secondary": ("하", "2차 요약·재인용"),
}

# 발행처가 이들에 해당하면 유형과 무관하게 '하' — 규칙 3 및 4절 금지 조항
MARKET_RESEARCH = re.compile(
    r"grand view|mordor|marketsandmarkets|precedence|fortune business|"
    r"research and markets|globaldata|imarc|technavio|straits|polaris market|"
    r"coherent market|zion market|verified market|synapse|patsnap|insight partners",
    re.I,
)
# 2차 요약 성격이 강한 매체 (1차 취재 산업지와 구분)
SECONDARY_PUB = re.compile(
    r"wikipedia|blog|medium\.com|substack|slideshare|researchgate|"
    r"ai\s*summary|chatgpt|perplexity", re.I,
)
# 1차 취재 기반 산업지 — company_pr 로 잘못 분류돼 있어도 '중' 유지
TRADE = re.compile(r"endpoints|fierce|stat ?news|biocentury|scrip|evaluate|"
                   r"바이오스펙테이터|히트뉴스|팜뉴스|바이오타임즈|더바이오|메디게이트", re.I)

# 자체 산출 추정치. 출처가 아니라 파생 계산이므로 절대 '상' 이 될 수 없다.
ESTIMATE = re.compile(r"\[EST\]|자체 추정|파생 추정|agent calculation|본 조사 산출|"
                      r"INTX \w+ 파생|에이전트 자체", re.I)
# 언론·요약 서비스를 거친 재인용. 원문이 상급이어도 한 단계 낮춘다.
RECITE = re.compile(r"재인용|인용\)|요약\)|stocktitan|을 인용|기사 인용", re.I)
# 접근 실패·시도 기록. 사실 근거가 아니라 절차 기록이다.
PROCESS = re.compile(r"접근 시도|시도 기록|검색 시도|접근 불가 기록", re.I)

DOWN = {"상": "중", "중": "하", "하": "하"}
# SEC 에 제출된 보도자료(8-K Ex-99.1 등)는 '보도자료'가 아니라 제출 문서다.
SEC_FILED = re.compile(r"sec\.gov|sec edgar|ex-?99|form 8-k|form 10-[qk]|form 20-f", re.I)


def main():
    if not os.path.exists(LEDGER):
        sys.exit(f"[FATAL] {LEDGER} 없음")
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    urlchk = json.load(open(URLCHK, encoding="utf-8"))["by_rid"] if os.path.exists(URLCHK) else {}

    out, review = [], []
    for r in rows:
        rid = r["rid"]
        st = (r.get("source_type") or "").strip()
        pub = f"{r.get('publisher','')} {r.get('title','')} {r.get('url','')}"
        grade, why = BASE.get(st, ("하", f"출처 유형 미상('{st}')"))
        downgrade = None
        rtype = "evidence"

        blob = f"{pub} {r.get('claim','')} {r.get('notes','')}"
        # 0) 자체 산출 추정치는 '출처'가 아니다. 근거로 승급시키지 않는다.
        if ESTIMATE.search(blob):
            rtype = "estimate"
            base_rids = re.findall(r"R\d{3,4}", f"{r.get('title','')} {r.get('notes','')} "
                                                f"{r.get('quote_ko','')}")
            # 파생 근거가 명시돼 있으면 '중', 계산 근거가 없으면 '하'
            new = "중" if base_rids else "하"
            if grade != new:
                downgrade = (f"자체 산출 추정치([EST])를 출처 유형 '{st}'({grade})로 분류 → {new}. "
                             f"추정치는 1차 출처가 아니다")
            grade = new
            why = ("자체 산출 추정치 — 파생 근거 " + ", ".join(base_rids[:4])
                   if base_rids else "자체 산출 추정치 — 계산 근거 rid 미표기")
        # 0-b) 접근 시도·실패 기록은 사실 근거가 아니다
        elif PROCESS.search(f"{r.get('title','')} {r.get('claim','')}"):
            rtype = "process"
            if grade == "상":
                downgrade = "접근 시도·실패 기록은 사실 근거가 아님(상→중)"
            grade = "중" if grade == "상" else grade
            why = "조사 절차 기록(접근 시도·실패)"
        # 1) 시장조사 보고서·AI 요약 플랫폼은 유형 불문 '하'
        if MARKET_RESEARCH.search(pub):
            if grade != "하":
                downgrade = f"시장조사·AI요약 플랫폼 발행({grade}→하). 규칙 4절 단독 근거 금지"
            grade, why = "하", "시장조사 보고서·AI 요약 플랫폼"
        # 2) 위키·블로그류 2차 요약
        elif SECONDARY_PUB.search(pub):
            if grade != "하":
                downgrade = f"2차 요약 매체({grade}→하)"
            grade, why = "하", "2차 요약·블로그"
        # 3) 산업지가 secondary 로 잘못 분류된 경우 '중'으로 복원
        elif st == "secondary" and TRADE.search(pub):
            grade, why = "중", "1차 취재 기반 산업지 (유형 재분류)"
        # 3-b) SEC 에 제출된 보도자료(8-K Ex-99.1)는 제출 문서이므로 '상'
        elif st == "company_pr" and SEC_FILED.search(pub):
            grade, why = "상", "SEC 제출 문서에 첨부된 보도자료(Ex-99.1 등)"

        # 3-c) 언론·요약 서비스를 거친 재인용은 원문이 상급이어도 한 단계 강등
        if rtype == "evidence" and RECITE.search(pub) and grade == "상":
            downgrade = (downgrade or "") + " | 언론·요약 서비스 재인용(상→중). 원문 미확인"
            grade, why = "중", why + " — 단, 재인용 경유"

        # 4) URL 실제 부존재는 한 단계 강등. 단 '차단(blocked)'은 강등하지 않는다
        u = urlchk.get(rid, {})
        ustat = u.get("status")
        if ustat in ("http_error", "error", "no_url") and not str(r.get("url", "")).startswith("http"):
            new = DOWN[grade]
            downgrade = (downgrade or "") + f" | URL 미기재({grade}→{new})"
            grade = new
        elif ustat == "http_error" and u.get("code") in (404, 410):
            new = DOWN[grade]
            downgrade = (downgrade or "") + f" | URL {u.get('code')} 부존재({grade}→{new})"
            grade = new

        rec = {
            "rid": rid,
            "reliability": grade,
            "reliability_rationale": why,
            "verified_by": "R",
            "url_status": ustat or "unchecked",
            "url_code": u.get("code"),
            "record_type": rtype,
        }
        if downgrade:
            rec["downgrade_reason"] = downgrade.strip(" |")
        out.append(rec)

        self_g = r.get("reliability_self")
        if self_g and self_g != grade:
            review.append({
                "rid": rid, "self": self_g, "R": grade, "source_type": st,
                "publisher": r.get("publisher", ""), "title": r.get("title", "")[:110],
                "url": r.get("url", ""), "claim": r.get("claim", "")[:160],
                "reason": downgrade or why,
            })

    with open(OUT, "w", encoding="utf-8") as fh:
        for rec in out:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    json.dump(review, open(REVIEW, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    g = Counter(x["reliability"] for x in out)
    rt = Counter(x["record_type"] for x in out)
    total = len(out)
    print(f"[OK] {OUT}")
    print(f"     등급화 {total}/{len(rows)} = {100.0*total/len(rows):.1f}%")
    print(f"     상 {g['상']} ({100.0*g['상']/total:.1f}%) · 중 {g['중']} ({100.0*g['중']/total:.1f}%) "
          f"· 하 {g['하']} ({100.0*g['하']/total:.1f}%)")
    print(f"     self 등급과 불일치 {len(review)}건 → {REVIEW} (R 에이전트 2단계 검토 대상)")
    print(f"     레코드 유형: {dict(rt)}  (estimate 는 [EST] 로 표기되며 1차 근거가 아님)")
    dg = [x for x in out if x.get("downgrade_reason")]
    print(f"     강등 {len(dg)}건")
    for x in dg[:12]:
        print(f"       {x['rid']} → {x['reliability']} : {x['downgrade_reason'][:90]}")


if __name__ == "__main__":
    main()
