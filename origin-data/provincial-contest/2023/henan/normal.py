import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/henan")
FETCH_URI = os.getenv(
    "FETCH_URI", "https://pintia.cn/api/problem-sets/1654882388524294144/rankings")
COOKIES_STR = os.getenv("COOKIES_STR", "")
TEAM_INFO_XLS_PATH = os.getenv("TEAM_INFO_XLS_PATH", "./raw/teams.xls")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第五届 CCPC 河南省大学生程序设计竞赛（正式赛）"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp("2023-5-7 10:00:00")
    c.end_time = utils.get_timestamp("2023-5-7 15:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, FETCH_URI, COOKIES_STR, TEAM_INFO_XLS_PATH, c)


if __name__ == "__main__":
    main()
