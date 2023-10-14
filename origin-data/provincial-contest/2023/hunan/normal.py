import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/hunan")

team_urls = [
    "./raw/team.json",
]

run_urls = [
    "./raw/solution.json",
]


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "湖南省第十九届大学生计算机程序设计竞赛"
    c.problem_quantity = 11
    c.start_time = utils.get_timestamp_second("2023-09-17 09:00:00")
    c.end_time = utils.get_timestamp_second("2023-09-17 14:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, team_urls, run_urls, 1026)


if __name__ == "__main__":
    main()
