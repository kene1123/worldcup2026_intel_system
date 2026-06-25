import time
import requests

from config import BASE_URL, HEADERS

# SAFE REQUEST HANDLER

def _make_request(
    endpoint,
    params=None,
    retries=3
):

    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(1, retries + 1):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:

            print(
                f"[API] Timeout "
                f"(Attempt {attempt}/{retries})"
            )

        except requests.exceptions.ConnectionError:

            print(
                f"[API] Connection Error "
                f"(Attempt {attempt}/{retries})"
            )

        except requests.exceptions.HTTPError as e:

            print(
                f"[API] HTTP Error: {e}"
            )

            return None

        except Exception as e:

            print(
                f"[API] Unexpected Error: {e}"
            )

        if attempt < retries:

            print(
                "[API] Retrying in 3 seconds..."
            )

            time.sleep(3)

    print(
        "[API] Request Failed"
    )

    return None

# ENDPOINT HELPERS

def get_teams(competition_id):

    return _make_request(
        f"competitions/{competition_id}/teams"
    )


def get_fixtures(
    competition_id,
    season=None
):

    params = (
        {"season": season}
        if season
        else None
    )

    return _make_request(
        f"competitions/{competition_id}/matches",
        params=params
    )


def get_standings(
    competition_id,
    season=None
):

    params = (
        {"season": season}
        if season
        else None
    )

    return _make_request(
        f"competitions/{competition_id}/standings",
        params=params
    )