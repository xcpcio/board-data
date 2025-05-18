import os
from pathlib import Path

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/50th/nanchang-invitational")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025年icpc全国邀请赛（南昌）暨2025年（icpc）江西省大学生程序设计竞赛 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2025-05-18 10:00:00")
    c.end_time = utils.get_timestamp_second("2025-05-18 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(Path(DATA_DIR), c, FETCH_URI)


if __name__ == "__main__":
    main()
