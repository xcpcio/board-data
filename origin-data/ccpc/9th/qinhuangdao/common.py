import os
import time

from xcpcio_board_spider import logger, Contest, ContestOptions, Teams, Submissions, constants, utils
from xcpcio_board_spider.spider.csg_cpc.v1 import CSG_CPC
from xcpcio_board_spider.type import Image

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

    c.options = ContestOptions()
    c.options.calculation_of_penalty = constants.CALCULATION_OF_PENALTY_ACCUMULATE_IN_SECONDS_AND_FINALLY_TO_THE_MINUTE

    c.logo = Image(preset="CCPC")

    return c


def handle_teams(teams: Teams):
    team_ids = []

    for team in teams.values():
        if team.name == "'-" or team.name == "裁判":
            team_ids.append(team.team_id)
            continue

        if team.official == True:
            team.official = 1

        if team.unofficial == True:
            team.unofficial = 1

        if team.girl == True:
            team.girl = 1

    for team_id in team_ids:
        del teams[team_id]


def handle_runs(runs: Submissions, problem_id_base: int):
    for run in runs:
        run.problem_id -= problem_id_base


def work(data_dir: str, c: Contest, team_uris, run_uris, problem_id_base: int):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    while True:
        log.info("loop start")

        try:
            csg_cpc = CSG_CPC(c, team_uris, run_uris)
            csg_cpc.fetch().parse_teams().parse_runs()

            handle_teams(csg_cpc.teams)
            handle_runs(csg_cpc.runs, problem_id_base)

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
