# PRE MATCH PAYLOAD BUILDER

def build_pre_match_payload(match):

    return {

        "fixture_id": match["fixture_id"],

        "home_team": match["home_team"],

        "away_team": match["away_team"],

        "group": match["group"],

        "stage": match["stage"],

        "matchday": match["matchday"],

        "date": match["date"],

        "status": match["status"]
    }