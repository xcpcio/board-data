import os

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/ccpc/11st/nanchang-invitational-warmup")

FETCH_URI = os.getenv(
    "FETCH_URI", "https://cpc.csgrandeur.cn/rank/contests/cba19d69-635b-4b35-b6f7-e77a27c342f9/")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025 CCPC 全国邀请赛（南昌）暨第二届江西省赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2025-09-12 15:00:00")
    c.end_time = utils.get_timestamp_second("2025-09-12 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, FETCH_URI)


if __name__ == "__main__":
    main()
