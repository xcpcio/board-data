import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/hubei")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/normal/Scoreboard HBCPC_2023 - DOMjudge.html")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第五届 CCPC 湖北省大学生程序设计竞赛（正式赛）"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp("2023-04-30 10:00:00")
    c.end_time = utils.get_timestamp("2023-04-30 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    common.work(DATA_DIR, FETCH_URI, get_contest())


main()
