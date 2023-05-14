import os

from xcpcio_board_spider import utils, logo

import common

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2023/guangdong-warmup")

team_urls = [
    "http://soj.csgrandeur.cn:20086/api/cpc_team_list?json=eyJmaWx0ZXIiOnsiY29udGVzdF9pZCI6WyI9IiwxMDAxXX19",
    "http://soj.csgrandeur.cn:20086/api/cpc_team_list?json=eyJmaWx0ZXIiOnsiY29udGVzdF9pZCI6WyI9IiwxMDAyXX19",
]

run_urls = [
    "http://soj.csgrandeur.cn:20086/api/solution_list?json=eyJjb250ZXN0X2lkIjoxMDAxLCJpbl9kYXRlX2FmdGVyIjoiMTk3MC0wMS0wMSAwODowMDowMCJ9",
    "http://soj.csgrandeur.cn:20086/api/solution_list?json=eyJjb250ZXN0X2lkIjoxMDAyLCJpbl9kYXRlX2FmdGVyIjoiMTk3MC0wMS0wMSAwODowMDowMCJ9",
]


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "第二十届 CCPC 广东省大学生程序设计竞赛（热身赛）"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2023-05-13 15:30:00")
    c.end_time = utils.get_timestamp_second("2023-05-13 18:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    common.work(DATA_DIR, c, team_urls, run_urls, 1000)


if __name__ == "__main__":
    main()
