import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/11st/nanchang-invitational")


FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/39f847f5-6cb8-4335-863c-890503294833")

def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025 CCPC 全国邀请赛（南昌）暨第二届江西省赛 - 正式赛"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2025-09-13 09:30:00")
    c.end_time = utils.get_timestamp_second("2025-09-13 14:30:00")
    c.medal = "ccpc"

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
