import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/shandong")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/812afc7e-0530-4c24-ae5f-55d71d9d913d")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025年山东省大学生程序设计竞赛 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2025-05-25 09:30:00")
    c.end_time = utils.get_timestamp_second("2025-05-25 14:30:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
