"""
qualification_builder.py — World Cup Intelligence Hub
get_qualification_status() returns:
  [{"group": "Group A", "qualified": ["TeamA", "TeamB"],
    "danger": ["TeamC", "TeamD"]}, ...]
fetch_world_cup_standings() returns:
  [{"group": "Group A", "table": [{...}]}, ...]
"""
from pathlib import Path
from collectors.qualification_tracker import get_qualification_status
from collectors.standings import fetch_world_cup_standings
from website.templates import build_page
from utils.country_flags import get_flag

OUTPUT_FILE = Path("public/qualification.html")


def build_qualification_page():
    try:
        standings_list = fetch_world_cup_standings()
        qual_list      = get_qualification_status()
    except Exception as e:
        print(f"[QUAL] Data error: {e}")
        standings_list = []
        qual_list      = []

    qual_lookup = {g["group"]: g for g in qual_list}

    if not standings_list:
        content = """
<div class="section-header">
  <div class="section-title">Qualification Tracker</div>
</div>
<div class="empty">
  <div class="empty-icon">📊</div>
  <p>Standings data is loading. Check back after the next match.</p>
</div>
"""
        _write(content)
        print("[QUALIFICATION] Updated (no data)")
        return

    group_sections = []

    for group in standings_list:
        group_name = group["group"]
        table      = group["table"]
        qual       = qual_lookup.get(group_name, {})
        qualified  = set(qual.get("qualified", []))
        danger     = set(qual.get("danger", []))

        rows = ""
        for team in table:
            name     = team["team"]
            rank_cls = "rank-q" if team["position"] <= 2 else "rank-n"
            gd       = team["goal_difference"]
            gd_str   = f"+{gd}" if gd > 0 else str(gd)

            if name in qualified:
                badge = '<span class="qual-status qual-qualified">&#10003; Advancing</span>'
            elif name in danger:
                badge = '<span class="qual-status qual-danger">Needs results</span>'
            else:
                badge = '<span class="qual-status qual-contention">In contention</span>'

            rows += f"""
<tr>
  <td><div class="rank-cell">
    <span class="rank-badge {rank_cls}">{team['position']}</span>{get_flag(name)} {name}
  </div></td>
  <td>{team['played']}</td>
  <td>{team['won']}</td>
  <td>{team['draw']}</td>
  <td>{team['lost']}</td>
  <td>{team['goals_for']}</td>
  <td>{team['goals_against']}</td>
  <td>{gd_str}</td>
  <td class="pts-col">{team['points']}</td>
  <td>{badge}</td>
</tr>"""

        slug = group_name.replace(" ", "_").lower()
        group_sections.append(f"""
<div class="standings-wrap" style="margin-bottom:1.25rem;">
  <div class="standings-group-head">
    <span class="standings-group-name">{group_name}</span>
    <a class="section-more" href="/groups/{slug}.html" style="font-size:12px;">Group page</a>
  </div>
  <table>
    <thead><tr>
      <th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th>
      <th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Status</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="qualify-note">Top 2 teams advance to Round of 32</div>
</div>""")

    legend = """
<div class="pill-row" style="margin-bottom:1.5rem;">
  <span class="qual-status qual-qualified" style="border-radius:20px;padding:4px 12px;">&#10003; Advancing</span>
  <span class="qual-status qual-contention" style="border-radius:20px;padding:4px 12px;">In contention</span>
  <span class="qual-status qual-danger" style="border-radius:20px;padding:4px 12px;">Needs results</span>
</div>"""

    content = f"""
<div class="section-header">
  <div class="section-title">Qualification Tracker</div>
  <span class="text-muted" style="font-size:13px;">Updated after each match</span>
</div>
{legend}
{"".join(group_sections)}
"""
    _write(content)
    print("[QUALIFICATION] Updated")


def _write(content):
    html = build_page(
        "Qualification Tracker",
        content,
        active_nav="Qualification",
        description="World Cup 2026 live group standings and qualification status."
    )
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
