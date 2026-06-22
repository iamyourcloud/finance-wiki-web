# Finance Wiki 마크다운 노트를 깔끔한 정적 웹사이트(dist/)로 변환하는 빌드 스크립트
import re
import sys
import json
import html
import shutil
from pathlib import Path

import markdown

# ---------- 경로 설정 ----------
PROJECT = Path(__file__).resolve().parent.parent
# 콘텐츠 원본(OneDrive). 환경에 따라 바꿀 수 있게 상단 상수로 노출.
SRC = Path(r"C:\Users\신현석\OneDrive\바탕 화면\HSShin\Finance\Wiki")
OUT = PROJECT / "docs"  # GitHub Pages가 /docs를 사이트 루트로 서빙
SITE_TITLE = "Finance Wiki"
SITE_SUBTITLE = "미국주식 리서치 노트"

# 사이드바 그룹으로 쓸 index.md 섹션(순서대로). 이 외 섹션은 본문 노트로 간주.
NAV_SECTIONS = ["테마", "종목(엔티티)", "소스·전략·관리"]

# ---------- 마크다운 파싱 ----------
META_RE = re.compile(r"\*\*(.+?)\*\*\s*[:：]\s*(.*)")
WL_RE = re.compile(r"\[\[([^\]]+)\]\]")
SRC_RE = re.compile(r"\((source:[^)]*)\)", re.IGNORECASE)


def parse_page(path: Path) -> dict:
    """한 .md 파일을 제목/메타/본문으로 분해한다."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = path.stem
    body_start = 0
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            title = ln[2:].strip()
            body_start = i + 1
            break

    rest = lines[body_start:]
    hr_idx = next((i for i, ln in enumerate(rest) if ln.strip() == "---"), None)
    header_lines = rest[:hr_idx] if hr_idx is not None else []
    body_lines = rest[hr_idx + 1:] if hr_idx is not None else rest

    meta = {}
    for ln in header_lines:
        m = META_RE.match(ln.strip())
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip()

    return {
        "slug": path.stem,
        "title": title,
        "summary": meta.get("summary", ""),
        "sources": meta.get("sources", ""),
        "updated": meta.get("last updated", ""),
        "body": "\n".join(body_lines).strip(),
    }


def render_body(body: str, title_by_slug: dict, valid_slugs: set):
    """본문 마크다운 → HTML. 위키링크/인용을 후처리한다. (html, 나가는링크목록) 반환."""
    tokens = []

    def grab(m):
        inner = m.group(1)
        target, label = (inner.split("|", 1) + [None])[:2]
        target = target.strip()
        if label is None:
            label = title_by_slug.get(target, target)
        tokens.append((target, label.strip()))
        return f"@@WL{len(tokens) - 1}@@"

    pre = WL_RE.sub(grab, body)
    out = markdown.markdown(pre, extensions=["tables", "fenced_code", "sane_lists"])

    def restore(m):
        target, label = tokens[int(m.group(1))]
        broken = "" if target in valid_slugs else " wikilink-broken"
        return (f'<a class="wikilink{broken}" href="{html.escape(target)}.html">'
                f'{html.escape(label)}</a>')

    out = re.sub(r"@@WL(\d+)@@", restore, out)
    out = SRC_RE.sub(lambda m: f'<span class="src">({html.escape(m.group(1))})</span>', out)
    outgoing = [t[0] for t in tokens]
    return out, outgoing


# ---------- index.md → 사이드바 그룹 ----------
def parse_index(path: Path):
    """index.md의 ## 섹션 → [(섹션명, [(slug, desc)])]."""
    groups = []
    if not path.exists():
        return groups
    cur = None
    for ln in path.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^##\s+(.*)", ln)
        if h:
            cur = (h.group(1).strip(), [])
            groups.append(cur)
            continue
        m = re.match(r"^-\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\]\s*[—\-]?\s*(.*)", ln)
        if m and cur is not None:
            cur[1].append((m.group(1).strip(), m.group(2).strip()))
    return groups


