import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/shandong-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/3ad355cb-63d0-445a-b068-b4c473cb5d40/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025年山东省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2025-05-24 15:00:00")
    c.end_time = utils.get_timestamp_second("2025-05-24 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
