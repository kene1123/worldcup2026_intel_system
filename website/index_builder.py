"""
index_builder.py — World Cup Intelligence Hub
Builds output/website/index.md.
Contract is unchanged from original — main.py calls build_index().
"""
from pathlib import Path

WEBSITE_DIR = Path("output/website")


def build_index():
    WEBSITE_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        [f for f in WEBSITE_DIR.glob("*.md")
         if f.name not in ("index.md", "timeline.md", "qualification_watch.md")],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    lines = [
        "# World Cup Intelligence Hub",
        "",
        "Auto-generated content index.",
        "",
        "## Latest Articles",
        "",
    ]

    for f in files[:30]:
        lines.append(f"- {f.stem}")

    index_path = WEBSITE_DIR / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("[INDEX] Website index updated")
