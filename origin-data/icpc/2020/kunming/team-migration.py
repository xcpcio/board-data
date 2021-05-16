
from os import path
from json import load, dumps
import xlrd

def json_output(data):
    return dumps(data, sort_keys=False, separators=(',', ':'), ensure_ascii=False)

def output(filename, data):
    with open(path.join(data_dir, filename), 'w') as f:
        f.write(json_output(data))

def json_input(path):
    with open(path, 'r') as f:
        return load(f)

_params = json_input('params.json')
data_dir = _params['data_dir']
team_migration_file_path = _params['team_migration_file_path']

workbook = xlrd.open_workbook(team_migration_file_path)
worksheet = workbook.sheet_by_index(0)

nrows = worksheet.nrows
ncols = worksheet.ncols

cnt = 0

team_origin_data = json_input(path.join(data_dir, "team.json"))
team_map = dict()

for i in range(nrows):
    if i == 0 or i == nrows - 1:
        continue
    row = worksheet.row_values(i)
    
    team_map["%s-%s" % (row[0], row[1])] = {
        "members": [row[2], row[3], row[4]]
    }
    
    if row[5] == '打星':
        cnt += 1

for key in team_origin_data.keys():
    team = team_origin_data[key]
    _key = "%s-%s" % (team['organization'], team['name'])
    if _key in team_map.keys():
        members = team_map[_key]
        team["members"] = members["members"]
    else:
        team["members"] = []

output("team.json", team_origin_data)
