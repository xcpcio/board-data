import os

from xcpcio_board_spider import utils, constants

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/shandong-warmup")
FETCH_URI = os.getenv(
    "FETCH_URI", "./raw/warmup/Scoreboard warmup - DOMjudge.html")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第十三届山东省 ICPC 大学生程序设计竞赛（热身赛）"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2023-06-03 15:30:00")
    c.end_time = utils.get_timestamp_second("2023-06-03 17:00:00")
    c.frozen_time = 30 * 60

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 0,
        constants.RESULT_PENDING: 0,
    }

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


main()
