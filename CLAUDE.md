# INTX — Individualized Neoantigen Therapy eXplorer

mRNA 기반 개인맞춤형 항암치료제 조사·보고 하니스.

## 0. MISSION

mRNA 기반 **개인맞춤형(individualized neoantigen) 항암치료제**의 전 영역 — 과학적 기전 · 임상 근거 · 제조/CMC 병목 · 특허/FTO · 시장/경제성 · 정책 리스크 · 국내외 플레이어 — 을 조사하여, **BD 의사결정에 바로 쓸 수 있는 근거 명문화 보고서**를 산출한다.

핵심 질문 (반드시 명시적으로 답할 것):

- **Q1.** 이 모달리티는 지금 어느 검증 단계에 있는가? (3상 데이터가 2b 신호를 재현하는가)
- **Q2.** 상업화의 진짜 병목은 무엇인가? (효능인가, vein-to-vein 시간인가, COGS인가, 급여인가)
- **Q3.** 밸류체인 어느 지점에 **원부자재·효소·CDMO 공급자**가 진입 가능한가? 그 시장의 크기와 마진 구조는?
- **Q4.** 실패·중단 사례가 말해주는 구조적 한계는 무엇인가?

## 1. 절대 규칙 (위반 시 해당 산출물 무효)

1. **완수 규칙.** 어려운 조사라도 미루거나 "추후 조사 필요"로 넘기지 않는다. 접근 불가한 자료는 *왜 불가한지*와 *대체 경로로 확보한 근거*를 명시한다. "정보 없음"은 최소 3개 이상의 서로 다른 검색 경로를 시도한 뒤에만 허용되며, 시도한 쿼리를 `gaps.md`에 기록한다.
2. **근거 명문화 규칙.** 모든 사실·수치·주장에 `[R###]` reference ID를 부여하고, 최종 산출물에서 HTML 근거 카드로 원문 출처(제목·발행처·URL·발행일·해당 문장/표 위치)를 확인할 수 있게 한다. 근거 없는 문장은 보고서에 넣지 않는다. 추정치는 반드시 `[EST]` 태그와 계산식·가정을 병기한다.
3. **신뢰도 독립 검증 규칙.** 조사 에이전트와 **분리된** 신뢰도 에이전트(R)가 모든 `[R###]`을 **상 / 중 / 하**로 등급화한다.
   - **상**: peer-reviewed 원논문, 기업 공시(10-K/20-F/IR), 규제기관 문서(FDA/EMA/MFDS), ClinicalTrials.gov 등록정보, 등록특허 원문
   - **중**: 학회 초록·발표(ASCO/AACR/ESMO/SITC), 기업 보도자료, 1차 취재 기반 산업지(Endpoints/Fierce/STAT)
   - **하**: 2차 요약·블로그·AI 요약 플랫폼·시장조사 보고서 요약본·언론 재인용
   - 단일 근거가 **하**인 주장은 본문에 단정형으로 쓸 수 없다. 헤지 표현 + 등급 표기 필수.
4. **가독성 규칙.** 글·표·도식을 적절히 섞어 비전문가도 흐름을 따라갈 수 있게 작성한다. 단, 수치는 절대 뭉개지 않는다 (N, HR, 95% CI, p, 추적기간 포함).
5. **대칭성 규칙.** 긍정 근거와 부정 근거를 **같은 강도로** 수집한다. 중단된 시험, 실패한 기업, 미충족 1차 평가변수, 회의적 전문가 견해를 별도 섹션으로 반드시 확보한다. 낙관 편향이 감지되면 V 에이전트가 반려한다.

## 2. 에이전트 구성

