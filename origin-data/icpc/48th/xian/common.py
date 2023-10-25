import os
import time
import re

from xcpcio_board_spider import logger, Contest, Teams, constants, Image, utils
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

log = logger.init_logger()


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

    c.status_time_display = constants.FULL_STATUS_TIME_DISPLAY

    c.logo = Image(preset="ICPC")

    return c


def handle_teams(teams: Teams):
    for team in teams.values():
        team.organization = re.sub(r'\(.*\)', '', team.organization)
        team.name = re.sub(r'\(.*\)', '', team.name)

        d_team = team.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        if "2" in d_team["group_ids"]:
            team.unofficial = True

        if "3" in d_team["group_ids"]:
            team.official = True


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()
            handle_teams(d.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
