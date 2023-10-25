import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/47th/ec-final")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/normal/contest.dat")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 47 届国际大学生程序设计竞赛亚洲区决赛（正式赛）"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-03-25 10:00:00")
    c.end_time = utils.get_timestamp_second("2023-03-25 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    common.work(DATA_DIR, FETCH_URI, get_contest())


main()
