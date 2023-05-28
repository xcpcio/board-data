import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/zhejiang-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "The 20th Zhejiang Provincial Collegiate Programming Contest Sponsored by TuSimple - Practice Session"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2023-04-15 09:15:00")
    c.end_time = utils.get_timestamp_second("2023-04-15 10:45:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
