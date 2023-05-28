import time
import os
import json

from xcpcio_board_spider import logger, Contest, constants, logo, utils, Team, Teams
from xcpcio_board_spider.spider.domjudge.v3.domjudge import DOMjudge

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
            t.members = d_team["public_description"].split("、")
            t.members = sorted(t.members)

        if "2023zjcpc_warmup_observers" in d_team["group_ids"] or "2023zjcpc_official_observers" in d_team["group_ids"]:
            t.unofficial = 1
        elif "2023zjcpc_warmup_undergraduate" in d_team["group_ids"] or "2023zjcpc_official_undergraduate" in d_team["group_ids"]:
            t.official = 1
            t.extra["undergraduate"] = True
        elif "2023zjcpc_warmup_specialist" in d_team["group_ids"] or "2023zjcpc_official_specialist" in d_team["group_ids"]:
            t.official = 1
            t.extra["vocational"] = True

    for t_id in filter_team_id:
        del teams[t_id]


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()

            handle_teams(d.teams)

            teams = {}
            for t in d.teams.values():
                team_id = t.team_id
                teams[team_id] = t.get_dict

                if "undergraduate" in t.extra.keys():
                    teams[team_id]["undergraduate"] = 1

                if "vocational" in t.extra.keys():
                    teams[team_id]["vocational"] = 1

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), teams)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
