# X THREAD GENERATOR + SAVER

from pathlib import Path


OUTPUT_DIR = Path("output/x_posts")


def generate_x_thread(payload):

    home = payload["home_team"]
    away = payload["away_team"]

    home_score = payload["home_score"]
    away_score = payload["away_score"]

    winner = payload["winner"]

    thread = []

    # Post 1

    thread.append(
        f"🚨 FULL TIME\n\n"
        f"{home} {home_score}-{away_score} {away}\n\n"
        f"{winner} take all three points in "
        f"{payload['group']}.\n\n"
        f"#FifaWorldCup #WorldCup2026 "
        f"#{home.replace(' ', '')}"
        f"#{away.replace(' ', '')}"
    )

    # Post 2

    thread.append(
        f"📊 MATCH SUMMARY\n\n"
        f"Stage: {payload['stage']}\n"
        f"Matchday: {payload['matchday']}\n"
        f"Result: {home} {home_score}-{away_score} {away}"
    )

    # Post 3

    thread.append(
        f"🌍 TOURNAMENT IMPACT\n\n"
        f"{winner} strengthen their position "
        f"in the competition after this result."
    )

    return thread


def save_x_thread(thread, title):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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

    filepath = OUTPUT_DIR / f"{safe_title}.txt"

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        for i, tweet in enumerate(
            thread,
            start=1
        ):

            f.write(
                f"\n--- POST {i} ---\n\n"
            )

            f.write(tweet)

            f.write("\n\n")

    print(
        f"[X SAVED] {filepath}"
    )

    return filepath