"""
search_builder.py — World Cup Intelligence Hub
Builds public/search.json (unchanged for compatibility)
and public/search.html (new: a proper search page).
"""
from pathlib import Path
import json
from website.templates import build_page

ARTICLES_DIR = Path("output/website")
SEARCH_JSON  = Path("public/search.json")
SEARCH_HTML  = Path("public/search.html")


def build_search_index():
    articles = []

    for file in ARTICLES_DIR.glob("*.md"):
        if file.name in ("index.md", "timeline.md", "qualification_watch.md"):
            continue
        if file.stat().st_size < 200:
            continue

        stem = file.stem
        is_report  = "Match Report" in stem
        is_preview = "vs" in stem and not is_report
        label = "Match Report" if is_report else ("Preview" if is_preview else "Article")

        articles.append({
            "title": stem,
            "url":   f"articles/{stem}.html",
            "type":  label,
        })

    articles.sort(key=lambda a: a["title"])

    # Write search.json (unchanged contract with any consumers)
    SEARCH_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SEARCH_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    # Write search.html with client-side search
    _build_search_page(articles)

    print("[SEARCH] Updated")


def _build_search_page(articles):
    articles_json = json.dumps(articles)

    content = f"""
<div class="section-header">
  <div class="section-title">Search Reports</div>
  <span class="text-muted" style="font-size:13px;" id="result-count"></span>
</div>

<div class="search-wrap">
  <input
    class="search-input"
    type="search"
    id="search-input"
    placeholder="Search match reports and previews..."
    autocomplete="off"
  >
  <span class="search-icon">🔍</span>
</div>

<div class="pill-row" id="filter-row">
  <button class="pill active" data-filter="all"    onclick="setFilter('all',this)">All</button>
  <button class="pill"        data-filter="Match Report" onclick="setFilter('Match Report',this)">Match Reports</button>
  <button class="pill"        data-filter="Preview"      onclick="setFilter('Preview',this)">Previews</button>
</div>

<div class="article-grid" id="results-grid"></div>

<script>
var ARTICLES = {articles_json};
var currentFilter = 'all';

function setFilter(f, btn) {{
  currentFilter = f;
  document.querySelectorAll('#filter-row .pill').forEach(function(b) {{ b.classList.remove('active'); }});
  btn.classList.add('active');
  doSearch();
}}

function doSearch() {{
  var q = document.getElementById('search-input').value.toLowerCase().trim();
  var grid = document.getElementById('results-grid');
  var count = document.getElementById('result-count');

  var filtered = ARTICLES.filter(function(a) {{
    var matchFilter = currentFilter === 'all' || a.type === currentFilter;
    var matchQ = !q || a.title.toLowerCase().includes(q);
    return matchFilter && matchQ;
  }});

  count.textContent = filtered.length + ' result' + (filtered.length !== 1 ? 's' : '');

  if (!filtered.length) {{
    grid.innerHTML = '<div class="empty"><div class="empty-icon">🔍</div><p>No results found for that search.</p></div>';
    return;
  }}

  var tagClass = {{ 'Match Report': 'report', 'Preview': 'preview', 'Article': 'analysis' }};

  grid.innerHTML = filtered.map(function(a) {{
    var tc = tagClass[a.type] || 'analysis';
    return '<div class="card">' +
      '<div class="card-type-bar ' + tc + '"></div>' +
      '<div class="card-body">' +
        '<div class="card-label">' + a.type + '</div>' +
        '<h3><a href="/' + a.url + '" style="text-decoration:none;color:inherit;">' + a.title + '</a></h3>' +
      '</div>' +
      '<div class="card-footer">' +
        '<a class="card-link" href="/' + a.url + '">Read report →</a>' +
      '</div>' +
    '</div>';
  }}).join('');
}}

document.getElementById('search-input').addEventListener('input', doSearch);
doSearch();
</script>
"""

    html = build_page(
        "Search",
        content,
        active_nav="",
        description="Search all World Cup 2026 match reports and previews."
    )

    SEARCH_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(SEARCH_HTML, "w", encoding="utf-8") as f:
        f.write(html)
