"""
group_center_builder.py — World Cup Intelligence Hub
Builds public/groups/group_X.html for every group.
Data shape from fetch_world_cup_standings():
  [{"group": "Group A", "table": [{"position", "team", "played",
    "won", "draw", "lost", "points", "goals_for", "goals_against",
    "goal_difference"}, ...]}, ...]
"""
from pathlib import Path
from collectors.standings import fetch_world_cup_standings
from website.templates import build_page

PUBLIC_GROUPS_DIR = Path("public/groups")


def build_group_pages():
    standings = fetch_world_cup_standings()

    PUBLIC_GROUPS_DIR.mkdir(parents=True, exist_ok=True)

    if not standings:
        print("[GROUP PAGES] No standings data available")
        return

    for group in standings:
        group_name = group["group"]          # e.g. "Group A"
        table      = group["table"]          # list of team dicts

        rows = ""
        for team in table:
            i         = team["position"] - 1
            rank_cls  = "rank-q" if team["position"] <= 2 else "rank-n"
            gd        = team["goal_difference"]
            gd_str    = f"+{gd}" if gd > 0 else str(gd)
            adv       = team["position"] <= 2

            status_html = (
                '<span class="qual-status qual-qualified" '
                'style="font-size:11px;">✓ Advancing</span>'
                if adv else
                '<span class="qual-status qual-danger" '
                'style="font-size:11px;">Needs results</span>'
            )

            rows += f"""
<tr>
  <td>
    <div class="rank-cell">
      <span class="rank-badge {rank_cls}">{team['position']}</span>
      {team['team']}
    </div>
  </td>
  <td>{team['played']}</td>
  <td>{team['won']}</td>
  <td>{team['draw']}</td>
  <td>{team['lost']}</td>
  <td>{team['goals_for']}</td>
  <td>{team['goals_against']}</td>
  <td>{gd_str}</td>
  <td class="pts-col">{team['points']}</td>
  <td>{status_html}</td>
</tr>"""

        content = f"""
<div class="section-header">
  <div class="section-title">{group_name}</div>
  <a class="section-more" href="/qualification.html">All groups →</a>
</div>

<div class="standings-wrap">
  <div class="standings-group-head">
    <span class="standings-group-name">Current Standings</span>
    <span class="text-muted" style="font-size:12px;">Updated live</span>
  </div>
  <table>
    <thead>
      <tr>
        <th>Team</th>
        <th>P</th><th>W</th><th>D</th><th>L</th>
        <th>GF</th><th>GA</th><th>GD</th>
        <th>Pts</th><th>Status</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="qualify-note">Top 2 teams advance to the Round of 32</div>
</div>

<hr class="divider">

<div class="section-header" style="margin-top:1.5rem;">
  <div class="section-title">All Groups</div>
</div>
<div class="pill-row">
  <a class="pill active" href="#">{group_name}</a>
  <a class="pill" href="/qualification.html">Full tracker</a>
</div>
"""

        slug     = group_name.replace(" ", "_").lower()   # group_a
        out_file = PUBLIC_GROUPS_DIR / f"{slug}.html"

        html = build_page(
            group_name,
            content,
            active_nav="Qualification",
            description=f"World Cup 2026 {group_name} standings and qualification outlook."
        )

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"[GROUP PAGES] Generated {len(standings)} pages")
