import json 

with open('../../data/default_data_role_playing.json', 'r') as f:
    response_json = json.load(f)['output_format']


print(response_json)