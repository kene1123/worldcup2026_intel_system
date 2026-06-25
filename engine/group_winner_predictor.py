# GROUP WINNER PREDICTOR


def predict_group_winner(group_data):

    table = group_data["table"]

    if not table:
        return None

    leader = sorted(
        table,
        key=lambda x: (
            x["points"],
            x["goal_difference"],
            x["goals_for"]
        ),
        reverse=True
    )[0]

    return {

        "group": group_data["group"],

        "favorite": leader["team"],

        "points": leader["points"],

        "goal_difference":
        leader["goal_difference"],

        "reason":
        (
            f"Top of the group with "
            f"{leader['points']} points"
        )
    }