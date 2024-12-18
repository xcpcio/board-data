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

raw_dir = "raw"
data_dir = "../../../../data/icpc/2020/jinan"
problem_num = 13
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
group = {
    "official":"正式队伍",
    "unofficial":"打星队伍",
}
medal = {
    'official': {
        'gold': 35,
        'silver': 70,
        'bronze': 105
    }
}
status_time_display = {
    'correct': 1,
}
balloon_color = [
    {'background_color': 'rgba(189, 14, 14, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(255, 144, 228, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(255, 255, 255, 0.7)', 'color': '#000' },
    {'background_color': 'rgba(38, 185, 60, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(239, 217, 9, 0.7)', 'color': '#000' },
    {'background_color': 'rgba(243, 88, 20, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(12, 76, 138, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(156, 155, 155, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(4, 154, 115, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(159, 19, 236, 0.7)' ,'color': '#fff' },
    {'background_color': 'rgba(42, 197, 202, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(142, 56, 54, 0.7)', 'color': '#fff' },
    {'background_color': 'rgba(0, 0, 0, 0.7)', 'color': '#fff'},
]
config = {
    'contest_name': '第 45 届国际大学生程序设计竞赛（ICPC）亚洲区域赛（济南）正式赛',
    'start_time': get_timestamp("2020-12-27 11:00:00"),
    'end_time': get_timestamp("2020-12-27 16:00:00"),
    'problem_id': problem_id,
    'group': group,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    "frozen_time": 60 * 60,
    'medal': medal,
    'balloon_color': balloon_color,
}

def config_out():
    output("config.json", config)


mkdir(data_dir)
config_out()
