import time
import os
import json
import requests

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
    }

    c.status_time_display = {
        constants.RESULT_CORRECT: 1,
        constants.RESULT_INCORRECT: 1,
        constants.RESULT_PENDING: 1,
    }

    c.logo = logo.CCPC

    return c


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)

    with open("./raw/team.json", "r") as f:
        utils.output(os.path.join(data_dir, "team.json"), json.loads(f.read()))

    utils.output(os.path.join(data_dir, "run.json"), [], True)

    while True:
        log.info("loop start")

        try:
            raw_runs = []

            if os.path.exists(fetch_uri):
                with open(fetch_uri) as f:
                    raw_runs = json.loads(f.read())
            else:
                req = requests.get(fetch_uri)
                raw_runs = json.loads(req.content)

            runs = []
            for run in raw_runs:
                status = run["status"]
                team_id = str(run["team_id"])
                timestamp = int(run["timestamp"])
                timestamp = timestamp // 60 * 60

                run["team_id"] = team_id
                run["timestamp"] = timestamp

                if status == "ce":
                    continue

                if status == "ac":
                    run["status"] = constants.RESULT_CORRECT
                elif status == "waiting":
                    run["status"] = constants.RESULT_PENDING
                else:
                    run["status"] = constants.RESULT_INCORRECT

                runs.append(run)

            utils.frozen_fallback(c, runs)
            utils.output(os.path.join(data_dir, "run.json"), runs)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
