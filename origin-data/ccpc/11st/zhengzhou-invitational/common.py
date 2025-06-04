import json
import time
from pathlib import Path

from xcpcio_board_spider import Contest, Image, logger, utils

log = logger.init_logger()

def get_basic_contest():
    c = Contest()
    c.logo = Image(preset="CCPC")
    return c


def work(data_dir: Path, fetch_uri: str, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(data_dir / "config.json", c.get_dict)
    utils.output(data_dir / "team.json", {}, True)
    utils.output(data_dir / "run.json", [], True)

    if len(fetch_uri) == 0:
        return

    while True:
        log.info("loop start")

        try:
            base_path = Path(fetch_uri)
            for asset in ["config", "team", "run"]:
                with open(base_path / f"{asset}.json", "r") as f:
                    utils.output(data_dir / f"{asset}.json",
                                json.loads(f.read()), False)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")
        time.sleep(5)
