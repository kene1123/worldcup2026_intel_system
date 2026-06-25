# WORLD CUP ENGINE

from datetime import (
    datetime,
    timezone
)

from collectors.fixtures import (
    fetch_world_cup_fixtures
)

from core.state_tracker import (
    load_processed,
    save_processed
)

from core.failed_tracker import (
    load_failed,
    add_failed,
    remove_failed
)

from engine.content_router import (
    process_match
)

from publishers.website import (
    save_article
)

from publishers.medium import (
    save_medium_article
)

from publishers.x_posts import (
    generate_x_thread,
    save_x_thread
)

from website.index_builder import (
    build_index
)

from website.timeline_builder import (
    add_event,
    build_timeline_page
)

from website.qualification_builder import (
    build_qualification_page
)

from website.group_center_builder import (
    build_group_pages
)

from website.site_builder import (
    build_article_pages
)

from website.homepage_builder import (
    build_homepage
)

from website.upcoming_builder import (
    build_upcoming_page
)

from website.search_builder import (
    build_search_index
)   

from website.host_city_builder import (
    build_host_city_page
)

FAILED_ARTICLE_TEXT = (
    "Article generation failed"
)

MAX_ARTICLES_PER_RUN = 4


def run_engine():

    print(
        "\n[ENGINE] Starting World Cup Engine"
    )

    fixtures = fetch_world_cup_fixtures()

    processed = load_processed()

    failed = load_failed()

    pre_processed = processed[
        "processed_pre_match"
    ]

    post_processed = processed[
        "processed_post_match"
    ]

    failed_pre = failed[
        "failed_pre_match"
    ]

    failed_post = failed[
        "failed_post_match"
    ]

    matches_to_process = []

    now = datetime.now(
        timezone.utc
    )

    # ---------------------------------
    # PRIORITY 1
    # RETRY FAILED ARTICLES FIRST
    # ---------------------------------

    failed_ids = set(
        failed_pre + failed_post
    )

    for match in fixtures:

        if (
            match["fixture_id"]
            in
            failed_ids
        ):

            matches_to_process.append(
                match
            )

    # ---------------------------------
    # PRIORITY 2
    # NEW ARTICLES
    # ---------------------------------

    for match in fixtures:

        fixture_id = match[
            "fixture_id"
        ]

        status = match[
            "status"
        ]

        if fixture_id in failed_ids:
            continue

        fixture_time = (
            datetime.fromisoformat(
                match["date"].replace(
                    "Z",
                    "+00:00"
                )
            )
        )

        hours_until_match = (
            fixture_time - now
        ).total_seconds() / 3600

        # PRE-MATCH

        if (
            status == "TIMED"
            and
            fixture_id not in pre_processed
            and
            0 <= hours_until_match <= 24
        ):

            matches_to_process.append(
                match
            )

        # POST-MATCH

        elif (
            status == "FINISHED"
            and
            fixture_id not in post_processed
        ):

            matches_to_process.append(
                match
            )

    print(
        f"[ENGINE] Total queue: "
        f"{len(matches_to_process)}"
    )

    # SAFETY LIMIT

    matches_to_process = (
        matches_to_process[
            :MAX_ARTICLES_PER_RUN
        ]
    )

    print(
        f"[ENGINE] Processing "
        f"{len(matches_to_process)} items"
    )

    # ---------------------------------
    # PROCESS MATCHES
    # ---------------------------------

    for match in matches_to_process:

        result = process_match(
            match
        )

        if not result:
            continue

        payload = result[
            "payload"
        ]

        article = result[
            "article"
        ]

        content_type = result[
            "content_type"
        ]

        fixture_id = payload[
            "fixture_id"
        ]

        title = payload.get(
            "headline",
            f"{payload['home_team']} vs "
            f"{payload['away_team']}"
        )

        print(
            f"\n[PROCESSING] "
            f"{title}"
        )

        save_article(
            article,
            title
        )

        save_medium_article(
            article,
            title
        )

        if (
            content_type
            ==
            "post_match"
        ):

            thread = (
                generate_x_thread(
                    payload
                )
            )

            save_x_thread(
                thread,
                title
            )

        # ------------------------------
        # SUCCESS
        # ------------------------------

        if (
            article
            and
            FAILED_ARTICLE_TEXT
            not in article
        ):

            if (
                content_type
                ==
                "pre_match"
            ):

                if (
                    fixture_id
                    not in pre_processed
                ):

                    pre_processed.append(
                        fixture_id
                    )

            else:

                if (
                    fixture_id
                    not in post_processed
                ):

                    post_processed.append(
                        fixture_id
                    )

                add_event(
                    payload
                )

            remove_failed(
                fixture_id,
                content_type
            )

            print(
                f"[SUCCESS] "
                f"{fixture_id}"
            )

        # ------------------------------
        # FAILURE
        # ------------------------------

        else:

            add_failed(
                fixture_id,
                content_type
            )

            print(
                f"[FAILED QUEUED] "
                f"{fixture_id}"
            )

    save_processed(
        processed
    )

    # ---------------------------------
    # WEBSITE BUILDERS
    # ---------------------------------

    build_index()

    build_timeline_page()

    build_qualification_page()

    build_group_pages()

    build_article_pages()

    build_homepage()
    
    build_search_index()
    
    build_upcoming_page()
    
    build_host_city_page()
    
    print(
        "\n[ENGINE] Finished"
    )


if __name__ == "__main__":

    run_engine()