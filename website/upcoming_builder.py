"""
upcoming_builder.py — World Cup Intelligence Hub
"""
from pathlib import Path
from datetime import datetime
from collectors.fixtures import fetch_world_cup_fixtures
from website.templates import build_page
from utils.country_flags import get_flag

OUTPUT_FILE = Path("public/upcoming.html")


def _status_pill(status):
    if status in ("IN_PLAY", "PAUSED", "LIVE"):
        return '<span class="fixture-status status-live"><span class="live-dot"></span> LIVE</span>'
    if status == "FINISHED":
        return '<span class="fixture-status status-ft">Full Time</span>'
    return '<span class="fixture-status status-upcoming">Upcoming</span>'


def _card_class(status):
    if status in ("IN_PLAY", "PAUSED", "LIVE"):
        return "live"
    if status == "FINISHED":
        return "finished"
    return "upcoming"


def build_upcoming_page():
    fixtures = fetch_world_cup_fixtures()

    upcoming = sorted(
        [m for m in fixtures if m["status"] == "TIMED"],
        key=lambda x: x["date"]
    )[:20]

    live = [m for m in fixtures if m["status"] in ("IN_PLAY", "PAUSED")]
    recent = sorted(
        [m for m in fixtures if m["status"] == "FINISHED"],
        key=lambda x: x["date"],
        reverse=True
    )[:6]

    def fixture_card(match, cls="upcoming"):
        try:
            dt = datetime.fromisoformat(match["date"].replace("Z", "+00:00"))
            date_str = dt.strftime("%d %b %Y")
            time_str = dt.strftime("%H:%M UTC")
        except Exception:
            date_str = match.get("date", "")
            time_str = ""

        stage = match.get("stage", "Group Stage").replace("_", " ").title()
        home  = match.get("home_team", "TBC")
        away  = match.get("away_team", "TBC")
        score = match.get("score", "")
        status = match.get("status", "TIMED")

        score_html = (
            f'<div class="fixture-score-num">{score}</div>'
            if score and status != "TIMED"
            else '<div class="fixture-score-vs">vs</div>'
        )

        return f"""
<div class="fixture-card {cls}">
  <div class="fixture-meta">
    <span class="fixture-stage">{stage}</span>
    {_status_pill(status)}
  </div>
  <div class="fixture-teams">
    <div class="fixture-team">
      <div class="fixture-team-name">
        {get_flag(home)} {home}
      </div>
    </div>
    <div class="fixture-score">
      {score_html}
      <div class="fixture-time">{date_str}{(' · ' + time_str) if time_str else ''}</div>
    </div>
    <div class="fixture-team">
      {get_flag(away)} {away}
    </div>
  </div>
</div>"""

    live_section = ""
    if live:
        live_cards = "\n".join(fixture_card(m, "live") for m in live)
        live_section = f"""
<div class="section-header">
  <div class="section-title">🔴 Live Now</div>
</div>
<div class="fixture-grid">
{live_cards}
</div>
<hr class="divider">
"""

    recent_section = ""
    if recent:
        recent_cards = "\n".join(fixture_card(m, "finished") for m in recent)
        recent_section = f"""
<div class="section-header" style="margin-top:2rem;">
  <div class="section-title">Recent Results</div>
</div>
<div class="fixture-grid">
{recent_cards}
</div>
<hr class="divider">
"""

    if upcoming:
        upcoming_cards = "\n".join(fixture_card(m, "upcoming") for m in upcoming)
        upcoming_section = f"""
<div class="section-header" style="margin-top:2rem;">
  <div class="section-title">Upcoming Fixtures</div>
  <span class="text-muted" style="font-size:13px;">Next {len(upcoming)} matches</span>
</div>
<div class="fixture-grid">
{upcoming_cards}
</div>
"""
    else:
        upcoming_section = """
<div class="empty">
  <div class="empty-icon">📅</div>
  <p>No upcoming fixtures scheduled at this time.</p>
</div>
"""

    content = live_section + recent_section + upcoming_section

    html = build_page("Fixtures", content, active_nav="Fixtures",
                      description="Upcoming and recent World Cup 2026 fixtures and results.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[UPCOMING] Updated")
