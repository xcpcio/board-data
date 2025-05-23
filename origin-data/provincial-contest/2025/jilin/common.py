import os
import shutil
import time

from xcpcio_board_spider import (
    Contest,
    Submissions,
    Teams,
    constants,
    logger,
    utils,
)
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

log = logger.init_logger()

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = "../zhejiang-assets"

ENABLE_FROZEN = os.getenv("ENABLE_FROZEN", "true").lower() == "true"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"

    c.group = {
        "A": "普通高校",
        "B": "独立学院",
        "A_female": "A组女队",
        "B_female": "B组女队",
        "star": "打星",
    }

    # c.logo = Image(preset="ICPC")
    # c.banner = Image(
    #     url="{}/banner.min.jpg".format(ASSETS_PATH))

    return c


def handle_teams(teams: Teams):
    filter_team_id = []
    for t in teams.values():
        d_team = t.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        if d_team["display_name"] is None:
            t.name = d_team["name"]

        # t.name = t.name.lstrip("*")

        if d_team["hidden"]:
            filter_team_id.append(t.team_id)
            continue

        # if d_team["public_description"] is not None and len(d_team["public_description"]) > 0:
        #     blocks = d_team["public_description"].split("、")
        #     t.members = blocks

        if "A" in d_team["group_ids"]:
            t.group.append("A")
        elif "B" in d_team["group_ids"]:
            t.group.append("B")
        elif "star" in d_team["group_ids"]:
            t.group.append("star")
        elif "A_female" in d_team["group_ids"]:
            t.group.append("A_female")
        elif "B_female" in d_team["group_ids"]:
            t.group.append("B_female")
        else:
            filter_team_id.append(t.team_id)

    if len(filter_team_id) > 0:
        for t_id in filter_team_id:
            del teams[t_id]
        print(f"filter teams[{len(filter_team_id)}]: {filter_team_id}")


def copy_assets(data_dir: str):
    try:
        assets_path = os.path.join(CUR_DIR, "assets")
        target_path = os.path.join(data_dir, ASSETS_PATH)
        if os.path.exists(assets_path) and os.path.isdir(assets_path):
            if os.path.exists(target_path) and os.path.isdir(target_path):
                shutil.rmtree(target_path)
            shutil.copytree(assets_path, target_path)
    except Exception as e:
        log.error("copy assets failed. ", e)


def is_frozen(c: Contest):
    unfrozen_time = 0

    if c.unfrozen_time <= 86400:
        unfrozen_time = c.end_time + c.unfrozen_time
    else:
        unfrozen_time = c.unfrozen_time

    if ENABLE_FROZEN and utils.get_now_timestamp_second() <= unfrozen_time:
        return True

    return False


def handle_runs(c: Contest, runs: Submissions):
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


def write_to_disk(data_dir: str, c: Contest, teams: Teams, runs: Submissions, if_not_exists=False):
    log.info("write to disk. [data_dir: {}]".format(data_dir))

    utils.ensure_makedirs(data_dir)

    utils.output(os.path.join(data_dir, "config.json"),
                 c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"),
                 teams, if_not_exists=if_not_exists)
    utils.output(os.path.join(data_dir, "run.json"),
                 runs.get_dict, if_not_exists=if_not_exists)


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    # copy_assets(data_dir)

    if len(SECRET_TOKEN) > 0:
        write_to_disk(data_dir + SECRET_TOKEN, c, Teams(), Submissions(), True)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().update_contest().parse_teams().parse_runs()

            handle_teams(d.teams)

            teams = {}
            for t in d.teams.values():
                team_id = t.team_id
                teams[team_id] = t.get_dict

            if len(SECRET_TOKEN) > 0:
                write_to_disk(data_dir + SECRET_TOKEN, c, teams, d.runs)

            handle_runs(c, d.runs)
            write_to_disk(data_dir, c, teams, d.runs)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
