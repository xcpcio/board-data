import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/zhejiang")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "「睿琪杯」浙江省第 22 届大学生程序设计竞赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2025-04-26 12:00:00")
    c.end_time = utils.get_timestamp_second("2025-04-26 17:00:00")

    c.medal = {
        "undergraduate": {
            "gold": 27,
            "silver": 40,
            "bronze": 67,
        },
        "vocational": {
            "gold": 16,
            "silver": 22,
            "bronze": 38,
        }
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
