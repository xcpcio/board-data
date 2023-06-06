import time
import os

from xcpcio_board_spider import Contest, logger, utils, constants, logo

from xcpcio_board_spider.spider.domjudge.v2 import DOMjudge as DOMjudgeV2
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge as DOMjudgeV3


l = logger.init_logger()


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

    c.logo = logo.ICPC

    return c


def handle_from_domjudge_html_scoreboard(c: Contest, fetch_uri: str):
    d = DOMjudgeV2(c, fetch_uri)
    d.fetch().parse_teams().parse_runs()

    for t in d.teams.values():
        if "cl_FFB7C5" in DOMjudgeV2.get_team_class_attr(t):
            t.girl = 1

        if t.name.startswith("⭐"):
            t.name = t.name[1:]
            t.official = 0
            t.unofficial = 1
        else:
            t.official = 1

    return d.teams.get_dict, d.runs.get_dict


def handle_teams_from_domjudge_api(c: Contest, fetch_uri: str):
    d = DOMjudgeV3(c, fetch_uri)
    d.fetch().parse_teams().parse_runs()

    filter_team_id = []

    for t in d.teams.values():
        d_team = t.extra[DOMjudgeV3.CONSTANT_EXTRA_DOMJUDGE_TEAM]

        if t.name.startswith("⭐"):
            t.name = t.name[1:]

        if "3" in d_team["group_ids"]:
            t.official = 1

        if "4" in d_team["group_ids"]:
            t.unofficial = 1

        if "5" in d_team["group_ids"]:
            t.girl = 1
            t.official = 1

    for t_id in filter_team_id:
        del d.teams[t_id]

    return d.teams.get_dict, d.runs.get_dict


def work(data_dir: str, c: Contest, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if os.getenv("ENABLE_SPIDER") != "true":
        return

    while True:
        l.info("loop start")

        try:
            if ".html" in fetch_uri:
                teams, runs = handle_from_domjudge_html_scoreboard(
                    c, fetch_uri)
            else:
                teams, runs = handle_teams_from_domjudge_api(c, fetch_uri)

            utils.output(os.path.join(data_dir, "team.json"), teams)
            utils.output(os.path.join(data_dir, "run.json"), runs)

            l.info("work successfully")
        except Exception as e:
            l.error("work failed. ", e)

        l.info("sleeping...")

        time.sleep(5)
