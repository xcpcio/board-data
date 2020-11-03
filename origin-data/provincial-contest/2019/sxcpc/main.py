from os import path
import os
import json
import time

def json_output(data):
    return json.dumps(data, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)

def json_input(path):
    with open(path, 'r') as f:
        return json.load(f)

def mkdir(_path):
    if not path.exists(_path):
        os.makedirs(_path)

def get_timestamp(dt):
    #转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))

data_dir = "../../../../data/provincial-contest/2019/sxcpc"
problem_num = 12
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
status_time_display = {
    'correct': 1,
}
balloon_color = [
    {'background_color': 'orange', 'color': '#fff' },
    {'background_color': 'black', 'color': '#fff' },
    {'background_color': '#87CEFA', 'color': '#000' },
    {'background_color': 'RED', 'color': '#fff' },
    {'background_color': '#2F4F4F', 'color': '#fff' },
    {'background_color': 'blue', 'color': '#fff' },
    {'background_color': 'white', 'color': '#000' },
    {'background_color': '#8B008B', 'color': '#fff' },
    {'background_color': 'green', 'color': '#fff' },
    {'background_color': 'purple' ,'color': '#fff' },
    {'background_color': 'yellow', 'color': '#000' },
    {'background_color': 'pink', 'color': '#fff' },
]
config = {
    'contest_name': 'The 2019 ICPC China Shaanxi Provincial Programming Contest',
    'start_time': get_timestamp("2019-6-2 12:00:00"),
    'end_time': get_timestamp("2019-6-2 17:00:00"),
    'frozen_time' : 60 * 60,
    'problem_id': problem_id,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    'balloon_color': balloon_color,
    'badge': 'Badge',
}

def config_out():
    output("config.json", config)

mkdir(data_dir)
config_out()
