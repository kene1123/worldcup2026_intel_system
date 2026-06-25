def build_qualification_payload(data):

    return {

        "headline":
        f"{data['group']} Qualification Update",

        "group":
        data["group"],

        "qualified":
        data["qualified"],

        "danger":
        data["danger"]
    }