import os
from pathlib import Path

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/shandong-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "http://ccpc.pintia.cn/sd/js/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2024 CCPC 全国邀请赛（山东）暨山东省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2024-05-25 15:00:00")
    c.end_time = utils.get_timestamp_second("2024-05-25 17:30:00")

    c.fill_problem_id().fill_balloon_color()

    # c.medal = {
    #     "official": {
    #         "gold": 12,
    #         "silver": 24,
    #         "bronze": 37,
    #     },
    # }

    return c


def main():
    c = get_contest()
    data_dir = Path(DATA_DIR)
    common.work(data_dir, FETCH_URI, c)


if __name__ == "__main__":
    main()
