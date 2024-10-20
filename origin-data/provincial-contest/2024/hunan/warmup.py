import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/hunan-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/814792f7-687e-4b7b-b440-f6008eb8b000/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "湖南省第二十届大学生计算机程序设计竞赛 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2024-10-12 15:30:00")
    c.end_time = utils.get_timestamp_second("2024-10-12 17:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
