
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
team_migration_file_path = "./第45届ICPC沈阳站参赛信息-最终版.xlsx"

workbook = xlrd.open_workbook(team_migration_file_path)
worksheet = workbook.sheet_by_index(0)

nrows = worksheet.nrows
ncols = worksheet.ncols

cnt = 0

team_origin_data = json_input(path.join(data_dir, "team.json"))
team_map = dict()

for i in range(nrows):
    if i == 0 or i == 1:
        continue

    row = worksheet.row_values(i)
    
    organization = row[1]
    team_name = row[10]
    coach = row[5]
    members = [row[12], row[16], row[20]]
    unofficial = True if row[25] == "打星" else False
    
    key = "%s-%s" % (organization, team_name)
    
    team_map[key] = {
        "coach" : coach,
        "members": members,
        "unofficial": unofficial
    }
    
matched = 0

for key in team_origin_data.keys():
    team = team_origin_data[key]
    _key = "%s-%s" % (team['organization'], team['name'])
    
    unofficial = False
    
    if team['organization'] == "东北大学":
        unofficial = True
    
    if _key in team_map.keys():
        members = team_map[_key]["members"]
        coach = team_map[_key]["coach"]
        unofficial = team_map[_key]["unofficial"]
        
        team["members"] = members
        team["coach"] = coach
        
        matched = matched + 1
    else:
        print(_key)
    
    if unofficial:
        del team["official"]
        team["unofficial"] = 1

print(nrows - 2, len(team_origin_data.keys()), matched)

output("team.json", team_origin_data)
