from pathlib import Path

from xcpcio_board_spider import Contest, Image, utils


def get_basic_contest():
    c = Contest()
    c.logo = Image(preset="CCPC")
    return c


def work(data_dir: Path, c: Contest):
    utils.ensure_makedirs(data_dir)
    utils.output(data_dir / "config.json", c.get_dict)
    utils.output(data_dir / "team.json", {}, True)
    utils.output(data_dir / "run.json", [], True)
