import time
import os

from xcpcio_board_spider import Teams, Contest, logger, utils, constants, logo
from xcpcio_board_spider.spider.domjudge.v2 import DOMjudge


l = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CH_GIRL,
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 0,
        constants.RESULT_PENDING: 0,
    }

    c.logo = logo.ICPC

    return c


def handle_teams(teams: Teams):
    for v in teams.values():
        if v.name.startswith("⭐"):
            v.name = v.name[1:]
            v.official = 0
            v.unofficial = 1
        else:
            v.official = 1


def work(data_dir: str, fetch_uri: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri) == 0:
        return

    while True:
        l.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()
            # handle_teams(d.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            l.info("work successfully")
        except Exception as e:
            l.error("work failed. ", e)

        l.info("sleeping...")

        time.sleep(5)
