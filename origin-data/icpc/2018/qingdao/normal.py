import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/2018/qingdao")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/normal/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 43 届 ICPC 国际大学生程序设计竞赛区域赛青岛站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2018-10-21 09:00:00")
    c.end_time = utils.get_timestamp_second("2018-10-21 14:00:00")

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
    common.work(DATA_DIR, FETCH_URI, c)


if __name__ == "__main__":
    main()
