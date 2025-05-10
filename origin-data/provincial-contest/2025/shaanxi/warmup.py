import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/shaanxi-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025 Shaanxi Provincial Collegiate Programming Contest (Warm up)"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2025-05-10 10:01:52")
    c.end_time = utils.get_timestamp_second("2025-05-10 11:10:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
