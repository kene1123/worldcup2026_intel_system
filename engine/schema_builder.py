# WORLD CUP ARTICLE SCHEMA BUILDER

def build_match_schema(match):

    return {

        # Core Match Info
        "fixture_id": match["fixture_id"],
        "date": match["date"],
        "status": match["status"],

        # Competition Context
        "matchday": match["matchday"],
        "stage": match["stage"],
        "group": match["group"],

        # Teams
        "home_team": match["home_team"],
        "away_team": match["away_team"],

        # Result
        "home_score": match["home_score"],
        "away_score": match["away_score"]
    }