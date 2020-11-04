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

def urltobase64(url):
    import base64
    import requests as req
    from io import BytesIO
    # 图片保存在内存
    response = req.get(url)
    # 得到图片的base64编码
    img_data_b64 = base64.b64encode(BytesIO(response.content).read())
    return bytes.decode(img_data_b64)

data_dir = "../../../../data/icpc/2018/world-finals"
problem_num = 11
problem_id = [chr(ord('A') + i) for i in range(problem_num)] 
status_time_display = {
    'correct': 1,
}
medal = {
    "all": {
        "gold": 4,
        "silver": 4,
        "bronze": 4,
    }
}
balloon_color = [
    {'background_color': '#58a2d1', 'color': '#fff' },
    {'background_color': '#fc6d3e', 'color': '#000' },
    {'background_color': '#7c54aa', 'color': '#fff' },
    {'background_color': '#64d6cb', 'color': '#000' },
    {'background_color': '#ffffff;', 'color': '#000' },
    {'background_color': '#d5c748', 'color': '#fff' },
    {'background_color': '#e84054', 'color': '#fff' },
    {'background_color': '#ef80a6', 'color': '#fff' },
    {'background_color': '#000000', 'color': '#fff' },
    {'background_color': '#ad79d3' ,'color': '#fff' },
    {'background_color': '#63d869', 'color': '#fff' },
]
config = {
    'contest_name': 'ICPC2018-42nd World Finals',
    'start_time': get_timestamp("2018-4-19 09:00:00"),
    'end_time': get_timestamp("2018-4-19 14:00:00"),
    'frozen_time' : 60 * 60,
    'problem_id': problem_id,
    'medal': medal,
    'status_time_display': status_time_display,
    'penalty': 20 * 60,
    'banner': {
        'base64': urltobase64(path.join('https://acm.sdut.edu.cn/acmss/icpc/2018/beijing/', './src/banner.png')),
    },
    'balloon_color': balloon_color,
    'badge': 'Badge',
}

def config_out():
    output("config.json", config)

mkdir(data_dir)
config_out()
