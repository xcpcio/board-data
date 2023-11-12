import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/shenzhen")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/127d0f90-dc48-43d8-95b1-163886d60698/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛深圳站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-11-12 09:00:00")
    c.end_time = utils.get_timestamp_second("2023-11-12 14:00:00")

    c.fill_problem_id().fill_balloon_color()

    medal_base = 24
    c.medal = {
        "official": {
            "gold": medal_base,
            "silver": medal_base * 2,
            "bronze": medal_base * 3,
        }
    }

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
