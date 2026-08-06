---
description: INTX 전체 조사 파이프라인 실행 (O → A‖B‖C‖D → R → V → W)
---

INTX 하니스를 전체 실행한다. `CLAUDE.md`의 절대 규칙 1–5와 정지 조건을 준수할 것.

1. **O**: `out/run_state.json`을 읽어 이미 완료된 모듈을 건너뛴다. 없으면 새로 생성.
2. **A‖B‖C‖D 병렬**: `.claude/agents/` 의 13개 조사 서브에이전트를 병렬 실행.
   각 에이전트는 `out/evidence/<ID>.jsonl` 에 배정된 rid 블록으로만 근거를 기록한다.
3. **머지**: `python3 scripts/merge_evidence.py` → `out/evidence_ledger.jsonl`
4. **R**: 조사 에이전트와 독립적으로 전 근거를 상/중/하 등급화 → `out/reliability_ledger.jsonl`
5. **V**: 근거-주장 매핑 감사. 반려 항목이 있으면 해당 에이전트만 재실행 → `out/V_audit.md`
6. **W**: `out/INTX_report.md` → `.docx`, `python3 scripts/build_evidence_html.py`, CSV 3종 산출.
7. 정지 조건 체크리스트를 전부 충족했는지 확인 후 완료 선언.

인자: $ARGUMENTS (특정 모듈만 재실행하려면 모듈 ID를 전달, 예: `/intx-run M2 M4`)
