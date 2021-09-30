#!/usr/bin/env python
import requests
import json
from os import path
import os
import time
import bs4


def json_output(data):
    return json.dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)


def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))


def json_input(path):
    with open(path, 'r') as f:
        return json.load(f)


def get_now():
    return int(round(time.time() * 1000))


def get_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return int(round(timestamp * 1000))


def get_time_diff(l, r):
    return int((r - l) // 1000)


def ensure_dir(s):
    if not os.path.exists(s):
        os.makedirs(s)


_params = json_input('params.json')

headers = {}
data_dir = _params['data_dir']
board_url = _params['board_url']

ensure_dir(data_dir)


def fetch():
    total = 0

    params = ()
    response = requests.get(board_url, headers=headers, params=params)

    return response.text


def team_output(html):
    team = {}
    soup = bs4.BeautifulSoup(html, 'html5lib')
    tbody = soup.select('tbody')[0]
    trs = tbody.select('tr')

    for tr in trs:
        if tr.has_attr('participantid'):
            team_id = tr['participantid']
        else:
            continue

        _team = {}
        _team['official'] = 1
        _team['name'] = tr.select('td')[1].text.strip('\n ')

        team[team_id] = _team

    if len(team.keys()) > 0:
        output("team.json", team)


def run_output(html):
    run = []
    soup = bs4.BeautifulSoup(html, 'html5lib')
    tbody = soup.select('tbody')[0]
    trs = tbody.select('tr')

    for tr in trs:
        if tr.has_attr('participantid'):
            team_id = tr['participantid']
        else:
            continue

        _run = {}
        _run['team_id'] = team_id

        for i in range(4, 17):
            td = tr.select('td')[i]

            __run = _run.copy()
            __run['problem_id'] = i - 4

            span = td.select('span')[0]

            if span.get("class")[0] == "cell-rejected":
                text = span.text

                if '-' in text:
                    num = int(text.split('-')[1])
                else:
                    num = 0

                for j in range(num):
                    ___run = __run.copy()
                    ___run['status'] = 'incorrect'
                    ___run['timestamp'] = 0
                    run.append(___run)

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

                ___run = __run.copy()
                ___run['timestamp'] = timestamp

                for j in range(num):
                    ____run = ___run.copy()
                    ____run['status'] = 'incorrect'
                    run.append(____run)

                ____run = ___run.copy()
                ____run['status'] = 'correct'

                run.append(____run)

    if len(run) > 0:
        output('run.json', run)


def sync():
    while True:
        print("fetching...")

        try:
            html = fetch()

            team_output(html)
            run_output(html)

            print("fetch successfully")
        except Exception as e:
            print("fetch failed...")
            print(e)

        print("sleeping...")
        time.sleep(20)


sync()
