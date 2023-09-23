import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/online-qualification-2")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 2023 ICPC Asia Regionals Online Contest (II)"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-09-23 12:00:00")
    c.end_time = utils.get_timestamp_second("2023-09-23 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, FETCH_URI, c)


if __name__ == "__main__":
    main()
