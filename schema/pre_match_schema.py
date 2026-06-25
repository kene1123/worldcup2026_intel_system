# PRE MATCH CONTENT BUILDER

def build_pre_match_payload(match):

    return {

        "headline":
        (
            f"{match['home_team']} vs "
            f"{match['away_team']}: "
            f"World Cup Match Preview"
        ),

        "home_team":
        match["home_team"],

        "away_team":
        match["away_team"],

        "group":
        match["group"],

        "stage":
        match["stage"],

        "matchday":
        match["matchday"],

        "date":
        match["date"],

        "status":
        match["status"]
    }