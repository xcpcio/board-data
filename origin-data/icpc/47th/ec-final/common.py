import time
import os
import re

from xcpcio_board_spider import Teams, Contest, logger, utils, constants, Image
from xcpcio_board_spider.spider.ghost.v1 import Ghost


log = logger.init_logger()


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60
    c.organization = "School"

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
    }

    c.status_time_display = constants.FULL_STATUS_TIME_DISPLAY

    c.logo = Image(preset="ICPC")

    return c


def handle_team(teams: Teams):
    for team in teams.values():
        if team.name.startswith("★"):
            team.name = team.name[1:]
            team.unofficial = True
        else:
            team.official = True

        ix = 0
        cnt = 0
        for c in team.name[::-1]:
            if c == ')':
                cnt += 1
            elif c == '(':
                if cnt == 1:
                    break
                else:
                    cnt -= 1
            ix += 1

        team.organization = team.name[-ix:-1]
        team.name = team.name[:-ix - 1]


def work(data_dir: str, fetch_uri: str, c: Contest):
    while True:
        log.info("loop start")

        try:
            d = Ghost(c, fetch_uri)
            d.fetch().parse_teams().parse_runs()

            handle_team(d.teams)

            utils.output(os.path.join(data_dir, "config.json"), c.get_dict)
            utils.output(os.path.join(data_dir, "team.json"), d.teams.get_dict)
            utils.output(os.path.join(data_dir, "run.json"), d.runs.get_dict)

            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)

        log.info("sleeping...")

        time.sleep(5)
