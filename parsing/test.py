from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd
import pickle
from selenium import webdriver
import re
import json

df = pd.DataFrame(columns=['제공기관', '관리부서명', '관리부서 전화번호', '등록일', '키워드', '보유근거', '수집방법',
                           '데이터한계', '이름', '비용부과유무', '수정일', '업데이트 주기', '다운로드 횟수',
                           '이용허락범위', '제공형태', 'URL', '설명', '차기등록예정일', '비용부과기준 및 단위',
                           '기타유의사항'])

# check count of data
# fileData is in index 0, openApi is in index 1
cnt_list = ['DATA', 'OPENAPI']
print("Counting number of data")
for i in range(2):
    check_cnt_url = 'https://www.data.go.kr/search/index.do?index=' + cnt_list[i] + \
                    '&query=&currentPage=1&countPerPage=10'
    with urllib.request.urlopen(check_cnt_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    print(cnt_list[i], ': ', sep='', end='')
    cnt_list[i] = int(soup.find('span', {'class': 'count'}).string.replace(',', ''))
    print(cnt_list[i])

'''
# get url of fileData
# 100 url will be append to list at once
# url_list will be saved to pickle file
print("Getting url of fileData")
url_list = []
for i in range(1, int(cnt_list[0] / 100) + 2):
    to_get_url = 'https://www.data.go.kr/search/index.do?index=DATA&query=&currentPage=' + \
                 str(i) + '&countPerPage=100'
    try:
        with urllib.request.urlopen(to_get_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
    except:
        print('ERROR')
        continue
    data_item = soup.find_all('div', {'class': 'data-item'})
    for j in data_item:
        url_list.append(j.find('a')['href'])
    print("Progress: ", (i / ((int(cnt_list[0]) / 100) + 2) * 100), "%", sep='')
with open('url_list.pickle', 'wb') as f:
    pickle.dump(url_list, f, pickle.HIGHEST_PROTOCOL)
'''

with open('url_list.pickle', 'rb') as f:
    url_list = pickle.load(f)
base_url = 'https://www.data.go.kr'

progress = 1
dict = {}
for i in url_list:
    data_url = base_url + i
    with urllib.request.urlopen(data_url) as response:
        html = response.read().decode('utf-8')
    html = html.split('new PublicData(')
    html = html[1].split(', [{"codeId"')
    dict2 = json.loads(html[0])
    dict[progress] = dict2
    print(progress / cnt_list[0] * 100, "%", sep='')
    progress += 1

with open("ttss.json", "w") as json_file:
    json.dump(dict, json_file, indent=4)
    json_file.write("\n")

    # print(dict['details'])