import os
import time

from xcpcio_board_spider import logger, Contest, Teams, Submissions, constants, utils
from xcpcio_board_spider.type import Image
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

ENABLE_FROZEN = os.getenv("ENABLE_FROZEN", "true")
ENABLE_SIMPLE = os.getenv("ENABLE_SIMPLE", "true")

log = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.logo = Image(preset="ICPC")

    medal_base = 29
    c.medal = {
        "official": {
            "gold": medal_base,
            "silver": medal_base * 2,
            "bronze": medal_base * 3,
        }
    }

    return c


def handle_teams(teams: Teams):
    filter_team_ids = []

    for team in teams.values():
        d_team = team.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        # if team.name.startswith('⭐'):
        #     team.name = team.name[len("⭐"):]

        if "3" in d_team["group_ids"]:
            team.official = True
        elif "4" in d_team["group_ids"]:
            team.unofficial = True
        else:
            filter_team_ids.append(team.team_id)
            continue

        if "public_description" in d_team.keys() and d_team["public_description"] is not None:
            team.members = d_team["public_description"].split(" ")

    for team_id in filter_team_ids:
        del teams[team_id]


def handle_runs(c: Contest, runs: Submissions):
    t = utils.get_timestamp_second(
        c.end_time) - utils.get_timestamp_second(c.start_time) - c.frozen_time
    t = t * 1000

    for run in runs:
        run.time = None

        if ENABLE_SIMPLE == "true":
            if run.status == constants.RESULT_ACCEPTED:
                pass
            elif run.status == constants.RESULT_COMPILATION_ERROR:
                pass
            else:
                run.status = constants.RESULT_REJECTED

        if ENABLE_FROZEN == "true":
            if run.timestamp >= t:
                run.status = constants.RESULT_FROZEN


def work(data_dir: str, c: Contest, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri) == 0:
        return

    d = DOMjudge(c, fetch_uri)

    while True:
        log.info("loop start")

        try:
            d.fetch().update_contest().parse_teams().parse_runs()

            handle_teams(d.teams)
            handle_runs(c, d.runs)

            # utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            # utils.output(os.path.join(data_dir, "team.json"),
            #              d.teams.get_dict)
            # utils.output(os.path.join(data_dir, "run.json"),
            #              d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
