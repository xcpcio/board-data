import time
import os

from xcpcio_board_spider import logger, Contest, Teams, constants, logo, utils
from xcpcio_board_spider.spider.pta.v1.pta import PTA

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
        "undergraduate": "本科组",
        "vocational": "专科组",
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.CCPC

    return c


def get_team_info(team_info_xls_path: str):
    team_info = {}

    for row in utils.xls_iterator_per_row(team_info_xls_path):
        team_id = row[4].strip()

        team_info[team_id] = {}
        cur_team = team_info[team_id]

        cur_team["organization"] = row[1]
        cur_team["team_name"] = row[2]
        cur_team["team_id"] = team_id
        cur_team["members"] = row[3].split(" ")
        cur_team["members"] = sorted(cur_team["members"])
        cur_team["unofficial"] = False
        cur_team["girl"] = False
        cur_team["vocational"] = False

        if "女队" in team_id:
            cur_team["girl"] = True

        if "专科" in team_id:
            cur_team["vocational"] = True

        if team_id.startswith("*"):
            cur_team["unofficial"] = True
            cur_team["team_name"] = cur_team["team_name"][1:]

    return team_info


def handle_teams(teams: Teams, team_info_xls_path: str):
    res_teams = {}

    team_info = get_team_info(team_info_xls_path)

    for team_id, team in teams.items():
        team_key = team.name
        cur_team_info = team_info[team_key]

        team.name = cur_team_info["team_name"]
        team.organization = cur_team_info["organization"]
        team.members = cur_team_info["members"]

        if cur_team_info["unofficial"]:
            team.unofficial = 1
            team.official = 0
        else:
            team.official = 1

        if cur_team_info["girl"]:
            team.girl = 1

        cur_team = team.get_dict
        res_teams[team_id] = cur_team

        if cur_team_info["vocational"]:
            cur_team["vocational"] = 1
        elif not cur_team_info["unofficial"]:
            cur_team["undergraduate"] = 1

    return res_teams


def work(c: Contest, data_dir: str, fetch_uri: str,  cookies_str: str, team_info_xls_path: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {})
    utils.output(os.path.join(data_dir, "run.json"), [])

    while True:
        log.info("loop start")

        try:
            p = PTA(c, fetch_uri=fetch_uri, cookies_str=cookies_str)
            p.fetch().parse_teams().parse_runs()

            teams = handle_teams(p.teams, team_info_xls_path)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), teams)
            utils.output(os.path.join(data_dir, "run.json"), p.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")

        time.sleep(5)
