from collectors.standings import (
    fetch_world_cup_standings
)

from schema.daily_recap_schema import (
    build_daily_recap_payload
)

from ai.prompts import (
    build_daily_recap_prompt
)

from ai.generator import (
    generate_article
)


def generate_daily_recap():

    standings = (
        fetch_world_cup_standings()
    )

    payload = (
        build_daily_recap_payload(
            standings
        )
    )

    prompt = (
        build_daily_recap_prompt(
            payload
        )
    )

    article = (
        generate_article(
            prompt
        )
    )

    return article