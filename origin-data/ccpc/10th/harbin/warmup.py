import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/10th/harbin-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/62132660-3e3b-44ac-b365-552c78dfd922/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 10 届 CCPC 中国大学生程序设计竞赛哈尔滨站 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2024-10-19 15:30:00")
    c.end_time = utils.get_timestamp_second("2024-10-19 17:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
