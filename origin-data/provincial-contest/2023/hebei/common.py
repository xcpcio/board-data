import time
import os

from xcpcio_board_spider import logger, Contest, Teams, constants, logo, utils

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
        cur_team["team_name"] = row[3]
        cur_team["team_id"] = team_id
        cur_team["members"] = []
        cur_team["official"] = True

        for ix in [5, 6, 7]:
            if len(row[ix]) > 0:
                cur_team["members"].append(row[ix])

        cur_team["members"] = sorted(cur_team["members"])
        cur_team["type"] = row[8]

    return team_info


def handle_teams(teams: Teams, team_info_xls_path: str):
    team_info = get_team_info(team_info_xls_path)

    for team in teams.values():
        team_key = team.name

        if team_key not in team_info.keys():
            if team_key.startswith("*"):
                team_key = team_key[1:]

            school, name = team_key.split("-")

            team.name = name
            team.organization = school

            team.official = 0
            team.unofficial = 1
        else:
            cur_team_info = team_info[team_key]

            team.name = cur_team_info["team_name"]
            team.organization = cur_team_info["organization"]
            team.members = cur_team_info["members"]

            if cur_team_info["type"] == "打星名额":
                team.unofficial = 1
                team.official = 0
            else:
                team.official = 1
                if cur_team_info["type"] == "女队名额":
                    team.girl = 1


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {})
    utils.output(os.path.join(data_dir, "run.json"), [])

    while True:
        log.info("loop start")

        try:
            # p = PTA(c, fetch_uri=fetch_uri, cookies_str=cookies_str)
            # p.fetch().parse_teams().parse_runs()

            # handle_teams(p.teams, team_info_xls_path)

            # utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            # utils.output(os.path.join(data_dir, "team.json"), p.teams.get_dict)
            # utils.output(os.path.join(data_dir, "run.json"), p.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")

        time.sleep(5)
