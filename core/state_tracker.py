# PROCESSED CONTENT TRACKER

import json
import os


PROCESSED_FILE = (
    "storage/processed.json"
)


def load_processed():

    if not os.path.exists(
        PROCESSED_FILE
    ):

        return {

            "processed_pre_match": [],

            "processed_post_match": []
        }

    with open(
        PROCESSED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_processed(data):

    with open(
        PROCESSED_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )