# KNOCKOUT STAGE DETECTOR


def get_tournament_phase(match):

    stage = match["stage"]

    knockout_stages = [

        "ROUND_OF_32",
        "ROUND_OF_16",

        "QUARTER_FINALS",

        "SEMI_FINALS",

        "THIRD_PLACE",

        "FINAL"
    ]

    if stage in knockout_stages:

        return {

            "phase": "knockout",

            "stage": stage
        }

    return {

        "phase": "group",

        "stage": stage
    }