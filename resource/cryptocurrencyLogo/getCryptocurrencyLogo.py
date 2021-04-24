# I wanna get all of cryptocurrency image from 
# https://cryptologos.cc/logos/, but I don't wanna do something boring,
# so I tried to script!

import requests
from bs4 import BeautifulSoup

import urllib.request

import re

file = open('./resource/cryptocurrencyLogo/cryptologocclogo_html.txt', 'r')     # 따로 copy한 파일

dir = "./resource/cryptocurrencyLogo/Real_Logos"    # 사진을 저장할 파일 위치
headers = {'User-Agent':'Chrome/66.0.3359.181'}

while True:
    line = file.readline()
    if ".PNG transparent file download" in line:
        try:
            url = line.split()[2].strip('href=').strip('\'').strip('\'>')       # 다운로드 받을 URL 추출
            filename = url.strip('https://cryptologos.cc/logos/').strip('.png?v=002').split('-')[-2]
            filename = ".\\resource\\cryptocurrencyLogo\\Real_Logos\\" + filename + ".jpg"
            # print(url)
            # print(filename)

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, filename)
            print(url)
            print(filename)
        except:
            print("[EXCEPTION] FAILED GETTING IMAGE...TRY NEXT ONE")
    if not line:
        break