import time
import os

from xcpcio_board_spider import logger, Contest, Teams, constants, logo, utils

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

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.CCPC

    return c


def work(data_dir: str, fetch_uri: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    # while True:
    #     log.info("loop start")

    #     try:
    #         p = PTA(c, fetch_uri=fetch_uri, cookies_str=cookies_str)
    #         p.fetch().parse_teams().parse_runs()

    #         handle_teams(p.teams, team_info_xls_path)

    #         utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    #         utils.output(os.path.join(data_dir, "team.json"), p.teams.get_dict)
    #         utils.output(os.path.join(data_dir, "run.json"), p.runs.get_dict)

    #         log.info("work successfully")
    #     except Exception as e:
    #         log.error("work failed. ", e)

    #     log.info("sleeping...")

    #     time.sleep(5)
