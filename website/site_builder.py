"""
site_builder.py — World Cup Intelligence Hub
Builds individual article HTML pages and the articles index.
"""
from pathlib import Path
import markdown
from website.templates import build_page, build_article_page

ARTICLES_DIR = Path("output/website")
PUBLIC_DIR   = Path("public/articles")


def _classify(stem):
    """Return (label, tag_class) based on article filename."""
    if "Match Report" in stem:
        return "Match Report", "report"
    if any(x in stem for x in ["vs", "Preview", "preview"]):
        return "Pre-Match Preview", "preview"
    return "Analysis", "analysis"


def build_article_pages():
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    files = [
        f for f in ARTICLES_DIR.glob("*.md")
        if f.name not in ("index.md", "timeline.md", "qualification_watch.md")
    ]
    count = 0

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Skip placeholder stubs
        if len(md_content.strip()) < 200:
            continue

        body_html = markdown.markdown(md_content)
        title     = file.stem
        label, tag_class = _classify(title)

        html = build_article_page(title, body_html, label=label, tag_class=tag_class)
        output_file = PUBLIC_DIR / f"{file.stem}.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        count += 1

    _build_articles_index()
    print(f"[SITE] Built {count} article pages")


def _build_articles_index():
    """Build public/articles/index.html — a searchable article listing."""
    files = [
        f for f in ARTICLES_DIR.glob("*.md")
        if f.name not in ("index.md", "timeline.md", "qualification_watch.md")
        and f.stat().st_size > 200
    ]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    reports  = [f for f in files if "Match Report" in f.stem]
    previews = [f for f in files if "vs" in f.stem or "Preview" in f.stem]
    previews = [f for f in previews if f not in reports]

    def card(f, tag_class, label):
        stem = f.stem
        href = f"{stem}.html"
        return f"""
<div class="card">
  <div class="card-type-bar {tag_class}"></div>
  <div class="card-body">
    <div class="card-label">{label}</div>
    <h3><a href="{href}" style="text-decoration:none;color:inherit;">{stem}</a></h3>
  </div>
  <div class="card-footer">
    <a class="card-link" href="{href}">Read →</a>
  </div>
</div>"""

    reports_html  = "\n".join(card(f, "report",  "Match Report")  for f in reports)  or "<p class='text-muted'>No reports yet.</p>"
    previews_html = "\n".join(card(f, "preview", "Pre-Match Preview") for f in previews) or "<p class='text-muted'>No previews yet.</p>"

    content = f"""
<div class="section-header">
  <div class="section-title">Match Reports</div>
  <span class="text-muted" style="font-size:13px;">{len(reports)} published</span>
</div>
<div class="article-grid">
{reports_html}
</div>

<hr class="divider">

<div class="section-header">
  <div class="section-title">Pre-Match Previews</div>
  <span class="text-muted" style="font-size:13px;">{len(previews)} published</span>
</div>
<div class="article-grid">
{previews_html}
</div>
"""
    html = build_page("Match Reports & Previews", content, active_nav="Reports")
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
