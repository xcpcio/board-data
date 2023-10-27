import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/qinhuangdao-warmup")

team_urls = [
    "./raw/warmup/team.json"
]

run_urls = [
    "./raw/warmup/solution.json"
]


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛秦皇岛站 - 热身赛"
    c.problem_quantity = 3
    c.start_time = utils.get_timestamp_second("2023-10-14 15:00:00")
    c.end_time = utils.get_timestamp_second("2023-10-14 17:30:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, team_urls, run_urls, 1001)


if __name__ == "__main__":
    main()
