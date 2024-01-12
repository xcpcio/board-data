import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/ecfinal-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 2023 ICPC Asia East Continent Final Contest Warmup"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2024-01-12 15:00:00")
    c.end_time = utils.get_timestamp_second("2024-01-12 17:00:00")
    c.frozen_time = 30 * 60
    c.unfrozen_time = 60 * 60

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
