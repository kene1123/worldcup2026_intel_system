def build_group_prediction_payload(
    prediction
):

    return {

        "headline":
        (
            f"{prediction['group']} "
            f"Winner Prediction"
        ),

        "group":
        prediction["group"],

        "favorite":
        prediction["favorite"],

        "points":
        prediction["points"],

        "reason":
        prediction["reason"]
    }