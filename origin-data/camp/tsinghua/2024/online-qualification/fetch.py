import time
import os
from pathlib import Path

from xcpcio_board_spider import logger, Contest, constants, logo, utils, Team, Teams, Submissions
from xcpcio_board_spider.type import Image

log = logger.init_logger()

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../../data/camp/tsinghua/2024/online-qualification")
FETCH_URI = os.getenv(
    "FETCH_URI", "")


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
    }

    return c


def handle_teams(teams: Teams):
    pass


def handle_runs(c: Contest, runs: Submissions):
    t = utils.get_timestamp_second(
        c.end_time) - utils.get_timestamp_second(c.start_time) - c.frozen_time
    t = t * 1000


def write_to_disk(data_dir: str, c: Contest, teams: Teams, runs: Submissions, if_not_exists=False):
    log.info("write to disk. [data_dir: {}]".format(data_dir))

    utils.ensure_makedirs(data_dir)

    utils.output(os.path.join(data_dir, "config.json"),
                 c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"),
                 teams, if_not_exists=if_not_exists)
    utils.output(os.path.join(data_dir, "run.json"),
                 runs.get_dict, if_not_exists=if_not_exists)


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)


if __name__ == "__main__":
    c = get_basic_contest()
    c.contest_name = "Tsinghua Bootcamp 2024 - Online Qualification"
    c.problem_quantity = 13
    c.start_time = utils.get_timestamp_second("2024-07-21 13:00:00")
    c.end_time = utils.get_timestamp_second("2024-07-21 18:00:00")
    c.fill_problem_id().fill_balloon_color()
    work(c, DATA_DIR, FETCH_URI)
