# Finance Wiki Web

미국주식 리서치 노트(Obsidian `Finance/Wiki` 폴더의 마크다운)를 깔끔한 정적 웹사이트로 빌드한다.

## 구조
- `scripts/build.py` — Wiki 마크다운을 읽어 `docs/`에 정적 HTML 사이트를 생성하는 빌더.
- `assets/styles.css`, `assets/search.js` — 사이트 디자인과 클라이언트 검색.
- `docs/` — 빌드 결과물(= GitHub Pages가 서빙하는 사이트). 깃에 커밋된다.

## 빌드
```bash
python scripts/build.py
```
콘텐츠 원본 경로는 `scripts/build.py` 상단의 `SRC` 상수에서 설정한다.

## 갱신 흐름
1. Obsidian에서 `Finance/Wiki` 노트를 수정한다.
2. `python scripts/build.py` 재실행 → `docs/` 갱신.
3. `git add -A && git commit -m "위키 갱신" && git push` → GitHub Pages 자동 반영.

## 메모
- 개인 노트라 검색엔진 비노출(`<meta robots noindex>` + `robots.txt`)이 기본 적용돼 있다.
- 빌드는 콘텐츠를 HTML에 구워 넣으므로 배포 시점에 원본 폴더 접근이 필요 없다.
