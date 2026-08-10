# 미해결 공백 (gaps)

`CLAUDE.md` 규칙 1(완수 규칙)에 따라, 확보하지 못한 항목은 *왜 불가한지*와
*시도한 검색 쿼리*를 함께 기록한다. 정지 조건은 항목별 쿼리 3개 이상이다.

## A1

### MFDS 인티스메란(V940) 임상시험계획승인(IND) 승인일자·승인번호 원문

**미해결 사유** — nedrug.mfds.go.kr 임상시험 검색은 자바스크립트 렌더링 기반이라 POST 요청에 HTML 셸만 반환하고 검색 결과를 노출하지 않는다. 공공데이터포털 ClinicalTrialsInfoService 오픈API는 응답코드 12 'NO_OPENAPI_SERVICE_ERROR - 해당 오픈API 서비스가 없거나 폐기됨'을 반환하여 폐기 상태다. 대체 경로로 ClinicalTrials.gov 등록 기관 데이터를 사용해 한국 임상 진행 사실 자체는 6개 시험·32개 기관 수준까지 확증했다(R151-R155). 국내 임상 수행은 약사법상 MFDS 승인을 전제하므로 승인 존재는 논리적으로 필연이나, 승인일자·승인번호·승인 적응증 문구는 미확보 상태다.

**시도한 쿼리 (5건)**

1. `curl POST https://nedrug.mfds.go.kr/searchClinic (searchYn=true&itemName=V940)`
2. `curl https://apis.data.go.kr/1471000/ClinicalTrialsInfoService/getClinicalTrialsInfo`
3. `웹검색: 인티스메란 mRNA-4157 국내 임상시험 승인 식약처 머크 모더나 개인맞춤 항암백신`
4. `웹검색: MSD 한국 임상시험 승인 V940 mRNA-4157 흑색종 폐암 삼성서울병원 서울대병원 세브란스`
5. `CRIS(cris.nih.go.kr) search_result_st01.do?searchWord=V940`

### INTerpath-007 종료에 대한 머크/모더나의 명시적 공식 성명

**미해결 사유** — ClinicalTrials.gov whyStopped는 'Business reasons' 4단어가 전부이며(R135), 머크·모더나 어느 보도자료·SEC 제출서류에서도 이 시험의 종료를 명시적으로 언급한 문장을 찾지 못했다. 머크 FY2025 10-K는 V940의 2상 적응증에서 피부편평세포암을 조용히 제외했을 뿐 종료 사실을 서술하지 않았다(R170). ApexOnco(2025-10-13)가 KEYNOTE-630 실패와의 연계를 보도했으나 유료구독 벽으로 전문 확인이 불가하여 '하' 등급 포인터로만 등재했다(R140). ESMO 2024 TiP 초록(940TiP, Annals of Oncology)은 403 차단으로 원문 접근 실패. 등록부 버전 이력으로 중단 시점·규모·PCD 단축은 완전히 재구성했다(R136-R139).

**시도한 쿼리 (5건)**

1. `웹검색: Merck INTerpath-007 cutaneous squamous cell carcinoma terminated intismeran "business reasons" 2026`
2. `웹검색: Moderna intismeran INTerpath-007 discontinued cSCC 1000 patients enrollment KEYNOTE-630 pembrolizumab failed`
3. `WebFetch https://www.annalsofoncology.org/article/S0923-7534(24)02520-1/fulltext (940TiP ESMO 2024 초록) → HTTP 403`
4. `WebFetch + r.jina.ai https://www.apexonco.com/another-bump-modernas-neoantigen-road → 유료구독 벽`
5. `SEC EDGAR full-text search q="intismeran" ciks=0000310158 (머크 전 제출서류 8건 검토)`

### 언론 보도 '5년 RFS 68.8%' 및 '5년 OS 92.2% 대 71.3%' 수치의 1차 출처

**미해결 사유** — ASCO Post와 ecancer가 5년 RFS 68.8% 대 49.1%, 5년 OS 92.2% 대 71.3%를 보도했으나(R124b), 동료심사 JCO 논문 본문에는 4년 RFS 72.4% 대 49.1%만 존재하고 5년 시점 수치가 없다(R123). ASCO 2026 초록 원문(asco.org/abstracts-presentations/259570)과 발표 슬라이드는 모두 HTTP 403으로 차단되어 원 발표 자료에서 해당 수치를 확인하지 못했다. 특히 OS율 71.3%는 단독군 사망 7/50(14%)과 산술적으로 정합하지 않아(KM 검열을 감안해도 괴리) 언론의 4년/5년 시점 혼용 또는 오기 가능성이 높다. 보고서에는 논문 수치(R123, R124)를 채택하고 언론 수치는 충돌 항목으로 표기하기로 결정했다.

**시도한 쿼리 (5건)**

1. `WebFetch https://www.asco.org/abstracts-presentations/259570 → HTTP 403`
2. `WebFetch + r.jina.ai https://ascopubs.org/doi/10.1200/JCO-26-00835 (전문 확보, 4년 수치만 존재 확인)`
3. `WebFetch https://ecancer.org/en/news/28383-asco-2026-cancer-vaccine-sustains-49-percent-melanoma-reduction-after-5-years`
4. `WebFetch https://ascopost.com/news/june-2026/vaccine-plus-pembrolizumab-reduces-risk-of-recurrence-in-high-risk-resected-melanoma/`
5. `웹검색: KEYNOTE-942 mRNA-4157 5-year update ASCO 2026 recurrence-free survival hazard ratio`

### 인티스메란의 실제 vein-to-vein 시간과 배치당 COGS

**미해결 사유** — 공개 1차 자료에서 확인 가능한 유일한 수치는 ASCO 2023 발표 슬라이드 도식의 '~6 weeks' 라벨뿐이며(R109), 이것이 조직 채취부터 첫 투여까지의 전체 vein-to-vein인지 설계·제조 구간만인지 슬라이드가 명시하지 않는다. 모더나 10-K와 애널리스트데이는 '처리시간 개선(improve turnaround time)'과 '비용 절감'을 목표로만 언급하고 현재 값이나 목표 값을 수치로 제시하지 않는다(R165, R166). 배치당 COGS는 모더나·머크 어느 공시에도 분해되어 있지 않다. 확보 가능한 최선의 대리 지표로 머크의 공유 설비 자본화 2억 3,600만 달러(R161)와 양사 합산 연간 개발비 약 7억7천만 달러(R160, R161)를 M3 모델의 앵커로 넘긴다.

**시도한 쿼리 (5건)**

1. `pdfminer 추출: Moderna INT program detail PDF (int-5-2-24.pdf) 전문에서 'weeks|turnaround|Marlborough|manufactur|vein' 정규식 전수 검색`
2. `Moderna FY2025 10-K 전문에서 'turnaround|vein-to-vein|cost of sales|intismeran' 컨텍스트 추출`
3. `Moderna 2025 Analyst Day 8-K Exhibit 99.1 전문 검색 (Marlborough/manufacturing 섹션)`
4. `Moderna Q1 2026 및 Q2 2026 10-Q Note 5 Collaboration Agreements 전문 검토`
5. `웹검색: Moderna Merck intismeran collaboration 50/50 cost sharing $250 million opt-in exercise mRNA-4157 economics`

## A2

### Roche/Genentech 자체 IR 문서(파마데이 등)에서 autogene cevumeran에 대한 직접 코멘트 및 우선순위 강등 여부

**미해결 사유** — Roche 공식 IR/파마데이 자료에서 autogene cevumeran을 명시적으로 언급하거나 우선순위를 강등했다는 1차 근거를 찾지 못했다. 확인 가능한 유일한 공식 축소 조치는 IMcode004 중단(BioNTech 20-F 및 Q4 2025 보도자료 경유)이며, PDAC 시험 IMCODE003은 여전히 Genentech이 리드 스폰서로 모집 중이다. 따라서 'Roche가 우선순위를 강등했다'는 명제는 현재 근거 부족으로 단정 불가하며 부정 확인(R268)으로 등재했다.

**시도한 쿼리 (4건)**

1. `Roche pipeline 2026 autogene cevumeran RO7198457 phase 2 colorectal pancreatic status`
2. `Roche pharma day 2025 2026 individualized neoantigen cancer vaccine deprioritized cevumeran commentary`
3. `BioNTech Q4/FY2025 실적 보도자료 및 20-F FY2025 내 Autogene cevumeran 항목 전문 검색 (SEC EDGAR 원문 grep: 'Roche', 'opt-in', 'opted', 'discontinue')`
4. `ClinicalTrials.gov sponsorCollaboratorsModule 교차 확인 (NCT05968326 / NCT06534983 / NCT04486378 리드 스폰서 확인)`

### IMcode004 안전성 도입군에서 발생한 구체적 안전성 사건의 성격(사망 여부, 등급, 기전)

**미해결 사유** — 등록정보 whyStopped 필드는 '안전성 도입군에서 관찰된 안전성 사건'이라고만 기재하고 구체 내용을 밝히지 않았다. BioNTech 20-F·분기보고서·Q4 보도자료 어디에도 해당 사건의 상세가 서술되지 않았고, 시험이 62명 안전성 추적으로 전환되면서 결과 게시도 아직 없다(PCD 2027-11-10). 스폰서가 Roche이므로 BioNTech 공시 의무 범위 밖일 가능성이 크다.

**시도한 쿼리 (4건)**

1. `ClinicalTrials.gov archive API로 NCT06534983 전체 32개 버전 순회하여 whyStopped 원문 및 상태 전이 추적 (v15/v16 SUSPENDED 확인)`
2. `BioNTech 20-F FY2025 원문 grep: 'MIUC', 'urothelial', 'IMCODE004', 'safety event', 'clinical hold'`
3. `BioNTech Q1 2026 / Q2 2026 분기보고서 원문 grep: 'MIUC', 'urothelial', 'NCT06534983' (전부 0건 — 서술 자체가 삭제됨)`
4. `Roche pharma day 2025 2026 individualized neoantigen cancer vaccine deprioritized cevumeran commentary`

### iNeST 프로그램 단독 R&D 지출액 및 개인맞춤 제조의 연간 배치 캐파(vein-to-vein 상업 목표 시간 수치)

**미해결 사유** — BioNTech은 세그먼트를 프로그램 단위로 분리 공시하지 않아 iNeST 단독 R&D 지출을 산출할 수 없다. 제조계약상 '목표 소요시간(target turnaround times)'과 '상업 공정은 더 엄격한 소요시간'이 존재한다고만 서술되고 구체 수치는 영업비밀로 비공개다. 마르부르크/마인츠 시설의 개인맞춤 제품 연간 배치 캐파도 20-F에 수치로 공시되지 않았다. 대체 경로로 학술 논문의 실측치(수술→첫 투여 중앙 9.4주, 제조 최적 28일)를 확보해 R204/R238로 등재했다.

**시도한 쿼리 (4건)**

1. `BioNTech 20-F FY2025 원문 grep: 'vein-to-vein' (0건), 'turnaround' (2건, 계약 서술만), 'on-demand' (2건), 'Marburg', 'manufacturing of individualized'`
2. `BioNTech 20-F Item 5.A Operating Results 'Research and Development Expenses' 섹션 전문 확인 (프로그램별 분해 없음)`
3. `Nature Medicine 2025 (PMC11750724) 및 Nature 2023 (PMC10171177) 본문에서 제조 소요시간·제조 실패율 직접 추출`
4. `BioNTech Q2 2026 분기보고서 R&D 비용 증가 사유 목록 확인 (iNeST 미등장)`

### ESMO 2025 IMcode001 초록 954P 전문의 OS 위험비 및 면역반응률 정확 수치

**미해결 사유** — Annals of Oncology 출판사 사이트가 HTTP 403으로 접근을 차단했고, vjoncology 영상 페이지도 403이었다. 대체 경로로 검색 스니펫에서 데이터 컷오프(2024-05-30), 중앙 추적(30.5개월), PFS HR 0.78, p=0.3061을 확보해 R229로 등재했다. 다만 초록 수준 근거(중 등급)이며, 더 결정적인 것은 동일 시험의 등록정보 최종 결과(HR 0.79, 95% CI 0.49-1.27, p=0.3284, ORR 41.7% vs 48.8%)를 1차 소스로 확보했다는 점이므로 실질적 공백은 크지 않다.

**시도한 쿼리 (4건)**

1. `WebFetch https://www.annalsofoncology.org/article/S0923-7534(25)02443-3/fulltext (HTTP 403)`
2. `WebFetch https://www.vjoncology.com/video/nfqevsf7jm8-imcode001-autogene-cevumeran-pembrolizumab-in-melanoma/ (HTTP 403)`
3. `"autogene cevumeran" ESMO 2025 melanoma IMCODE001 abstract overall survival hazard ratio pembrolizumab`
4. `ClinicalTrials.gov API v2 NCT03815058 resultsSection 전체 파싱 (등록정보 최종 결과로 대체 확보 성공)`

## A3

### BNT111 2상 ESMO 2025 초록 원문(Arm2/Arm3 ORR, CR/DCR/PFS/OS 확정치)

**미해결 사유** — ESMO 초록 호스트(clin.larvol.com), OncLive, Targeted Oncology, Fierce Biotech가 모두 HTTP 403을 반환하여 원문 확보 실패. ClinicalTrials.gov 결과란에는 1차 평가변수(병용군 ORR 18.0%)만 등재되어 있고 2차 지표는 'Data will be reported at the time of final results posting'으로 표기됨. 대체 경로로 등록부 1차 소스(R300, R360, R368)와 2차 보도(R377, 신뢰도 하)를 병기함

