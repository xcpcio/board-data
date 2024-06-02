import os
import time
from pathlib import Path
import shutil

from xcpcio_board_spider import logger, Contest, Teams, Submissions, constants, utils
from xcpcio_board_spider.type import Image, constants
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

log = logger.init_logger()

ENABLE_FROZEN = os.getenv("ENABLE_FROZEN", "true").lower() == "true"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")


def get_basic_contest():
    c = Contest()
    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CH_GIRL,
    }
    c.logo = Image(preset="ICPC")

    return c


def handle_teams(teams: Teams):
    filter_team_ids = []

    for t in teams.values():
        d_team = t.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        t.name = t.name.lstrip("⭐")

        if "3" in d_team["group_ids"]:
            t.official = True
        elif "4" in d_team["group_ids"]:
            t.unofficial = True
        elif "6" in d_team["group_ids"]:
            t.official = True
            t.girl = True
        else:
            filter_team_ids.append(t.team_id)
            continue

        if d_team["public_description"] is not None and len(d_team["public_description"]) > 0:
            t.members = d_team["public_description"].split(",")
            if len(t.members) > 3:
                t.coach = t.members[3]
                t.coach = t.coach.rstrip("(教练)")
                t.members = t.members[:3]

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

    team_ids = [x.team_id for x in teams.values()]
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

    filter_run_ids.sort(reverse=True)
    for run_id in filter_run_ids:
        del runs[run_id]


def work(data_dir: Path, c: Contest, fetch_uri: str):
    utils.save_to_disk(data_dir, c, Teams(), Submissions(), True)

    if len(SECRET_TOKEN) > 0:
        utils.save_to_disk(data_dir / SECRET_TOKEN,
                           c, Teams(), Submissions(), True)

    if len(fetch_uri) == 0:
        return

    d = DOMjudge(c, fetch_uri)

    while True:
        log.info("loop start")

        try:
            d.fetch().update_contest().parse_teams().parse_runs()
            handle_teams(d.teams)

            if len(SECRET_TOKEN) > 0:
                utils.save_to_disk(data_dir / SECRET_TOKEN, c, d.teams, d.runs)

            handle_runs(c, d.runs, d.teams)
            utils.save_to_disk(data_dir, c, d.teams, d.runs)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
