import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/beijing")
FETCH_URI = os.getenv(
    "FETCH_URI", "http://ccpc.pintia.cn/bj/js/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2024 北京市大学生程序设计竞赛"
    c.problem_quantity = 11
    c.start_time = utils.get_timestamp_second("2024-05-19 10:15:00")
    c.end_time = utils.get_timestamp_second("2024-05-19 15:15:00")

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
    common.work(DATA_DIR, FETCH_URI, c)


if __name__ == "__main__":
    main()
