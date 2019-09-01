from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd
import pickle
import re
import json
import os
import multiprocessing
import sys
import time
size = 20

def good(aaa):
    proc = os.getpid()
    try:
        dicts = {}
        num = aaa.pop()
        print("Processing")
        # cnt = 0
        # k = ""
        base_url = 'https://www.data.go.kr'
        for index, i in enumerate(aaa):
            data_url = base_url + i
            try:
                with urllib.request.urlopen(data_url) as response:
                    html = response.read().decode('utf-8')
                html = html.split('new PublicData(')
                html = html[1].split(', [{"codeId"')
                dic = json.loads(html[0])
                dicts[index] = dic
            except:
                print("Continue")
                continue
            # if cnt == 0:
            #    k = dic["details"]
            #    k = k[0]["publicDataDetailPk"]
            #    cnt += 1
            # print(index / 26000 * 100*size, "%", sep='')
        print("Start saving")
        # k = k[5:]
        try:
            with open("json/" + str(proc) + ".json", "w", encoding='UTF-8-sig') as json_file:
                json.dump(dicts, json_file, indent=4, ensure_ascii=False)
                json_file.write("\n")
            print("Finish saving")
        except:
            print("Continue2")
    except:
        print("ERROR"+str(proc))
    sys.exit(1)
    return
        # print(dict['details'])


if __name__ == '__main__':
    print("Multiprocessing start")
    with open('url_list.pickle', 'rb') as f:
        url_list = pickle.load(f)
    print(len(url_list))
    urllist = []

    for i in range(size):
        urllist.append(url_list[int(i*(len(url_list)/4)):int((i+1)*(len(url_list)/4))])

    url_list = urllist[0] + urllist[3]
    urllist = []

    for i in range(size):
        urllist.append(url_list[int(i*(len(url_list)/size)):int((i+1)*(len(url_list)/size))])

    print(len(url_list))
    for i in range(size):
        print(len(url_list[i]))
    pool = multiprocessing.Pool(processes=size)
    pool.map(good, urllist)
    pool.close()
    pool.join()


