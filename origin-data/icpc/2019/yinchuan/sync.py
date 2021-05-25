from json import dumps, load, loads
from os import path, makedirs

def json_input(path):
    with open(path, 'r') as f:
        return load(f)

_params = json_input('params.json')

data_dir = _params['data_dir']
ghosts_file_path = _params['ghosts_file_path']

def json_output(data):
    return dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)

def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))

def ensure_dir(_path):
    if not path.exists(_path):
        makedirs(_path)

def team_out(data):
    teams = {}
    
    for line in data:
      if line[0] == '{':
        raw_data = loads(line)
        
        team = {}
        
        team['name'] = raw_data['teamname_raw']
        team['organization'] = raw_data['school_raw']
        
        if raw_data['category'] == "Participants":
          team['official'] = 1
        elif raw_data['category'] == "Observers":
          team['unofficial'] = 1
        
        teams[raw_data['teamid']] = team
        
    output("team.json", teams)
            

def run_out(data):
    runs = []
    
    for line in data:
        if len(line) < 3 or not (line[1] == 's' and line[2] == ' '):
            continue
        
        line = line.split(' ')[1]
        line = line.split(',')

        team_id = line[0]
        problem_id = ord(line[1]) - ord('A')
        timestamp = line[3]
        status = line[4]

        if status == "OK":
            status = "correct"
        elif status == "CE":
            continue
        else:
            status = "incorrect"
        
        run = {}
        run["team_id"] = team_id
        run["timestamp"] = int(timestamp)
        run["status"] = status
        run["problem_id"] = problem_id
        
        runs.append(run)
        
    output("run.json", runs)

with open(ghosts_file_path, 'r', encoding="utf-8") as f:
    data = f.read().split("\n")

ensure_dir(data_dir)
team_out(data)
run_out(data)