| ID | 역할 | 산출물 |
|---|---|---|
| **O** | 오케스트레이터. 모듈 분해·작업 큐·중복 제거·정지조건 판정 | `run_state.json` |
| **A** | 임상·과학 근거 (A1 intismeran / A2 cevumeran / A3 comparators / A4 Korea / A5 failures) | `out/evidence/A*.jsonl` |
| **B** | 기술 스택 랜드스케이프 (B1 예측·설계 / B2 RNA형태·전달체) | `out/evidence/B*.jsonl` |
| **C** | 제조·CMC·경제성 (C1 제조 / C2 COGS·밸류체인 / C3 시장) | `out/evidence/C*.jsonl` |
| **D** | 특허·기업·딜·규제·정책 (D1 IP상류 / D2 IP하류·소송 / D3 정책·재무) | `out/evidence/D*.jsonl` |
| **V** | 내부감사. 근거-주장 매핑 검증, 인용 오류·과대해석·낙관편향 적발 | `V_audit.md`, `conflicts.md` |
| **R** | 신뢰도 등급화 (A/B/C/D와 독립 실행) | `reliability_ledger.jsonl` |
| **W** | 최종 보고서 + 근거 UI 렌더링 | `INTX_report.docx`, `INTX_evidence.html` |

**실행 순서:** O → (A‖B‖C‖D 병렬) → R → V → (반려 시 재실행) → W

**V 반려 조건:** 근거 없는 문장 1개 이상 / 인용-주장 불일치 / 부정 근거 섹션 공백 / **하** 등급 단독 근거의 단정형 서술

## 4. 검색 전략 (1차 소스 우선)

- ClinicalTrials.gov API v2 / EU CTR — NCT 직접 조회, 상태·1차평가변수·`whyStopped` 확인
- PubMed / NEJM / Nature / JCO / Cancer Cell — 원논문 본문·supplementary
- ASCO / AACR / ESMO / SITC 초록 및 발표자료
- 기업 IR: 10-K, 20-F, 분기 실적, R&D Day (Moderna, BioNTech, Roche, Merck, Maravai, Danaher)
- FDA/EMA: designation, guidance (individualized therapy · platform technology), AdComm
- 특허: Google Patents / Espacenet / KIPRIS — **클레임 원문 확보 필수**
- 국내: MFDS 임상승인 현황, NTIS 국가R&D 과제 DB, DART, 바이오스펙테이터·히트뉴스

**금지:** AI 요약 플랫폼(Synapse/PatSnap 블로그 등)이나 시장조사 보도자료를 **단독 근거**로 사용. 1차 소스로 가는 포인터로만 사용하고, 원문을 확인한 뒤 원문을 `[R###]`으로 등재한다.

## 7. 정지 조건

- [ ] Q1–Q4에 근거 기반 직접 답변이 존재
- [ ] M2 표에 진행 중 프로그램 15건 이상 + **중단/실패 사례 3건 이상**
- [ ] 모든 문장에 `[R###]` 또는 `[EST]` 부착
- [ ] R 에이전트가 전체 근거의 100% 등급화 완료, **상** 등급 비중과 산출 근거 명시
- [ ] V 감사 반려 항목 0건
- [ ] `gaps.md`에 미해결 항목별 **시도한 검색 쿼리 3개 이상** 기록
- [ ] `INTX_evidence.html`이 실제로 렌더링되어 근거 카드가 열림

## 산출물

| 파일 | 내용 |
|---|---|
| `out/INTX_report.docx` | 최종 보고서 |
| `out/INTX_report.md` | 보고서 마크다운 원본 |
| `out/INTX_evidence.html` | 근거 카드 UI (등급별·모듈별 필터) |
| `out/pipeline_matrix.csv` | M2 임상 프로그램 전수 표 |
| `out/cogs_model.csv` | M3 COGS 분해 및 밸류체인 진입점 |
| `out/ip_landscape.csv` | M4 레이어별 특허 패밀리·만료시계 |
| `out/evidence_ledger.jsonl` | 전체 근거 원장 |
| `out/reliability_ledger.jsonl` | R 등급화 결과 |
| `out/V_audit.md` `out/conflicts.md` `out/gaps.md` | 감사 / 충돌 / 공백 |
| `out/run_state.json` | 실행 상태·검색 쿼리 로그 |
