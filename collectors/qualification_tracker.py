# WORLD CUP QUALIFICATION TRACKER

from collectors.standings import (
    fetch_world_cup_standings
)


def get_qualification_status():

    standings = (
        fetch_world_cup_standings()
    )

    groups = []

    for group in standings:

        table = group["table"]

        qualified = []
        danger = []

        for team in table:

            # Simple V1 logic

            if team["position"] <= 2:

                qualified.append(
                    team["team"]
                )

            else:

                danger.append(
                    team["team"]
                )

        groups.append({

            "group":
            group["group"],

            "qualified":
            qualified,

            "danger":
            danger
        })

    return groups