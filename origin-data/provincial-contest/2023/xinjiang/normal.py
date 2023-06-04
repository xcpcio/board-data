import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/xinjiang")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2023 年国际大学生程序设计竞赛（ACM-ICPC）新疆赛区"
    c.problem_quantity = 10
    c.start_time = utils.get_timestamp_second("2023-05-20 13:00:00")
    c.end_time = utils.get_timestamp_second("2023-05-20 18:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    common.work(DATA_DIR, get_contest(), 57840)


main()
