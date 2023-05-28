import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/zhejiang")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 20th Zhejiang Provincial Collegiate Programming Contest Sponsored by TuSimple"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-04-15 12:00:00")
    c.end_time = utils.get_timestamp_second("2023-04-15 17:00:00")

    c.medal = {
        "undergraduate": {
            "gold": 18,
            "silver": 40,
            "bronze": 57,
        },
        "vocational": {
            "gold": 11,
            "silver": 22,
            "bronze": 34,
        }
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
