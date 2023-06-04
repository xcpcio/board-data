import time
import os

from xcpcio_board_spider import Teams, Contest, logger, utils, constants, logo
from xcpcio_board_spider.spider.nowcoder.v1 import NowCoder


l = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.ICPC

    return c


def work(data_dir: str, c: Contest, contest_id: int):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if os.getenv("ENABLE_SPIDER") != "true":
        return

    while True:
        l.info("loop start")

        try:
            n = NowCoder(c, contest_id)
            n.fetch().parse_teams().fetch_submissions()

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), n.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), n.runs.get_dict)

            l.info("work successfully")
        except Exception as e:
            l.error("work failed. ", e)

        l.info("sleeping...")
        time.sleep(5)
