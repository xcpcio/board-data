import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/nanjing-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 48 届 ICPC 国际大学生程序设计竞赛区域赛南京站 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2023-11-4 14:30:00")
    c.end_time = utils.get_timestamp_second("2023-11-4 17:00:00")
    c.frozen_time = 30 * 60

    medal_base = 34
    c.medal = {
        "official": {
            "gold": medal_base,
            "silver": medal_base * 2,
            "bronze": medal_base * 3,
        }
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
