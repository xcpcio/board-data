import os
import time

from xcpcio_board_spider import logger, Contest, Teams, Submissions, constants, utils
from xcpcio_board_spider.type import Image
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge as DOMjudgeV3

log = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.logo = Image(preset="CCPC")

    return c


def handle_teams(teams: Teams):
    filter_team_ids = []

    for team_id in filter_team_ids:
        del teams[team_id]


def handle_runs(c: Contest, runs: Submissions):
    for run in runs:
        if run.timestamp >= utils.get_timestamp_second(c.end_time) - c.frozen_time:
            run.status = constants.RESULT_FROZEN


def work(data_dir: str, c: Contest, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            d = DOMjudgeV3(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()

            handle_teams(d.teams)
            handle_runs(d.runs)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"),
                         d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"),
                         d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
