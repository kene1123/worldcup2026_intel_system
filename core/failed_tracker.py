# FAILED ARTICLE TRACKER

import json
import os


FAILED_FILE = (
    "storage/failed_articles.json"
)


def load_failed():

    if not os.path.exists(
        FAILED_FILE
    ):

        return {
            "failed_pre_match": [],
            "failed_post_match": []
        }

    with open(
        FAILED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_failed(data):

    with open(
        FAILED_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def add_failed(
    fixture_id,
    content_type
):

    data = load_failed()

    key = (
        "failed_pre_match"
        if content_type == "pre_match"
        else
        "failed_post_match"
    )

    if fixture_id not in data[key]:

        data[key].append(
            fixture_id
        )

        save_failed(data)


def remove_failed(
    fixture_id,
    content_type
):

    data = load_failed()

    key = (
        "failed_pre_match"
        if content_type == "pre_match"
        else
        "failed_post_match"
    )

    if fixture_id in data[key]:

        data[key].remove(
            fixture_id
        )

        save_failed(data)