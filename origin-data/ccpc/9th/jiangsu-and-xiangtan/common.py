import time
import os
import json
import requests
import typing

from xcpcio_board_spider import logger, Contest, constants, logo, utils

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
        "jiangsu": "江苏省赛",
        "xiangtan": "CCPC 湘潭",
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.CCPC

    return c


def handle_teams(teams, fetch_uri, flag):
    current_teams = {}

    with open(os.path.join(fetch_uri, "team.json"), "r") as f:
        current_teams = json.loads(f.read())

    for team_id, t in current_teams.items():
        team_id = str(flag + team_id)
        t["team_id"] = team_id
        t[flag] = 1

        teams[team_id] = t


def handle_runs(runs, fetch_uri, flag):
    current_runs = []

    with open(os.path.join(fetch_uri, "run.json"), "r") as f:
        current_runs = json.loads(f.read())

    for r in current_runs:
        r["team_id"] = str(flag + r["team_id"])
        runs.append(r)


def work(c: Contest, data_dir: str, fetch_js_uri: str, fetch_xt_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {})
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_js_uri) == 0 and len(fetch_xt_uri) == 0:
        return

    while True:
        log.info("loop start")

        teams = {}
        runs = []

        handle_teams(teams, fetch_js_uri, "jiangsu")
        handle_runs(runs, fetch_js_uri, "jiangsu")

        handle_teams(teams, fetch_xt_uri, "xiangtan")
        handle_runs(runs, fetch_xt_uri, "xiangtan")

        utils.output(os.path.join(data_dir, "team.json"), teams)
        utils.output(os.path.join(data_dir, "run.json"), runs)

        try:
            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
