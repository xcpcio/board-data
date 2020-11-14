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
data_dir = "../../../../data/provincial-contest/2020/jscpc"
problem_num = 5
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
group = {
}
status_time_display = {
    'correct': 1,
}
config = {
    'contest_name': '2020ICPC 江西省大学生程序设计竞赛热身赛',
    'start_time': get_timestamp("2020-11-14 15:00:00"),
    'end_time': get_timestamp("2020-11-14 18:00:00"),
    'frozen_time' : 0,
    'problem_id': problem_id,
    'group': group,
    'organization': 'School',
    'status_time_display': status_time_display,
    'penalty': 60 * 60,
}

def config_out():
    output("config.json", config)


mkdir(data_dir)
config_out()