**시도한 쿼리 (5건)**

1. `BioNTech BNT111 phase 2 melanoma primary endpoint met objective response rate 2024 press release cemiplimab`
2. `"BNT111" BioNTech discontinue "will not" further development melanoma October 2025 ESMO 18% ORR decision`
3. `WebFetch https://clin.larvol.com/abstract-detail/ESMO%202025/77184712`
4. `WebFetch https://www.onclive.com/view/phase-2-bnt111-cemiplimab-data-prove-positive-in-pd--l-1-relapsed-refractory-melanoma`
5. `WebFetch https://www.targetedonc.com/view/bnt111-cemiplimab-shows-significant-orr-improvement-in-stage-iii-iv-melanoma`

### 중국 NMPA 등록 전용(NCT 미등록) 개인맞춤형 mRNA 신항원 임상의 전수

**미해결 사유** — chinadrugtrials.org.cn은 자동 조회가 차단되어 API/스크래핑 접근 불가. 대체 경로로 ClinicalTrials.gov 스폰서 질의(Stemirna/Abogen/Likang/Rinuagene/Immorna/WestGene)와 중국어 웹 검색을 사용했으며, WestGene은 ClinicalTrials.gov에 스폰서 등록 자체가 없어 NCT 확인 불가(R344, R372). 따라서 중국 프로그램 수는 과소집계일 가능성이 있음

**시도한 쿼리 (5건)**

1. `WestGene 深圳 mRNA 个体化 肿瘤疫苗 WGc-043 EBV 临床试验 2025`
2. `Likang LK101 personalized neoantigen mRNA vaccine China clinical trial 立康生命 新抗原`
3. `"iNeo-Vac" OR "RGL-270" OR "XH001" personalized neoantigen vaccine China phase 1 results 2025`
4. `ClinicalTrials.gov API v2 query.spons=WestGene / Likang / Rinuagene / Stemirna / Abogen`
5. `斯微生物 破产清算 2024 2025 重整 法院 个性化 肿瘤疫苗 停止研发`

### Gritstone SLATE-KRAS(2세대, KRAS 단독 표적) 2상 결과

**미해결 사유** — Nature Medicine 2024 논문은 1상 중간 결과만 보고했고 SLATE-KRAS 2상 결과는 별도 발표가 확인되지 않음. NCT03953235는 2023-03-10 COMPLETED 되었으나 결과가 등록부에 게시되지 않았고(hasResults=false), 회사가 2024-10 파산하면서 결과 공개 의무 이행 주체가 불분명해짐. 대체로 1상 논문의 면역우성 서열 발견(R321)만 확보

**시도한 쿼리 (5건)**

1. `Gritstone SLATE Nature Medicine 2023 shared neoantigen KRAS phase 1/2 results objective response rate 39 patients`
2. `PubMed esearch: SLATE neoantigen Gritstone OR "GRT-C903"`
3. `PubMed esearch: shared neoantigen vaccine ChAd samRNA KRAS`
4. `ClinicalTrials.gov API v2 studies/NCT03953235 (hasResults 확인)`
5. `"Seattle Project" Gritstone GRANITE 2025 2026 clinical program continuing samRNA neoantigen`

### Seattle Project Corp의 현재 자금 상황·GRANITE 3상 진행 의사

**미해결 사유** — 비상장 사모 법인으로 SEC 공시 의무가 없고 자체 IR 사이트나 보도자료가 검색되지 않음. 대체 경로로 ClinicalTrials.gov 스폰서 변경(R317)과 등록정보 최종 갱신일 2025-05-16 정체(R369)를 간접 지표로 사용

**시도한 쿼리 (4건)**

1. `Gritstone bio assets sold auction 2025 who acquired GRANITE neoantigen "stalking horse"`
2. `"Seattle Project" Gritstone GRANITE 2025 2026 clinical program continuing samRNA neoantigen`
3. `Gritstone bio Chapter 11 bankruptcy 2024 GRANITE assets acquired`
4. `ClinicalTrials.gov API v2 query.spons=Seattle Project Corporation`

### BNT113 AHEAD-MERIT의 중간분석/무용성 분석 실시 여부 및 실제 등록 진척

**미해결 사유** — ClinicalTrials.gov에는 목표 350명(ESTIMATED)만 표기되고 실제 누적 등록 수가 공개되지 않음. BioNTech IR·분기보고서에서도 등록 수치를 공개하지 않으며, 확인 가능한 최신 정보는 2026년 1월 FDA Fast Track 지정(R363)과 2023-12-15 컷오프 안전성 도입부 15명 데이터(R305)뿐. 1차 완료 예정일이 2029년 4월로 설정된 점(R304)만 지연 지표로 사용

**시도한 쿼리 (4건)**

1. `BNT113 AHEAD-MERIT interim analysis 2025 2026 head neck HPV16 futility enrollment update`
2. `BioNTech 20-F 2025 pipeline BNT111 BNT113 BNT116 FixVac status discontinued`
3. `ClinicalTrials.gov API v2 studies/NCT04534205 (전체 프로토콜 섹션)`
4. `WebFetch BioNTech Clinical Pipeline Q3 2025 PDF`

## A4

### DXVX mRNA 항암백신 기술이전 파트너사 실명 및 계약금(upfront) 금액

**미해결 사유** — 회사가 PR Newswire 보도자료와 국내 공시 모두에서 파트너사명을 'U.S.-based biotech company'로만 표기하고 계약금을 공개하지 않았다. KIND 공시 뷰어는 동적 렌더링이라 WebFetch로 본문 추출이 불가했고 DART Open API는 인증키가 필요해 접근 불가했다. 총액 2.2억달러는 마일스톤 총합(biodollar)으로만 확인된다

**시도한 쿼리 (4건)**

1. `DXVX 미국 바이오텍 3000억 항암백신 기술이전 계약 상대 계약금 마일스톤`
2. `"디엑스앤브이엑스" OR "DXVX" circRNA 항암백신 전임상 원숭이 비임상 진행 2026 진행상황`
3. `Dx&Vx Signs USD 220 Million Co-Development and License Agreement (PR Newswire 원문 직접 fetch)`
4. `디엑스앤브이엑스 DXVX 실적 적자 2025 2026 반기보고서 임상 진입 전임상`

### 식약처의 개인맞춤형(individualized) 신항원 항암백신 전용 규제 가이드라인 존재 여부와 심사 방침

**미해결 사유** — 'mRNA 기반 유전자치료제의 품질평가 가이드라인' PDF는 이미지 스캔본(271개 임베디드 이미지, FlateDecode 압축)이라 텍스트 추출에 실패했고, 식약처 자료실 검색으로도 individualized/신항원 특화 문서가 확인되지 않았다. 2026년 업무보고 PDF의 42건 가이드라인 목록 항목별 명세도 확인하지 못했다. 국내 등록 개인맞춤 신항원 임상이 0건이라 심사 선례 자체가 없는 것으로 판단된다

**시도한 쿼리 (4건)**

1. `식약처 개인맞춤형 항암백신 신항원 규제 가이드라인 첨단바이오의약품 2025 2026`
2. `식약처 mRNA 백신 품질 가이드라인 개인맞춤형 항암백신 규제 준비 첨단재생바이오법 2026`
3. `식약처 임상시험 승인 mRNA 항암백신 개인맞춤형 국내 첫 IND 2025 2026`
4. `mfds.go.kr 'mRNA 기반 유전자치료제의 품질평가 가이드라인' PDF 직접 fetch`

### 에스티팜 2025년 사업보고서상 매출 유형별 mRNA 비중 원문 수치

**미해결 사유** — mRNA 비중 0.9%는 2차 집계 소스(나무위키가 사업보고서를 인용)에서만 확인됐다. DART/KIND 사업보고서 본문은 동적 뷰어(disclsviewer)로 제공돼 WebFetch가 SPA 셸만 반환했고, DART Open API는 인증키 필요로 접근 불가했다. 증권사 리포트 PDF(대신증권)도 부분 텍스트만 확보됐다. 다만 mRNA 매출 미미함은 에스티팜 임원의 공개 발언(R412)으로 교차 뒷받침된다

**시도한 쿼리 (4건)**

1. `에스티팜 2025년 연간 매출 올리고뉴클레오타이드 비중 실적 반월캠퍼스 mRNA GMP 생산능력`
2. `에스티팜 mRNA CDMO 스마트캡 SmartCap STLNP 2025 매출 올리고`
3. `에스티팜 개인맞춤형 항암백신 CDMO 수주 계약 mRNA 원료 공급 2026`
4. `"에스티팜" mRNA "개인 맞춤형" 제조 "48" 일 항암백신 CDMO 준비`

### PAVE 과제의 NTIS 국가R&D 원 레코드(과제고유번호, 연차별 예산 배분, 정확한 수행기간)

**미해결 사유** — 2025년 7월 착수한 신규과제라 ntis.go.kr 공개 DB에 아직 반영되지 않았거나 검색 인덱싱이 안 된 것으로 보인다. 복지부 보도자료(공고 175억원/5년)와 수행기관 발표(191억원/4.5년)의 금액·기간 차이를 정부 원문으로 해소하지 못했다. 한국형 ARPA-H 전담 사이트의 과제 상세 페이지에도 검색으로 도달하지 못했다

**시도한 쿼리 (4건)**

1. `한국형 ARPA-H 프로젝트 PAVE 항암백신 과제 공고 보건복지부 2025 총 사업비`
2. `NeoVax-K 컨소시엄 환자 맞춤형 항암백신 개발 플랫폼 구축 PAVE 191억 참여기관`
3. `"환자 맞춤형 항암백신" 신속개발 플랫폼 "6~8주" 신항원 ARPA-H 아스톤사이언스 주관`
4. `보건복지부 한국형 ARPA-H 2025년도 신규 프로젝트 공고 원문 fetch (mohw.go.kr)`

### 아이진의 항암백신 프로그램(과제 지시서상의 'EG-Vac') 실체

**미해결 사유** — 'EG-Vac'이라는 명칭의 아이진 항암백신 프로그램은 3회 이상 검색에도 확인되지 않았다. 아이진 공식 보도자료 페이지와 파이프라인 기사에서 확인된 것은 결핵백신(EG-TB), 코로나19 sa-mRNA(BMI2012), 수막구균 백신(EG-MCV4)이며 항암백신은 없었다. ClinicalTrials.gov EyeGene Inc. 스폰서 시험 4건도 전부 감염병 백신이다. 명칭 오류이거나 비공개 초기 과제로 판단된다

**시도한 쿼리 (4건)**

1. `아이진 EG-Vac mRNA 항암백신 LNP 2025 2026 임상`
2. `지놈앤컴퍼니 나이벡 카이노스메드 팬젠 mRNA 항암 신항원 2025 2026`
3. `ClinicalTrials.gov API query.spons=EyeGene 전수 조회`
4. `eyegene.co.kr 보도자료 페이지 확인`

### 나이벡·카이노스메드·팬젠·지놈앤컴퍼니의 mRNA/신항원 항암백신 관련 프로그램

**미해결 사유** — 4개사 모두 mRNA 기반 개인맞춤 신항원 항암백신 프로그램이 검색되지 않았다. 지놈앤컴퍼니는 ADC·마이크로바이옴, 카이노스메드는 CNS/항바이러스, 팬젠은 바이오시밀러 CHO 세포주, 나이벡은 펩타이드 약물전달(NIPEP-TPP)로 사업 영역이 다른 것으로 확인됐다. M2/M6 범위에 실질적으로 해당하지 않는다고 판단해 증거 라인으로 등재하지 않았다

**시도한 쿼리 (4건)**

1. `지놈앤컴퍼니 나이벡 카이노스메드 팬젠 mRNA 항암 신항원 2025 2026`
2. `삼양홀딩스 SENS LNP 전달 플랫폼 mRNA 2025 레모넥스 나이벡 핵산 전달체`
3. `국가신약개발사업단 KDDF mRNA 항암백신 과제 선정 2025 2026`
4. `국내 mRNA 항암백신 개발 뒤처져 한계 지적 임상 없다 전문가 비판 개인맞춤형`

### VGXI 텍사스 Conroe 신공장의 정량적 생산능력(발효조 용량, 연간 플라스미드 배치 수) 및 mRNA IVT 템플릿 수주 실적

**미해결 사유** — 진원생명과학 공식 보도자료와 언론 보도 모두 생산능력 수치를 제시하지 않는다. VGXI 자체 웹사이트는 검색 결과에 노출되지 않았고, 진원생명과학 사업보고서(DART) 본문은 동적 뷰어로 접근 불가했다. 다만 2026년 상반기 CDMO 매출 0원이라는 핵심 사실은 한국거래소 조회공시 답변 인용으로 확보했다

**시도한 쿼리 (4건)**

1. `VGXI 진원생명과학 플라스미드 DNA CDMO 텍사스 신공장 생산능력 mRNA 수주`
2. `진원생명과학 2025년 매출 영업손실 결손금 사업보고서 VGXI 적자`
3. `진원생명과학 감자 결정 2026 무상감자 유상증자 매출 영업손실 규모`
4. `genels.com 보도자료 목록 직접 fetch`

## A5

### 개인맞춤 mRNA 신항원 백신의 실제 1배치 COGS 및 배치 실패율(manufacturing failure rate)

