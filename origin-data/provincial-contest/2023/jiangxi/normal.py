import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/jiangxi")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2023 年 ICPC 江西省大学生程序设计竞赛（正式赛）"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp_second("2023-05-21 10:00:00")
    c.end_time = utils.get_timestamp_second("2023-05-21 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
