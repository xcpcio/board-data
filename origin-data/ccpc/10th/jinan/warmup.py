import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/10th/jinan-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/e4587f93-aca4-4227-9567-3ec7452d64e8/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 10 届 CCPC 中国大学生程序设计竞赛济南站 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2024-10-26 15:00:00")
    c.end_time = utils.get_timestamp_second("2024-10-26 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