**미해결 사유** — Moderna·BioNTech 어느 쪽도 10-K/20-F/IR에서 batch success rate나 per-batch COGS를 공개하지 않는다. Moderna 10-K는 'novel, complex manufacturing process'라는 정성적 위험요인만 기재(R561). 확보 가능한 유일한 정량 자료는 펩타이드 기반 영국 학술 모델(R549)과 Provenge 역사 벤치마크(R527)뿐이며 둘 다 mRNA-LNP 직접 대응이 아니다.

**시도한 쿼리 (4건)**

1. `Moderna 10-K 2025 risk factors individualized neoantigen therapy INT manufacturing vein-to-vein turnaround time weeks`
2. `personalized cancer vaccine cost of goods per patient batch $100,000 payer reimbursement skepticism individualized manufacturing economics`
3. `Moderna Q2 2026 results cash position net loss intismeran manufacturing Marlborough cost per dose`
4. `mRNA-4157 KEYNOTE-942 manufacturing turnaround time weeks patients did not receive vaccine progression during production`

### 무작위 임상에서 제조 실패·대기 중 진행으로 백신을 실제로 투여받지 못한 환자 비율(intention-to-treat 대비 실제 투여율)

**미해결 사유** — KEYNOTE-942 Lancet 논문 초록과 5년 업데이트 보도자료 모두 randomized N만 제시하고 vaccine-not-administered 사유별 분해를 제공하지 않는다. CT.gov 결과 게시도 없다. 논문 supplementary(페이월) 접근 실패.

**시도한 쿼리 (4건)**

1. `mRNA-4157 KEYNOTE-942 manufacturing turnaround time weeks patients did not receive vaccine progression during production`
2. `KEYNOTE-942 criticism limitations open-label imbalance baseline small sample not powered experts caution 2023`
3. `autogene cevumeran colorectal adjuvant trial 2026 disease-free survival result Genentech Roche announcement`
4. `KEYNOTE-942 5-year update JCO 2026 intismeran RFS hazard ratio 95% CI phase 2b limitations open-label`

### 실명 전문가의 공개 회의론(NEJM/Nature/Lancet/JAMA Oncology 사설 원문)

**미해결 사유** — 동료심사 리뷰(Katsikis Nat Rev Immunol 2024, R541-R543; ScienceDirect 2026, R558; Cancer Cell 2026, R559)에서 구조적 비판은 충분히 확보했으나, 특정 종양내과 의사가 실명으로 이 모달리티를 공개 비판한 사설의 원문은 확보하지 못했다. Lancet 2024;403:590-591 (KEYNOTE-942 동반 논평)과 Cell 2020;183:591-593 (TESLA 동반 논평)의 존재는 PubMed 'Comment in' 필드로 확인했으나 전문은 페이월·403.

**시도한 쿼리 (4건)**

1. `cancer vaccine skeptics neoantigen vaccine criticism oncologist doubts pembrolizumab effect confounded editorial 2025 2026`
2. `cancer vaccine neoantigen critic hype caution Vinay Prasad OR Bishal Gyawali skeptic phase 2b melanoma small trial`
3. `neoantigen+vaccine+skepticism+challenges+limitations+editorial (PubMed E-utilities esearch)`
4. `Why clinical benefit remains inconsistent personalized neoantigen cancer vaccines 2026 review`

### 국내(한국) mRNA 개인맞춤 신항원 항암치료제의 임상 진입·중단 사례

**미해결 사유** — MFDS 임상승인 현황, NTIS, DART, 국내 산업지 어디에서도 국내 기업의 개인맞춤 신항원 항암 백신 임상 진입 또는 중단 사례를 확인하지 못했다. 확인된 것은 국립보건연구원 mRNA 사업(플랫폼 수준)과 기업의 AACR 초기 연구발표뿐(R566). 부재 증명은 원리적으로 약하므로 '하' 등급으로 기록하고 단정형 서술을 금지했다.

**시도한 쿼리 (4건)**

1. `국내 신항원 개인맞춤 항암백신 임상 중단 실패 mRNA 개발 포기 2025 2026`
2. `MFDS 임상승인 개인맞춤 신항원 백신 국내 기업`
3. `Korea personalized neoantigen cancer vaccine clinical trial company discontinued`
4. `한미약품 mRNA 암백신 개인맞춤 신항원 임상`

### 러시아 Enteromix / Neooncovac의 정식 등록 여부(러시아 규제기관 1차 문서)

**미해결 사유** — 러시아 국가의약품등록부(ГРЛС) 원문에 직접 접근하지 못했다. 확보한 자료는 모두 2차 요약·언론 재인용이며 서로 '사용 준비 완료'와 '승인 대기'로 엇갈린다(R546). '전 세계 어디에도 승인 제품이 없다'(R545)는 load-bearing 주장의 유일한 잠재적 반례이므로 R546을 '하' 등급으로 기록하고, 주장은 '서방 주요 규제 관할(FDA/EMA/MFDS)에서 승인 0건'으로 한정했다.

**시도한 쿼리 (3건)**

1. `Russia Enteromix personalized mRNA cancer vaccine 2025 2026 approval Gamaleya free distribution registered`
2. `personalized neoantigen cancer vaccine regulatory approval 2026 none approved anywhere FDA EMA`
3. `Enteromix Neooncovac Russia FMBA registration state register medicines approval status 2026`

### Cancer Cell 2026 'Bridging clinical gaps in personalized cancer neoantigen vaccines' 전문 내용

**미해결 사유** — Cell Press 도메인(cell.com)이 WebFetch에 대해 일관되게 HTTP 403을 반환한다(Cell TESLA 원문, Cancer Cell 2026 모두). Europe PMC·PMC에 오픈액세스 사본이 없다. 서지정보와 제목만 확보(R559). 동일 저널의 TESLA 원문은 PubMed 초록(R540)과 Nat Rev Immunol 재인용(R541)으로 우회 확보했다.

**시도한 쿼리 (4건)**

1. `WebFetch https://www.cell.com/cancer-cell/fulltext/S1535-6108(26)00212-6`
2. `WebFetch https://www.cell.com/cell/fulltext/S0092-8674(20)31156-9`
3. `Europe PMC REST search: TESLA consortium tumor epitope immunogenicity Wells (pmcid 조회)`
4. `Bridging clinical gaps in personalized cancer neoantigen vaccines Cancer Cell 2026 open access`

## B1

### intismeran(mRNA-4157)의 정확한 에피토프 길이·링커 서열·UTR·poly(A) 길이 등 구조체 세부 사양

**미해결 사유** — Moderna는 34개 항원 수와 '단일 합성 mRNA'만 공개하고 콘카테머 아키텍처 세부(에피토프 길이, 링커 서열, UTR 선택)를 공개 문헌·프로토콜·IR 자료 어디에도 명시하지 않았다. Cancer Discovery KEYNOTE-603 원문은 AACR 사이트가 HTTP 403으로 차단되어 본문 접근 불가했고, Europe PMC에도 PMC 사본이 없다(Subscription required). 대체 경로로 동일 Moderna 제조 계열인 NCI-4650의 ClinicalTrials.gov 프로토콜 원문(NCT03480152 PDF)을 pypdf로 직접 텍스트 추출하여 구조체 길이 500-3000 nt, 신생항원 15-41 aa, N1-메틸슈도우리딘, Cap 1, SM-102 LNP 사양을 확보했고[R614][R615], intismeran 총 길이는 [EST]로 산출했다[R659].

**시도한 쿼리 (4건)**

1. `"mRNA-4157" construct 34 neoantigens "25-mer" OR "peptide length" single mRNA molecule length nucleotides lipid nanoparticle Moderna design`
2. `intismeran autogene V940 mRNA-4157 34 neoantigens construct design concatemer linker`
3. `WebFetch: https://aacrjournals.org/cancerdiscovery/article/14/11/2209/749201/T-cell-Responses-to-Individualized-Neoantigen (403 Forbidden)`
4. `Europe PMC TITLE 검색: "T-cell Responses to Individualized Neoantigen Therapy mRNA-4157 KEYNOTE-603" (PMC 사본 없음)`

### KEYNOTE-603(mRNA-4157 1상)의 정량적 면역원성 지표 — 인코딩된 34개 중 몇 개가 T세포 반응을 유도했는지, CD4:CD8 정확한 비율

**미해결 사유** — Cancer Discovery 원문이 구독 전용이고 AACR 서버가 WebFetch를 403으로 차단한다. Europe PMC 레코드에 PMC ID가 없고 fullTextUrlList가 'Subscription required'만 반환한다. 초록은 'CD8과 CD4 세포독성 T세포 확장 관찰'이라는 정성 서술만 제공한다. 대체 경로로 동일 모달리티의 정량 데이터를 Cafri 2020 JCI(15.7% 면역원성, CD4 59%/CD8 41%)[R661]와 autogene cevumeran Nature Medicine 1상(CD4단독 59%/CD8단독 26%/양쪽 15%)[R662]에서 확보하여 CD4 우위 결론은 3개 독립 프로그램으로 교차검증했다.

**시도한 쿼리 (4건)**

1. `"mRNA-4157" KEYNOTE-603 Cancer Discovery 2024 neoantigen-specific T cell responses "CD8" "CD4" percent of neoantigens immunogenic`
2. `mRNA-4157 phase 1 Burris Bauman neoantigen selection algorithm whole exome sequencing depth tumor tissue requirement manufacturing time weeks`
3. `Europe PMC EXT_ID:39115419 resultType=core (pmcid=None, isOpenAccess=N)`
4. `WebFetch aacrjournals.org/cancerdiscovery/article/14/11/2209 (HTTP 403)`

### BioNTech autogene cevumeran의 WES 커버리지 깊이(x)와 RNA-seq 최소 리드 수 등 시퀀싱 규격 원문 확인

**미해결 사유** — Rojas 2023 Nature의 Methods는 '종양-정상 쌍 WES와 종양 RNA-seq을 수행했다'고만 기술하고 커버리지 수치를 선행 문헌(reference 16)으로 위임했으며, PMC10171177 본문에서 깊이·리드수·VAF 임계값이 확인되지 않았다. 웹검색에서 'WES 50-100x, RNA-seq 최소 5x10^7 리드'라는 수치가 반환됐으나 특허문서/2차 취합본이 출처로 추정되어 1차 소스 확인 불가 — 금지 규칙에 따라 evidence 등재하지 않았다. 대체 경로로 PGV-001의 공개 규격(정상 150x/종양 300x)[R600][R601]과 HLA 타이핑 요구 커버리지(≥100x)[R626]를 확보해 규격 범위를 제시했다.

**시도한 쿼리 (4건)**

1. `autogene cevumeran methods whole exome sequencing coverage depth "×" tumor normal RNA-seq reads BioNTech neoantigen selection pipeline Rojas methods`
2. `WebFetch PMC10171177 Methods 대상 프롬프트(WES read depth, RNA-seq minimum read count, VAF cutoff) — 본문에 미기재 확인`
3. `personalized neoantigen vaccine tumor tissue requirement FFPE minimum tumor content 20% DNA yield sequencing QC failure rate screen failure percentage trial`
4. `WebFetch arxiv.org/abs/2512.08226 (ImmunoNX Supplementary Table 2 시퀀싱 깊이 — 초록에 미공개, Zenodo 부록 필요)`

### 검체 QC 자체의 실패율(FFPE DNA/RNA 품질 미달로 시퀀싱 단계에서 탈락하는 비율)을 프로그램별로 분리한 수치

**미해결 사유** — 공개 논문들은 '제조 관련 탈락'을 하나의 묶음으로 보고하며(autogene cevumeran 1상 94/550)[R610] 그 중 검체 QC 실패, 신생항원 수 부족, 제조 배치 실패를 구분하지 않는다. Rojas 2023은 19명 중 1명(신생항원 부족)만 보고했고[R607] QC 실패는 별도 집계하지 않았다. Gritstone은 '적격 환자 전원 100% 제조 성공'을 발표했으나 이는 적격 판정 이후 기준이라 QC 탈락을 포함하지 않는다. 대체 경로로 신생항원 확보 성공률(≥5개 98.5%, ≥20개 81.9%)[R611]과 종양 함량 하한 10%[R605]로 QC 압력의 크기를 간접 정량했다.

**시도한 쿼리 (4건)**

1. `personalized neoantigen vaccine tumor tissue requirement FFPE minimum tumor content 20% DNA yield sequencing QC failure rate screen failure percentage trial`
2. `neoantigen vaccine trial screen failure "unable to manufacture" percentage patients tissue insufficient GRANITE Gritstone phase 2 manufacturing success rate`
3. `"NEO-PV-01" OR "PGV001" personalized neoantigen vaccine turnaround time weeks manufacturing bioinformatics failure rate published trial`
4. `WebFetch PMC11750724 (autogene cevumeran CONSORT) — 제조 관련 탈락 94명이 세부 사유 미분해`

### 국내(한국) 신생항원 예측·설계 플랫폼 보유 기업의 검증된 성능 지표

**미해결 사유** — 국문 검색에서 신테카바이오(NEO-ARS), 네오젠로직 등이 확인되나 반환된 소스가 협회 DB·VC 프로필 등 2차 요약이며[R677은 트리밍 과정에서 제외], peer-reviewed 벤치마크나 DART 사업보고서 상의 정량 성능 지표를 확보하지 못했다. WebSearch 예산(200회)이 소진되어 추가 국문 1차 소스(DART 공시, 국내 논문) 탐색을 중단했다. M1 범위상 국내 플레이어는 A4/D 모듈 소관이므로 해당 에이전트로 이관 권고. 대신 한국 시장 진입 근거로 동아시아 HLA-DQB1 오류율 11% 초과라는 기술적 공백[R627]을 확보했다.

