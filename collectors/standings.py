# WORLD CUP STANDINGS COLLECTOR

from core.api_client import (
    get_standings
)

from core.cache import (
    load_cache,
    save_cache
)


COMPETITION_ID = 2000


def fetch_world_cup_standings():

    print(
        "[STANDINGS] Fetching standings"
    )

    data = get_standings(
        COMPETITION_ID
    )

    if not data:

        print(
            "[STANDINGS] API unavailable"
        )

        cache = load_cache()

        standings = cache.get(
            "standings",
            []
        )

        if standings:

            print(
                f"[STANDINGS] Using cached standings "
                f"({len(standings)} groups)"
            )

            return standings

        return []

    standings = []

    for group in data.get(
        "standings",
        []
    ):

        group_name = group.get(
            "group"
        )

        table = []

        for team in group.get(
            "table",
            []
        ):

            table.append({

                "position":
                team["position"],

                "team":
                team["team"]["name"],

                "played":
                team["playedGames"],

                "won":
                team["won"],

                "draw":
                team["draw"],

                "lost":
                team["lost"],

                "points":
                team["points"],

                "goals_for":
                team["goalsFor"],

                "goals_against":
                team["goalsAgainst"],

                "goal_difference":
                team["goalDifference"]
            })

        standings.append({

            "group":
            group_name,

            "table":
            table
        })

    cache = load_cache()

    cache["standings"] = standings

    save_cache(cache)

    print(
        f"[STANDINGS] Saved "
        f"{len(standings)} groups"
    )

    return standings