import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/hubei")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 2024 ICPC in Hubei Province, China"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-04-27 10:00:00")
    c.end_time = utils.get_timestamp_second("2024-04-27 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
