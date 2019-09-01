import pickle
import urllib.request
import urllib.parse
import json

size = 4

with open('url_list.pickle', 'rb') as f:
    url_list = pickle.load(f)
print(len(url_list))
urllist = []

for i in range(size):
    urllist.append(url_list[int(i * (len(url_list) / size)):int((i + 1) * (len(url_list) / size))])

appendUrl = []
appendUrl.append(urllist[0])
appendUrl.append(urllist[3])
for j in range(2):
    base_url = 'https://www.data.go.kr'
    pros = 0
    for index, i in enumerate(appendUrl[j]):
        dicts = {}
        data_url = base_url + i
        with urllib.request.urlopen(data_url) as response:
            html = response.read().decode('utf-8')
        html = html.split('new PublicData(')
        html = html[1].split(', [{"codeId"')
        dic = json.loads(html[0])
        dicts[index] = dic
        print(pros)
        pros += 1
        with open(str(index) + ".json", "w", encoding='UTF-8-sig') as json_file:
            json.dump(dicts, json_file, indent=4, ensure_ascii=False)
            json_file.write("\n")

