import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/liaoning")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/e400a48c-25dd-4fe0-99ba-49a0bf770541")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第五届辽宁省大学生程序设计竞赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-11-03 09:20:00")
    c.end_time = utils.get_timestamp_second("2024-11-03 14:20:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
