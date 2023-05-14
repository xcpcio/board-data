import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/icpc/48th/xian-invitational-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/warmup/Scoreboard warmup - DOMjudge.html")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 48 届 ICPC 国际大学生程序设计竞赛西安邀请赛（热身赛）"
    c.problem_quantity = 2
    c.start_time = utils.get_timestamp_second("2023-05-14 08:00:00")
    c.end_time = utils.get_timestamp_second("2023-05-14 09:30:00")
    c.frozen_time = 30 * 60

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(c, DATA_DIR, FETCH_URI)


if __name__ == "__main__":
    main()
