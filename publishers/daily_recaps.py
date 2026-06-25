from pathlib import Path


OUTPUT_DIR = Path(
    "output/daily_recaps"
)


def save_daily_recap(article):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filepath = (
        OUTPUT_DIR /
        "daily_recap.md"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(article)

    print(
        f"[DAILY RECAP SAVED] "
        f"{filepath}"
    )

    return filepath