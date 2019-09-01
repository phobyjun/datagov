import json
import os

path = './result_json'
file_list = os.listdir(path)

json_data = []
for i in file_list:
    with open(path + '/' + i, encoding="utf-8-sig") as json_file:
        json_datum = json.load(json_file)
    json_data.append(json_datum)

json_len = 0
for i in json_data:
    json_len += len(i)

dicts = {}
idx = 1
for i in json_data:
    for j in i:
        dicts[idx] = i[j]
        idx += 1

with open("result.json", "w", encoding='UTF-8-sig') as json_file:
    json.dump(dicts, json_file, indent=4, ensure_ascii=False)
    json_file.write("\n")