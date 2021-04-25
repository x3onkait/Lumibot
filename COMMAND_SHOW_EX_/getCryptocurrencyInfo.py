# renewal version 2

import requests
from bs4 import BeautifulSoup
import time, datetime

import json

import sys, os

##################################################################################################
# 이 getStockInfo.py를 기준으로 1단계 상위 디렉토리 레벨선상에 있는 resource파일을 가져오기 위해
# import sys, os를 사용하고, sys.path.append(...)로 이를 가능하게 한다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로깅 처리 함수 불러오기
from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog

# 단위 붙이기
from resource.sub_function_used_globally import getWonwhaString
##################################################################################################

def getCryptocurrencyInfo(symbol):

    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://api.bithumb.com/public/ticker/" + symbol
    #print(url)

    CRYPTO_KR_NAME = getNameFromCryptoSymbol(symbol)
    CRYPTO_PICTURE_URL = getCryptocurrencyURL(symbol)
    
    if CRYPTO_KR_NAME == 404:        # 항목 없음 에러 코드
        printCommandLog("show crypto --symbol(Function)", "FAILED", "UNAVAILABLE_CRYPTO_REQUEST")
        return 404                              # 함수 종료

    if CRYPTO_PICTURE_URL == 404:
        printCommandLog("show crypto --symbol(Function)", "RUNNING", "NO_CRYPTO_LOGO_PIC_SKIPPED")
        CRYPTO_PICTURE_URL = 404

    try:
        response = requests.get(url, timeout=0.9)
        printCommandLog("show crypto --symbol(Function)", "RUNNING", "Getting Stock Information : " + symbol)
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

        # 아기자기한 효과) 변동량에 따라서 디스코드에 이모지를 출력해 보자!
        if 30 >= float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) > 0:     # 0 ~ 30% 상승
            CURRENT_CRYPTO_CHANGE_EMOJI = ":arrow_up:"            
        elif -15 <= float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) < 0:     # 0 ~ 15% 하락
            CURRENT_CRYPTO_CHANGE_EMOJI = ":arrow_down:"
        elif 50 >= float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) > 30:       # 30% ~ 50% 상승
            CURRENT_CRYPTO_CHANGE_EMOJI = ":arrow_double_up:"
        elif -30 <= float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) < -15:        # 15 ~ 30% 하락
            CURRENT_CRYPTO_CHANGE_EMOJI = ":arrow_double_down:"
        elif float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) > 50:             # 50% 초과 상승
            CURRENT_CRYPTO_CHANGE_EMOJI = ":fire:"
        elif float(CURRENT_CRYPTO_PERCENT_CHANGE_24h) < -30:              # 30% 초과 하락
            CURRENT_CRYPTO_CHANGE_EMOJI = ":cloud_lightning:"
        else:                                                           # 보합 상태(변동률 0%)
            CURRENT_CRYPTO_CHANGE_EMOJI = ":arrows_counterclockwise:"

        CURRENT_CRYPTO_PERCENT_CHANGE_24h = "{:,}".format(float(CURRENT_CRYPTO_PERCENT_CHANGE_24h)) + " %"
        #print("24시간 변동률 : " + CURRENT_CRYPTO_KRW_CHANGE_24h + " ( " + CURRENT_CRYPTO_PERCENT_CHANGE_24h + " ) ")

        CURRENT_UPDATE_TIME = int(cryptocurrencyInfoSet["data"]["date"]) / 1000                     # 업데이트 시간
        CURRENT_UPDATE_TIME = datetime.datetime.fromtimestamp(CURRENT_UPDATE_TIME).strftime('%Y년 %m월 %d일 %H시 %M분 %S.%f초').replace('000','')
        #print("업데이트 시간 : " + CURRENT_UPDATE_TIME)

        _END_TIME = time.time()
        running_time = round((_END_TIME - _START_TIME), 4)
        printCommandLog("show crypto --symbol(Function)", "RUNNING", "running time : " + str(running_time) + " sec/pass")
        # print("작동 시간 : " + _RUNNING_TIME + " 초")

        #print()

        # str()을 하지 않으면 Discord Embed에서 출력이 제대로 되지 않을 수 있다. 
        return str(CRYPTO_KR_NAME), str(CURRENT_CRYPTO_VALUE_KRW), str(CURRENT_CRYPTO_VALUE_OPENING_00h), str(CURRENT_CRYPTO_VALUE_MIN_00h), str(CURRENT_CRYPTO_VALUE_MAX_00h), str(CURRENT_CRYPTO_UNIT_TRADE_24h), str(CURRENT_CRYPTO_KRW_TRADE_24h), str(CURRENT_CRYPTO_KRW_CHANGE_24h), str(CURRENT_CRYPTO_PERCENT_CHANGE_24h), str(CURRENT_UPDATE_TIME), str(running_time), str(CURRENT_CRYPTO_CHANGE_EMOJI), str(CRYPTO_PICTURE_URL)

