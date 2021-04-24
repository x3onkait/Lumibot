import requests
from bs4 import BeautifulSoup

# 시가총액은 coinmarketcap에서
# 그 외 정보는 bithumb에서 받아오자

def getBTCtoKRW():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:
        #print("access ok")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    
        # 비트코인 가격(KRW)
        BTCtoKRW = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > td')
        BTCtoKRW = BTCtoKRW.get_text().replace('₩','')

        return BTCtoKRW

    else: 
        print(response.status_code)

def getBTCchange24hr():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 비트코인 시세 변동량(KRW, 24hr)
        BTCchangeInKRW24hr = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td > span')
       
        # 비트코인 시세 변동률(Percent, 24hr)
        BTCchangeRate24hr = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td > div > span')

        if float(BTCchangeInKRW24hr.get_text().replace('₩','').replace(',','')) >= 0:
            result = BTCchangeInKRW24hr.get_text().replace('₩','') + " 원 "+ "(" + BTCchangeRate24hr.get_text() + ")"
            return result
        else:
            result = BTCchangeInKRW24hr.get_text().replace('₩','') + " 원 "+ "( -" + BTCchangeRate24hr.get_text() + " )"
            return result
        
    else: 
        print(response.status_code)

def getBTCMinMaxValue24hr():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 비트코인 최고/최저가(KRW, 24hr)
        BTCmaxPrice24hr = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td > div:nth-child(2)')
        BTCminPrice24hr = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td > div:nth-child(1)')

        result = BTCmaxPrice24hr.get_text().replace('₩','') + " 원 / " + BTCminPrice24hr.get_text().replace('₩','').replace('/','').replace(' ','') + " 원"
        return result

    else: 
        print(response.status_code)

def getBTCtransactionInKRW24hr():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:
        #print("access ok")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 비트코인 거래량(KRW, 24hr)
        BTCtransactionInKRW24hr = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td > span')

        result = "≈ " + BTCtransactionInKRW24hr.get_text().replace('₩','').split('.', 1)[0] + " 원"
        return result

    else: 
        print(response.status_code)

def getCryptocurrencyMarketStakeAndRank_BTC():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:
        #print("access ok")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 비트코인 시장 점유율과 등수
        CryptocurrencyMarketStake_BTC = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(6) > td > span')
        CryptocurrencyMarketRank_BTC = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(7) > td')

        result = CryptocurrencyMarketStake_BTC.get_text() + " ( " + CryptocurrencyMarketRank_BTC.get_text().replace('#','') + " 위 )"
        return result

    else: 
        print(response.status_code)

def getBTCMarketCap():
    url = "https://coinmarketcap.com/ko/currencies/bitcoin/"

    response = requests.get(url)

    if response.status_code == 200:
        #print("access ok")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 비트코인 시가총액(KRW)
        BTCMarketCap = soup.select_one('#__next > div > div.sc-fznJRM.bTIjTR.cmc-body-wrapper > div > div.sc-AxjAm.kQhMzz.container > div > div.sc-AxjAm.dqhsML > div.sc-AxjAm.hsgfno > div:nth-child(2) > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > span')

        result = " ≈ " + BTCMarketCap.get_text().replace('₩','').split('.', 1)[0] + " 원"
        return result

    else: 
        print(response.status_code)