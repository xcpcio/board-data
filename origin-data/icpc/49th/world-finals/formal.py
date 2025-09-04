import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/49th/world-finals")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "49th ICPC World Finals"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2025-09-04 15:00:00")
    c.end_time = utils.get_timestamp_second("2025-09-04 20:00:00")
    c.banner_mode = "ONLY_BANNER"

    c.medal = {}

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
