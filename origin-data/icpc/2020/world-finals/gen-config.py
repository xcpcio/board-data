from os import path
import os
import json
import time


def mkdir(_path):
    if not path.exists(_path):
        os.makedirs(_path)


def get_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def urltobase64(url):
    import base64
    import requests as req
    from io import BytesIO

    if os.path.isfile(url):
        f = open(url, 'rb')
        img_data_b64 = base64.b64encode(f.read())
        f.close()
    else:
        response = req.get(url)
        img_data_b64 = base64.b64encode(BytesIO(response.content).read())

    return bytes.decode(img_data_b64)


def json_output(data):
    return json.dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)


def json_input(path):
    with open(path, 'r') as f:
        return json.load(f)


def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))


def generate_problem_label(num):
    return [chr(ord('A') + i) for i in range(num)]


def generate_balloon_color(num):
    default_balloon_color = [
        {'background_color': '#ed0206', 'color': '#fff'},
        {'background_color': '#af6b29', 'color': '#fff'},
        {'background_color': '#85abf3', 'color': '#000'},
        {'background_color': '#60a001', 'color': '#fff'},
        {'background_color': '#d7a476', 'color': '#000'},
        {'background_color': '#ff8600', 'color': '#fff'},
        {'background_color': '#ff70b2', 'color': '#000'},
        {'background_color': '#0086de', 'color': '#fff'},
        {'background_color': '#b073e0', 'color': '#000'},
        {'background_color': '#ffffff', 'color': '#000'},
        {'background_color': '#032abf', 'color': '#fff'},
        {'background_color': '#08b4b3', 'color': '#fff'},
        {'background_color': '#6800cf', 'color': '#fff'},
        {'background_color': '#fff400', 'color': '#000'},
        {'background_color': '#000000', 'color': '#fff'},
    ]

    return default_balloon_color[:num]


raw_dir = "raw"
data_dir = "../../../../data/icpc/2020/world-finals/"

problem_num = 15

group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
}

status_time_display = {
    'correct': 1,
}

medal = {
    "official": {
        'gold': 30,
        'silver': 60,
        'bronze': 90,
    }
}

config = {
    'contest_name': 'ICPC 44th World Finals',
    'start_time': get_timestamp("2021-10-5 14:21:00"),
    'end_time': get_timestamp("2021-10-5 19:21:00"),
    'frozen_time': 60 * 60,
    'problem_id': generate_problem_label(problem_num),
    # 'group': group,
    # 'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    # 'medal': medal,
    'banner': {
        'base64': urltobase64('./raw/banner-compress.png'),
    },
    'balloon_color': generate_balloon_color(problem_num),
}


def config_out():
    output("config.json", config)


mkdir(data_dir)
config_out()
