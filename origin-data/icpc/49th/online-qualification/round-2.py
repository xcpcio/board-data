import os
from pathlib import Path

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/49th/online-qualification-2")
CONTEST_ID = os.getenv("CONTEST_ID", "1835981416207253504")


def get_contest():
    c = common.get_basic_contest()
    c.contest_name = "The 49th ICPC Asia Regionals Online Contest (II)"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-09-21 13:00:00")
    c.end_time = utils.get_timestamp_second("2024-09-21 18:00:00")
    c.fill_problem_id().fill_balloon_color()
    return c


def main():
    c = get_contest()
    common.work(Path(DATA_DIR), CONTEST_ID, c)


if __name__ == "__main__":
    main()
