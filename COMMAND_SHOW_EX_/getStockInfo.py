import requests
from bs4 import BeautifulSoup as bs
import json

import sys,os

import time

############################################################################
# 이 getStockInfo.py를 기준으로 1단계 상위 디렉토리 레벨선상에 있는 resource파일을 가져오기 위해
# import sys, os를 사용하고, sys.path.append(...)로 이를 가능하게 한다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# resource 파일 내의 getWonwhaString이란 모듈(*.py)을 가져온다.
from resource.sub_function_used_globally import getWonwhaString

# 로깅 처리 함수 불러오기
from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog
############################################################################


def getStockInfo(companyName):

    _START_TIME = time.time()

    if getStockCode(companyName) == 404:        # 종목 없음 에러 코드
        return 404                              # 함수 종료

    try:
        companyCode = getStockCode(companyName)
        printCommandLog("show stock --search {} (Function)".format(companyName), "RUNNING", "Getting Stock Information : " + companyName)
        #print("getting information about : " + companyName)

        url = "https://finance.daum.net/api/quote/A" + companyCode + "/sectors"

        response = requests.get(url)
        headers = {
            'Referer' : 'https://finance.daum.net/quotes/A' + companyCode,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=0.9)
    except:
        printCommandLog("show stock --search {} (Function)".format(companyName), "RUNNING", "NO_RESPONSE_RETURNED")
        return 404, 404, 404, 404, 404, 404, 404

    stockData = response.json()
    #print(type(stockData))      # Dictionary 타입
    stockData = list(stockData.values())
    #print(type(stockData))

    # print("종목코드 : " + stockData[0][0].get("symbolCode"))
    # print("종목이름 : " + stockData[0][0].get("name"))
    # print("종목가격 : " + str(stockData[0][0].get("tradePrice")).replace('.0','') + " 원")
    # print("종목가격 변동량 : " + str(stockData[0][0].get("changePrice")) + " 원")
    # print("종목가격 변동률 : " + str(stockData[0][0].get("changeRate") * 100) + " %")
    # print("시가총액 : ≈ " + str(stockData[0][0].get("marketCap")).replace('.0','')[:6] + " 억 원")

    symbolCode = stockData[0][0].get("symbolCode")[1:]                                # 종목 코드
    companyName = stockData[0][0].get("name")                                           # 종목 이름
    
    tradePrice = str(stockData[0][0].get("tradePrice")).replace('.0','')                # 종목 가격
    tradePrice = "{:,}".format(int(tradePrice)) + " 원"     # 1,000 단위마다 콤마 붙이기, 원 기호 

    changePrice = str(stockData[0][0].get("changePrice")).replace('.0','')                 # 종목 가격 변동량
    changePrice = "{:,}".format(int(changePrice)) + " 원"     # 1,000 단위마다 콤마 붙이기, 원 기호

    changeRate = str(round((stockData[0][0].get("changeRate") * 100),2)) + " %"                    # 종목 가격 변동률
    
    marketCap = str(stockData[0][0].get("marketCap")).replace('.0','')     # 시가총액
    marketCap = "≈ " + getWonwhaString.getWonhwaString(int(marketCap)) + " 원"     

    _END_TIME = time.time()
    running_time = round((_END_TIME - _START_TIME), 4)
    printCommandLog("show stock --search {}(Function)".format(companyName), "RUNNING", "running time : " + str(running_time) + " sec/pass")
    #print("running time : ", str(running_time) + " SEC.")

    return symbolCode, companyName, tradePrice, changePrice, changeRate, marketCap, str(running_time)

def getStockCode(companyName):

    file = open('./resource/stock_function_data/stockCodeList.txt','rt', encoding='UTF8')
    
    try:
        while True:
            line = file.readline()
            if companyName == line.split()[0]:      #정확한 회사명만 검색
                code = line.split('\t')[1].strip()
                break
            if not line:
                return 404
    except:         # 제대로 입력하지 않아 예외가 생기면 모두 404 에러처리
        return 404

    file.close()

    return code

# print(getStockInfo("삼성전자"))
# print(getStockInfo("LG"))
# print(getStockInfo("CJ대한통운"))
# print(getStockInfo("카카오"))
# print(getStockInfo("BGF리테일"))
# print(getStockInfo("CJ제일제당"))
# print(getStockInfo("대한항공"))
# print(getStockInfo("롯데제과"))
# print(getStockInfo("이트론"))
# print(getStockInfo("씨젠"))
# print(getStockInfo("아모레퍼시픽"))
# print(getStockInfo("엔씨소프트"))
# print(getStockInfo("한국전력"))
# print(getStockInfo("삼성생명"))
# print(getStockInfo("KT"))
# print(getStockInfo("넷마블"))
# print(getStockInfo("기업은행"))
