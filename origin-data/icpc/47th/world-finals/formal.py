import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/47th/world-finals")
FETCH_URI = os.getenv(
    "FETCH_URI", "https://scoreboard.icpc.global/47/index.html")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 47th ICPC World Finals"
    c.problem_quantity = 11
    c.start_time = utils.get_timestamp_second("2024-04-18 17:48:00")
    c.end_time = utils.get_timestamp_second("2024-04-18 22:48:00")

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
