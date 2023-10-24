import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/46th/ec-final")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/events.xml")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 46 届国际大学生程序设计竞赛亚洲区决赛（正式赛）"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2022-07-20 09:00:00")
    c.end_time = utils.get_timestamp_second("2022-07-20 14:00:00")

    c.medal = {
        "official": {
            "gold": 36,
            "silver": 72,
            "bronze": 108,
        }
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
