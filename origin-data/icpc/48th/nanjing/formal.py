import os

from xcpcio_board_spider import utils, Color

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/nanjing")

FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 48 届 ICPC 国际大学生程序设计竞赛区域赛南京站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-11-5 09:30:00")
    c.end_time = utils.get_timestamp_second("2023-11-5 14:30:00")

    c.fill_problem_id()

    c.balloon_color = [
        Color(background_color="#006400", color="#fff"),
        Color(background_color="#a52a2a", color="#fff"),
        Color(background_color="#ffa500", color="#fff"),
        Color(background_color="#ffffff", color="#000"),
        Color(background_color="#0000ff", color="#fff"),
        Color(background_color="#87ceeb", color="#fff"),
        Color(background_color="#000000", color="#fff"),
        Color(background_color="#ff69b4", color="#fff"),
        Color(background_color="#ff00ff", color="#fff"),
        Color(background_color="#90ee90", color="#fff"),
        Color(background_color="#ff0000", color="#fff"),
        Color(background_color="#800080", color="#fff"),
        Color(background_color="#ffff00", color="#000"),
    ]

    medal_base = 33
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
