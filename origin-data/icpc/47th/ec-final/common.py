import time
import os

from xcpcio_board_spider import Teams, Contest, logger, utils, constants, logo
from xcpcio_board_spider.spider.domjudge.v2 import DOMjudge


log = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 0,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.ICPC

    return c


def handle_team(teams: Teams):
    for team in teams.values():
        if team.official:
            team.official = 1
        elif team.unofficial:
            team.unofficial = 1


def work(data_dir: str, fetch_uri: str, c: Contest):
    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c.start_time, c.end_time, fetch_uri)
            d.fetch().parse_teams().parse_runs().handle_default_observers_team()

            handle_team(d.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")

        time.sleep(5)
