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
        {'background_color': '#bd0e0e', 'color': '#fff'},
        {'background_color': '#ff90e4', 'color': '#fff'},
        {'background_color': '#ffffff', 'color': '#000'},
        {'background_color': 'rgba(38, 185, 60, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(239, 217, 9, 0.7)', 'color': '#000'},
        {'background_color': 'rgba(243, 88, 20, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(12, 76, 138, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(156, 155, 155, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(4, 154, 115, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(159, 19, 236, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(42, 197, 202, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(142, 56, 54, 0.7)', 'color': '#fff'},
        {'background_color': 'rgba(0, 0, 0, 0.7)', 'color': '#fff'},
    ]

    return default_balloon_color[:num]


raw_dir = "raw"
data_dir = "../../../../data/provincial-contest/2021/henan-warmup"

problem_num = 3

group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
    'girl': '女队',
}

status_time_display = {
    'correct': 1,
    'incorrect': 1,
    'pending': 1,
}

medal = {
    "official": {
        'gold': 22,
        'silver': 44,
        'bronze': 66,
    }
}

config = {
    'contest_name': '2021 年河南省第三届 CCPC 大学生程序设计竞赛热身赛',
    'start_time': get_timestamp("2021-10-30 9:00:00"),
    'end_time': get_timestamp("2021-10-30 11:00:00"),
    'frozen_time': 0,
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