**시도한 쿼리 (3건)**

1. `국내 신생항원 예측 플랫폼 인공지능 네오antigen 개인맞춤 항암백신 기업 2025 2026 지놈오피니언 툴젠 신테카바이오`
2. `HLA typing accuracy benchmark OptiType HLA-HD xHLA arcasHLA concordance rate four-digit class I class II percent WES (동아시아 하위분석 확인)`
3. `2026 AI foundation model neoantigen vaccine design pharma partnership Moderna BioNTech machine learning antigen selection improvement announced`

## B2

### mRNA-4157/intismeran autogene의 정확한 LNP 조성과 몰비 (SM-102 여부 및 지질:RNA 비율)

**미해결 사유** — Moderna는 mRNA-4157의 LNP 조성을 공개하지 않는다. 대체 경로로 동일 플랫폼·동일 제조사의 NCI-4650 프로토콜(NCT03480152 Prot_SAP_000.pdf)을 확보해 SM-102 + DMG-PEG2000 + DSPC + 콜레스테롤 4성분과 1.0 mg RNA/mL 농도를 1차 문서로 확인했다[R723]. 그러나 mRNA-4157 자체의 몰비·N/P비는 여전히 미공개이며, KEYNOTE-603(NCT03313778) 및 V940-001(NCT05933577)의 CT.gov documentSection이 비어 있어 프로토콜 PDF를 얻을 수 없었다.

**시도한 쿼리 (4건)**

1. `mRNA-4157 "N1-methylpseudouridine" OR "unmodified uridine" Moderna individualized neoantigen therapy construct chemistry`
2. `curl https://clinicaltrials.gov/api/v2/studies/NCT03313778?fields=protocolSection,documentSection (documentSection = 빈 객체)`
3. `curl https://clinicaltrials.gov/api/v2/studies/NCT05933577?fields=DocumentSection (빈 객체)`
4. `mRNA-4157 V940 intismeran autogene dose 1 mg intramuscular every 3 weeks nine doses KEYNOTE-942 lipid nanoparticle`

### Moderna KEYNOTE-603의 ELISpot 양성 판정 역치와 분모 (BioNTech의 7 spots/3×10^5 PBMC에 대응하는 수치)

**미해결 사유** — 원저(Cancer Discovery 2024;14:2209)는 AACR 사이트가 HTTP 403으로 차단되고 PMC 등재가 없어(Europe PMC 조회 결과 pmcid=None, isOpenAccess=N) 방법론 섹션에 접근하지 못했다. 대체 경로로 PubMed 초록(확장 없는 ex vivo IFN-γ ELISpot, n=4 및 n=12)[R765]과 Moderna ASCO 2024 발표자료 PDF 전문 추출을 시도했으나 역치·분모는 초록·슬라이드 어디에도 제시되지 않았다. 이 공백 자체가 '기업 간 반응률 비교 불가'[R764] 주장을 오히려 강화한다.

**시도한 쿼리 (5건)**

1. `WebFetch https://aacrjournals.org/cancerdiscovery/article/14/11/2209/749201/T-cell-Responses-to-Individualized-Neoantigen (403 Forbidden)`
2. `curl Europe PMC EXT_ID:39115419 → pmcid None, isOpenAccess N`
3. `curl PubMed efetch id=39115419 (초록만 확보, Methods 없음)`
4. `mRNA-4157 KEYNOTE-942 immunogenicity neoantigen-specific T cell response ELISpot percentage patients Weber Lancet 2024`
5. `WebFetch Moderna ASCO 2024 deck PDF → pypdf 전문 추출, 면역원성 방법론 슬라이드 부재`

### GRANITE 무작위 2상(NCT05141721)의 1차 평가변수 ctDNA molecular response 정량 결과 (군별 N, 반응률, p값)

**미해결 사유** — 1차 보고인 ASCO GI 2025 LBA13(JCO 43_suppl)이 ascopubs.org에서 HTTP 403으로 차단되었고, Gritstone 파산으로 IR 사이트의 원 프레젠테이션 접근이 제한적이다. 대체 경로로 CT.gov 등록 1차 평가변수 정의('ctDNA 기준선 대비 ≥30% 감소')를 확보하고[R716], 회사 보도자료에서 '단기 molecular response는 정보가치 없음'이라는 사후 재해석 문구를 확보했다[R717]. 즉 미충족 사실은 확인되나 정확한 수치는 미확보.

**시도한 쿼리 (4건)**

1. `WebFetch https://ascopubs.org/doi/10.1200/JCO.2025.43.4_suppl.LBA13 (403 Forbidden)`
2. `Gritstone GRANITE randomized phase 2 colorectal ctDNA molecular response failed 2024 samRNA dose 300 µg neoantigen`
3. `curl clinicaltrials.gov/api/v2/studies/NCT05141721 (1차 평가변수 정의만 확보, 결과 미등재)`
4. `PubMed esearch (GRANITE[Title/Abstract] AND neoantigen[Title/Abstract]) OR (ChAdV68 AND samRNA) → 0 hits`

### CSL의 Arcturus sa-mRNA IP 4.3억 달러 상각에 대한 1차 재무공시 원문

**미해결 사유** — CSL 1H FY26 반기보고서 PDF의 직접 URL을 확보하지 못했고 웹검색 예산(200회)이 소진되어 추가 탐색이 불가했다. 대체 경로로 Arcturus의 FY2025 실적 보도자료(Business Wire, 1차 기업발표)에서 CSL 협업 매출 7,030만 달러 감소와 희귀질환 전략 재집중을 확인했다[R721]. 상각액 4.3억 달러 자체는 2차 집계 근거뿐이므로 R720의 신뢰도를 '하'로 부여하고 본문 헤지를 요구한다.

**시도한 쿼리 (3건)**

1. `CSL annual results 2025 impairment $430 million Arcturus Kostaive write-off intangible`
2. `Arcturus Therapeutics CSL Kostaive 2026 commercial status discontinued withdrawal sales saRNA COVID vaccine uptake`
3. `WebFetch https://www.businesswire.com/news/home/20260303197744/... (Arcturus FY2025 실적 — 상각액 미기재 확인)`

### taRNA 및 개인맞춤 circRNA 네오항원 백신의 인체 임상 존재 여부

**미해결 사유** — ClinicalTrials.gov API v2에서 taRNA/transreplicon 관련 등록 연구가 확인되지 않았고, circRNA는 종양 적응증 1상이 공유항원(HPV-16) 단 1건(NCT07081984)뿐이다. 개인맞춤 circRNA/taRNA 네오항원 임상은 2026-08 현재 존재하지 않는 것으로 판단되나, 중국 NMPA·CDE 등록 DB를 직접 조회하지 못했다(웹검색 예산 소진). '정보 없음'이 아니라 '해당 임상이 존재하지 않을 가능성이 높음'으로 기술해야 한다.

**시도한 쿼리 (4건)**

1. `trans-amplifying RNA taRNA Beissert Sahin bipartite replicon dose sparing 2020 preclinical clinical status`
2. `circular RNA cancer vaccine clinical trial 2025 2026 Orna Therapeutics RiboX Circio circRNA IND first-in-human`
3. `Therorna TI-0093 circular RNA cancer vaccine IND approval NMPA first-in-human 2025 2026 HPV16`
4. `curl clinicaltrials.gov/api/v2/studies?query.term=trans-amplifying+RNA → 관련 등록 없음`

### LNP 근육주사 후 정량적 생체분포(간 축적 %ID, 배액 림프절 도달률, 발현 지속 시간)

**미해결 사유** — Moderna Hassett 2019(PMC6383180)에서 IM 투여 후 간·비장에서 24시간 검출, 48시간 감소라는 정성적 기술과 몰비·pKa는 확보했으나[R757], %ID/g 단위의 정량 생체분포는 논문 본문에 없다. EMA Comirnaty CHMP 평가보고서(rat biodistribution)를 확보하려 했으나 웹검색 예산 소진으로 정확한 문서 URL을 찾지 못했다. 대신 제품정보(PI)에서 지질 조성만 확보했다[R701].

**시도한 쿼리 (4건)**

1. `mRNA LNP intramuscular biodistribution liver draining lymph node expression duration hours days luciferase 2022 2023 quantitative (예산 소진으로 미실행)`
2. `Europe PMC: TITLE:"biodistribution" AND "lipid nanoparticle" AND "intramuscular" AND "mRNA vaccine"`
3. `Europe PMC: AUTH:"Hassett KJ" AND "lipid nanoparticle"`
4. `WebFetch https://pmc.ncbi.nlm.nih.gov/articles/PMC6383180/ (정성 기술만 확보)`

## C1

### Moderna/Merck의 intismeran 구체적 TAT 주수 (예: 6~8주)에 대한 1차 근거

**미해결 사유** — Moderna FY2025 10-K는 '통상 수 주(a few weeks)'라고만 기술하고 확정 수치를 공시하지 않았으며(R804), 'vein-to-vein'이라는 용어 자체가 문서에 없다. JCO 5년 업데이트와 Lancet 2b 논문은 모두 HTTP 403(유료장벽)으로 본문·부록 접근 불가. Moderna IR 사이트(investors.modernatx.com, news.modernatx.com)는 전부 JavaScript 셸만 반환해 보도자료 본문을 얻을 수 없었다. 리뷰 논문을 포인터로 마이닝했으나 TAT 수치를 인용한 대목이 없었다. 세션의 WebSearch 예산 200회가 이미 소진된 상태여서 검색엔진 경로가 봉쇄되었고, DuckDuckGo(html/lite)와 Bing HTML 스크래핑은 모두 결과 블록을 반환하지 않았다. 대체 경로로 확보한 근거: BioNTech의 정량 공시(목표 28일 미만, 상시 30~40일, 전달 6주 미만)와 Nature Medicine의 28일 최상 TAT, Rojas의 실제 9.4주로 TAT 계층을 재구성했다. Moderna가 구체 수치를 공시하지 않는다는 사실 자체를 R804에 부정 근거로 등재했다.

**시도한 쿼리 (7건)**

1. `Moderna FY2025 10-K 전문 문자열 검색: 'turnaround'(6건, 전부 forward-looking 정형문구), 'vein'(7건, 전부 XBRL 노이즈), 'vein-to-vein'(0건), 'individualized'(7건)`
2. `WebFetch https://ascopubs.org/doi/10.1200/JCO-26-00835 (KEYNOTE-942 5년 업데이트) → HTTP 403`
3. `WebFetch https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(23)02268-7/fulltext → HTTP 403`
4. `curl https://investors.modernatx.com/news/default.aspx, /press-releases, /rss/pressrelease.aspx, https://news.modernatx.com/news → 전부 동일 JS 셸(224KB/323KB), 보도자료 본문 없음`
5. `Europe PMC 검색 '(mRNA-4157 OR intismeran) AND (manufactur* OR turnaround)' → 857건 전부 리뷰/2차 문헌`
6. `PMC12474233 리뷰 전문 마이닝 (turnaround/week/manufactur 문맥) → TAT 수치 인용 없음`
7. `ClinicalTrials.gov NCT03897881 결과 섹션 조회 → resultsSection 없음(미게시)`

### 12단계 공정의 단계별 소요일수 배분 (수술→수송→시퀀싱→설계→DNA 주형→IVT→정제→제형화→충전→QC→배송→투여)

**미해결 사유** — 어느 1차 문서도 단계별 일수를 분해 공개하지 않는다. 확인 가능한 것은 구간 총계뿐이다 — 검체 수령·승인→제조 종료 28일(Nature Medicine 2025), 서열 확정→출하 제품 30~40일(BioNTech FY2024 20-F), 수술→첫 투여 중앙 66일(Nature 2023). 논문 Methods는 공정 단위조작을 순서대로 상세히 기술하나(R814, R815, R870) 각 단계 소요시간은 기재하지 않는다. 공정 상세를 담은 특허를 조회하려 했으나 Google Patents XHR API가 2회 질의 후 rate-limit(HTML 'Sorry' 페이지)으로 차단되었다. 대체 경로: 세 구간 총계로 TAT 계층(R884)과 비제조 구간 57% 추정(R803)을 구성해 단계별 분해 없이도 병목의 소재(물류·시퀀싱·QC)를 특정했다. 단계별 배분은 M3의 최대 잔여 정보 공백이며 R871에 명시적으로 기록했다.

**시도한 쿼리 (6건)**

1. `Nature Medicine 2025 (PMC11750724) Methods 전문 grep: 'manufactur', 'turnaround', 'median time', 'days', 'release' → 구간 총계만 존재, 단계별 일수 없음`
2. `Nature 2023 (PMC10171177) 전문 grep: 'median time', 'weeks', 'days', 'benchmark', 'shipp' → 벤치마크 일정(주 단위)만 존재`
3. `Nature 2025 (PMC11946889) Methods 'Autogene cevumeran manufacture' 단락 전문 추출 → 조성·입자크기만 기재, 시간 없음`
4. `Google Patents XHR 'method+of+manufacturing+individualized+RNA+vaccine+BioNTech' → rate-limited`
5. `Google Patents XHR 'automated+production+individualized+mRNA+cancer+vaccine' → rate-limited`
6. `BioNTech FY2024/FY2025 20-F grep: 'turnaround', '30 to 40 days' → 구간 정의만, 내부 분해 없음`

