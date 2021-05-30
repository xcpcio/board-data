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
        {'background_color': '#995f53', 'color': '#000' },
        {'background_color': '#bb93ab', 'color': '#000' },
        {'background_color': '#38183a', 'color': '#fff' },
        {'background_color': '#00363a', 'color': '#fff' },
        {'background_color': '#b5b3b9', 'color': '#000' },
        {'background_color': '#8a7312', 'color': '#000' },
        {'background_color': '#6a4926', 'color': '#fff' },
        {'background_color': '#054b53', 'color': '#fff' },
        {'background_color': '#4B6422', 'color': '#fff' },
        {'background_color': '#081460' ,'color': '#fff' },
        {'background_color': '#459b9c', 'color': '#fff' },
        {'background_color': '#917312', 'color': '#fff' },
        {'background_color': '#b6b2ac', 'color': '#fff'},
    ]
    
    return default_balloon_color[:num]

data_dir = "../../../../data/ccpc/2020/final"

problem_num = 13

group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
}

status_time_display = {
    'correct': 1,
    # 'incorrect': 1,
    # 'pending': 1,
}

medal = {
    "official": {
        'gold': 50,
        'silver': 100,
        'bronze': 150,
    }
}

config = {
    'contest_name': '第六届中国大学生程序设计竞赛总决赛（正式赛）',
    'start_time': get_timestamp("2021-5-30 9:00:00"),
    'end_time': get_timestamp("2021-5-30 14:00:00"),
    'frozen_time' : 60 * 60,
    'problem_id': generate_problem_label(problem_num),
    'group': group,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    # 'medal': medal,
    'balloon_color': generate_balloon_color(problem_num),
}

def config_out():
    output("config.json", config)

mkdir(data_dir)
config_out()