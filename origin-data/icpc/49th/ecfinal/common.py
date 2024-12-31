import os
import time
from pathlib import Path
import shutil
from typing import Optional, Dict
import json

from xcpcio_board_spider import logger, Contest, Teams, Submissions, constants, utils
from xcpcio_board_spider.type import Image, Reaction
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

CUR_DIR = Path(__file__).parent
ASSETS_PATH = "assets"

ENABLE_FROZEN = os.getenv("ENABLE_FROZEN", "true").lower() == "true"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")
LIVE_V3_RUNS: Optional[str] = os.getenv("LIVE_V3_RUNS", None)

log = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.logo = Image(preset="ICPC")
    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CN_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CN_GIRL,
    }
    # c.banner = Image(url=f"{ASSETS_PATH}/banner.png")
    return c


def handle_teams(teams: Teams):
    filter_team_ids = []

    for team in teams.values():
        d_team = team.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        if "3" in d_team["group_ids"]:
            team.official = True
        elif "6" in d_team["group_ids"]:
            team.unofficial = True
        elif "Girls" in d_team["group_ids"]:
            team.official = True
            team.girl = True
        else:
            filter_team_ids.append(team.team_id)
            continue

        if "public_description" in d_team.keys() and d_team["public_description"] is not None:
            description = d_team["public_description"]

            members = description.split(",")
            team.members = members[:3]
            if len(members) > 3:
                team.coach = members[3]
                team.coach = team.coach.replace("(教练)", "")

        if team.name.startswith("⭐"):
            team.name = team.name.replace("⭐", "")

        if team.name.startswith("🌟"):
            team.name = team.name.replace("🌟", "")

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


def handle_runs(c: Contest, runs: Submissions, live_v3_runs: Optional[Dict] = None):
    t = utils.get_timestamp_second(
        c.end_time) - utils.get_timestamp_second(c.start_time) - c.frozen_time
    t = t * 1000

    for run in runs:
        run.time = None

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


def write_to_disk(data_dir: Path, c: Contest, teams: Teams, runs: Submissions, if_not_exists=False):
    if not data_dir.exists():
        data_dir.mkdir(parents=True)

    log.info("write to disk. [data_dir: {}]".format(data_dir))
    utils.output(data_dir / "config.json", c.get_dict)
    utils.output(data_dir / "team.json", teams.get_dict,
                 if_not_exists=if_not_exists)
    utils.output(data_dir / "run.json", runs.get_dict,
                 if_not_exists=if_not_exists)


def copy_assets(data_dir: Path):
    try:
        assets_path = CUR_DIR / "assets"
        target_path = data_dir / ASSETS_PATH
        if not assets_path.exists() or not assets_path.is_dir():
            raise Exception(
                "assets path not exists. [path: {}]".format(assets_path))

        if target_path.exists() and target_path.is_dir():
            shutil.rmtree(target_path)
        shutil.copytree(assets_path, target_path)
    except Exception as e:
        log.error("copy assets failed. ", e)


def work(data_dir: Path, c: Contest, fetch_uri: str):
    write_to_disk(data_dir, c, Teams(), Submissions(), True)
    # copy_assets(data_dir)

    secret_data_dir = None
    if len(SECRET_TOKEN) > 0:
        secret_data_dir = data_dir.parent / (data_dir.name + SECRET_TOKEN)
        if not secret_data_dir.exists():
            secret_data_dir.mkdir(parents=True)

    if secret_data_dir is not None:
        write_to_disk(secret_data_dir, c, Teams(), Submissions(), True)

    if len(fetch_uri) == 0:
        return

    live_v3_runs: Optional[Dict] = None
    if LIVE_V3_RUNS is not None:
        c.options.submission_has_reaction = True
        live_v3_runs = dict()
        with open(LIVE_V3_RUNS, "r") as f:
            data = json.loads(f.read())
            for item in data:
                live_v3_runs[item["id"]] = item

    d = DOMjudge(c, fetch_uri)

    while True:
        log.info("loop start")

        try:
            d.fetch().update_contest().parse_teams().parse_runs()

            handle_teams(d.teams)

            if secret_data_dir is not None:
                write_to_disk(secret_data_dir, c, d.teams, d.runs)

            handle_runs(c, d.runs, live_v3_runs)
            write_to_disk(data_dir, c, d.teams, d.runs)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
