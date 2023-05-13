import os
import time

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

    return c


def handle_teams(teams: Teams):
    pass


def work(data_dir: str, fetch_uri_prefix: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    while True:
        log.info("loop start")

        try:
            # z = ZOJ(c, fetch_uri_prefix)

            # z.fetch().parse_teams().parse_runs()

            # handle_teams(z.teams)

            # utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            # utils.output(os.path.join(data_dir, "team.json"), z.teams.get_dict)
            # utils.output(os.path.join(data_dir, "run.json"), z.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")

        time.sleep(1)
