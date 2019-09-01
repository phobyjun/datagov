from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd
import pickle
from selenium import webdriver
import re

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


# get metadata from url in url_list
# base url + url_list is the url of the fileData
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.implicitly_wait(3)
with open('url_list.pickle', 'rb') as f:
    url_list = pickle.load(f)
base_url = 'https://www.data.go.kr'

progress = 1
for i in url_list:
    try:
        data_url = base_url + i
        driver.get(data_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # get metadata from class: dataset-meta in html
        dataset_meta = soup.find('div', {'class': 'dataset-meta'})
        meta_items = dataset_meta.find_all('ul', {'class': 'meta-items'})
        meta_items.pop()
        di = {}
        for cnt in meta_items:
            items = cnt.find_all('li')
            di[items[0].string.strip()] = items[1].string.strip()

        dataset_metatable = soup.find('table', {'class': 'table table-bordered detail-table detail-api-table'})
        metatable_th = dataset_metatable.find_all('th')
        metatable_td = dataset_metatable.find_all('td')
        di['이름'] = metatable_th[0].string.strip()
        metatable_th.pop(0)

        for th, td in zip(metatable_th, metatable_td):
            try:
                di[th.string.strip()] = td.string.strip()
            except:
                try:
                    di[th.string.strip()] = td.a.string.strip()
                except:
                    try:
                        di[th.string.strip()] = td.a.find('img')['alt']
                    except:
                        di[th.string.strip()] = ''
                        print('ERORR')

        if '제공기관' not in di:
            di['제공기관'] = ''
        if '관리부서명' not in di:
            di['관리부서명'] = ''
        if '관리부서 전화번호' not in di:
            di['관리부서 전화번호'] = ''
        if '등록일' not in di:
            di['등록일'] = ''
        if '키워드' not in di:
            di['키워드'] = ''
        if '보유근거' not in di:
            di['보유근거'] = ''
        if '수집방법' not in di:
            di['수집방법'] = ''
        if '데이터한계' not in di:
            di['데이터한계'] = ''
        if '이름' not in di:
            di['이름'] = '이름'
        if '비용부과유무' not in di:
            di['비용부과유무'] = '비용부과유무'
        if '수정일' not in di:
            di['수정일'] = '수정일'
        if '업데이트 주기' not in di:
            di['업데이트 주기'] = '업데이트 주기'
        if '다운로드 횟수' not in di:
            di['다운로드 횟수'] = '다운로드 횟수'
        if '이용허락범위' not in di:
            di['이용허락범위'] = '이용허락범위'
        if '제공형태' not in di:
            di['제공형태'] = '제공형태'
        if 'URL' not in di:
            di['URL'] = 'URL'
        if '설명' not in di:
            di['설명'] = '설명'
        if '차기등록예정일' not in di:
            di['차기등록예정일'] = '차기등록예정일'
        if '비용부과기준 및 단위' not in di:
            di['비용부과기준 및 단위'] = '비용부과기준 및 단위'
        if '기타유의사항' not in di:
            di['기타유의사항'] = ''

        df = df.append(pd.DataFrame([[di['제공기관'], di['관리부서명'], di['관리부서 전화번호'], di['등록일'], di['키워드'],
                                      di['보유근거'], di['수집방법'], di['데이터한계'], di['이름'], di['비용부과유무'],
                                      di['수정일'], di['업데이트 주기'], di['다운로드 횟수'], di['이용허락범위'],
                                      di['제공형태'], di['URL'], di['설명'], di['차기등록예정일'], di['비용부과기준 및 단위'],
                                      di['기타유의사항']]],
                                    columns=['제공기관', '관리부서명', '관리부서 전화번호', '등록일', '키워드', '보유근거',
                                             '수집방법', '데이터한계', '이름', '비용부과유무', '수정일', '업데이트 주기',
                                             '다운로드 횟수', '이용허락범위', '제공형태', 'URL', '설명', '차기등록예정일',
                                             '비용부과기준 및 단위', '기타유의사항']), ignore_index=True, sort=True)

        print("Progress: ", progress / cnt_list[0] * 100, sep='')
        progress += 1
    except:
        continue

df.to_csv("test_final.csv", mode='w', encoding="euc-kr")