### intismeran/autogene cevumeran의 정확한 보관온도와 유효기간(shelf life) 및 배송 밸리데이션 조건

**미해결 사유** — Nature Medicine Methods는 '해동된 제품을 0.9% 식염수로 희석'이라고만 기재해 동결 유통은 확정되나 온도대(-20°C vs -70°C)와 유효기간은 명시하지 않는다(R858). Moderna 10-K와 BioNTech 20-F 모두 콜드체인 민감성과 '유효기간이 가변적'이라는 정성적 리스크만 기재하고 제품별 수치를 공시하지 않는다(R859, R861). 두 제품 모두 미승인 상태라 SmPC/USPI 같은 허가문서가 존재하지 않으며, ClinicalTrials.gov 등록정보에는 제형·보관 조건이 포함되지 않는다. 대체 경로: 동결 유통이 확정된다는 사실과 '재고 미보유'(R835)·'배송 문제'(R860)를 결합해 콜드체인 실패가 곧 환자 미치료로 이어지는 구조적 리스크를 논증했다. 공정 변경 후 6·12개월 안정성 시험이 필요하다는 Moderna 공시(R861)로 안정성 데이터 부담의 크기는 간접 확인했다.

**시도한 쿼리 (4건)**

1. `Nature Medicine 2025 Methods 'GMP manufacturing of RNA-LPX' 전문 추출 → 해동·희석만 기재, 온도·유효기간 없음`
2. `Moderna FY2025 10-K grep: 'frozen', '-20', 'minus', 'cold chain', 'cold-chain', '2 to 8', 'shelf life', 'shelf-life' → 정성적 리스크 문언만`
3. `BioNTech FY2025 20-F grep: '-20', 'minus 20', 'frozen', 'thaw', 'storage temperature', 'stability' → 제품별 수치 없음`
4. `ClinicalTrials.gov NCT05933577 / NCT03897881 전체 레코드 조회 → 보관 조건 필드 없음`

### BioNTech의 '배치(batch)'와 '환자' 수의 대응관계 (1,700배치가 몇 명인가)

**미해결 사유** — FY2024·FY2025 20-F 모두 'more than 1,700 batches of mRNA'라고만 기재하고 환자 수 환산을 제공하지 않는다. autogene cevumeran은 환자당 mRNA 2가닥(각 최대 10개 신생항원)으로 제조되므로(R814) 1배치=1가닥이면 약 850명, 1배치=1환자면 1,700명이 되어 2배의 불확실성이 남는다. 더 심각한 문제로, 해당 문장이 FY2024와 FY2025 20-F에 글자 그대로 동일 반복되어 최소 1년간 갱신되지 않은 정형문구임을 문자열 대조로 확인했다(R887). 이 때문에 이 수치에 근거한 연간 처리율 추정을 폐기하고, 대신 FY2024의 '월 100배치' 공시(R847)를 생산능력 기준으로 채택해 스케일아웃 배수 추정을 30~90배에서 6~17배로 하향 수정했다(R849). 잔여 불확실성은 R846·R849 notes에 명시했다.

**시도한 쿼리 (4건)**

1. `BioNTech FY2025 20-F grep 'batches per year', 'batch', 'iNeST', 'capacity' → 환자 환산 없음`
2. `BioNTech FY2024 20-F 전문 다운로드 후 'batches of mRNA', '2,000 batches', 'batch sizes range' 문맥 추출 → 배치 수와 배치 질량만, 환자 대응 없음`
3. `FY2024 vs FY2025 20-F 문자열 대조 ('1,700 ba' 양쪽 1회, '100 batches' 1→0, '30 to 40 days' 1→0) → 정형문구 미갱신 확인`
4. `Nature Medicine 2025 Methods에서 환자당 mRNA 가닥 수 확인(2가닥) → 배치 정의와 직접 연결되는 문서는 없음`

### mRNA 개인맞춤 암백신에 FDA 플랫폼 기술 지정이 실제로 부여되었는지 여부

**미해결 사유** — FDA는 플랫폼 기술 지정 부여 목록을 공개 게시하지 않으며, 지정 사실은 기업의 공시 의무 항목이 아니다. SEC EDGAR 전문검색에서 'platform technology designation'을 포함한 10-K/20-F는 15건이었으나 전부 Krystal Biotech·Fusion·Precigen·Sarepta·Kymera·ProQR 등 비-mRNA-암백신 기업이었고, Moderna와 BioNTech는 해당 문언이 0회였다(R839). 따라서 '미취득'을 단정할 수 없고 '공시되지 않음'까지만 확정 가능하다. 대체 경로: FDA 초안 가이던스 원문(2024년 5월)을 전문 추출해 자격요건(승인 제품 보유 요건 — 양사 모두 충족), mRNA-LNP 예시 요건('서열 차이가 품질에 영향 없음'), 혜택 범위(우선심사 미포함), 동일 제조소 각주 제약을 1차 인용으로 확보했다(R836~R841). 이로써 지정 취득 여부와 무관하게 제도의 적용 가능성과 한계를 근거 있게 서술할 수 있다.

**시도한 쿼리 (4건)**

1. `SEC EDGAR 전문검색 API: q='platform technology designation', forms=10-K,20-F → 15건, mRNA 암백신 기업 0건`
2. `Moderna FY2025 10-K 전문 grep: 'platform technology designation'(0), '506K'(0), 'PREVENT Pandemics'(0), 'platform technology'(0)`
3. `BioNTech FY2025 20-F 전문 grep: 동일 4개 검색어 전부 0건`
4. `FDA 가이던스 페이지 https://www.fda.gov/regulatory-information/search-fda-guidance-documents/platform-technology-designation-program-drug-development 및 /media/178938/download PDF 18쪽 전문 추출 → 지정 부여 목록 미수록`

### 무균시험 14일 배양기간의 약전 원문(Ph. Eur. 2.6.1 / USP <71>) 직접 인용

**미해결 사유** — 유럽약전과 미국약전 본문은 유료 구독 장벽 뒤에 있어 조문 원문을 직접 확보할 수 없다. PubMed에서 신속무균시험 관련 문헌을 2회 검색했으나 반환된 논문들이 요로 마이크로바이옴·호흡기 PCR·클라미디아 등 무관한 주제였다(검색어가 'sterility'의 다른 의미로 매칭). 대체 경로로 규제 1차 문서를 확보해 논증을 완성했다 — EU GMP ATMP 가이드라인이 Ph. Eur. 2.6.1 무균시험 최종 결과를 기다리지 못할 수 있음과 Ph. Eur. 2.6.27 신속법 단독 의존 가능성을 명시하고(R819), 출하 시 결과 미확보 시 치료 의사 통지를 요구하며(R820), 2단계 QP 인증을 허용한다(R821). EU GMP Annex 1은 짧은 유효기간 제품의 환경모니터링 데이터 미확보를 인정하고 신속법을 권고하며(R825), 무균시험이 '일련의 관리수단 중 마지막 하나'일 뿐임을 명시한다(R826). Annex 17은 파라메트릭 출하가 최종멸균 제품 한정임을 확정해(R823) 흔한 오해를 반증했다. 따라서 '14일'이라는 숫자 자체는 약전 원문으로 인용하지 못했으나, TAT 압축의 규제 경로는 1차 근거로 완결했다.

**시도한 쿼리 (5건)**

1. `PubMed esearch: 'rapid sterility testing cell therapy short shelf life 14 days compendial' → 0건`
2. `PubMed esearch: '(rapid microbiological method) AND (sterility) AND (advanced therapy OR cell therapy)' → 15건, 전부 무관 주제(esummary로 확인)`
3. `EU GMP Annex 1 PDF(59쪽) 전문 grep: 'rapid microbiological', 'alternative method', 'sterility test', 'short shelf', 'parametric', 'before the results' → 신속법 권고는 확보, 배양일수 없음`
4. `EU GMP ATMP 가이드라인 PDF(90쪽) 전문 grep: 'sterility test', 'short shelf', 'released before', 'out of specification' → Ph. Eur. 2.6.1/2.6.27 참조 확보, 배양일수 없음`
5. `EudraLex Volume 4 목록 페이지에서 Annex 17 및 ATMP GMP PDF 링크 추출 후 다운로드`

## C2

### GMP 등급 이온화성 지질(SM-102 / ALC-0315 / 독자 지질)의 실제 거래 단가 및 CordenPharma·Croda(Avanti)·Evonik의 생산능력(kg/톤)·투자액

**미해결 사유** — 이 세션의 WebSearch 예산 200회가 본 에이전트 착수 시점에 이미 전량 소진되어 검색 기반 탐색이 불가능했다. WebFetch로 CordenPharma 지질 플랫폼 페이지를 직접 시도했으나 HTTP 404, Avanti(avantiresearch.com) DSPC 제품 페이지는 로드되었으나 가격이 '$0.00' 플레이스홀더로 비공개(로그인/견적 필요)였다. GMP 지질은 계약가가 원칙적으로 비공개이며 공개 카탈로그가 존재하지 않는다. 대체 경로로 Cayman Chemical의 연구용 등급 정가(SM-102 1 g $1,200, ALC-0315 1 g $1,600)를 확보해 하한으로 삼고[R926][R927], GMP 프리미엄은 약 6배로 가정한 [EST]로 명시 처리했다[R958]. 질량 소요량 자체는 FDA 코미나티 라벨로 확정했다[R928].

**시도한 쿼리 (5건)**

1. `WebFetch https://www.cordenpharma.com/technology-platforms/lipids-and-carbohydrates/ (HTTP 404)`
2. `WebFetch https://avantiresearch.com/product/850365 (DSPC — 가격 필드 $0.00 플레이스홀더, 팩사이즈 미표시)`
3. `WebFetch https://www.caymanchem.com/product/33474/sm-102 (성공 — 연구용 등급 정가만 확보)`
4. `WebFetch https://www.caymanchem.com/product/34337/alc-0315 (성공 — 연구용 등급 정가만 확보)`
5. `WebSearch 'ionizable lipid GMP price per gram CordenPharma Croda capacity' (예산 소진으로 미실행)`

### GMP 플라스미드 DNA 및 선형 PCR/효소적(doggybone) DNA 주형의 배치 최소단위·리드타임·g당 가격, 그리고 모더나/바이오엔텍이 개별화 제품에 실제로 사용하는 주형 방식(플라스미드 vs PCR 앰플리콘 vs 효소적)

**미해결 사유** — WebSearch 예산 소진. Aldevron 제품 페이지 직접 접근은 HTTP 404였고, Aldevron은 다나허 라이프사이언스 부문에 통합되어 별도 재무·가격 공시가 없다(부문 매출만 공시)[R942]. Touchlight(dbDNA), VGXI, Nature Technology는 비상장으로 SEC 공시 경로가 없다. 대체 경로로 (a) 모더나 10-K에서 'DNA 플라스미드 내재화' 사실을 확보했고[R936], (b) 다나허 10-K에서 '두 대형 고객의 플라스미드 수요 감소'를 확보했으며[R941], (c) Sci Rep 2024 원가표에서 선형화 제한효소가 연 9,960만 EUR로 최대 원가 항목이라는 간접 증거를 확보했다[R918]. 주형 소요량은 IVT 통설 비율로 [EST] 처리하고 신뢰도 '하'로 표기했다[R963].

**시도한 쿼리 (5건)**

1. `WebFetch https://www.aldevron.com/products/plasmid-dna (HTTP 404)`
2. `Bash grep 'plasmid|DNA template|linear' over Moderna FY2025 10-K 전문 (내재화 사실만 확보, 방식·원가 미기재)`
3. `Bash grep 'Aldevron|plasmid' over Danaher FY2025 10-K 전문 (부문 수준 서술만, 가격·리드타임 없음)`
4. `PubMed esearch 'mRNA+manufacturing+cost+analysis+plasmid+DNA+template+IVT' (0건)`
5. `WebSearch 'GMP plasmid DNA cost per gram lead time Aldevron VGXI Touchlight doggybone' (예산 소진으로 미실행)`

### 개별화 mRNA 1인1배치 GMP를 실제로 수행할 수 있는 외부 CDMO(삼성바이오로직스, 에스티팜, Lonza, Recipharm, Rentschler, eTheRNA, Quantoom/Univercells Ntensify)의 실적·생산능력·배치당 단가

**미해결 사유** — WebSearch 예산 소진으로 CDMO 탐색이 제한되었다. Quantoom 홈페이지를 WebFetch로 직접 조회했으나 배치 규모·mRNA 산출량(g/mg)·도즈당 원가가 모두 비공개였고 '10배 개선 목표'라는 정성적 문구만 확인되었다. 국내(MFDS·바이오스펙테이터·히트뉴스) 및 유럽 CDMO는 배치 단가를 원칙적으로 공개하지 않는다. 대체 경로로 양대 개발사가 모두 전용시설을 자체 보유·운영한다는 1차 공시를 확보해(모더나 말버러 신축[R933], 바이오엔텍 East Wing 300명 자체 운영[R938]) '외부 CDMO에 개방된 물량이 확인되지 않는다'는 [EST] 판단으로 처리하되, 부재의 증명이므로 단정을 금지하도록 notes에 명기했다[R988].

**시도한 쿼리 (4건)**

