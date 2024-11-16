import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/10th/zhengzhou")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/9de35784-ec9d-421e-8501-34353101a3ed")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 10 届 CCPC 中国大学生程序设计竞赛郑州站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-11-17 09:00:00")
    c.end_time = utils.get_timestamp_second("2024-11-17 14:00:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
