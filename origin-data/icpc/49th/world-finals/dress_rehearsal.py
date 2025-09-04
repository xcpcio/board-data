import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/49th/world-finals-dress-rehearsal")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "49th ICPC World Finals - Dress Rehearsal"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp_second("2025-09-03 15:00:00")
    c.end_time = utils.get_timestamp_second("2025-04-26 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
