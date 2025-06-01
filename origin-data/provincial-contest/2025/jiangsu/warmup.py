import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/jiangsu-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "「华为杯」2025 年江苏省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2025-06-01 15:00:00")
    c.end_time = utils.get_timestamp_second("2025-06-01 16:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
