# DAILY RECAP PAYLOAD BUILDER

def build_daily_recap_payload(standings):

    groups = []

    for group in standings:

        groups.append({

            "group":
            group["group"],

            "leader":
            group["table"][0]["team"],

            "leader_points":
            group["table"][0]["points"],

            "second":
            group["table"][1]["team"],

            "second_points":
            group["table"][1]["points"]
        })

    return {

        "groups":
        groups
    }