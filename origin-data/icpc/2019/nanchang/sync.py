import requests
import json
from os import path
import time
import bs4
import os

def json_input(path):
    with open(path, 'r') as f:
        return json.load(f)

_params = json_input('params.json')
data_dir = _params['data_dir']
image_download_host = _params['image_download_host']
charset = _params['charset']
end_time = _params['end_time']
start_time = _params['start_time']

def json_output(data):
    return json.dumps(data, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)

def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))

def get_timestamp(dt):
    #转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def get_now():
    return int(time.time())

def get_incorrect_timestamp():
    return min(get_now(), get_timestamp(end_time)) - get_timestamp(start_time)

def mkdir(_path):
    if not path.exists(_path):
        os.makedirs(_path)

def urltobase64(url):
    from PIL import Image
    import urllib.request
    from io import StringIO
    from io import BytesIO
    import base64

    max_length = 32

    print("downloading... " + url)
    origin_file = BytesIO(urllib.request.urlopen(url).read())
    img = Image.open(origin_file)
    w, h = img.size
    larger_side = max(w, h)
    if larger_side > max_length:
        img = img.resize((int(float(max_length) * w / larger_side),
                          int(float(max_length) * h / larger_side)), Image.ANTIALIAS)
    jpeg_image_buffer = BytesIO()
    img.save(jpeg_image_buffer, format="PNG")
    base64_str = base64.b64encode(jpeg_image_buffer.getvalue())
    print(url + " downloaded.")
    return bytes.decode(base64_str)

def fetch():
    if 'board_url' in _params.keys():
        board_url = _params['board_url']
        params = (
            ('t', get_now()),
        )   
        response = requests.get(board_url, params=params)
        html = response.text.encode("latin1").decode(charset)
        return html
    else:
        board_file = _params['board_file']
        with open(board_file, 'r') as f:
            return f.read()

def team_out(html):
    team = {}
    soup = bs4.BeautifulSoup(html,'html5lib')
    # 默认选择第0个 如果在榜单前出现其他 tbody 元素会出错
    tbody = soup.select('tbody')[0]
    # print(tbody)
    trs = tbody.select('tr')
    for tr in trs:
        if 'id' in tr.attrs:
            _team = {}
            team_id = tr['id']

            img_src = tr.select('img')[0]['src'].split('?')[0]

            name = ""
            scoretn = tr.select('.scoretn')[0].contents
            if str(scoretn[0])[0] == '<':
                name = scoretn[1]
            else:
                name = scoretn[0]

            if len(name) > 0 and name[0] == '*':
                name = name[1:len(name)]
                _team['unofficial'] = 1
            else:
                _team['official'] = 1

            try:
                if tr.select('.scoretn')[0]['style'] == 'background: #78ff57;':
                    _team['girl'] = 1
            except:
                pass
            
            _team['organization'] = tr.select('img')[0]['title']
            badge_base64 = urltobase64(path.join(image_download_host, img_src))
            _team['badge'] = {}
            _team['badge']['base64'] = badge_base64
            _team['name'] = name
            team[team_id] = _team

    if len(team.keys()) > 0:
        output("team.json", team)

def run_out(html):
    run = []
    soup = bs4.BeautifulSoup(html,'html5lib')
    # 默认选择第0个 如果在榜单前出现其他 tbody 元素会出错
    tbody = soup.select('tbody')[0]
    trs = tbody.select('tr')
    for tr in trs:
        if 'id' in tr.attrs:
            team_id = tr['id']
            _run = {}
            _run['team_id'] = team_id
            
            score_cells = tr.select('.score_cell')
            index = -1
            for score_cell in score_cells:
                index += 1
                _run['problem_id'] = index
                score_correct = score_cell.select('.score_correct')
                score_incorrect = score_cell.select('.score_incorrect')

                if len(score_correct) > 0:
                    timestamp = int(score_correct[0].contents[0].split('\n')[0].strip()) * 60
                    cnt = int(score_correct[0].contents[1].string.split('\n')[0].strip().split(' ')[0])
                    _run['timestamp'] = timestamp
                    _run['status'] = 'incorrect'
                    for i in range(1, cnt):
                        run.append(_run.copy())
                    _run['status'] = 'correct'
                    run.append(_run.copy())

                if len(score_incorrect) > 0:
                    cnt = int(score_incorrect[0].select('span')[0].string.split('\n')[0].strip().split(' ')[0])
                    for i in range(cnt):
                        _run['status'] = 'incorrect'
                        _run['timestamp'] = get_incorrect_timestamp()
                        run.append(_run.copy())
            
    if len(run) > 0:
        output('run.json', run)

def sync():
    while True:
        print("fetching...")
        try:
            html = fetch()
            team_out(html)
            run_out(html)
            print("fetch successfully")
        except Exception as e:
            print("fetch failed...")
            print(e)
        print("sleeping...")
        time.sleep(20)

sync()