import os
import time
import shutil

from xcpcio_board_spider import logger, Contest, Teams, Submissions, constants, utils
from xcpcio_board_spider.type import Image, constants
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

ENABLE_FROZEN = os.getenv("ENABLE_FROZEN", "true").lower() == "true"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")

log = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
    }
    c.logo = Image(preset="ICPC")
    return c


def handle_teams(teams: Teams):
    filter_team_ids = []

    for team in teams.values():
        d_team = team.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        team.name = team.name.lstrip("*")

        if "3" in d_team["group_ids"]:
            team.official = True
        elif "2" in d_team["group_ids"]:
            team.unofficial = True
        else:
            filter_team_ids.append(team.team_id)
            continue

    for team_id in filter_team_ids:
        del teams[team_id]


def is_frozen(c: Contest):
    unfrozen_time = 0

    if c.unfrozen_time <= 86400:
        unfrozen_time = c.end_time + c.unfrozen_time
    else:
        unfrozen_time = c.unfrozen_time

    if ENABLE_FROZEN and utils.get_now_timestamp_second() <= unfrozen_time:
        return True

    return False


def handle_runs(c: Contest, runs: Submissions, teams: Teams):
    t = utils.get_timestamp_second(
        c.end_time) - utils.get_timestamp_second(c.start_time) - c.frozen_time
    t = t * 1000

    team_ids = teams.get_dict.keys()
    filter_run_ids = []

    for ix, run in enumerate(runs):
        run.time = None
        if run.team_id not in team_ids:
            filter_run_ids.append(ix)

        if is_frozen(c):
            if run.status == constants.RESULT_ACCEPTED:
                pass
            elif run.status == constants.RESULT_COMPILATION_ERROR:
                pass
            elif run.status == constants.RESULT_PENDING:
                pass
            else:
                run.status = constants.RESULT_REJECTED

            if run.timestamp >= t:
                run.status = constants.RESULT_FROZEN

    for run_id in filter_run_ids:
        del runs[run_id]


def write_to_disk(data_dir: str, c: Contest, teams: Teams, runs: Submissions, if_not_exists=False):
    log.info("write to disk. [data_dir: {}]".format(data_dir))

    utils.ensure_makedirs(data_dir)

    utils.output(os.path.join(data_dir, "config.json"),
                 c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"),
                 teams.get_dict, if_not_exists=if_not_exists)
    utils.output(os.path.join(data_dir, "run.json"),
                 runs.get_dict, if_not_exists=if_not_exists)


def work(data_dir: str, c: Contest, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    write_to_disk(data_dir, c, Teams(), Submissions(), True)

    if len(SECRET_TOKEN) > 0:
        write_to_disk(data_dir + SECRET_TOKEN, c, Teams(), Submissions(), True)

    if len(fetch_uri) == 0:
        return

    d = DOMjudge(c, fetch_uri)

    while True:
        log.info("loop start")

        try:
            d.fetch().update_contest().parse_teams().parse_runs()

            handle_teams(d.teams)

            if len(SECRET_TOKEN) > 0:
                write_to_disk(data_dir + SECRET_TOKEN, c, d.teams, d.runs)

            handle_runs(c, d.runs, d.teams)
            write_to_disk(data_dir, c, d.teams, d.runs)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
