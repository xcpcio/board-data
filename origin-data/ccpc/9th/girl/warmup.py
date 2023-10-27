import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/girl-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/warmup")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛女生专场 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2023-10-20 15:15:00")
    c.end_time = utils.get_timestamp_second("2023-10-20 17:15:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, FETCH_URI, c)


if __name__ == "__main__":
    main()
