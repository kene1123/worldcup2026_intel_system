# WORLD CUP SCHEDULER

import schedule
import time

from main import run_engine


def start_scheduler():

    print(
        "[SCHEDULER] Started"
    )

    schedule.every().day.at(
        "08:00"
    ).do(run_engine)

    schedule.every().day.at(
        "12:00"
    ).do(run_engine)

    schedule.every().day.at(
        "16:00"
    ).do(run_engine)

    schedule.every().day.at(
        "20:00"
    ).do(run_engine)

    while True:

        schedule.run_pending()

        time.sleep(30)


if __name__ == "__main__":

    start_scheduler()