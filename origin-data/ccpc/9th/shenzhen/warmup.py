import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/shenzhen-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/6ac0c14e-b974-4b4c-8616-52ef1cd1660b/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛深圳站 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2023-11-11 15:30:00")
    c.end_time = utils.get_timestamp_second("2023-11-11 17:30:00")

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
