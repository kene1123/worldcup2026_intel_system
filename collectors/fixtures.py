from core.api_client import _make_request 
from core.cache import load_cache, save_cache 

COMPETITION_ID = 2000 

def fetch_world_cup_fixtures(): 
    print("[FIXTURES] Fetching World Cup fixtures") 
    data = _make_request( 
        f"competitions/{COMPETITION_ID}/matches" 
    ) 
    
    # API FAILED -> USE CACHE 
    if not data: 
        print( 
            "[FIXTURES] API unavailable" 
        ) 
        cache = load_cache() 
        fixtures = cache.get( 
            "fixtures", [] 
        ) 
        if fixtures: 
            print( 
                f"[FIXTURES] Using cached fixtures " 
                f"({len(fixtures)} found)" 
            ) 
            return fixtures 
        print( 
            "[FIXTURES] No cache available" 
        ) 
        return [] 
        
    # API SUCCESS 
    matches = data.get( 
        "matches", [] 
    ) 
    normalized = [] 
    for match in matches: 
        home_score = match["score"]["fullTime"]["home"] 
        away_score = match["score"]["fullTime"]["away"] 
        score = "" 
        if ( 
            home_score is not None and 
            away_score is not None 
        ): 
            score = ( 
                f"{home_score} - {away_score}" 
            ) 
        normalized.append({ 
            "fixture_id": match["id"], 
            "date": match["utcDate"], 
            "status": match["status"], 
            "matchday": match["matchday"], 
            "stage": match["stage"], 
            "group": match.get( 
                "group" 
            ), 
            "home_team": match["homeTeam"]["name"], 
            "away_team": match["awayTeam"]["name"], 
            "home_score": home_score, 
            "away_score": away_score, 
            "score": score 
        }) 
    cache = load_cache() 
    cache["fixtures"] = normalized 
    save_cache(cache) 
    print( 
        f"[FIXTURES] Saved {len(normalized)} fixtures" 
    ) 
    return normalized