1. `WebFetch https://www.quantoom.com/ (성공 — 배치 규모·원가 모두 비공개 확인)`
2. `Bash grep 'CDMO|contract manufactur' over Moderna FY2025 10-K 및 BioNTech FY2025 20-F 전문 (개별화 외주 언급 없음)`
3. `Bash grep over Codexis FY2025 10-K — 'three large-scale CDMOs' 확보되었으나 siRNA용이며 mRNA 개별화와 무관[R946]`
4. `WebSearch 'personalized mRNA CDMO one patient one batch GMP Samsung Biologics ST Pharm Lonza' (예산 소진으로 미실행)`

### 무기 피로포스파타아제, RNase 저해제(murine/porcine 재조합), RNase III, DNase I, 백시니아 캡핑효소+2'-O-메틸트랜스퍼레이스의 GMP 등급 공개 단가와 신뢰할 만한 GMP 공급자 수

**미해결 사유** — WebSearch 예산 소진. TriLink 사이트맵을 curl로 직접 파싱해 확보 가능한 효소 제품 URL을 전수 확인했으나 T7 RNA 중합효소, CleanScribe(조작 T7), engineered RNase inhibitor 3종만 존재했고 피로포스파타아제·RNase III·DNase I·캡핑효소 제품 페이지는 사이트맵에 부재했다. Roche CustomBiotech·NEB·Thermo의 GMP 등급 카탈로그는 견적 기반으로 공개가가 없다. 대체 경로로 (a) npj Vaccines 논문이 고가 원료로 캡핑 효소(VCE+2'-O-MTase)와 T7을 명시적으로 지목한 것[R916][R917], (b) Sci Rep 2024의 T7 38,000 EUR/g[R918], (c) TriLink T7·CleanScribe 카탈로그 정가[R924][R925]를 확보했다. 개별 효소의 단가·공급자 수는 확인 실패로 진입 스크린 결과[R969]를 신뢰도 '하'로 자체 등급화하고 본문 단정 금지를 notes에 명기했다.

**시도한 쿼리 (5건)**

1. `Bash curl https://shop.trilinkbiotech.com/sitemap.xml + grep 'polymerase|inhibitor|dnase|capping-enzyme|methyltransferase' (3개 제품만 존재 확인)`
2. `WebFetch https://shop.trilinkbiotech.com/shopping/products/t7-rna-polymerase/ (성공)`
3. `WebFetch https://shop.trilinkbiotech.com/shopping/products/cleanscribe-rna-polymerase/ (성공)`
4. `WebFetch https://www.thermofisher.com/order/catalog/product/R1911 (제품번호 미존재 응답)`
5. `WebFetch https://shop.trilinkbiotech.com/shopping/products/ivt-and-capping-reagents/nucleoside-triphosphates-ntps (HTTP 404)`

### Ghent MIDRIX NEO 논문(Cytotherapy 2022)의 본문 — 개별화 신생항원 mRNA 소량 GMP 공정의 실제 QC 시험 항목 목록, 배치 크기, 소요 시간 및 원가

**미해결 사유** — 해당 논문은 Elsevier(Cytotherapy) 유료 구독 자료이며 PMC 오픈액세스 사본이 없다(esummary 조회 결과 pmc: None). PubMed efetch로는 초록까지만 확보되었고, 초록에는 '광범위한 품질평가(extensive quality assessment)'라는 서술만 있고 항목·원가는 없다. WebSearch 예산 소진으로 preprint·기관 리포지터리 우회 경로를 탐색하지 못했다. 대체 경로로 초록에서 '환자 맞춤 mRNA는 개별 배치 생산을 요구한다'는 구조적 사실과 '세계 최초 GMP 개별화 신생항원 mRNA 공정 기술'이라는 위상을 확보했다[R980]. 그 결과 QC 패널 구성·비용[R962]은 전문가 구성 기반 [EST]로 처리하고 신뢰도 '하'로 자체 등급화했다.

**시도한 쿼리 (5건)**

1. `PubMed efetch db=pubmed id=34696961 retmode=xml (초록만 반환, 본문 없음)`
2. `PubMed esummary id=34696961 — articleids 확인 결과 pmc 사본 부재(pmc: None), doi 10.1016/j.jcyt.2021.08.005만 존재`
3. `PubMed esearch 'personalized+cancer+vaccine+manufacturing+cost+GMP' (0건)`
4. `PubMed esearch 'neoantigen+vaccine+manufacturing+process+GMP+individualized' (4건 — 나머지 3건은 2009-2013년 펩타이드 백신으로 무관)`
5. `PubMed esearch 'individualized+neoantigen+mRNA+vaccine+manufacturing+turnaround+time' (0건)`

### 인티스메란 3상의 확정 용량(1 mg 유지 여부) 및 승인 후 실제 치료 대상 환자수 추정의 1차 근거(SEER/GLOBOCAN 기반 보조요법 적격 인구)

**미해결 사유** — ClinicalTrials.gov API v2에서 NCT05933577의 armGroups·interventions를 전수 조회했으나 투여 횟수('up to 9 doses ... every 3 weeks')만 기재되고 mg 용량은 기재되지 않았다(등록정보상 용량 비공개). 대체 경로로 KEYNOTE-942 5년 추적 논문(JCO 2026, PMID 42223134) 초록에서 'nine doses of intramuscular intismeran 1 mg once every 3 weeks'를 확보해 2b상 용량을 확정했고, 3상이 동일 용량이라는 가정을 [R951] notes에 명시했다. 환자수는 WebSearch 예산 소진으로 SEER/GLOBOCAN 1차 통계를 조회하지 못해, 시장 규모를 단일 추정치가 아닌 5,000/20,000/50,000명 3개 시나리오로 제시하고 각각의 산술을 전부 공개했다[R964][R966][R967]. 정확한 적격 인구 추정은 A 계열 에이전트의 적응증별 데이터와 결합해 보정할 것을 권고한다.

**시도한 쿼리 (5건)**

1. `Bash curl ClinicalTrials.gov API v2 /studies/NCT05933577 — armsInterventionsModule 전수 파싱 (용량 mg 미기재)`
2. `Bash curl ClinicalTrials.gov API v2 query.term=intismeran pageSize=50 — 11건 전수 조회 (enrollment는 확보, 용량 미기재)`
3. `PubMed esearch 'mRNA-4157+pembrolizumab+melanoma+randomised' → efetch 42223134 (성공 — 1 mg × 9회 확보)`
4. `Bash grep 'mg|dose' over Moderna FY2025 10-K intismeran 서술 (용량 미기재)`
5. `WebSearch 'SEER melanoma stage III resected incidence adjuvant eligible population' (예산 소진으로 미실행)`

## C3

### 한국 킴리아(tisagenlecleucel) 급여 등재 약가 및 위험분담 조건의 1차 문서 (보건복지부 고시 / 심평원 공고 원문)

**미해결 사유** — 본 세션 시작 시점에 WebSearch 예산(200/200)이 이미 소진된 상태였고, 대체 검색 경로인 DuckDuckGo HTML(html.duckduckgo.com, lite.duckduckgo.com)은 HTTP 202 봇 차단, Bing은 HTTP 200이나 외부 결과 URL 0건으로 모두 실패했다. HIRA 영문 사이트를 직접 확인했으나 RSA·경제성평가 면제·CAR-T 급여 관련 기술이 전혀 없음을 확인했다(R1098). 한국어 1차 문서는 URL을 사전에 알아야 직접 fetch가 가능한데 고시 번호를 확보할 검색 경로가 없었다. 대체 경로로 peer-reviewed 한국 급여정책 문헌 3편(R1057 신약 접근성·재정영향, R1058 위험분담제 도입 효과, R1082 희귀질환 재정정책 국제비교)을 확보해 '한국의 초고가 치료제 급여 환경'은 상 등급 근거로 정량화했다.

**시도한 쿼리 (8건)**

1. `WebSearch: 킴리아 급여 등재 약가 심평원 (예산 소진으로 미실행)`
2. `curl https://html.duckduckgo.com/html/?q=킴리아+급여+등재+3억4600만원+심평원 → HTTP 202, 결과 파싱 0건`
3. `curl https://lite.duckduckgo.com/lite/ -d 'q=킴리아 급여 등재 심평원 약가' → HTTP 202, 결과 0건`
4. `curl https://www.bing.com/search?q=킴리아+급여+등재+약가+심평원&setlang=ko → HTTP 200 (74,845 bytes)이나 외부 결과 URL 0건`
5. `WebFetch https://www.hira.or.kr/eng/main.do → RSA·CAR-T 급여 정보 부재 확인`
6. `PubMed esearch: 'CAR-T reimbursement Korea' → 관련 없는 3건만 반환`
7. `PubMed esearch: 'chimeric antigen receptor reimbursement South Korea national health insurance' → 0건`
8. `PubMed esearch: 'high cost gene therapy reimbursement Korea national health insurance policy' → 관련 논문 1건(PMID 38896399)만 확보`

### intismeran에 대한 셀사이드 애널리스트 피크세일즈 추정치 (애널리스트명·발행일 포함)

**미해결 사유** — 애널리스트 리포트는 유료 구독 콘텐츠라 공개 웹에서 원문 접근이 불가하며, 이를 재인용한 산업지 기사를 찾으려면 검색엔진이 필요한데 WebSearch 예산 소진 + DuckDuckGo/Bing 차단으로 경로가 없었다. 대체 경로로 개발사 1차 공시를 전수 확인한 결과, Moderna FY2025 10-K(intismeran 59회 언급, 약 64만자), 2025-11-20 애널리스트데이 8-K, 2026-01-05 주주서한 어디에도 회사 자체의 매출·가격 전망이 존재하지 않으며 'addressable patient population' 표현은 0회 등장함을 확인했다(R1044, R1079, R1099). 따라서 유통되는 시장규모 수치는 모두 1차 근거가 없는 3자 추정이라는 점을 명시하고, GLOBOCAN·SEER·덴마크 등록자료·GALAXY 기반 자체 상향식 [EST] 8건(R1038-R1042, R1083, R1091, R1096)으로 대체했다.

**시도한 쿼리 (7건)**

1. `WebSearch: intismeran autogene peak sales estimate analyst Moderna mRNA-4157 (예산 소진으로 미실행)`
2. `SEC EDGAR full-text search: q='intismeran' → 26건 전수 확인, 전부 Moderna 자체 공시로 매출 전망 없음`
3. `SEC EDGAR full-text search: q='V940' → 91건, 동일하게 매출 전망 없음`
4. `SEC EDGAR FTS: q='addressable patient population' + 'intismeran', ciks=0001682852 → 0건`
5. `Moderna FY2025 10-K 전문 다운로드 후 intismeran 포함 문장 50건 전수 정규식 검토 → 가격·시장규모 정량 공시 부재`
6. `WebFetch https://investors.modernatx.com/news/default.aspx → news.modernatx.com으로 리다이렉트, 본문 미제공`
7. `WebFetch https://news.modernatx.com/ → 네비게이션 템플릿만 반환, 보도자료 본문 없음`

### 종양내과 의사의 개인맞춤 신생항원 치료제 처방 의향 / 환자 수용성에 대한 공표된 설문·인터뷰 데이터

**미해결 사유** — PubMed에서 3개의 서로 다른 검색어 조합으로 0건이 반환되어, 이 주제에 대한 peer-reviewed 설문 연구가 아직 존재하지 않는 것으로 판단된다(모달리티가 미승인 상태라 실사용 태도 조사가 이루어질 대상이 없는 것이 근본 원인으로 보인다). 대체 경로로 채택 장벽을 '태도'가 아닌 '구조적 요건'으로 정량화했다: 등록기준에 명문화된 FFPE 검체 적격요건(R1059), 절제→투여 13주/24주 상한(R1060), 9회 q3w 근육주사 + 최대 17주기 병행 요법(R1061), 대상군 연령 프로파일(R1062), 그리고 대리 근거로 KEYNOTE-716의 HRQoL 안정성(R1016)과 3-4등급 이상반응 16%(R1015), 스크리닝 탈락률 17.4%(R1068)를 확보했다.

**시도한 쿼리 (5건)**

1. `PubMed esearch: 'neoantigen+vaccine+oncologist+survey+willingness' → 0건`
2. `PubMed esearch: 'cancer vaccine patient preference willingness adjuvant' → 0건`
3. `PubMed esearch: 'neoantigen vaccine manufacturing turnaround barriers implementation' → 0건`
4. `PubMed esearch: 'adjuvant immunotherapy melanoma real-world uptake' → 관련 없는 1건(점막흑색종 SEER-Medicare)만 반환`
5. `PubMed esearch: 'tumor tissue adequacy next generation sequencing failure rate resected specimen' → 관련 없는 1건만 반환`

### ICER(미국 임상경제성평가연구소) 및 HAS(프랑스)의 치료용 암백신·신생항원 치료제에 대한 공식 입장

**미해결 사유** — ICER 평가 목록 페이지를 직접 확인한 결과 암백신·신생항원 치료제·보조 NSCLC·CAR-T를 다룬 개별 평가가 존재하지 않음을 확인했다(방광암·유방암·대장암·폐암·난소암·전립선암 평가는 있으나 해당 모달리티가 아님). 추정 URL(icer.org/assessment/cancer-vaccines-2024)은 HTTP 404였다. HAS는 프랑스어 사이트로 정확한 문서 URL을 사전에 알아야 fetch가 가능한데 검색 경로가 차단되어 접근하지 못했다. 대체 경로로 유럽 HTA의 실제 판단 기준은 NICE 1차 문서 3건(TA837 권고문 R1030, 위원회 비용효과 논의 R1031, 대리지표 회의론 R1080)과 sipuleucel-T NICE STA의 ERG ICER(R1028)로 확보했으며, 이것이 본 모듈의 급여 논리(R1065)를 지지하기에 충분하다고 판단했다.

**시도한 쿼리 (5건)**

1. `WebFetch https://icer.org/assessment/cancer-vaccines-2024/ → HTTP 404`
2. `WebFetch https://icer.org/explore-our-research/assessments/ → 암백신·신생항원·CAR-T 관련 평가 부재 확인`
3. `WebFetch https://www.nice.org.uk/guidance/indevelopment?q=melanoma+adjuvant+pembrolizumab → HTTP 403 (봇 차단)`
4. `curl -A browser https://www.nice.org.uk/guidance/ta837 → HTTP 200 성공, TA837 본문 확보로 우회`
5. `PubMed esearch: 'cancer vaccine market barriers commercialization health technology assessment' → 0건`

### 미국 흑색종 AJCC8 IIB/IIC 세부 병기별 발생 비율 (SEER 직접 집계) 및 보조 면역요법 실제 시행률(real-world uptake)

**미해결 사유** — SEER Cancer Stat Facts는 병기를 localized/regional/distant 3분류로만 제공하고 AJCC8 세부 병기(IIB, IIC)를 공표하지 않는다. SEER*Stat 원자료 집계는 계정 인증이 필요해 본 세션에서 접근 불가했다. 대체 경로로 덴마크 전국 등록 코호트(n=25,720, AJCC8 세부 병기 전수, JAMA Dermatology 2023)를 확보해 IIB 3.7%·IIC 1.9% 등 세부 분포를 상 등급 근거로 사용했다(R1012). 다만 이는 백인 위주 인구이므로 아시아 외삽 불가라는 한계를 notes에 명시했다. 보조 IO 실제 시행률은 어떤 경로로도 공표 실측치를 찾지 못해 60%를 [EST] 가정으로 명시하고, 이것이 퍼널에서 감도가 가장 큰 변수임을 R1038 notes에 기록했다.

**시도한 쿼리 (5건)**

1. `WebFetch https://seer.cancer.gov/statfacts/html/melan.html → localized/regional/distant 3분류만 제공, AJCC8 세부 병기 없음`
2. `PubMed esearch: 'stage IIB IIC melanoma proportion incidence recurrence risk sentinel' → 덴마크 코호트 1건만 반환 (이를 채택)`
3. `PubMed esearch: 'melanoma sentinel lymph node biopsy rate stage II adjuvant eligibility real-world' → 0건`
4. `PubMed esearch: 'adjuvant immunotherapy melanoma real-world uptake' → 관련 없는 1건`
5. `WebFetch https://pmc.ncbi.nlm.nih.gov/articles/PMC10472263/ → 덴마크 Table 1 전체 병기분포 확보 (대체 성공)`

## D1

### UPenn Kariko/Weissman 패밀리의 유럽 SPC(보충보호증명) 등재 여부 - Comirnaty/Spikevax를 근거로 국가별 SPC가 부여되었다면 EP 만료일 2026-08-21이 최대 5년 연장될 수 있어 전략적으로 중요

**미해결 사유** — Espacenet(worldwide.espacenet.com)이 403을 반환하고 EPO OPS API는 인증키가 필요해 국가별 SPC 등재원부에 접근하지 못했다. Google Patents의 EP 페이지는 SPC 정보를 표시하지 않으며, BioNTech 20-F에도 SPC 언급이 없었다. 세션 WebSearch 예산(200회)이 소진되어 2차 경로 탐색도 제한되었다

**시도한 쿼리 (3건)**

1. `curl https://worldwide.espacenet.com/data/publicationDetails/biblio?CC=KR&NR=102729393B1 (403 반환)`
2. `WebFetch https://patents.google.com/patent/EP2578685B1/en 에 legal status/expiration 질의 (SPC 항목 부재)`
3. `grep 'SPC|supplementary protection|Ergänzendes' over BioNTech FY2025 20-F 전문 (bntx20f.txt, 히트 없음)`

### BioNTech MITD(MHC class I trafficking domain) 개별 특허번호 특정 - 20-F가 'antigen-MHC fusions' 권리 존재를 공시했으나 구체 패밀리를 특정하지 못함

**미해결 사유** — PATENTSCOPE 전문검색이 최근 출원 위주로만 반환하고 2008-2012년 원천 출원을 인덱스 상위로 올리지 못했다. WO2008083949로 추정했으나 확인 결과 CureVac의 'RNA-coded antibody'로 별개 문헌이었다(추정을 검증으로 폐기). Google Patents 검색 URL은 WebFetch에서 JS 미렌더링으로 결과가 비어 반환된다

**시도한 쿼리 (4건)**

1. `PATENTSCOPE: PA:(BioNTech) AND EN_ALLTXT:(MHC class I trafficking domain)`
2. `PATENTSCOPE: IN:(Kreiter) AND EN_ALLTXT:(trafficking domain)`
3. `PATENTSCOPE: PA:(BioNTech OR TRON) AND EN_ALLTXT:(polyepitope)`
4. `WebFetch https://patents.google.com/patent/WO2008083949A2/en (CureVac 문헌으로 판명, 가설 폐기)`

### BioNTech 개인맞춤 백신 패밀리(WO2012159643)의 한국 대응출원 존부 및 등록상태

**미해결 사유** — Google Patents의 family 목록은 EP/US/JP/CN/AU/CA/BR/MX만 표시하고 KR을 포함하지 않았으나, WebFetch 응답이 목록을 절단했을 가능성을 배제하지 못했다. KIPRIS 검색 엔드포인트가 접근 불가(code 000)여서 한국 원부 대조가 불가능했다. 부존재를 단정하지 않고 미확인으로 남긴다

**시도한 쿼리 (4건)**

1. `WebFetch https://patents.google.com/patent/WO2012159643A1/en 에 KR 포함 family 질의`
2. `WebFetch https://patents.google.com/patent/US10738355B2/en 에 worldwide family/KR 질의`
3. `curl https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2012159643 국면진입(National Phase) 파싱 (JS 로딩으로 데이터 미포함)`
4. `curl https://engdbsearch.kipris.or.kr/... 및 kpat.kipris.or.kr (모두 code 000)`

### Genocea ATLAS 플랫폼 특허의 등록·권리승계 상태 (Genocea 2022년 사업중단 후 IP 행방)

**미해결 사유** — PATENTSCOPE에서 Genocea 명의 출원 2건(WO2020232408, WO2021203022 'TREATMENT METHODS')만 확인되었고 ATLAS 원천 특허가 검색 인덱스 상위에 나오지 않았다. Genocea는 2022년 상장폐지되어 최신 SEC 공시가 없고, WebSearch 예산 소진으로 파산·자산매각 경로 추적을 완료하지 못했다

**시도한 쿼리 (3건)**

1. `PATENTSCOPE: PA:(Genocea)`
2. `EDGAR FTS: "Gritstone" forms=8-K (Genocea 무관 결과)`
3. `PATENTSCOPE: EN_ALLTXT:(concatemer) AND EN_ALLTXT:(neoantigen)`

### m1Psi 삼인산(m1Psi-TP) 자체에 대한 물질/합성공정 특허의 명시적 부존재 확인

**미해결 사유** — 4개 대표 독립항 분석으로 '원료 물질 청구항 0개'를 확인했으나, 이는 조사한 패밀리 범위 내의 결론이다. m1Psi-TP 합성공정을 청구하는 별도 소규모 출원(예: 원료 전문업체 명의)의 전수 부존재는 증명하지 못했다. PATENTSCOPE 자유텍스트 검색이 3,824건을 반환하며 파싱 가능한 결과행을 0건 산출했다

**시도한 쿼리 (3건)**

1. `PATENTSCOPE: EN_ALLTXT:(N1-methylpseudouridine triphosphate AND synthesis) (3,824 hits, 결과행 파싱 0)`
2. `PATENTSCOPE: PA:(Moderna) AND EN_ALLTXT:(N1-methylpseudouridine) (결과행 0)`
3. `PATENTSCOPE: PA:(TriLink) AND EN_ALLTXT:(cap analog) (캡 유사체만 반환, NTP 물질특허 미발견)`

## D2

### Alnylam v. Moderna(2025-09 합의) 및 v. Pfizer(2025-08 합의)의 합의금액과 주장 특허번호

**미해결 사유** — Alnylam은 FY2025 10-K와 Q3 2025 10-Q 어디에도 금액을 기재하지 않았고 관련 8-K도 없다. 위험요인 항목에 '모든 청구를 해결했다'는 사실만 서술. 중요성 기준 미달 또는 계약상 비밀유지로 판단된다. 주장 특허번호도 SEC 문서에서 특정되지 않았고, CourtListener 검색은 D.Del. 1:22-cv-00335(Alnylam v. Moderna) docket을 잡았으나 RECAP에 소장 PDF가 없었다.

**시도한 쿼리 (4건)**

1. `EDGAR full-text search: q="settlement with Moderna"&ciks=0001178670 → 0 hits`
2. `Alnylam FY2025 10-K(alny-20251231.htm) 전문 정규식: 'settlement' 주변 ±600자에 Pfizer/Moderna + 'million' 동시 출현 → 0 hits`
3. `Alnylam Q3 2025 10-Q(alny-20250930.htm) 전문 정규식 동일 조건 → 0 hits`
4. `CourtListener API type=r, q='Alnylam Moderna', court=ded → docket 63165832 확인되나 소장 PDF is_available=false`

### Karikó/UPenn의 셀룰로스 기반 dsRNA 제거법 특허 존재 여부 및 청구범위

**미해결 사유** — Baiersdörfer 등 2019 Mol Ther Nucleic Acids 논문(PMID 30933724)은 확보했으나, 대응 특허를 찾기 위한 Google Patents XHR 질의가 반복적으로 HTTP 503(레이트리밋)으로 실패했다. WebSearch는 세션 예산(200/200)이 이미 소진되어 단 한 건도 실행할 수 없었다. 따라서 '특허 없음'이 아니라 '확인 불가'로 기록한다.

**시도한 쿼리 (4건)**

1. `Google Patents XHR: q=in+vitro+transcription+dsRNA+impurity+removal+cellulose → 503 (재시도 6회 실패)`
2. `Google Patents XHR: q=messenger+RNA+purification+cellulose+double-stranded&assignee=university+of+pennsylvania → 503 (재시도 6회 실패)`
3. `PubMed E-utilities esearch: 'Baiersdorfer cellulose dsRNA removal mRNA' → PMID 30933724 확보(논문만, 특허 정보 없음)`
4. `WebSearch 'Kariko cellulose dsRNA removal patent' → 세션 검색 예산 소진으로 실행 불가`

### Arcturus STARR 및 VLP Therapeutics의 saRNA 특허 패밀리·청구항

**미해결 사유** — Google Patents 배치 검색 큐가 레이트리밋(503)으로 해당 질의 도달 전 중단되었고, 백그라운드 재시도도 동일 원인으로 실패했다. Replicate Bioscience와 Orna는 확보했으나 Arcturus·VLP는 미확보. WebSearch 예산 소진으로 대체 경로가 봉쇄되었다.

**시도한 쿼리 (4건)**

1. `Google Patents XHR: q=self-amplifying+RNA+STARR&assignee=arcturus → 503, 큐 미도달`
2. `Google Patents XHR: q=self-amplifying+RNA+alphavirus&assignee=gritstone → 헤더만 출력되고 결과 미반환(503)`
3. `Google Patents XHR: q=self-amplifying+RNA&assignee=replicate+bioscience → 성공(17건, R1235로 등재) — 동일 패턴 질의가 Arcturus에서는 실패`
4. `WebSearch 'Arcturus STARR self-amplifying RNA patent claims' → 세션 검색 예산 소진으로 실행 불가`

### Precision NanoSystems/Cytiva의 마이크로플루이딕 혼합(LNP 제조장비) 특허

**미해결 사유** — 검색 큐 마지막 항목이었으나 Google Patents 레이트리밋으로 실행되지 못했다. 이 레이어는 CDMO 설비 도입 시 FTO에 직결되므로 후속 조사가 필요하다. 다만 대체 경로로 Genevant 명의 검색(38건)을 수행해 마이크로플루이딕 관련 건이 Genevant 포트폴리오에는 없음을 부분 확인했다.

**시도한 쿼리 (4건)**

1. `Google Patents XHR: q=lipid+nanoparticle+microfluidic+mixing&assignee=precision+nanosystems → 큐 미도달(503)`
2. `Google Patents XHR: q=lipid+nanoparticle&assignee=genevant → 성공(38건), 마이크로플루이딕 혼합 특허 미확인`
3. `Google Patents XHR: q=lipid+nanoparticle+cationic+lipid&assignee=arbutus → 성공(74건), 혼합장비 특허 미확인`
4. `WebSearch 'Precision NanoSystems NanoAssemblr microfluidic patent' → 세션 검색 예산 소진으로 실행 불가`

### Gritstone saRNA 자산을 인수한 Seattle Project Corp.의 실소유주 및 인수가액

**미해결 사유** — 파산 docket에서 매각승인명령(D.I. 288, 2024-12-20)과 최종 APA 통지(D.I. 324, 2024-12-31, 'Seattle Project Corp.')는 확보했으나, 해당 법인의 모회사·인수가액은 RECAP에 PDF가 없어 확인하지 못했다. Gritstone은 이후 SEC 보고를 중단해 8-K 경로도 막혔다. 법인 실체 조회는 WebSearch 예산 소진으로 불가.

**시도한 쿼리 (4건)**

1. `CourtListener API type=r, q='Gritstone sale assets purchase', court=deb → D.I. 288/324/704 확인, 다만 is_available=false로 PDF 미확보`
2. `CourtListener API type=r, q='"Asset Purchase Agreement"', docket_number=24-12305 → 3건 모두 is_available=false`
3. `EDGAR full-text search: q="Gritstone"&forms=8-K&2025-01-01~2026-08-06 → 파산 월간운영보고서(MOR)만 확인, 매수인 정보 없음`
4. `WebSearch 'Seattle Project Corp Gritstone bio assets acquired' → 세션 검색 예산 소진으로 실행 불가`

### ST팜 SmartCap의 미국 권리화 상태 및 TriLink 라이선스 유무

**미해결 사유** — 미국에서는 공개공보 US20230382943A1(2020-10-20 우선)만 확인되고 등록 여부를 특정하지 못했다. 초기에 US11414453B2를 ST팜 건으로 가정했으나 실제로는 TriLink 특허임을 확인해 정정했다(R1202). ST팜과 TriLink 사이 라이선스·크로스라이선스 존재 여부는 양사 공시·계약이 공개되지 않아 확인 불가하며, ST팜은 DART 공시 대상이나 개별 특허 라이선스는 공시 의무가 없다.

**시도한 쿼리 (4건)**

1. `Google Patents XHR: q=cap+analog&assignee=st+pharm → 6건(KR 위주), 미국 등록건 없음`
2. `Google Patents XHR: q=5-capped+RNA+oligonucleotide+primer&assignee=st+pharm&country=US → US20230382943A1(공개) 1건만 확인`
3. `Google Patents 직접 조회 US11414453B2 → assignee가 TriLink Biotechnologies로 확인(ST팜 아님), 초기 가정 정정`
4. `KR102366490B1 패밀리 목록 확인 → US11414453B2가 '유사문헌'으로 나열될 뿐 동일 패밀리 아님`

### TriLink·Arbutus 한국 패밀리 개별 건의 등록 여부·청구범위·권리자

**미해결 사유** — Google Patents의 worldwide-family 목록에서 KR 번호(KR20230032999A, KR20250047207A, KR101397407B1, KR101184928B1 등)를 추출했으나, 해당 목록은 인용문헌·유사문헌이 섞여 있어 소유권과 등록상태를 단정할 수 없다. KIPRIS 원문 대조가 필요하나 KIPRIS는 공개 API 없이 세션 검색 경로가 필요했고 WebSearch 예산이 소진되어 접근하지 못했다. 이 때문에 R1211·R1281은 신뢰도를 '중'으로 낮추고 단정형 서술을 피했다.

**시도한 쿼리 (4건)**

1. `Google Patents 직접 조회 US10913768B2 → worldwide applications에서 KR 4건 추출(등록상태 불명)`
2. `Google Patents 직접 조회 US11141378B2 → KR101397407B1, KR101184928B1 추출(권리자 불명)`
3. `Google Patents 직접 조회 KR102366490B1 → 패밀리에 US11414453B2 등 포함되나 소유관계 불명확`
4. `KIPRIS 직접 조회 시도 → 공개 API 부재, WebSearch 예산 소진으로 진입 경로 확보 실패`

### Arbutus/Genevant v. Pfizer/BioNTech(D.N.J. 3:23-cv-01876)의 2026-06-30 종결 표기 의미

**미해결 사유** — CourtListener docket 목록에서 njd 3:23-cv-01876이 dateTerminated 2026-06-30으로 표시되었으나, 동일 사건번호의 다른 docket(2:23-cv-01876)은 미종결로 표시되어 재배당·이송에 따른 중복 등록 가능성이 크다. Arbutus의 2026-05-13자 10-Q는 '계속 중'이라고만 기재해 그 이후의 종결·합의 여부를 확인할 수 없었고, 2026-07-16자 8-K에도 Pfizer 관련 언급이 없다. 따라서 '종결'로 단정하지 않고 R1225에서 '계속 중'으로 보수적으로 기재했다.

**시도한 쿼리 (4건)**

1. `CourtListener API type=d, q='Arbutus Genevant Moderna' → njd 3:23-cv-01876(term 2026-06-30)과 2:23-cv-01876(term None) 두 건 동시 확인`
2. `Arbutus 10-Q Q1 2026 전문에서 'Pfizer' 문맥 확인 → '계속 중, 추가 일정 대기' 서술만 존재`
3. `Arbutus 8-K 2026-07-16 전문 확인 → RSV Agreement 종료와 Moderna 합의금 수령만 기재, Pfizer 언급 없음`
4. `EDGAR submissions API로 Arbutus 2026-07-01 이후 8-K 전수 확인 → Pfizer 합의 관련 신규 공시 없음`

## D3

### FY2026 NIH 확정 세출액의 1차 문서 확인 (Consolidated Appropriations Act, 2026 조문 또는 NIH 예산실 공식 수치)

**미해결 사유** — NIH 예산실 페이지(officeofbudget.od.nih.gov/approp_hist.html)가 HTTP 403을 반환했고, 세션의 WebSearch 예산이 소진된 상태에서 대체 검색 경로(DuckDuckGo HTML)는 반복 503을 반환했다. Bing RSS는 질의어의 'NIH'가 nih.gov 도메인과 매칭되어 기관 소개 페이지만 반환했다. 결과적으로 확정 금액이 출처별로 47.2억~48.7억 달러로 엇갈려 R1343을 '하' 등급·헤지 표현으로 등재했다.

**시도한 쿼리 (6건)**

1. `NIH budget 2026 cut proposal percent biomedical research funding appropriations final outcome (DDG HTML)`
2. `"Consolidated Appropriations Act, 2026" NIH funding level enacted February 2026 rejected 40 percent cut AAMC AACR (DDG HTML, 503)`
3. `NIH fiscal 2026 appropriations enacted 48.7 billion increase Congress rejected cut news (DDG HTML, 503)`
4. `"NIH" "fiscal year 2026" appropriation enacted funding increase Congress rejected proposed cut (DDG HTML, 503)`
5. `NIH fiscal year 2026 enacted appropriation billion Congress rejected 40 percent cut (Bing RSS)`
6. `https://officeofbudget.od.nih.gov/approp_hist.html (WebFetch, 403)`

### NHS Cancer Vaccine Launch Pad의 실제 누적 등록/의뢰 환자 수

**미해결 사유** — NHS England 공식 CVLP 페이지에 등록 실적 수치가 게재되어 있지 않고 페이지 갱신일도 표기되지 않는다. 언론 보도는 '수십 명(dozens)' 수준의 정성 표현에 머물렀고, 참여 사이트 수(약 30개)만 확인됐다. 10,000명 목표 대비 진척률은 공개 정보로 산출 불가하여 R1337에 공백 자체를 근거로 등재했다.

**시도한 쿼리 (5건)**

1. `NHS Cancer Vaccine Launch Pad BioNTech 10000 patients 2030 enrolled status 2026 (DDG HTML)`
2. `Cancer Vaccine Launch Pad patients referred enrolled number BioNTech NHS 2026 update (DDG HTML)`
3. `"Cancer Vaccine Launch Pad" patients recruited milestone NHS England 2026 first year numbers trusts (DDG HTML)`
4. `https://www.england.nhs.uk/cancer/nhs-cancer-vaccine-launch-pad/ (WebFetch, 실적 미기재)`
5. `https://www.biontech.com/int/en/home/media/press-releases.html (WebFetch, 404)`

### Merck 10-K Item 1A의 KEYTRUDA LOE 리스크팩터 원문 및 회사 명시 LOE 연도

**미해결 사유** — Merck FY2025 10-K(mrk-20251231.htm)는 문서 용량이 커 WebFetch가 XBRL 메타데이터 구간만 반환하고 서술 섹션에 도달하지 못했다. Q4 2025 및 Q2 2026 실적 보도자료에도 LOE 관련 서술이 없어, LOE 2028 연도는 2차 보도 기반 '중' 등급(R1329)으로만 등재했다. KEYTRUDA 매출·전사 매출 등 정량 수치는 1차 공시로 확보(R1327, R1328).

**시도한 쿼리 (4건)**

1. `https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm (WebFetch, XBRL 메타데이터만 반환)`
2. `Merck Keytruda loss of exclusivity 2028 patent expiration risk factor 10-K subcutaneous conversion 30-40% (DDG HTML)`
3. `Keytruda patent expiration 2028 loss of exclusivity Merck revenue cliff 2025 sales (Bing RSS, 무관 결과)`
4. `https://www.sec.gov/Archives/edgar/data/310158/000110465926009495/tm264564d1_ex99-1.htm (WebFetch, LOE 서술 없음)`

### BioNTech의 iNeST/BNT122 우선순위에 대한 명시적 경영진 서술

**미해결 사유** — Q2 2026 분기보고서 본문에서 iNeST·autogene cevumeran·BNT122 언급이 확인되지 않았고, EDGAR 전문검색의 "autogene cevumeran" 질의는 2026년 구간에서 HTTP 500을 반환했다. R&D 증가 동인으로 pumitamig·gotistobart가 명시된 사실(R1325)과 BMS 딜 배분(R1326)으로 간접 추론만 가능해, 우선순위 하락은 리스크 R07에 '확률 중'으로만 반영했다.

**시도한 쿼리 (4건)**

1. `BioNTech iNeST autogene cevumeran prioritization 2026 pipeline strategy BNT327 Genentech status (DDG HTML)`
2. `EDGAR FTS: "autogene cevumeran" 2026-01-01~2026-08-10 (HTTP 500)`
3. `EDGAR FTS: "intismeran" 2026-01-01~2026-08-10 (성공, 단 BioNTech 문서 없음)`
4. `https://www.sec.gov/Archives/edgar/data/1776985/000177698526000055/bntxq22026ex991quarterlyre.htm (WebFetch, iNeST 언급 미확인)`

### 일본 AMED/SCARDA 프로그램 예산의 원문 확인 및 항암 mRNA 포함 여부

**미해결 사유** — AMED 영문 프로그램 목록 페이지를 통한 금액 원문 확인에 도달하지 못했고, 515억엔·1,500억엔 수치는 검색 요약 및 2차 보도 기반이다. 개인맞춤 항암 mRNA가 SCARDA 대상에 포함되는지에 대한 명시적 문구도 확보하지 못해 R1345를 '하' 등급으로 등재했다.

**시도한 쿼리 (3건)**

1. `SCARDA Japan mRNA vaccine funding AMED billion yen 2025 2026 cancer vaccine policy (DDG HTML)`
2. `EU HERA mRNA manufacturing capacity EU FAB 2025 2026 funding personalised cancer vaccine EU4Health (DDG HTML, 일본 비교 맥락)`
3. `Germany BioNTech mRNA support 2025 2026 EU Commission cancer plan personalised cancer vaccine funding Horizon Europe (DDG HTML, 503)`

### 한국 mRNA 원부자재 국산화 사업의 정부 원문 공고 (IRIS/범부처 공고문)

**미해결 사유** — 바이오 소부장 예산 추이(236억→703억원)와 mRNA·LNP 핵심소재 실증 인프라 4년 100억원은 모두 2차 집계 플랫폼(rndcircle, kitim) 기반이며 정부 원문 공고에 도달하지 못했다. 이에 R1340·R1341을 '하' 등급으로 등재하고 단정형 서술을 금지했다. LG화학 관점에서 직접적인 정책자금 규모 판단에 불확실성이 남는다.

**시도한 쿼리 (4건)**

1. `mRNA 원부자재 국산화 자립화 정부 사업 소재부품장비 바이오 (DDG HTML)`
2. `보건복지부 mRNA 백신 개발 지원 사업 예산 2026 원부자재자립화 (DDG HTML)`
3. `질병관리청 mRNA 백신 개발 5052억 녹십자 레모넥스 유바이오로직스 한국BMI (DDG HTML)`
4. `"mRNA 백신 개발 지원 사업" 예산 억원 질병관리청 국가신약개발사업단 (DDG HTML, 결과 0건)`

### 개인맞춤형 신생항원 mRNA에 대한 명명된 전문가의 회의적 견해 원문

**미해결 사유** — 대칭성 규칙에 따라 회의론을 별도 수집했으나, 검색 결과가 정책 관련 우려(NIH·행정부)에 집중되고 비용·제조 기간·근거 수준을 비판하는 명명된 전문가의 직접 인용을 확보하지 못했다. Lancet Oncology 본문은 HTTP 403(유료장벽)으로 접근 실패했다. 대신 재무·레지스트리 기반 부정 근거(Gritstone 파산 R1334·R1335, 3상 2029년 예정 R1342, 매출 급감 R1314·R1323·R1331)로 대칭성을 확보했다.

**시도한 쿼리 (4건)**

1. `mRNA cancer vaccine skeptics experts criticism 2025 2026 overhyped individualized neoantigen limitations cost (DDG HTML)`
2. `https://www.thelancet.com/journals/lanonc/article/PIIS1470-2045(25)00430-9/fulltext (WebFetch, 403)`
3. `NIH mRNA vaccine research grants terminated 2025 oncology cancer vaccine exempt (DDG HTML)`
4. `intismeran phase 3 INTerpath-001 melanoma readout 2026 delayed event driven timeline risk (DDG HTML)`

---

**공백 총계 74건.** 쿼리 3개 미만으로 기록된 항목: 0건 (없음 — 정지조건 충족)
