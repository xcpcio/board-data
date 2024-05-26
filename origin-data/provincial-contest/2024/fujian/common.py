import os
import time
from pathlib import Path

from xcpcio_board_spider import logger, Contest, Teams, Image, constants, utils
from xcpcio_board_spider.spider.zoj.v2.zoj import ZOJ

log = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        # constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CH_GIRL,
    }
    c.logo = Image(preset="CCPC")
    return c


def handle_teams(teams: Teams):
    for team in teams.values():
        type = ZOJ.get_team_type(team)

        if "type1" in type:
            team.official = True

        if "unofficial" in type:
            team.unofficial = True

        if "girls" in type:
            team.girl = True


def work(data_dir: Path, fetch_uri_prefix: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(data_dir / "config.json", c.get_dict)
    utils.output(data_dir / "team.json", {}, True)
    utils.output(data_dir / "run.json", [], True)

    if len(fetch_uri_prefix) == 0:
        return

    while True:
        log.info("loop start")

        try:
            z = ZOJ(c, fetch_uri_prefix)

            z.fetch().parse_teams().parse_runs()

            handle_teams(z.teams)

            utils.output(data_dir / "config.json", c.get_dict)
            utils.output(data_dir / "team.json", z.teams.get_dict)
            utils.output(data_dir / "run.json", z.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.exception(e)

        log.info("sleeping...")
        time.sleep(5)
