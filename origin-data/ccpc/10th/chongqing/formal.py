import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/10th/chongqing")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/40fb3fb6-402d-48fe-918d-64a0426d1dc9")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 10 届 CCPC 中国大学生程序设计竞赛重庆站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-11-10 09:20:00")
    c.end_time = utils.get_timestamp_second("2024-11-10 14:20:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
