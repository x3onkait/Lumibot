# renewal version 2

import requests
from bs4 import BeautifulSoup
import time, datetime

import json

def getCryptocurrencyInfo(symbol):

    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://api.bithumb.com/public/ticker/" + symbol
    #print(url)

    CRYPTO_KR_NAME = getNameFromCryptoSymbol(symbol)
    if CRYPTO_KR_NAME == 404:        # 항목 없음 에러 코드
        print("Unavailable Cryptocurrency Request")
        _END_TIME = time.time()
        _RUNNING_TIME = round((_END_TIME - _START_TIME), 4)
        print("작동 시간 : " + str(_RUNNING_TIME) + " 초")
        
        return 404                              # 함수 종료

    try:
        response = requests.get(url, timeout=0.9)
        print("getting information about : " + symbol)
    except:
        return 404

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser').decode('UTF8')

        cryptocurrencyInfoSet = json.loads(soup)       # List 형식으로 암호화폐 정보를 가져옴.
                                                       # 실제로는 키-쌍 형식의 JSON 형식으로 데이터를 사용함

        # print(cryptocurrencyInfoSet)
        # print()

        #print("암호화폐 이름 : " + CRYPTO_KR_NAME)

        CURRENT_CRYPTO_VALUE_KRW = cryptocurrencyInfoSet["data"]["closing_price"]       # 현재가(00시 종가)
        CURRENT_CRYPTO_VALUE_KRW = "{:,}".format(float(CURRENT_CRYPTO_VALUE_KRW)).replace('.0','') + " 원"
        #print("00시 종가 : " + CURRENT_CRYPTO_VALUE_KRW)

        CURRENT_CRYPTO_VALUE_OPENING_00h = cryptocurrencyInfoSet["data"]["opening_price"]      # 00시 시가
        CURRENT_CRYPTO_VALUE_OPENING_00h = "{:,}".format(float(CURRENT_CRYPTO_VALUE_OPENING_00h)).replace('.0','') + " 원"
        #print("00시 시가 : " + CURRENT_CRYPTO_VALUE_OPENING_00h)

        CURRENT_CRYPTO_VALUE_MIN_00h =  cryptocurrencyInfoSet["data"]["min_price"]              # 00시 저가
        CURRENT_CRYPTO_VALUE_MIN_00h = "{:,}".format(float(CURRENT_CRYPTO_VALUE_MIN_00h)).replace('.0','') + " 원"
        #print("00시 저가 : " + CURRENT_CRYPTO_VALUE_MIN_00h)

        CURRENT_CRYPTO_VALUE_MAX_00h = cryptocurrencyInfoSet["data"]["max_price"]              # 00시 고가
        CURRENT_CRYPTO_VALUE_MAX_00h = "{:,}".format(float(CURRENT_CRYPTO_VALUE_MAX_00h)).replace('.0','') + " 원"
        #print("00시 고가 : " + CURRENT_CRYPTO_VALUE_MAX_00h)

        CURRENT_CRYPTO_UNIT_TRADE_24h = cryptocurrencyInfoSet["data"]["units_traded_24H"]           # 최근 24시간 거래량(crypto)
        CURRENT_CRYPTO_UNIT_TRADE_24h = "≈ " + "{:,}".format(round(float(CURRENT_CRYPTO_UNIT_TRADE_24h), 3)) + " " + symbol
        CURRENT_CRYPTO_KRW_TRADE_24h = cryptocurrencyInfoSet["data"]["acc_trade_value_24H"]         # 최근 24시간 거래량(KRW)
        CURRENT_CRYPTO_KRW_TRADE_24h = "≈ " + "{:,}".format(int(float(CURRENT_CRYPTO_KRW_TRADE_24h))) + " 원"
        #print("24시간 거래량 : " + CURRENT_CRYPTO_UNIT_TRADE_24h + " ( " + CURRENT_CRYPTO_KRW_TRADE_24h + ")")

        CURRENT_CRYPTO_KRW_CHANGE_24h = cryptocurrencyInfoSet["data"]["fluctate_24H"]               # 최근 24시간 변동량(KRW)
        CURRENT_CRYPTO_KRW_CHANGE_24h = "{:,}".format(float(CURRENT_CRYPTO_KRW_CHANGE_24h)).replace('.0','') + " 원"
        CURRENT_CRYPTO_PERCENT_CHANGE_24h = cryptocurrencyInfoSet["data"]["fluctate_rate_24H"]      # 최근 24시간 변동량(Percent)
        CURRENT_CRYPTO_PERCENT_CHANGE_24h = "{:,}".format(float(CURRENT_CRYPTO_PERCENT_CHANGE_24h)) + " %"
        #print("24시간 변동률 : " + CURRENT_CRYPTO_KRW_CHANGE_24h + " ( " + CURRENT_CRYPTO_PERCENT_CHANGE_24h + " ) ")

        CURRENT_UPDATE_TIME = int(cryptocurrencyInfoSet["data"]["date"]) / 1000                     # 업데이트 시간
        CURRENT_UPDATE_TIME = datetime.datetime.fromtimestamp(CURRENT_UPDATE_TIME).strftime('%Y년 %m월 %d일 %H시 %M분 %S.%f초').replace('000','')
        #print("업데이트 시간 : " + CURRENT_UPDATE_TIME)

        _END_TIME = time.time()
        _RUNNING_TIME = str(round((_END_TIME - _START_TIME), 4))
        print("작동 시간 : " + _RUNNING_TIME + " 초")

        #print()

        # str()을 하지 않으면 Discord Embed에서 출력이 제대로 되지 않을 수 있다.
        return str(CRYPTO_KR_NAME), str(CURRENT_CRYPTO_VALUE_KRW), str(CURRENT_CRYPTO_VALUE_OPENING_00h), str(CURRENT_CRYPTO_VALUE_MIN_00h), str(CURRENT_CRYPTO_VALUE_MAX_00h), str(CURRENT_CRYPTO_UNIT_TRADE_24h), str(CURRENT_CRYPTO_KRW_TRADE_24h), str(CURRENT_CRYPTO_KRW_CHANGE_24h), str(CURRENT_CRYPTO_PERCENT_CHANGE_24h), str(CURRENT_UPDATE_TIME), str(_RUNNING_TIME)


def getNameFromCryptoSymbol(symbol):

    file = open('./resource/cryptocurrencySymbolList.txt','rt', encoding='UTF8')
    
    try:
        while True:
            line = file.readline()
            if symbol == line.split()[0]:     # 정확한 암호화폐명을 입력해야만 결과를 반환
                name = line.split('\t')[1].strip()
                break
            if not line:
                return 404

    except:         # 제대로 입력하지 않아 예외가 생기면 모두 404 에러처리
        return 404
    
    file.close()

    return name

# print(getCryptocurrencyInfo("VET"))
# print(getCryptocurrencyInfo("BTC"))
# print(getCryptocurrencyInfo("XRP"))
# print(getCryptocurrencyInfo("ETC"))
# print(getCryptocurrencyInfo("MKR"))
# print(getCryptocurrencyInfo("ETH"))
# print(getCryptocurrencyInfo("BCH"))
# print(getCryptocurrencyInfo("CMP"))
# print(getCryptocurrencyInfo("AAVE"))
# print(getCryptocurrencyInfo("BSV"))
# print(getCryptocurrencyInfo("LTC"))
# print(getCryptocurrencyInfo("BTG"))
# print(getCryptocurrencyInfo("INVALID_TEST"))

