from pathlib import Path


OUTPUT_DIR = Path("output/website")


def save_article(article, title):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = (
    title.replace(":", "")
         .replace("/", "-")
         .replace("?", "")
         .replace("*", "")
         .replace('"', "")
         .replace("<", "")
         .replace(">", "")
         .replace("|", "")
)

    filepath = OUTPUT_DIR / f"{safe_title}.md"

    with open(filepath, "w", encoding="utf-8") as f:

        f.write(article)

    print(f"[SAVED] {filepath}")

    return filepath