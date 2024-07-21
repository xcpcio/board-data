import time
import os
from pathlib import Path
import requests
import bs4
import copy

from xcpcio_board_spider import logger, Contest, constants, logo, utils, Team, Teams, Submissions, Submission
from xcpcio_board_spider.type import Image

log = logger.init_logger()

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../../data/camp/tsinghua/2024/online-qualification")
FETCH_URI = os.getenv(
    "FETCH_URI", "")
COOKIE = os.getenv("COOKIE", "")


def get_basic_contest():
    c = Contest()

    c.frozen_time = 60 * 60
    c.penalty = 20 * 60

    c.group = {
        constants.TEAM_TYPE_OFFICIAL: constants.TEAM_TYPE_ZH_CN_OFFICIAL,
        constants.TEAM_TYPE_UNOFFICIAL: constants.TEAM_TYPE_ZH_CH_UNOFFICIAL,
    }
    c.organization = None

    return c


def fetch(uri: str) -> str:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': COOKIE,
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    resp = requests.get(uri, headers=headers, timeout=20, verify=False)
    if resp.status_code != 200:
        raise RuntimeError(
            f"fetch failed. [status_code={resp.status_code}]")
    return resp.text


def parse_pagination(html: str) -> int:
    soup = bs4.BeautifulSoup(html, 'html5lib')
    pagination_div = soup.select('.custom-links-pagination')[0]
    children = pagination_div.find_all(recursive=False)
    return len(children)


def parse_teams(html: str) -> Teams:
    teams = Teams()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    tbody = soup.select('tbody')[0]
    trs = tbody.select('tr')
    for tr in trs:
        if tr.has_attr('participantid'):
            team_id = tr['participantid']
        else:
            continue
        name = tr.select('td')[1].text.strip('\n ')
        team = Team()
        team.team_id = team_id
        team.name = name
        team.official = True
        teams[team_id] = team
    return teams


def parse_submissions(html: str) -> Submissions:
    soup = bs4.BeautifulSoup(html, 'html5lib')
    tbody = soup.select('tbody')[0]
    trs = tbody.select('tr')
    submissions = Submissions()

    for tr in trs:
        if tr.has_attr('participantid'):
            team_id = tr['participantid']
        else:
            continue

        submission = Submission()
        submission.team_id = team_id

        for i in range(4, 17):
            tds = tr.select('td')
            try:
                td = tr.select('td')[i]
            except:
                continue

            _submission = copy.deepcopy(submission)
            _submission.problem_id = i - 4

            span = td.select('span')[0]

            if span.get("class")[0] == "cell-rejected":
                text = span.text

                if '-' in text:
                    num = int(text.split('-')[1])
                else:
                    num = 0

                for j in range(num):
                    __submission = copy.deepcopy(_submission)
                    __submission.status = constants.RESULT_REJECTED
                    __submission.timestamp = 0
                    submissions.append(__submission)

            elif span.get("class")[0] == "cell-accepted":
                text = span.text

                if text == '+':
                    num = 0
                else:
                    num = int(text.split('+')[1])

                timestamp_text = td.select('span')[1].text
                h = int(timestamp_text.split(':')[0])
                m = int(timestamp_text.split(':')[1])
                timestamp = h * 60 * 60 + m * 60

                __submission = copy.deepcopy(_submission)
                __submission.timestamp = timestamp

                for j in range(num):
                    ___submission = copy.deepcopy(__submission)
                    ___submission.status = constants.RESULT_REJECTED
                    ___submission.timestamp = 0
                    submissions.append(___submission)

                ___submission = copy.deepcopy(__submission)
                ___submission.status = constants.RESULT_CORRECT
                submissions.append(___submission)
    return submissions


def write_to_disk(data_dir: str, c: Contest, teams: Teams, runs: Submissions, if_not_exists=False):
    log.info("write to disk. [data_dir: {}]".format(data_dir))

    utils.ensure_makedirs(data_dir)

    utils.output(os.path.join(data_dir, "config.json"),
                 c.get_dict)
    utils.output(os.path.join(data_dir, "team.json"),
                 teams.get_dict, if_not_exists=if_not_exists)
    utils.output(os.path.join(data_dir, "run.json"),
                 runs.get_dict, if_not_exists=if_not_exists)


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
            teams = Teams()
            submissions = Submissions()
            page = 1
            cur_index = 1
            while cur_index <= page:
                uri = f"{fetch_uri}/groupmates/true/page/{cur_index}"
                resp = fetch(uri)
                page = parse_pagination(resp)
                log.info(f"fetch page {cur_index}/{page}")
                _teams = parse_teams(resp)
                _submissions = parse_submissions(resp)
                teams.update(_teams)
                submissions.extend(_submissions)
                cur_index += 1
            write_to_disk(data_dir, c, teams, submissions)
            log.info("work successfully")
        except Exception as e:
            log.error("work failed. ", e)
        log.info("sleeping...")
        time.sleep(10)


if __name__ == "__main__":
    c = get_basic_contest()
    c.contest_name = "Tsinghua Bootcamp 2024. Qualification Round"
    c.problem_quantity = 12
    c.start_time = utils.get_timestamp_second("2024-07-21 13:00:00")
    c.end_time = utils.get_timestamp_second("2024-07-21 18:00:00")
    c.fill_problem_id().fill_balloon_color()
    work(c, DATA_DIR, FETCH_URI)
