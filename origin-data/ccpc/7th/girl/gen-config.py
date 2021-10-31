from os import path
import os
import json
import time


def json_output(data):
    return json.dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)


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


def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))


def generate_problem_label(num):
    return [chr(ord('A') + i) for i in range(num)]


def generate_balloon_color(num):
    default_balloon_color = [
        {'background_color': '#d71345', 'color': '#fff'},
        {'background_color': '#f1b8e4', 'color': '#000'},
        {'background_color': '#f391a9', 'color': '#000'},
        {'background_color': '#7d5886', 'color': '#fff'},
        {'background_color': '#c37e00', 'color': '#fff'},
        {'background_color': '#411445', 'color': '#fff'},
        {'background_color': '#005831', 'color': '#fff'},
        {'background_color': '#fffffb', 'color': '#000'},
        {'background_color': '#ffd400', 'color': '#000'},
        {'background_color': '#a1a3a6', 'color': '#fff'},
        {'background_color': '#004080', 'color': '#fff'},
        {'background_color': 'rgba(142, 56, 54, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(0, 0, 0, 0.7)', 'color': '#fff'},
    ]

    return default_balloon_color[:num]


raw_dir = "raw"
data_dir = "../../../../data/ccpc/7th/girl/"

problem_num = 11

group = {
    # 'official': '正式队伍',
    # 'unofficial': '打星队伍',
}

status_time_display = {
    'correct': 1,
    'incorrect': 1,
    'pending': 1,
}

medal = {
    "all": {
        'gold': 26,
        'silver': 52,
        'bronze': 78,
    }
}

config = {
    'contest_name': '2021 年中国大学生程序设计竞赛女生专场 正式赛',
    'start_time': get_timestamp("2021-10-31 9:00:00"),
    'end_time': get_timestamp("2021-10-31 14:00:00"),
    'frozen_time': 60 * 60,
    'problem_id': generate_problem_label(problem_num),
    'group': group,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    'medal': medal,
    'balloon_color': generate_balloon_color(problem_num),
}


def config_out():
    output("config.json", config)


mkdir(data_dir)
config_out()
