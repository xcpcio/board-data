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

data_dir = "../../../../data/provincial-contest/2019/jscpc"
problem_num = 12
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
status_time_display = {
    'correct': 1,
}
balloon_color = [
    {'background_color': '#f50000', 'color': '#fff' },
    {'background_color': '#ff38d1', 'color': '#fff' },
    {'background_color': '#d4933f', 'color': '#000' },
    {'background_color': '#45ff51', 'color': '#fff' },
    {'background_color': '#f9ff54', 'color': '#000' },
    {'background_color': '#ff6a3d', 'color': '#fff' },
    {'background_color': '#ffffff', 'color': '#000' },
    {'background_color': '#6a0ff2', 'color': '#fff' },
    {'background_color': '#c670db', 'color': '#fff' },
    {'background_color': '#000000' ,'color': '#fff' },
    {'background_color': '#6bc9a0', 'color': '#000' },
    {'background_color': '#149918', 'color': '#fff' },
]
group = {
    'official': '正式队伍',
    'unofficial': '打星队伍'
}

config = {
    'contest_name': '“SHEIN杯”2019年江苏省大学生程序设计大赛',
    'start_time': get_timestamp("2019-5-14 9:00:00"),
    'end_time': get_timestamp("2019-5-14 14:00:00"),
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
