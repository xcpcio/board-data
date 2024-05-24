import os
from pathlib import Path

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/guangdong-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/2cd982ea-45d6-4f31-bc75-85190ff0e654/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第二十一届广东省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2024-05-25 10:30:00")
    c.end_time = utils.get_timestamp_second("2024-05-25 13:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    data_dir = Path(DATA_DIR)
    common.work(data_dir, c, FETCH_URI)


if __name__ == "__main__":
    main()
