"""
homepage_builder.py — World Cup Intelligence Hub
Builds public/index.html with a sports-news editorial layout.
Reads article files from output/website/ to populate Latest Reports.
"""
from pathlib import Path
from website.templates import build_page

OUTPUT_FILE = Path("public/index.html")
ARTICLES_DIR = Path("output/website")


def _get_latest_articles(limit=6):
    """Return the most recently modified article .md files."""
    if not ARTICLES_DIR.exists():
        return []
    files = [
        f for f in ARTICLES_DIR.glob("*.md")
        if f.name not in ("index.md", "timeline.md", "qualification_watch.md")
        and f.stat().st_size > 500
    ]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[:limit]


def _article_cards(files):
    if not files:
        return """
<div class="empty">
  <div class="empty-icon">📰</div>
  <p>Match reports will appear here as the tournament progresses.</p>
</div>
"""
    cards = []
    for i, f in enumerate(files):
        stem = f.stem
        href = f"/articles/{stem}.html"
        is_report = "Match Report" in stem or "World Cup" in stem
        tag_class = "report" if is_report else "preview"
        label = "Match Report" if is_report else "Pre-Match Preview"
        featured = "featured-card" if i == 0 else ""
        cards.append(f"""
<div class="card {featured}">
  <div class="card-type-bar {tag_class}"></div>
  <div class="card-body">
    <div class="card-label">{label}</div>
    <h2><a href="{href}" style="text-decoration:none;color:inherit;">{stem}</a></h2>
  </div>
  <div class="card-footer">
    <a class="card-link" href="{href}">Read report →</a>
  </div>
</div>""")
    return "\n".join(cards)


def build_homepage():
    latest = _get_latest_articles(6)
    article_cards = _article_cards(latest)

    content = """
<div class="hero">
  <div class="hero-tag">🏆 FIFA World Cup 2026 · Live Coverage</div>
  <h1>World Cup <span>Intelligence Hub</span></h1>
  <p>Live match coverage, group standings, qualification tracking,
     host city guides, and AI-generated match reports — all in one place.</p>
  <div class="hero-flags">
    <span class="hero-flag">🇨🇦 Canada</span>
    <span class="hero-flag">🇲🇽 Mexico</span>
    <span class="hero-flag">🇺🇸 United States</span>
  </div>
</div>

<div class="stats-bar">
  <div class="stat-box">
    <div class="stat-num">48</div>
    <div class="stat-label">Teams</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">104</div>
    <div class="stat-label">Matches</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">16</div>
    <div class="stat-label">Host Cities</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">12</div>
    <div class="stat-label">Groups</div>
  </div>
</div>

<div class="section-header">
  <div class="section-title">Latest Reports</div>
  <a class="section-more" href="/articles/index.html">All reports →</a>
</div>
<div class="article-grid">
""" + article_cards + """
</div>

<hr class="divider">

<div class="section-header">
  <div class="section-title">Coverage</div>
</div>
<div class="fixture-grid">
  <div class="fixture-card upcoming">
    <div class="fixture-meta">
      <span class="fixture-stage">Navigate</span>
    </div>
    <div style="padding:.25rem 0;">
      <div style="font-family:var(--ff-head);font-size:17px;color:var(--text);margin-bottom:.5rem;">
        📅 Upcoming Fixtures
      </div>
      <div style="font-size:13px;color:var(--text-2);margin-bottom:.75rem;">
        Next scheduled World Cup matches, sorted by date.
      </div>
      <a class="card-link" href="/upcoming.html">View fixtures →</a>
    </div>
  </div>
  <div class="fixture-card upcoming">
    <div class="fixture-meta">
      <span class="fixture-stage">Navigate</span>
    </div>
    <div style="padding:.25rem 0;">
      <div style="font-family:var(--ff-head);font-size:17px;color:var(--text);margin-bottom:.5rem;">
        📊 Qualification Tracker
      </div>
      <div style="font-size:13px;color:var(--text-2);margin-bottom:.75rem;">
        Group standings and who's through to the knockout stage.
      </div>
      <a class="card-link" href="/qualification.html">View tracker →</a>
    </div>
  </div>
  <div class="fixture-card upcoming">
    <div class="fixture-meta">
      <span class="fixture-stage">Navigate</span>
    </div>
    <div style="padding:.25rem 0;">
      <div style="font-family:var(--ff-head);font-size:17px;color:var(--text);margin-bottom:.5rem;">
        🗓️ Tournament Timeline
      </div>
      <div style="font-size:13px;color:var(--text-2);margin-bottom:.75rem;">
        Key events and results as the tournament unfolds.
      </div>
      <a class="card-link" href="/timeline.html">View timeline →</a>
    </div>
  </div>
  <div class="fixture-card upcoming">
    <div class="fixture-meta">
      <span class="fixture-stage">Navigate</span>
    </div>
    <div style="padding:.25rem 0;">
      <div style="font-family:var(--ff-head);font-size:17px;color:var(--text);margin-bottom:.5rem;">
        🌆 Host Cities
      </div>
      <div style="font-size:13px;color:var(--text-2);margin-bottom:.75rem;">
        Stadiums, attractions, and city guides for every venue.
      </div>
      <a class="card-link" href="/host-cities.html">Explore cities →</a>
    </div>
  </div>
</div>
"""

    html = build_page("World Cup Intelligence Hub", content, active_nav="Home")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[HOMEPAGE] Updated")
