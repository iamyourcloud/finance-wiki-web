# Finance Wiki Web — 체크리스트

목표: HSShin/Finance/Wiki 폴더의 마크다운 노트를 깔끔한 정적 웹사이트로 빌드하고 온라인(URL)에 배포한다.

## Phase 1 — 정적 사이트 빌더
- [ ] 프로젝트 골격 (`Apps/finance-wiki-web`, OneDrive 밖) → verify: 폴더 생성됨
- [ ] `scripts/build.py` 작성 (Wiki md → dist/ 정적 HTML) → verify: 에러 없이 실행
- [ ] 페이지 파싱: 제목 / Summary·Sources·Last updated 헤더 / 본문 분리 → verify: 한 페이지 수동 확인
- [ ] `[[위키링크]]`·`[[링크|별칭]]` → `<a href>` 변환, 깨진 링크 표시 → verify: nvidia 페이지 링크 클릭 이동
- [ ] index.md 기반 사이드바 그룹(테마/종목/관리) + 기타 → verify: 모든 페이지가 사이드바에 1회 등장
- [ ] 백링크(역참조) 섹션 자동 생성 → verify: micron 페이지에 역참조 표시
- [ ] 클라이언트 검색(search-index.json + search.js) → verify: "HBM" 검색 시 결과 노출
- [ ] 홈 대시보드(그룹 카드 + 미해결/검증 대기) → verify: index.html 열림

## Phase 2 — 로컬 확인
- [ ] `python scripts/build.py` 빌드 성공 → verify: dist/ 에 페이지 수 == md 수
- [ ] 로컬 서버로 열어 육안 확인 → verify: 링크·검색·반응형 동작

## Phase 3 — 온라인 배포
- [ ] git 저장소 초기화 + GitHub repo 생성(gh) → verify: push 성공
- [ ] 호스팅 연결(GitHub Pages 또는 Vercel) → verify: 공개 URL 접속됨
- [ ] (선택) 비공개 처리 방법 안내

## 운영
- [ ] "Wiki 수정 → build.py 재실행 → 재배포" 흐름 사용자에게 안내
