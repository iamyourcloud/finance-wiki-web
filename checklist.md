# Finance Wiki Web — 체크리스트

목표: HSShin/Finance/Wiki 폴더의 마크다운 노트를 깔끔한 정적 웹사이트로 빌드하고 온라인(URL)에 배포한다.

## Phase 1 — 정적 사이트 빌더
- [x] 프로젝트 골격 (`Apps/finance-wiki-web`, OneDrive 밖) → verify: 폴더 생성됨
- [x] `scripts/build.py` 작성 (Wiki md → dist/ 정적 HTML) → verify: 에러 없이 실행
- [x] 페이지 파싱: 제목 / Summary·Sources·Last updated 헤더 / 본문 분리 → verify: 한 페이지 수동 확인
- [x] `[[위키링크]]`·`[[링크|별칭]]` → `<a href>` 변환, 깨진 링크 표시 → verify: nvidia 페이지 링크 클릭 이동
- [x] index.md 기반 사이드바 그룹(테마/종목/관리) + 기타 → verify: 모든 페이지가 사이드바에 1회 등장
- [x] 백링크(역참조) 섹션 자동 생성 → verify: micron 페이지에 역참조 표시
- [x] 클라이언트 검색(search-index.json + search.js) → verify: "HBM" 검색 시 결과 노출
- [x] 홈 대시보드(그룹 카드 + 미해결/검증 대기) → verify: index.html 열림

## Phase 2 — 로컬 확인
- [x] `python scripts/build.py` 빌드 성공 → verify: dist/ 에 페이지 수 == md 수
- [x] 로컬 서버로 열어 육안 확인 → verify: 링크·검색·반응형 동작

## Phase 3 — 온라인 배포
- [x] git 저장소 초기화 + 첫 커밋 (gh repo 생성·push 대기 — 로그인 필요)
- [x] 호스팅 연결(GitHub Pages, /docs) → https://iamyourcloud.github.io/finance-wiki-web/ (200 확인)
- [x] 검색엔진 비노출(noindex + robots.txt) 기본 적용

## 운영
- [x] "Wiki 수정 → build.py 재실행 → 재배포" 흐름 README + 채팅으로 안내

## 배포 정보
- repo: https://github.com/iamyourcloud/finance-wiki-web (public, GitHub 계정 iamyourcloud)
- live: https://iamyourcloud.github.io/finance-wiki-web/
- Pages 소스: main 브랜치 /docs, noindex+robots 차단.
