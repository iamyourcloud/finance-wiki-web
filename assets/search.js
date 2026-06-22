// 클라이언트 검색 + 모바일 메뉴 토글
(function () {
  // 모바일 메뉴
  var menu = document.getElementById("menu");
  var sidebar = document.querySelector(".sidebar");
  if (menu && sidebar) {
    menu.addEventListener("click", function () { sidebar.classList.toggle("open"); });
  }

  var input = document.getElementById("search");
  var box = document.getElementById("results");
  var nav = document.getElementById("nav");
  if (!input || !box) return;

  var INDEX = [];
  fetch("search-index.json")
    .then(function (r) { return r.json(); })
    .then(function (d) { INDEX = d; })
    .catch(function () {});

  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }

  function snippet(text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (i < 0) return text.slice(0, 90);
    var s = Math.max(0, i - 30);
    return (s > 0 ? "…" : "") + text.slice(s, s + 90);
  }

  function run(q) {
    q = q.trim().toLowerCase();
    if (!q) { box.hidden = true; if (nav) nav.style.display = ""; return; }
    var hits = INDEX.filter(function (p) {
      return (p.title + " " + p.summary + " " + p.text).toLowerCase().indexOf(q) >= 0;
    }).slice(0, 12);

    if (!hits.length) {
      box.innerHTML = '<div class="r-empty">검색 결과 없음</div>';
    } else {
      box.innerHTML = hits.map(function (p) {
        var base = (p.summary || p.text || "");
        return '<a href="' + p.slug + '.html">' +
          '<div class="r-title">' + esc(p.title) + '</div>' +
          '<div class="r-snip">' + esc(snippet(base, q)) + '</div></a>';
      }).join("");
    }
    box.hidden = false;
    if (nav) nav.style.display = "none";
  }

  input.addEventListener("input", function () { run(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { input.value = ""; run(""); input.blur(); }
    if (e.key === "Enter") {
      var first = box.querySelector("a");
      if (first) window.location.href = first.getAttribute("href");
    }
  });
})();
