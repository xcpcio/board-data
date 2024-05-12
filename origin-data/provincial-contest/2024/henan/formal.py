import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2024/henan")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/cb59e47a-c935-436b-8661-8908abb52196/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 6 届 CCPC 河南省大学生程序设计竞赛 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-05-12 09:30:00")
    c.end_time = utils.get_timestamp_second("2024-05-12 14:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
