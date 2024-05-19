import os
import time

from xcpcio_board_spider import logger, Contest, Teams, Image, constants, utils
from xcpcio_board_spider.spider.zoj.v2.zoj import ZOJ

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
        "undergraduate": "省内本科组",
        "vocational": "省内专科组",
    }

    c.status_time_display = constants.FULL_STATUS_TIME_DISPLAY

    return c


def handle_teams(teams: Teams):
    for team in teams.values():
        type = ZOJ.get_team_type(team)

        if "type1" in type:
            team.official = 1

        if "unofficial" in type:
            team.unofficial = 1

        if "girls" in type:
            team.girl = 1

        if "type2" in type:
            team.enable_group("undergraduate")

        if "type3" in type:
            team.enable_group("vocational")

        # type4 本科组
        # type5 专科组


def work(data_dir: str, fetch_uri_prefix: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri_prefix) == 0:
        return

    while True:
        log.info("loop start")

        try:
            z = ZOJ(c, fetch_uri_prefix)

            z.fetch().parse_teams().parse_runs()

            handle_teams(z.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), z.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), z.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.exception(e)

        log.info("sleeping...")
        time.sleep(1)
