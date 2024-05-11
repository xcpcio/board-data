import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/henan-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/87eaf6fc-bbc1-4e95-9d08-34bb161ac405/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 6 届 CCPC 河南省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2024-05-11 14:30:00")
    c.end_time = utils.get_timestamp_second("2024-05-11 17:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
