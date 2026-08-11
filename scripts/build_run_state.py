#!/usr/bin/env python3
"""O 에이전트 산출물 — out/run_state.json 생성.

실행 상태·모듈별 진척·검색 쿼리 로그·정지 조건 판정을 한 파일에 모은다.
정지 조건은 실제 산출물을 읽어 기계적으로 판정하며, 미충족 항목은 숨기지 않는다.
"""

import csv
import glob
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")


def jload(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def jlines(p):
    try:
        return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    except Exception:
        return []


AGENT_ROLE = {
    "A1": ("M2", "intismeran autogene (Moderna/Merck)"),
    "A2": ("M2", "autogene cevumeran (BioNTech/Roche)"),
    "A3": ("M2", "비교·경쟁 프로그램"),
    "A4": ("M2/M6", "국내 역량·정책"),
    "A5": ("M2", "실패·부정 근거 (적대적)"),
    "B1": ("M1", "신항원 예측·서열설계"),
    "B2": ("M1", "RNA 형태·전달체·면역측정"),
    "C1": ("M3", "제조·CMC·turnaround"),
    "C2": ("M3", "COGS·밸류체인"),
    "C3": ("M5", "시장·경제성"),
    "D1": ("M4", "특허 레이어 1-3"),
    "D2": ("M4", "특허 레이어 4-7·소송"),
    "D3": ("M6", "정책·재무·리스크"),
    "O": ("전체", "오케스트레이터 직접 검증 앵커"),
}


def main():
    ledger = jlines(os.path.join(OUT, "evidence_ledger.jsonl"))
    grades = jlines(os.path.join(OUT, "reliability_ledger.jsonl"))
    returns = [r["result"] for r in jlines(os.path.join(OUT, "raw", "agent_returns.jsonl"))
               if r.get("type") == "result" and isinstance(r.get("result"), dict)]
    snap = jload(os.path.join(OUT, "raw", "registry_snapshot.json"), {"studies": [], "queries": {}})

    # 프로그램 표
    programs, stopped = [], []
    pm = os.path.join(OUT, "pipeline_matrix.csv")
    if os.path.exists(pm):
        programs = list(csv.DictReader(open(pm, encoding="utf-8-sig")))
        stopped = [p for p in programs
                   if re.search(r"중단|종료|실패|TERMIN|WITHDRAW|SUSPEND", p.get("status", ""), re.I)]

    # 보고서 인용 무결성
    report = ""
    rp = os.path.join(OUT, "INTX_report.md")
    if os.path.exists(rp):
        report = open(rp, encoding="utf-8").read()
    cited = set(re.findall(r"\[(R\d{1,4})\]", report))
    for m in re.findall(r"\[(R\d{1,4}(?:\s*,\s*R\d{1,4})+)\]", report):
        cited |= {x.strip() for x in m.split(",")}
    rids = {r["rid"] for r in ledger}
    dangling = sorted(cited - rids, key=lambda r: int(r[1:]))

    g = Counter(r.get("reliability") or "미등급" for r in ledger)
    rt = Counter(x.get("record_type", "?") for x in grades)
    total = len(ledger) or 1

    # 공백
    gaps, short_q = [], []
    for v in returns:
        for gp in (v.get("gaps") or []):
            gaps.append(gp)
            if len(gp.get("queries_tried") or []) < 3:
                short_q.append(gp.get("topic", "")[:60])

    # 검색 쿼리 로그
    query_log = {}
    for v in returns:
        a = v.get("agent", "?")
        qs = list(v.get("queries_logged") or [])
        for gp in (v.get("gaps") or []):
            qs += list(gp.get("queries_tried") or [])
        query_log[a] = sorted(set(qs))
    query_log["O"] = sorted(snap.get("queries", {}).keys())
    total_queries = sum(len(v) for v in query_log.values())

    modules = {}
    for a, (mod, role) in AGENT_ROLE.items():
        n = sum(1 for r in ledger if r.get("agent") == a)
        modules[a] = {
            "module": mod, "role": role, "evidence": n,
            "queries_logged": len(query_log.get(a, [])),
            "status": "done" if n else "no_output",
        }

    v_audit = os.path.join(OUT, "V_audit.md")
    v_done = os.path.exists(v_audit)
    v_rejects = None
    if v_done:
        txt = open(v_audit, encoding="utf-8").read()
        m = re.search(r"반려 항목\s*[:：]?\s*\*{0,2}(\d+)", txt)
        v_rejects = int(m.group(1)) if m else None

    checks = [
        {"id": "Q1-Q4 직접 답변", "pass": bool(re.search(r"Q1.*직접 답변|### Q1", report)),
         "detail": "Executive Summary 직답표 + §7.1-7.5"},
        {"id": "M2 진행 프로그램 15건 이상", "pass": len(programs) >= 15,
         "detail": f"{len(programs)}건 (중단·실패 {len(stopped)}건 포함)"},
        {"id": "중단·실패 3건 이상", "pass": len(stopped) >= 3, "detail": f"{len(stopped)}건"},
        {"id": "보고서 인용 rid 전건 실재", "pass": not dangling,
         "detail": f"인용 {len(cited)}건, 미존재 {len(dangling)}건 {dangling[:5]}"},
        {"id": "R 100% 등급화", "pass": len(grades) == len(ledger) and g.get("미등급", 0) == 0,
         "detail": f"{len(grades)}/{len(ledger)}, 상 {g.get('상',0)} ({100.0*g.get('상',0)/total:.1f}%)"},
        {"id": "gaps 항목별 쿼리 3개 이상", "pass": not short_q,
         "detail": f"공백 {len(gaps)}건, 쿼리 3개 미만 {len(short_q)}건"},
        {"id": "INTX_evidence.html 생성", "pass": os.path.exists(os.path.join(OUT, "INTX_evidence.html")),
         "detail": f"{os.path.getsize(os.path.join(OUT,'INTX_evidence.html'))//1024} KB"
                   if os.path.exists(os.path.join(OUT, "INTX_evidence.html")) else "없음"},
        {"id": "INTX_report.docx 생성", "pass": os.path.exists(os.path.join(OUT, "INTX_report.docx")),
         "detail": f"{os.path.getsize(os.path.join(OUT,'INTX_report.docx'))//1024} KB"
                   if os.path.exists(os.path.join(OUT, "INTX_report.docx")) else "없음"},
        {"id": "V 감사 반려 0건", "pass": (v_rejects == 0) if v_rejects is not None else False,
         "detail": f"V_audit.md {'있음' if v_done else '없음'}, 반려 {v_rejects}"},
    ]

    state = {
        "harness": "INTX — Individualized Neoantigen Therapy eXplorer",
        "data_asof": "2026-08-10",
        "pipeline": "O → (A‖B‖C‖D 병렬 13) → R → V → W",
        "evidence": {
            "total": len(ledger),
            "by_grade": dict(g),
            "high_grade_pct": round(100.0 * g.get("상", 0) / total, 1),
            "by_module": dict(Counter(r.get("module") for r in ledger)),
            "by_record_type": dict(rt),
            "rid_blocks": {a: f"R{lo}-R{hi}" for a, (lo, hi) in {
                "O": (1, 99), "A1": (100, 199), "A2": (200, 299), "A3": (300, 399),
                "A4": (400, 499), "A5": (500, 599), "B1": (600, 699), "B2": (700, 799),
                "C1": (800, 899), "C2": (900, 999), "C3": (1000, 1099),
                "D1": (1100, 1199), "D2": (1200, 1299), "D3": (1300, 1399)}.items()},
        },
        "agents": modules,
        "registry_snapshot": {
            "unique_studies": len(snap.get("studies", [])),
            "queries": snap.get("queries", {}),
            "stopped_with_reason": sum(1 for s in snap.get("studies", [])
                                       if s.get("why_stopped")),
        },
        "pipeline_matrix": {"programs": len(programs), "stopped_or_failed": len(stopped)},
        "gaps": {"total": len(gaps), "with_fewer_than_3_queries": len(short_q),
                 "topics_short": short_q},
        "search_query_log": query_log,
        "search_query_total": total_queries,
        "environment_blockers": [
            {"resource": "patents.google.com", "status": "HTTP 503 전면 차단",
             "workaround": "freepatentsonline.com 에서 청구항 원문 확보 (scripts/verify_patents.py)"},
            {"resource": "worldwide.espacenet.com", "status": "HTTP 403", "workaround": "동일"},
            {"resource": "patents.justia.com", "status": "Cloudflare 차단", "workaround": "동일"},
            {"resource": "workflow 서브에이전트", "status": "간헐적 권한 핸들러 오류로 도구 호출 전면 실패",
             "workaround": "정상 동작한 실행분만 채택하고 손상된 실행은 폐기 후 재실행"},
        ],
        "stop_conditions": checks,
        "all_passed": all(c["pass"] for c in checks),
    }

    p = os.path.join(OUT, "run_state.json")
    json.dump(state, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"[OK] {p}")
    print(f"     근거 {len(ledger)} · 프로그램 {len(programs)} · 공백 {len(gaps)} · 쿼리 로그 {total_queries}건")
    print("\n[정지 조건]")
    for c in checks:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:32s} {c['detail']}")
    print(f"\n  전체: {'충족' if state['all_passed'] else '미충족 항목 있음'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
