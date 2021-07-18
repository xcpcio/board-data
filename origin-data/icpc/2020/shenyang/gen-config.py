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
        {'background_color': '#614307', 'color': '#fff' },
        {'background_color': '#8100b8', 'color': '#fff' },
        {'background_color': '#80ff00', 'color': '#000' },
        {'background_color': '#5cffff', 'color': '#000' },
        {'background_color': '#0ddb89', 'color': '#000' },
        {'background_color': '#ff0000', 'color': '#fff' },
        {'background_color': '#ffff00', 'color': '#000' },
        {'background_color': '#0000ff', 'color': '#fff' },
        {'background_color': '#ff99f5', 'color': '#000' },
        {'background_color': '#ffffff' ,'color': '#000' },
        {'background_color': '#ff7700', 'color': '#fff' },
        {'background_color': '#a6a6a6', 'color': '#fff' },
        {'background_color': '#000000', 'color': '#fff'},
    ]
    
    return default_balloon_color[:num]

raw_dir = "raw"
data_dir = "../../../../data/icpc/2020/shenyang"

problem_num = 13

group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
}

status_time_display = {
    'correct': 1,
    'incorrect': 1,
    'pending': 1,
}

medal = {
    "official": {
        'gold': 26,
        'silver': 52,
        'bronze': 78,
    }
}

config = {
    'contest_name': 'The 45th ICPC Asia Shenyang Regional Programming Contest',
    'start_time': get_timestamp("2021-7-18 9:00:00"),
    'end_time': get_timestamp("2021-7-18 14:00:00"),
    'frozen_time' : 60 * 60,
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