# ---------- HTML 템플릿 ----------
def sidebar_html(nav_groups, active_slug):
    parts = ['<nav class="sidebar">']
    parts.append(f'<a class="brand" href="index.html"><span class="logo">◆</span>'
                 f'<span><b>{html.escape(SITE_TITLE)}</b><small>{html.escape(SITE_SUBTITLE)}</small></span></a>')
    parts.append('<input id="search" class="search" type="search" '
                 'placeholder="검색 (예: HBM, 마이크론)" autocomplete="off">')
    parts.append('<div id="results" class="results" hidden></div>')
    parts.append('<div id="nav">')
    for name, items in nav_groups:
        if not items:
            continue
        parts.append(f'<div class="nav-group"><div class="nav-title">{html.escape(name)}</div>')
        for slug, title in items:
            cls = "nav-link active" if slug == active_slug else "nav-link"
            parts.append(f'<a class="{cls}" href="{html.escape(slug)}.html">{html.escape(title)}</a>')
        parts.append("</div>")
    parts.append("</div></nav>")
    return "\n".join(parts)


def page_shell(title, sidebar, main_html):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ctext y='26' font-size='26'%3E%E2%97%86%3C/text%3E%3C/svg%3E">
<title>{html.escape(title)} · {html.escape(SITE_TITLE)}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<button id="menu" class="menu-btn" aria-label="메뉴">☰</button>
{sidebar}
<main class="content">
{main_html}
</main>
<script src="search.js"></script>
</body>
</html>"""


def meta_bar(page):
    bits = []
    if page["updated"]:
        bits.append(f'<span class="chip">갱신 {html.escape(page["updated"])}</span>')
    if page["sources"]:
        bits.append(f'<span class="chip src">출처 {html.escape(page["sources"])}</span>')
    return f'<div class="metabar">{"".join(bits)}</div>' if bits else ""


def render_page_html(page, body_html, backlinks, nav_groups, title_by_slug):
    sidebar = sidebar_html(nav_groups, page["slug"])
    head = [f'<header class="page-head"><h1>{html.escape(page["title"])}</h1>']
    if page["summary"]:
        # summary 안의 위키링크/인용도 살려준다
        sm, _ = render_body(page["summary"], title_by_slug, set(title_by_slug.keys()))
        head.append(f'<p class="summary">{sm}</p>')
    head.append(meta_bar(page))
    head.append("</header>")

    bl = ""
    if backlinks:
        links = " ".join(
            f'<a class="wikilink" href="{html.escape(s)}.html">{html.escape(title_by_slug.get(s, s))}</a>'
            for s in backlinks
        )
        bl = f'<section class="backlinks"><h3>여기를 참조하는 페이지</h3><div>{links}</div></section>'

    main_html = "\n".join(head) + f'<article class="article">{body_html}</article>' + bl
    return page_shell(page["title"], sidebar, main_html)


def render_home(nav_groups, pages_by_slug, desc_by_slug, unresolved_html):
    sidebar = sidebar_html(nav_groups, None)
    cards = []
    for name, items in nav_groups:
        if not items:
            continue
        cards.append(f'<section class="home-group"><h2>{html.escape(name)}</h2><div class="cards">')
        for slug, _title in items:
            p = pages_by_slug.get(slug)
            t = p["title"] if p else slug
            d = desc_by_slug.get(slug) or (p["summary"] if p else "")
            cards.append(
                f'<a class="card" href="{html.escape(slug)}.html"><b>{html.escape(t)}</b>'
                f'<span>{html.escape(d)}</span></a>')
        cards.append("</div></section>")

    hero = (f'<header class="hero"><h1>{html.escape(SITE_TITLE)}</h1>'
            f'<p>{html.escape(SITE_SUBTITLE)} · 테마와 종목을 한곳에서.</p></header>')
    watch = (f'<section class="home-group"><h2>미해결 / 검증 대기</h2>'
             f'<div class="watchbox">{unresolved_html}</div></section>') if unresolved_html else ""
    return page_shell("홈", sidebar, hero + "\n".join(cards) + watch)


# ---------- 빌드 ----------
def main():
    if not SRC.exists():
        sys.exit(f"[에러] 소스 폴더를 찾을 수 없음: {SRC}")

    # log=변경이력, index=사이드바 정의용 → 콘텐츠 페이지에서 제외
    md_files = sorted(p for p in SRC.glob("*.md") if p.stem.lower() not in {"log", "index"})
    pages = [parse_page(p) for p in md_files]
    pages_by_slug = {p["slug"]: p for p in pages}
    title_by_slug = {p["slug"]: p["title"] for p in pages}
    valid = set(pages_by_slug)

    # 본문 렌더 + 나가는 링크 수집
    rendered, outgoing = {}, {}
    for p in pages:
        body_html, links = render_body(p["body"], title_by_slug, valid)
        rendered[p["slug"]] = body_html
        outgoing[p["slug"]] = [l for l in links if l in valid]

    # 백링크 계산
    backlinks = {s: [] for s in valid}
    for src_slug, targets in outgoing.items():
        for t in set(targets):
            if t != src_slug:
                backlinks[t].append(src_slug)
    for s in backlinks:
        backlinks[s] = sorted(set(backlinks[s]))

    # 사이드바 그룹: index.md의 NAV_SECTIONS + 어디에도 안 잡힌 페이지는 '기타'
    raw_groups = parse_index(SRC / "index.md")
    desc_by_slug = {slug: desc for _n, items in raw_groups for slug, desc in items if desc}
    nav_groups, placed = [], set()
    for name in NAV_SECTIONS:
        items = next((items for n, items in raw_groups if n == name), [])
        clean = []
        for slug, _desc in items:
            if slug in valid and slug not in placed:
                clean.append((slug, title_by_slug[slug]))
                placed.add(slug)
        if clean:
            nav_groups.append((name, clean))
    extras = [(s, title_by_slug[s]) for s in sorted(valid) if s not in placed and s != "index"]
    if extras:
        nav_groups.append(("기타", extras))

    # 홈: '미해결/검증 대기' 섹션을 index.md에서 추출
    unresolved_html = ""
    idx_unres = next((items for n, items in raw_groups
                      if "미해결" in n or "검증" in n), [])
    if idx_unres:
        lis = "".join(
            f'<li><a class="wikilink" href="{html.escape(s)}.html">'
            f'{html.escape(title_by_slug.get(s, s))}</a> — {html.escape(d)}</li>'
            for s, d in idx_unres if s in valid)
        if lis:
            unresolved_html = f"<ul>{lis}</ul>"

    # 출력 폴더 초기화
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # 페이지 쓰기
    for p in pages:
        if p["slug"] == "index":
            continue  # index.md는 사이드바 정의용 → 홈으로 대체
        html_doc = render_page_html(p, rendered[p["slug"]], backlinks[p["slug"]],
                                    nav_groups, title_by_slug)
        (OUT / f"{p['slug']}.html").write_text(html_doc, encoding="utf-8")

    # 홈
    (OUT / "index.html").write_text(
        render_home(nav_groups, pages_by_slug, desc_by_slug, unresolved_html), encoding="utf-8")

    # 검색 인덱스
    search_index = [{
        "slug": p["slug"],
        "title": p["title"],
        "summary": p["summary"],
        "text": re.sub(r"\s+", " ", p["body"])[:1200],
    } for p in pages if p["slug"] != "index"]
    (OUT / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8")

    # 정적 자산 복사
    assets = PROJECT / "assets"
    for fn in ("styles.css", "search.js"):
        shutil.copyfile(assets / fn, OUT / fn)

    # 검색엔진 차단 + GitHub Pages용 .nojekyll
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    n = len(list(OUT.glob("*.html")))
    print(f"[완료] {n}개 HTML 페이지 → {OUT}")
    broken = sum(1 for s in outgoing for t in outgoing[s] if t not in valid)
    print(f"[정보] 페이지 {len(pages)}개, 검색항목 {len(search_index)}개, 깨진 위키링크 {broken}개")


if __name__ == "__main__":
    main()
