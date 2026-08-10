#!/usr/bin/env python3
"""에이전트 구조화 반환(out/raw/agent_returns.jsonl)에서 산출 표를 생성한다.

  out/pipeline_matrix.csv  M2 임상 프로그램 전수 표
  out/cogs_model.csv       M3 COGS 분해 및 밸류체인 진입점
  out/ip_landscape.csv     M4 레이어별 특허 패밀리·만료시계
  out/gaps.md              미해결 공백 + 시도한 검색 쿼리 (정지조건: 항목별 3개 이상)
  out/findings_digest.md   에이전트별 핵심/부정 발견 (W 에이전트의 집필 소스)
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "out", "raw", "agent_returns.jsonl")
OUT = os.path.join(ROOT, "out")

# cogs_model.csv 로 보낼 수치의 담당 에이전트와 키워드
COGS_AGENTS = {"C1", "C2"}
IP_AGENTS = {"D1", "D2"}


def load():
    if not os.path.exists(SRC):
        sys.exit(f"[FATAL] 에이전트 반환이 없습니다: {SRC}")
    res = {}
    for line in open(SRC, encoding="utf-8"):
        r = json.loads(line)
        if r.get("type") == "result" and isinstance(r.get("result"), dict):
            v = r["result"]
            res[v.get("agent", "?")] = v
    return res


def norm_nct(s):
    m = re.search(r"NCT\d{8}", str(s or ""))
    return m.group(0) if m else ""


def build_pipeline(res):
    """프로그램 행을 NCT(없으면 프로그램명)로 중복 제거해 병합한다."""
    cols = ["program", "code", "company", "platform", "indication", "nct", "phase",
            "setting", "n", "combo", "primary_endpoint", "result", "immune_response",
            "grade3_ae", "discontinuation", "data_cutoff", "next_readout", "status",
            "why_stopped", "rid", "source_agent"]
    bykey = {}
    for agent in ("A1", "A2", "A3", "A4", "A5"):
        for p in (res.get(agent, {}).get("programs") or []):
            nct = norm_nct(p.get("nct"))
            key = nct or (str(p.get("program", ""))[:60].strip().lower() or str(p.get("code", "")))
            if not key:
                continue
            row = {c: str(p.get(c, "") or "").replace("\n", " ").strip() for c in cols[:-1]}
            row["nct"] = nct or str(p.get("nct", "") or "")
            row["source_agent"] = agent
            if key in bykey:
                # 더 정보량이 많은 행을 남기고, 빈 칸만 보완한다
                old = bykey[key]
                merged = dict(old)
                for c in cols[:-1]:
                    if not merged.get(c) and row.get(c):
                        merged[c] = row[c]
                    elif row.get(c) and len(row[c]) > len(merged.get(c, "")) * 1.5:
                        merged[c] = row[c]
                merged["source_agent"] = f"{old['source_agent']}+{agent}"
                bykey[key] = merged
            else:
                bykey[key] = row

    rows = list(bykey.values())

    def sortkey(r):
        st = r.get("status", "")
        stopped = 1 if re.search(r"중단|종료|실패|TERMIN|WITHDRAW|SUSPEND", st, re.I) else 0
        return (stopped, r.get("company", ""), r.get("program", ""))

    rows.sort(key=sortkey)
    path = os.path.join(OUT, "pipeline_matrix.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    stopped = [r for r in rows if re.search(r"중단|종료|실패|TERMIN|WITHDRAW|SUSPEND",
                                            r.get("status", ""), re.I)]
    active = len(rows) - len(stopped)
    print(f"[OK] {path}  프로그램 {len(rows)}건 (진행/완료 {active} · 중단·실패 {len(stopped)})")
    return rows, stopped


def build_numbers_csv(res, agents, path, title):
    cols = ["label", "value", "unit", "caveat", "rid", "agent"]
    rows = []
    for a in sorted(agents):
        for n in (res.get(a, {}).get("numbers") or []):
            rows.append({
                "label": str(n.get("label", "")).strip(),
                "value": str(n.get("value", "")).strip(),
                "unit": str(n.get("unit", "")).strip(),
                "caveat": str(n.get("caveat", "")).replace("\n", " ").strip(),
                "rid": str(n.get("rid", "")).strip(),
                "agent": a,
            })
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] {path}  {title} {len(rows)}행")
    return rows


def build_gaps(res):
    path = os.path.join(OUT, "gaps.md")
    total = 0
    short = []
    lines = [
        "# 미해결 공백 (gaps)",
        "",
        "`CLAUDE.md` 규칙 1(완수 규칙)에 따라, 확보하지 못한 항목은 *왜 불가한지*와",
        "*시도한 검색 쿼리*를 함께 기록한다. 정지 조건은 항목별 쿼리 3개 이상이다.",
        "",
    ]
    for a in sorted(res.keys()):
        gaps = res[a].get("gaps") or []
        if not gaps:
            continue
        lines += [f"## {a}", ""]
        for g in gaps:
            total += 1
            qs = g.get("queries_tried") or []
            if len(qs) < 3:
                short.append((a, g.get("topic", "")))
            lines += [
                f"### {g.get('topic','(제목 없음)')}",
                "",
                f"**미해결 사유** — {g.get('why_unresolved','')}",
                "",
                f"**시도한 쿼리 ({len(qs)}건)**",
                "",
            ]
            lines += [f"{i}. `{q}`" for i, q in enumerate(qs, 1)]
            lines.append("")
    lines += [
        "---",
        "",
        f"**공백 총계 {total}건.** 쿼리 3개 미만으로 기록된 항목: "
        f"{len(short)}건{' — ' + ', '.join(f'{a}/{t[:40]}' for a, t in short[:10]) if short else ' (없음 — 정지조건 충족)'}",
        "",
    ]
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[OK] {path}  공백 {total}건 (쿼리 3개 미만 {len(short)}건)")
    return total, short


def build_digest(res):
    """W 에이전트가 집필할 때 읽을 발견 요약. 근거 원장과 별개로 서사 구조를 보존한다."""
    path = os.path.join(OUT, "findings_digest.md")
    lines = ["# 에이전트 발견 요약 (집필 소스)", ""]
    NAME = {
        "A1": "intismeran autogene (Moderna/Merck)", "A2": "autogene cevumeran (BioNTech/Roche)",
        "A3": "비교·경쟁 프로그램", "A4": "국내 역량", "A5": "실패·부정 근거",
        "B1": "신항원 예측·서열설계", "B2": "RNA 형태·전달체·면역측정",
        "C1": "제조·CMC·turnaround", "C2": "COGS·밸류체인", "C3": "시장·경제성",
        "D1": "특허 레이어 1-3", "D2": "특허 레이어 4-7·소송", "D3": "정책·재무·리스크",
    }
    for a in sorted(res.keys()):
        v = res[a]
        lines += [f"## {a} — {NAME.get(a,'')}", "",
                  f"근거 {v.get('evidence_count','?')}건 ({v.get('rid_range','')})", "",
                  "### 핵심 발견", ""]
        lines += [f"- {x}" for x in (v.get("key_findings") or [])]
        lines += ["", "### 부정·반대 근거", ""]
        lines += [f"- {x}" for x in (v.get("negative_findings") or [])]
        nums = v.get("numbers") or []
        if nums:
            lines += ["", "### 정량 데이터", "", "| 항목 | 값 | 단위 | 유의사항 | 근거 |", "|---|---|---|---|---|"]
            for n in nums:
                cav = str(n.get("caveat", "")).replace("|", "/")
                lines.append(
                    f"| {str(n.get('label','')).replace('|','/')} | {str(n.get('value','')).replace('|','/')} "
                    f"| {n.get('unit','')} | {cav} | [{n.get('rid','')}] |"
                )
        lines.append("")
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[OK] {path}")


def main():
    res = load()
    os.makedirs(OUT, exist_ok=True)
    rows, stopped = build_pipeline(res)
    build_numbers_csv(res, COGS_AGENTS, os.path.join(OUT, "cogs_model.csv"), "COGS·밸류체인")
    build_numbers_csv(res, IP_AGENTS, os.path.join(OUT, "ip_landscape.csv"), "특허 패밀리·만료시계")
    total_gaps, short = build_gaps(res)
    build_digest(res)

    print("\n[정지조건 점검]")
    print(f"  M2 프로그램 15건 이상: {len(rows)}건 → {'충족' if len(rows) >= 15 else '미충족'}")
    print(f"  중단·실패 3건 이상:    {len(stopped)}건 → {'충족' if len(stopped) >= 3 else '미충족'}")
    print(f"  공백 쿼리 3개 이상:    미달 {len(short)}건 → {'충족' if not short else '미충족'}")


if __name__ == "__main__":
    main()
