import os

from xcpcio_board_spider import utils

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/9th/harbin")

team_urls = [
    "https://cpc.csgrandeur.cn/rank/contests/2b11e159-401b-4c3d-96b3-4dd6a9eac89c/team.json"
]

run_urls = [
    "https://cpc.csgrandeur.cn/rank/contests/2b11e159-401b-4c3d-96b3-4dd6a9eac89c/solution.json"
]


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第 9 届 CCPC 中国大学生程序设计竞赛哈尔滨站 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2023-11-5 09:00:00")
    c.end_time = utils.get_timestamp_second("2023-11-5 14:00:00")

    c.fill_problem_id().fill_balloon_color()

    medal_base = 24
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
    common.work(DATA_DIR, c, team_urls, run_urls, 1004, {
        "1015": 0,
        "1008": 1,
        "1007": 2,
        "1009": 3,
        "1004": 4,
        "1011": 5,
        "1016": 6,
        "1013": 7,
        "1014": 8,
        "1005": 9,
        "1006": 10,
        "1012": 11,
        "1010": 12
    })


if __name__ == "__main__":
    main()
