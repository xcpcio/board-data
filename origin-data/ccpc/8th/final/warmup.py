import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/8th/final-warmup")
FETCH_URI_PREFIX = os.getenv(
    "FETCH_URI_PREFIX", "http://ccpc.pintia.cn/js")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第八届中国大学生程序设计竞赛总决赛（热身赛）"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp("2023-05-13 10:00:00")
    c.end_time = utils.get_timestamp("2023-05-13 12:00:00")
    c.frozen_time = 30 * 60

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, FETCH_URI_PREFIX, c)


if __name__ == "__main__":
    main()