def getCryptocurrencyBrief():       # [developing::개발중]
    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://coinranking.com/overview"

    try:
        response = requests.get(url, timeout = 1)
        printCommandLog("show crypto --brief(Function)", "RUNNING", "Getting Brief Information")
    except:
        allMarketCap = 404              # 일종의 비표 역할. 실패할 경우 이 데이터가 실패를 알림.
        return 404

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        allMarketCap = soup.select_one('#__layout > div > section > div.stats-list > table > tbody > tr:nth-child(1) > td > abbr')
        allMarketCap = str(allMarketCap).split()[3].replace('title="','').replace('"><!--','')[:-3]
        allMarketCap = " ≈ " + getWonwhaString.getWonhwaString(int(allMarketCap.replace(',',''))) + " 달러"
        #print(allMarketCap)
        
        dayCryptoVolume = soup.select_one('#__layout > div > section > div.stats-list > table > tbody > tr:nth-child(2) > td > abbr')
        dayCryptoVolume = str(dayCryptoVolume).split()[3].replace('title="','').replace('"><!--','')[:-3]
        dayCryptoVolume = " ≈ " + getWonwhaString.getWonhwaString(int(dayCryptoVolume.replace(',',''))) + " 달러"
        #print(dayCryptoVolume)
    
        allCryptoQuantity = soup.select_one('#__layout > div > section > div.stats-list > table > tbody > tr:nth-child(3) > td')
        allCryptoQuantity = allCryptoQuantity.get_text().strip() + " 개"
        #print(allCryptoQuantity)

        allCryptoExchanges = soup.select_one('#__layout > div > section > div.stats-list > table > tbody > tr:nth-child(4) > td')
        allCryptoExchanges = allCryptoExchanges.get_text().strip() + " 개"
        #print(allCryptoExchanges)

        _END_TIME = time.time()
        running_time = round((_END_TIME - _START_TIME), 4)
        printCommandLog("show crypto --brief(Function)", "RUNNING", "running time : " + str(running_time) + " sec/pass")

        return str(allMarketCap), str(dayCryptoVolume), str(allCryptoQuantity), str(allCryptoExchanges), str(running_time)



def getNameFromCryptoSymbol(symbol):

    file = open('./resource/crypto_function_data/cryptocurrencySymbolList.txt','rt', encoding='UTF8')
    
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

def getCryptocurrencyURL(symbol):

    file = open('./resource/crypto_function_data/cryptoLogoURL.txt','rt')

    try:
        while True:
            line = file.readline()
            #print(line)
            #print(line.split('  ')[1].strip())      # BTC, XRP, ETH..등만 잘라서 가져오기
            if symbol == line.split('  ')[1].strip():
                returnURL = line.split(' ')[0]
                break
            if not line:
                return 404
    except:
        return 404

    file.close()

    return returnURL

# print(getCryptocurrencyBrief())

# print(getCryptocurrencyInfo("LF"))
# print(getCryptocurrencyInfo("BTC"))

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

