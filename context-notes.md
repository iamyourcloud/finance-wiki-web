# Finance Wiki Web — 컨텍스트 노트

작업 중 내린 결정과 근거를 계속 덧붙인다.

## 2026-06-22 시작

### 무엇을 / 왜
- 사용자가 후배의 임상 레지스트리(krod.snuhos.org 등)·koreantickers.com 같은 "깔끔한 웹사이트"를 보고 본인도 만들고 싶어 함.
- 실제 목적은 임상/연구가 아니라 **본인 미국주식 리서치 노트(HSShin/Finance/Wiki)를 웹으로 정리**하는 것. 환자 데이터 아님 → 로그인·보안 불필요.
- 디자인은 레퍼런스와 똑같을 필요 없음. "정보가 잘 분류된 깔끔한 금융 사이트" 느낌이면 됨.

### 핵심 설계 결정
- **정적 사이트 생성기(Python)** 채택. 이유: ① 정적 결과물이라 GitHub Pages/Vercel/Netlify 어디든 배포 → URL 확보, ② Node 빌드 의존성 없이 이미 있는 Python으로, ③ Wiki 수정 후 build.py 재실행만으로 갱신, ④ 한글 사용자명 인코딩 함정과 무관.
  - 대안(Next.js 등 SSG 프레임워크)도 가능하나 초기 설정·의존성이 과함. 단순함 우선(CLAUDE.md #2).
- **프로젝트 위치 = OneDrive 밖** (`C:\Users\신현석\Apps\finance-wiki-web`). 이유: 깃 저장소를 OneDrive 안에 두면 `.git` 동기화 충돌 + 턴 경계 revert 함정. 콘텐츠 원본(Wiki)은 OneDrive에 그대로 두고 **읽기만** 함.
- 콘텐츠는 dist HTML에 **구워서**(bake) 배포. 배포 시점에 OneDrive 접근 불필요.

### 콘텐츠 형식(파싱 규약)
- 파일: `Wiki/*.md` (slug = 파일명). `index.md`는 사이드바 그룹 정의용으로도 사용.
- 페이지 구조: `# 제목` → `**Summary**/**Sources**/**Last updated**` 헤더 블록 → `---` → 본문(## 섹션들).
- 링크: `[[slug]]`, `[[slug|별칭]]`. slug는 파일명과 직접 매칭.
- 본문에 `(source: 파일.md)` 인용 패턴 → 시각적으로 muted 처리.
- index.md 섹션: `## 테마`, `## 종목(엔티티)`, `## 소스·전략·관리` = 사이드바 그룹. `## 미해결/검증 대기`는 홈에 노출.

### 환경
- node v24.15 / git 2.54 / gh 2.92 / python markdown 3.10.2(설치함) 모두 사용 가능.
- C:\claude 정션 존재(워크스페이스 ASCII 경로).

### 빌드 검증 완료(2026-06-22)
- `python scripts/build.py` → dist/ 25개 콘텐츠 페이지 + 홈, 검색항목 25, 깨진 위키링크 0.
- Playwright 육안 검증: 홈 카드 그리드·엔티티 페이지(위키링크/출처 muted/타임라인/Related/백링크)·사이드바·검색 정상.
- 버그 1건 수정: 홈 카드 설명이 제목을 반복 → index.md 한 줄 설명(desc_by_slug) 사용하도록 교정.
- index.md·log.md는 콘텐츠 페이지에서 제외(index는 사이드바/홈 정의 전용).
- 개인 노트라 전 페이지 `<meta robots noindex,nofollow>` + `robots.txt(Disallow /)` 기본 적용. GitHub Pages용 `.nojekyll` 포함.
- 로컬 서버가 dist/ 폴더를 잠가 rmtree 실패 → 재빌드 전 8765/8766 리스너 kill 필요(함정).

### 다음 세션 진입점
- 배포 도구 미인증 상태(gh·vercel 로그인 안 됨). 사용자 1회 로그인 필요.
- 사용자에게 배포 경로(GitHub Pages / Vercel / Netlify Drop / 보류) 선택 요청함 → 선택에 따라 단계 안내.
