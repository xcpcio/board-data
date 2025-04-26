import os
from pathlib import Path

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/50th/wuhan-invitational-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 50 届 ICPC 国际大学生程序设计竞赛区域赛武汉站 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2025-04-26 14:45:00")
    c.end_time = utils.get_timestamp_second("2025-04-26 17:15:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(Path(DATA_DIR), c, FETCH_URI)


if __name__ == "__main__":
    main()
