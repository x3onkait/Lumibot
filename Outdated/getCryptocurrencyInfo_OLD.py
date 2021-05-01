import requests
from bs4 import BeautifulSoup
import time

def getCryptocurrencyInfo(symbol):

    url = "https://www.bithumb.com/"

    _START_TIME = time.time()

    if getNameFromCryptoSymbol(symbol) == 404:        # 항목 없음 에러 코드
        return 404                              # 함수 종료

    try:
        response = requests.get(url, timeout=0.9)
        print("getting information about : " + symbol)
        #time.sleep(1)
    except:
        # timeout 내에 제대로 bithumb.com에서 응답이 돌아오지 않는 경우
        # 404란 error returning code를 대신 반환하고,
        # 이것을 run.py
        return 404, 404, 404, 404, 404, 404, 404

    if response.status_code == 200:
        #print("access ok")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # selector name 가져오기
        SELECTOR_NAME_PRICE = "#assetReal" + symbol + "_KRW"
        SELECTOR_NAME_CHANGE_KRW = "#assetRealPrice" + symbol + "_KRW"
        SELECTOR_NAME_CHANGE_PERCENT = "#assetRealRate" + symbol + "_KRW"
        SELECTOR_NAME_TRANSACTION = "#assetReal" + symbol + "_KRW2KRW"

        cryptocurrency_KRname = getNameFromCryptoSymbol(symbol)
        cryptocurrency_to_KRW = soup.select_one(SELECTOR_NAME_PRICE).get_text()     # 가격 추출
        cryptocurrency_change_KRW = soup.select_one(SELECTOR_NAME_CHANGE_KRW).get_text()       # 변동량 추출
        cryptocurrency_change_PERCENT = soup.select_one(SELECTOR_NAME_CHANGE_PERCENT).get_text()    # 변동률 추출
        cryptocurrency_transaction_KRW = soup.select_one(SELECTOR_NAME_TRANSACTION).get_text().replace('₩','').split('.', 1)[0] + " [bithumb 거래소 기준]"      # 거래량(24hr) 추출

        # 추가 정보
        # 암호화폐 거래량을 KRW 단위가 아닌 요청한 암호화폐 단위로 보여준다.
        realTransactionKRW = int(soup.select_one(SELECTOR_NAME_TRANSACTION).get_text().replace('≈','').replace(',','').replace('원','').replace(' ',''))
        realTransactionCRYPTO = int(soup.select_one(SELECTOR_NAME_PRICE).get_text().replace(',','').replace('원','').replace(' ',''))
        #print(realTransactionKRW) 
        #print(realTransactionCRYPTO)
        cryptocurrency_transaction_CRYPTO = round((realTransactionKRW / realTransactionCRYPTO), 2)
        cryptocurrency_transaction_CRYPTO = "≈ " + ("{:,}".format(cryptocurrency_transaction_CRYPTO))

        # print(cryptocurrency_KRname)
        # print(cryptocurrency_to_KRW)
        # print(cryptocurrency_change_KRW)
        # print(cryptocurrency_change_PERCENT)
        # print(cryptocurrency_transaction_KRW)
        # print(cryptocurrency_transaction_CRYPTO)

        # 문자열로 모두 변환시켜주자(원활한 출력을 위해서)

        _END_TIME = time.time()
        running_time = round((_END_TIME - _START_TIME), 4)
        print("running time : ", str(running_time) + " SEC.")

        return str(cryptocurrency_KRname), str(cryptocurrency_to_KRW), str(cryptocurrency_change_KRW), str(cryptocurrency_change_PERCENT), str(cryptocurrency_transaction_KRW), str(cryptocurrency_transaction_CRYPTO), str(running_time)


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

# print(getNameFromCryptoSymbol("ARW"))

# print(getCryptocurrencyInfo("BTC"))
# print(getCryptocurrencyInfo("ETH"))
# print(getCryptocurrencyInfo("XRP"))
# print(getCryptocurrencyInfo("DOT"))
# print(getCryptocurrencyInfo("XLM"))
# print(getCryptocurrencyInfo("EOS"))
# print(getCryptocurrencyInfo("TRX"))
# print(getCryptocurrencyInfo("ARW"))
# print(getCryptocurrencyInfo("LTC"))
# print(getCryptocurrencyInfo("CRO"))
# print(getCryptocurrencyInfo("XTZ"))
# print(getCryptocurrencyInfo("ETC"))
# print(getCryptocurrencyInfo("UNI"))
# print(getCryptocurrencyInfo("VET"))
# print(getCryptocurrencyInfo("XEM"))
# print(getCryptocurrencyInfo("ENJ"))
# print(getCryptocurrencyInfo("GRT"))