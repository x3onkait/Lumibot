import requests
from bs4 import BeautifulSoup
import time

# 실시간 세계 인구 통계 제공

def getLiveWorldPopulation():
    url = "https://countrymeters.info/en/World"

    response = requests.get(url)

    time.sleep(1)

    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        LiveWorldPopulation = soup.select_one('#cp1')
        LiveWorldPopulation = LiveWorldPopulation.get_text()
        #print(LiveWorldPopulation.get_text())
        return LiveWorldPopulation

    else:
        print(response.status_code)

#getLiveWorldPopulation()