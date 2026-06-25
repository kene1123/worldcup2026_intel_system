# ARTICLE PROMPT BUILDER

def build_post_match_prompt(payload):

    return f"""
You are an elite football journalist covering the FIFA World Cup.

Write a professional, engaging, SEO-friendly match report.

MATCH INFORMATION

Headline:
{payload['headline']}

Stage:
{payload['stage']}

Group:
{payload['group']}

Teams:
{payload['home_team']} vs {payload['away_team']}

Result:
{payload['home_score']} - {payload['away_score']}

Winner:
{payload['winner']}

Requirements:

- Write between 500 and 800 words
- Use a journalistic tone
- Discuss the result and its significance
- Discuss tournament implications
- Discuss standings implications when relevant
- Focus on verified information only

Strict Rules:

- Do not invent goalscorers
- Do not invent player names
- Do not invent match events
- Do not invent stadiums
- Do not invent cities
- Do not invent attendance
- Do not invent possession statistics
- Do not invent tactical details
- Do not invent quotes
- No false host city or stadium 
- We are talking about the FIFA World Cup 2026, so do not invent any information
- Do not invent players, statistics or quotes
- Only use information provided in the match data.

If information is unavailable, discuss the result, tournament context, and implications instead.

Output only the article.
"""

# PRE MATCH ARTICLE PROMPT

def build_pre_match_prompt(payload):

    return f"""
You are a professional football journalist.

Write a detailed World Cup pre-match preview.

Match:
{payload['home_team']} vs {payload['away_team']}

Group:
{payload['group']}

Stage:
{payload['stage']}

Requirements:

- Strong headline
- Introduction
- What is at stake
- Tactical expectations
- Historical context if relevant
- Prediction section
- No invented statistics
- No invented player information
- Do not invent player names
- Do not invent match events
- Do not invent stadiums
- Do not invent cities
- Do not invent attendance
- Conclusion

Length:
500-700 words.

Use engaging football journalism style.

Add relevant hashtags at the end.
"""

def build_daily_recap_prompt(payload):

    summary = ""

    for group in payload["groups"]:

        summary += (
            f"{group['group']}:\n"
            f"1st {group['leader']} "
            f"({group['leader_points']} pts)\n"
            f"2nd {group['second']} "
            f"({group['second_points']} pts)\n\n"
        )

    return f"""
You are an elite football journalist.

Write a FIFA World Cup Daily Recap article.

Current Group Leaders:

{summary}

Requirements:

- 500 to 700 words
- Professional football journalism style
- Discuss qualification races
- Discuss standout groups
- Explain tournament implications
- SEO friendly
- No invented statistics
- No invented player information
- Add hashtags at the end

Strict Rules:

- Do not invent goalscorers
- Do not invent player names
- Do not invent match events
- Do not invent stadiums
- Do not invent cities
- Do not invent attendance
- Do not invent possession statistics
- Do not invent tactical details
- Do not invent quotes

Output only the article.
"""

def build_qualification_prompt(payload):

    return f"""
You are a World Cup analyst.

Write a qualification update article.

Group:
{payload['group']}

Currently in qualification positions:
{", ".join(payload['qualified'])}

Currently outside qualification positions:
{", ".join(payload['danger'])}

Requirements:

- Explain current situation
- Discuss qualification race
- Discuss pressure on teams below the line
- 400-600 words
- Professional football journalism style

Output only article.
"""

def build_group_prediction_prompt(
    payload
):

    return f"""
You are a football analyst.

Write a World Cup group winner prediction article.

Group:
{payload['group']}

Current Favorite:
{payload['favorite']}

Points:
{payload['points']}

Reason:
{payload['reason']}

Requirements:

- Explain why this team leads the group
- Discuss qualification situation
- Discuss possible threats
- Professional football journalism tone
- 400-600 words

Output only article.
"""

def build_knockout_prompt(
    payload
):

    return f"""
You are a World Cup football journalist.

Write a knockout stage preview.

Match:
{payload['home_team']}
vs
{payload['away_team']}

Stage:
{payload['stage']}

Requirements:

- Explain knockout stakes
- Explain winner advances
- Explain loser is eliminated
- Discuss tactical expectations
- Discuss tournament pressure
- Professional football journalism tone
- 500-700 words

Output only article.
"""