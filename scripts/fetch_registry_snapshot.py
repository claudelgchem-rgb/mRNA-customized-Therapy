#!/usr/bin/env python3
"""ClinicalTrials.gov API v2 로부터 개인맞춤형/신항원 항암백신 시험 전수를 내려받아
out/raw/registry_snapshot.csv 와 out/raw/registry_snapshot.json 으로 저장한다.

V 감사 에이전트가 A 에이전트들의 임상 주장을 대조할 독립 기준선(ground truth)이다.
등록정보는 규칙 3의 '상' 등급 소스이므로, 여기서 나온 값이 보도자료와 충돌하면 이쪽이 우선한다.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "out", "raw")
API = "https://clinicaltrials.gov/api/v2/studies"

QUERIES = [
    "neoantigen", "neoepitope", "personalized cancer vaccine",
    "individualized cancer vaccine", "individualized neoantigen therapy",
    "iNeST", "mRNA cancer vaccine", "therapeutic cancer vaccine mRNA",
    "intismeran", "mRNA-4157", "V940", "autogene cevumeran", "BNT122",
    "RO7198457", "BNT111", "BNT113", "BNT116", "TG4050", "GRANITE Gritstone",
    "ELI-002", "GNOS-PV02", "VB10.NEO", "self-amplifying RNA cancer",
]

FIELDS = [
    "NCTId", "BriefTitle", "OfficialTitle", "OverallStatus", "WhyStopped",
    "Phase", "EnrollmentCount", "EnrollmentType", "StartDate",
    "PrimaryCompletionDate", "CompletionDate", "LastUpdatePostDate",
    "StudyFirstPostDate", "LeadSponsorName", "CollaboratorName", "Condition",
    "InterventionName", "PrimaryOutcomeMeasure", "LocationCountry",
    "DesignAllocation", "DesignMaskingInfo", "DesignPrimaryPurpose",
]


def fetch(query, page_token=None, retries=4):
    params = {
        "query.term": query,
        "pageSize": "100",
        "fields": "|".join(FIELDS),
        "countTotal": "true",
    }
    if page_token:
        params["pageToken"] = page_token
    url = API + "?" + urllib.parse.urlencode(params)
    delay = 2
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # 네트워크 지연은 흔하다 — 지수 백오프
            if attempt == retries - 1:
                print(f"  [실패] {query!r}: {exc}", file=sys.stderr)
                return None
            time.sleep(delay)
            delay *= 2
    return None


def flat(study):
    ps = study.get("protocolSection", {})
    ident = ps.get("identificationModule", {})
    status = ps.get("statusModule", {})
    design = ps.get("designModule", {})
    spons = ps.get("sponsorCollaboratorsModule", {})
    cond = ps.get("conditionsModule", {})
    arms = ps.get("armsInterventionsModule", {})
    outc = ps.get("outcomesModule", {})
    loc = ps.get("contactsLocationsModule", {})

    enroll = design.get("enrollmentInfo", {}) or {}
    countries = sorted({
        l.get("country") for l in (loc.get("locations") or []) if l.get("country")
    })

    return {
        "nct": ident.get("nctId", ""),
        "title": (ident.get("briefTitle") or "").replace("\n", " "),
        "status": status.get("overallStatus", ""),
        "why_stopped": (status.get("whyStopped") or "").replace("\n", " "),
        "phase": ",".join(design.get("phases") or []),
        "enrollment": enroll.get("count", ""),
        "enrollment_type": enroll.get("type", ""),
        "allocation": (design.get("designInfo") or {}).get("allocation", ""),
        "masking": ((design.get("designInfo") or {}).get("maskingInfo") or {}).get("masking", ""),
        "purpose": (design.get("designInfo") or {}).get("primaryPurpose", ""),
        "start": (status.get("startDateStruct") or {}).get("date", ""),
        "primary_completion": (status.get("primaryCompletionDateStruct") or {}).get("date", ""),
        "completion": (status.get("completionDateStruct") or {}).get("date", ""),
        "first_posted": (status.get("studyFirstPostDateStruct") or {}).get("date", ""),
        "last_update": (status.get("lastUpdatePostDateStruct") or {}).get("date", ""),
        "sponsor": (spons.get("leadSponsor") or {}).get("name", ""),
        "collaborators": "; ".join(
            c.get("name", "") for c in (spons.get("collaborators") or [])
        ),
        "conditions": "; ".join(cond.get("conditions") or []),
        "interventions": "; ".join(
            i.get("name", "") for i in (arms.get("interventions") or [])
        )[:400],
        "primary_outcome": "; ".join(
            o.get("measure", "") for o in (outc.get("primaryOutcomes") or [])
        )[:400],
        "countries": "; ".join(countries),
        # API v2 는 국가명을 "South Korea" 로 반환한다 ("Korea, Republic of" 아님)
        "has_korea": "Y" if any("Korea" in c for c in countries) else "",
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    studies, seen, hits = {}, set(), {}

    for q in QUERIES:
        token, n, pages = None, 0, 0
        while True:
            data = fetch(q, token)
            if not data:
                break
            for s in data.get("studies", []):
                row = flat(s)
                if row["nct"] and row["nct"] not in seen:
                    seen.add(row["nct"])
                    studies[row["nct"]] = row
                n += 1
            token = data.get("nextPageToken")
            pages += 1
            if not token or pages >= 6:
                break
        hits[q] = n
        print(f"  {q:42s} {n:4d}건")

    rows = sorted(studies.values(), key=lambda r: (r["status"], r["nct"]))

    csv_path = os.path.join(OUTDIR, "registry_snapshot.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    json_path = os.path.join(OUTDIR, "registry_snapshot.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"queries": hits, "studies": rows}, fh, ensure_ascii=False, indent=1)

    from collections import Counter
    st = Counter(r["status"] for r in rows)
    stopped = [r for r in rows if r["why_stopped"]]
    korea = [r for r in rows if r["has_korea"]]

    print(f"\n[OK] 고유 시험 {len(rows)}건 → {csv_path}")
    print(f"     상태 분포: {dict(st.most_common())}")
    print(f"     중단 사유(whyStopped) 기재 시험: {len(stopped)}건  ← 부정 근거의 1차 소스")
    print(f"     한국 사이트 포함 시험: {len(korea)}건")
    for r in stopped[:25]:
        print(f"       {r['nct']} [{r['status']}] {r['title'][:58]} :: {r['why_stopped'][:80]}")
    if korea:
        print("     한국 참여:")
        for r in korea[:20]:
            print(f"       {r['nct']} [{r['status']}] {r['title'][:70]}")


if __name__ == "__main__":
    main()
