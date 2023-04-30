from os import path
import os
import json
import time


def json_input(path):
    with open(path, 'r') as f:
        return json.load(f)


def mkdir(_path):
    if not path.exists(_path):
        os.makedirs(_path)


def get_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def json_output(data):
    return json.dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)


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


def output(filename, data, if_not_exists=False):
    dir_name = path.join(data_dir, filename)

    if if_not_exists and path.exists(dir_name):
        return

    with open(dir_name, 'w') as f:
        f.write(json_output(data))


def generate_problem_label(num):
    return [chr(ord('A') + i) for i in range(num)]


def generate_balloon_color(num):
    return default_balloon_color[:num]


default_balloon_color = [
    {'background_color': '#15BA47', 'color': '#fff'},
    {'background_color': '#951FD9', 'color': '#fff'},
    {'background_color': 'rgba(255, 255, 255, 0.7)', 'color': '#000'},
    {'background_color': 'rgba(38, 185, 60, 0.7)', 'color': '#fff'},
]

data_dir = "../../../../data/provincial-contest/2023/wuhan-warmup"

problem_num = 3

group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
    'girl': '女队'
}

status_time_display = {
    'correct': 1,
    'incorrect': 1,
    'pending': 1,
}

medal = {
    "official": {
        'gold': 35,
        'silver': 70,
        'bronze': 105,
    }
}

config = {
    'contest_name': '第五届湖北省大学生程序设计竞赛（热身赛）',
    'start_time': get_timestamp("2023-4-29 15:00:00"),
    'end_time': get_timestamp("2023-4-29 17:00:00"),
    'frozen_time': 30 * 60,
    'problem_id': generate_problem_label(problem_num),
    'group': group,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    # 'medal': medal,
    'balloon_color': generate_balloon_color(problem_num),
    # 'logo': {
    #     'base64': urltobase64('https://raw.githubusercontent.com/XCPCIO/logo/main/icpc/icpc_logo_with_word.min.png')
    # }
}


mkdir(data_dir)
output("config.json", config)
output("team.json", {}, True)
output("run.json", [], True)
