import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/2017/qingdao")
FETCH_URI = os.getenv("FETCH_URI")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 42 届 ICPC 国际大学生程序设计竞赛区域赛青岛站 - 正式赛"
    c.problem_quantity = 11
    c.start_time = utils.get_timestamp_second("2017-09-01 09:00:00")
    c.end_time = utils.get_timestamp_second("2017-09-01 14:00:00")

    medal_base = 36
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
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
