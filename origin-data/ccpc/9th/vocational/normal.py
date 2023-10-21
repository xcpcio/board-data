import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/vocational")
FETCH_URI = os.getenv(
    "FETCH_URI", "http://ccpc.pintia.cn/v/js/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2023年中国大学生程序设计竞赛高职专场"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp_second("2023-10-21 09:00:00")
    c.end_time = utils.get_timestamp_second("2023-10-21 14:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, FETCH_URI, c)


if __name__ == "__main__":
    main()
