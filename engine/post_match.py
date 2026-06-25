# POST MATCH CONTENT BUILDER

def build_post_match_payload(schema):

    home_team = schema["home_team"]
    away_team = schema["away_team"]

    home_score = schema["home_score"]
    away_score = schema["away_score"]

    if home_score > away_score:
        winner = home_team

    elif away_score > home_score:
        winner = away_team

    else:
        winner = "Draw"

    return {

        "fixture_id": schema["fixture_id"],

        "headline": (
            f"{home_team} {home_score}-{away_score} "
            f"{away_team}: World Cup Match Report"
        ),

        "winner": winner,

        "group": schema["group"],

        "stage": schema["stage"],

        "home_team": home_team,
        "away_team": away_team,

        "home_score": home_score,
        "away_score": away_score,

        "matchday": schema["matchday"],

        "status": schema["status"],

        "date": schema["date"]
    }