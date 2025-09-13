import os
import time

from xcpcio_board_spider import Contest, Teams, constants, logger, utils
from xcpcio_board_spider.spider.csg_cpc.v1 import CSG_CPC
from xcpcio_board_spider.type import Image

log = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CN_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CN_GIRL,
    }
    c.options.calculation_of_penalty = constants.CALCULATION_OF_PENALTY_ACCUMULATE_IN_SECONDS_AND_FINALLY_TO_THE_MINUTE
    c.logo = Image(preset="ccpc")

    return c


def handle_teams(teams: Teams):
    team_ids = []

    for team in teams.values():
        if team.name == "'-" or team.name == "裁判" or len(team.name) == 0:
            team_ids.append(team.team_id)
            continue

    for team_id in team_ids:
        del teams[team_id]


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
            csg_cpc = CSG_CPC(c, fetch_uri)
            csg_cpc.fetch().update_contest().parse_teams().parse_runs()

            handle_teams(csg_cpc.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"),
                         csg_cpc.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"),
                         csg_cpc.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
