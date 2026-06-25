# WORLD CUP CONTENT ROUTER

from engine.schema_builder import (
    build_match_schema
)

from engine.post_match import (
    build_post_match_payload
)

from engine.pre_match import (
    build_pre_match_payload
)

from ai.prompts import (
    build_post_match_prompt,
    build_pre_match_prompt
)

from ai.generator import (
    generate_article
)


def process_match(match):

    schema = build_match_schema(match)

    status = schema["status"]

    # POST MATCH

    if status == "FINISHED":

        payload = build_post_match_payload(
            schema
        )

        prompt = build_post_match_prompt(
            payload
        )

        article = generate_article(
            prompt
        )

        return {

            "content_type":
            "post_match",

            "payload":
            payload,

            "article":
            article
        }

    # PRE MATCH
    
    elif status == "TIMED":

        payload = build_pre_match_payload(
            schema
        )

        prompt = build_pre_match_prompt(
            payload
        )

        article = generate_article(
            prompt
        )

        return {

            "content_type":
            "pre_match",

            "payload":
            payload,

            "article":
            article
        }

    return None