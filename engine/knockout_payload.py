def build_knockout_payload(
    match
):

    return {

        "fixture_id":
        match["fixture_id"],

        "home_team":
        match["home_team"],

        "away_team":
        match["away_team"],

        "stage":
        match["stage"],

        "date":
        match["date"],

        "status":
        match["status"]
    }