"""
timeline_builder.py — World Cup Intelligence Hub
main.py calls: add_event(payload) and build_timeline_page()
"""
from pathlib import Path
from website.templates import build_page

OUTPUT_FILE  = Path("public/timeline.html")
TIMELINE_MD  = Path("output/website/timeline.md")
EVENTS_FILE  = Path("storage/timeline_events.json")


# ── add_event ─────────────────────────────────────────────────────
def add_event(payload):
    """
    Called by main.py after a successful post-match article.
    Appends event to storage/timeline_events.json.
    """
    import json
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    events = []
    if EVENTS_FILE.exists():
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
        except Exception:
            events = []

    home    = payload.get("home_team", "")
    away    = payload.get("away_team", "")
    score   = payload.get("score", "")
    group   = payload.get("group", "")
    date    = payload.get("date", "")[:10] if payload.get("date") else ""
    headline = payload.get("headline", f"{home} vs {away}")

    event = {
        "date":     date,
        "title":    headline,
        "desc":     f"{home} {score} {away} — {group}".strip(" —"),
        "fixture_id": payload.get("fixture_id", ""),
    }

    # Avoid duplicates by fixture_id
    ids = {e.get("fixture_id") for e in events}
    if event["fixture_id"] not in ids:
        events.append(event)
        events.sort(key=lambda e: e.get("date", ""), reverse=True)

        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    print(f"[TIMELINE] Event added: {headline}")


# ── build_timeline_page ────────────────────────────────────────────
def build_timeline_page():
    events = _load_events()

    if events:
        items = ""
        for e in events:
            desc_html = (
                f"<div class='timeline-desc'>{e['desc']}</div>"
                if e.get("desc") else ""
            )
            items += f"""
<div class="timeline-item">
  <div class="timeline-date">{e.get('date','')}</div>
  <div class="timeline-title">{e.get('title','')}</div>
  {desc_html}
</div>"""
        timeline_html = f'<div class="timeline">{items}</div>'
    else:
        timeline_html = """
<div class="empty">
  <div class="empty-icon">🗓️</div>
  <p>Match results will appear here as the tournament progresses.</p>
</div>"""

    content = f"""
<div class="section-header">
  <div class="section-title">Tournament Timeline</div>
  <span class="text-muted" style="font-size:13px;">Updated after each match day</span>
</div>
{timeline_html}
"""

    html = build_page(
        "Tournament Timeline",
        content,
        active_nav="Timeline",
        description="World Cup 2026 tournament timeline — key results and events."
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[TIMELINE] Updated")


# ── helpers ────────────────────────────────────────────────────────
def _load_events():
    """Load from JSON store first, fall back to parsing timeline.md."""
    import json

    if EVENTS_FILE.exists():
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
            if events:
                return events
        except Exception:
            pass

    return _parse_timeline_md()


def _parse_timeline_md():
    if not TIMELINE_MD.exists():
        return []

    events = []
    current = {}

    with open(TIMELINE_MD, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line:
                if current.get("title"):
                    events.append(current)
                    current = {}
                continue
            if line.startswith("## "):
                if current.get("title"):
                    events.append(current)
                current = {"date": line[3:].strip(), "title": "", "desc": ""}
            elif line.startswith("### ") and current:
                current["title"] = line[4:].strip()
            elif line.startswith("- ") and current:
                current["desc"] = (current.get("desc","") + " " + line[2:].strip()).strip()
            elif current.get("date") and not current.get("title") and line.strip():
                current["title"] = line.strip()

    if current.get("title"):
        events.append(current)

    return [e for e in events if e.get("date") and e.get("title")]
