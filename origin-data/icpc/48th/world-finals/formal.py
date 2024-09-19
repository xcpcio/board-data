import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/world-finals")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 48th ICPC World Finals"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-09-19 13:55:00")
    c.end_time = utils.get_timestamp_second("2024-09-19 18:55:00")
    c.group = {}

    c.medal = {
        "all": {
            "gold": 4,
            "silver": 4,
            "bronze": 4,
        },
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
