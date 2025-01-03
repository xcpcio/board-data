import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/harbin")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/2b11e159-401b-4c3d-96b3-4dd6a9eac89c")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛哈尔滨站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-11-5 09:00:00")
    c.end_time = utils.get_timestamp_second("2023-11-5 14:00:00")

    c.fill_problem_id().fill_balloon_color()

    c.medal = {
        "official": {
            "gold": 24,
            "silver": 46,
            "bronze": 70,
        }
    }

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
