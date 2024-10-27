import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/10th/jinan")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/f0cfdcc1-0903-4481-b326-b1aca051204e")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 10 届 CCPC 中国大学生程序设计竞赛济南站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-10-27 09:00:00")
    c.end_time = utils.get_timestamp_second("2024-10-27 14:00:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
