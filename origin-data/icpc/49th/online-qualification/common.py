import time
from pathlib import Path

from xcpcio_board_spider import logger, Contest, constants, utils
from xcpcio_board_spider.spider.pta.v2 import PTA
from xcpcio_board_spider.type import Image

logger = logger.init_logger()


def get_basic_contest():
    c = Contest()
    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"
    c.status_time_display = constants.FULL_STATUS_TIME_DISPLAY
    c.logo = Image(preset="ICPC")
    return c


def work(data_dir: Path, contest_id: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(data_dir / "config.json", c.get_dict)
    utils.output(data_dir / "team.json", {}, True)
    utils.output(data_dir / "run.json", [], True)

    while True:
        logger.info("loop start")
        try:
            pta = PTA(c, contest_id)
            pta.run(fetch_runs=True)
            utils.output(data_dir / "config.json", c.get_dict)
            utils.output(data_dir / "team.json",
                         pta.teams.get_dict)
            utils.output(data_dir / "run.json", pta.runs.get_dict)
            logger.info("work successfully")
        except Exception as e:
            logger.error(f"work failed: {e}")
        logger.info("sleeping...")
        time.sleep(1)
