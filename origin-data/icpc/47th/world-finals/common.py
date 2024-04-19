import os
import time
import shutil

from xcpcio_board_spider import logger, Contest, Teams, constants, logo, utils, Image
from xcpcio_board_spider.spider.domjudge.v2 import DOMjudge

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = "../world-finals-assets"

log = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = None

    c.group = {}

    c.status_time_display = {
        constants.RESULT_CORRECT.lower(): True,
        constants.RESULT_INCORRECT.lower(): False,
        constants.RESULT_PENDING.lower(): False,
    }

    c.logo = logo.ICPC
    c.banner = Image(url=f"{ASSETS_PATH}/banner.min.png")

    return c


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


def work(c: Contest, data_dir: str, fetch_uri: str):
    utils.ensure_makedirs(data_dir)
    utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"), {}, True)
    utils.output(os.path.join(data_dir, "run.json"), [], True)
    copy_assets(data_dir)

    while True:
        log.info("loop start")

        try:
            d = DOMjudge(c, fetch_uri)
            d.fetch().parse_contest().parse_teams().parse_runs()

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(1)
