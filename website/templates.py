"""
templates.py — World Cup Intelligence Hub
Drop-in replacement for the old templates.py.
build_page() has the same signature — the rest of your backend is untouched.
"""

NAV_LINKS = [
    ("/index.html",        "Home"),
    ("/upcoming.html",     "Fixtures"),
    ("/qualification.html","Qualification"),
    ("/timeline.html",     "Timeline"),
    ("/articles/index.html","Reports"),
    ("/host-cities.html",  "Host Cities"),
]


def _nav_html(active_title=""):
    items = []
    for href, label in NAV_LINKS:
        active = ' class="active"' if label == active_title else ''
        items.append(f'<a href="{href}"{active}>{label}</a>')
    return "\n".join(items)


def build_page(title, content, active_nav="", description=""):
    """
    Drop-in replacement for the original build_page().
    Same 2-arg call still works: build_page(title, content)
    Extra kwargs are optional enhancements.
    """
    desc = description or f"{title} — World Cup 2026 Intelligence Hub"
    nav  = _nav_html(active_nav or title.split("|")[0].strip())

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title} | World Cup Intelligence Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>

<header>
  <div class="header-inner">
    <a class="site-brand" href="/index.html">
      <div class="brand-icon">⚽</div>
      <div>
        <div class="brand-label">World Cup Hub</div>
        <div class="brand-sub">FIFA 2026 · Live Intelligence</div>
      </div>
    </a>
    <nav>
      {nav}
    </nav>
  </div>
</header>

<main>
{content}
</main>

<footer>
  <div class="footer-inner">
    <div class="footer-brand">⚽ World Cup Intelligence Hub</div>
    <div class="footer-note">FIFA World Cup 2026 · Canada · Mexico · United States</div>
    <div class="footer-links">
      <a href="/index.html">Home</a>
      <a href="/upcoming.html">Fixtures</a>
      <a href="/articles/index.html">Reports</a>
      <a href="/host-cities.html">Host Cities</a>
    </div>
  </div>
</footer>

<a id="btt" href="#" aria-label="Back to top">↑</a>

<script>
window.addEventListener('scroll', function() {{
  document.getElementById('btt').classList.toggle('show', window.scrollY > 300);
}});
</script>

</body>
</html>"""


def build_article_page(title, body_html, label="Match Report", tag_class="report"):
    """
    Specialised page builder for match reports and previews.
    Wraps article content with editorial typography.
    """
    content = f"""
<div class="article-page">
  <div class="card-label" style="margin-bottom:1rem;">
    <span class="tag" style="font-size:11px;padding:3px 10px;">{label}</span>
  </div>
  <h1 class="article-headline">{title}</h1>
  <div class="article-byline">
    <span class="byline-source">⚡ World Cup Intelligence Hub</span>
    <span>FIFA World Cup 2026</span>
    <span>AI-generated report</span>
  </div>
  <div class="article-body">
    {body_html}
  </div>
</div>
"""
    return build_page(title, content, active_nav="Reports")
