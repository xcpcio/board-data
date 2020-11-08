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

data_dir = "../../../../data/icpc/2019/nanchang"
problem_num = 13
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
status_time_display = {
    'correct': 1,
}
balloon_color = [
    {'background_color': '#ff0000', 'color': '#fff' },
    {'background_color': '#0011ff', 'color': '#fff' },
    {'background_color': '#00660a', 'color': '#fff' },
    {'background_color': '#ffff00', 'color': '#000' },
    {'background_color': '#ffffff', 'color': '#000' },
    {'background_color': '#ff9900', 'color': '#fff' },
    {'background_color': '#AE435F', 'color': '#000' },
    {'background_color': '#5A458A', 'color': '#fff' },
    {'background_color': '#050180', 'color': '#fff' },
    {'background_color': '#45d4ff' ,'color': '#fff' },
    {'background_color': '#6e3b39', 'color': '#fff' },
    {'background_color': '#d593c3', 'color': '#fff' },
    {'background_color': '#00ff33', 'color': '#fff' },
]
group = {
    'official': '正式队伍',
    'unofficial': '打星队伍',
    'girl': '女队',
}

config = {
    'contest_name': 'The 44th ICPC International Collegiate Programming Contest Asian Regional Contest (Nanchang)',
    'start_time': get_timestamp("2019-11-11 9:00:00"),
    'end_time': get_timestamp("2019-11-11 14:00:00"),
    'frozen_time' : 60 * 60,
    'problem_id': problem_id,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    'balloon_color': balloon_color,
    'badge': 'Badge',
    'group': group,
}

def config_out():
    output("config.json", config)

mkdir(data_dir)
config_out()
