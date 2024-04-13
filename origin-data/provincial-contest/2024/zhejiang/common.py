import time
import os
import shutil

from xcpcio_board_spider import logger, Contest, constants, logo, utils, Team, Teams, Submissions
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge
from xcpcio_board_spider.type import Image

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
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
        constants.TEAM_TYPE_GIRL: constants.TEAM_TYPE_ZH_CH_GIRL,
        "undergraduate": "本科组",
        "vocational": "专科组",
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = Image(preset="ICPC")
    c.banner = Image(
        url="{}/banner.min.png".format(ASSETS_PATH))

    return c


def handle_teams(teams: Teams):
    filter_team_id = []
    for t in teams.values():
        d_team = t.extra[DOMjudge.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        if d_team["display_name"] is None:
            t.name = d_team["name"]

        if d_team["hidden"] == True:
            filter_team_id.append(t.team_id)

        if d_team["public_description"] is not None and len(d_team["public_description"]) > 0:
            t.members = d_team["public_description"].split("|")
            t.members = sorted(t.members)

        if "observers" in d_team["group_ids"]:
            t.unofficial = 1
        elif "undergraduate" in d_team["group_ids"]:
            t.official = 1
            t.extra["undergraduate"] = True
        elif "vocational" in d_team["group_ids"]:
            t.official = 1
            t.extra["vocational"] = True

    for t_id in filter_team_id:
        del teams[t_id]


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


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    copy_assets(data_dir)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()

            handle_teams(d.teams)
            handle_runs(c, d.runs)

            teams = {}
            for t in d.teams.values():
                team_id = t.team_id
                teams[team_id] = t.get_dict

                if "undergraduate" in t.extra.keys():
                    teams[team_id]["undergraduate"] = True

                if "vocational" in t.extra.keys():
                    teams[team_id]["vocational"] = True

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), teams)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
