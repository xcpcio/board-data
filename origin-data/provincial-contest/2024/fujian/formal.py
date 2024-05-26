import os
from pathlib import Path

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/fujian")
FETCH_URI = os.getenv(
    "FETCH_URI", "http://ccpc.pintia.cn/fj/js/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第十一届福建省大学生程序设计竞赛暨 CCPC 全国邀请赛（福州）"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp_second("2024-05-26 9:30:00")
    c.end_time = utils.get_timestamp_second("2024-05-26 14:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    data_dir = Path(DATA_DIR)
    common.work(data_dir, FETCH_URI, c)


if __name__ == "__main__":
    main()
