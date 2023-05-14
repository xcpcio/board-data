import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/guangdong")

team_urls = [
    "./raw/normal/team_list_1004.json",
    "./raw/normal/team_list_1005.json",
]

run_urls = [
    "./raw/normal/run_list_1004.json",
    "./raw/normal/run_list_1005.json",
]


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第二十届 CCPC 广东省大学生程序设计竞赛（正式赛）"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-05-14 10:00:00")
    c.end_time = utils.get_timestamp_second("2023-05-14 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, team_urls, run_urls, 1004)


if __name__ == "__main__":
    main()
