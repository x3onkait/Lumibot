import urllib                   # 한글 요청이 포함될 때 오류 발생하면 사용..

import requests
from bs4 import BeautifulSoup

import sys, os

import json

######################################################################################
# 이 getStockInfo.py를 기준으로 1단계 상위 디렉토리 레벨선상에 있는 resource파일을 가져오기 위해
# import sys, os를 사용하고, sys.path.append(...)로 이를 가능하게 한다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로깅 처리 함수 불러오기
from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog
######################################################################################

import time

def getLOLUserStatistics(fromWho, username):

    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://poro.gg/summoner/kr/" + username

    try:
        response = requests.get(url, timeout = 0.9)
        printCommandLog(fromWho, "show gameStat --LOL --username {}(Function)".format(username), "RUNNING", "Getting LOL Statistics.. username : " + username)

    except:
        OVERALL_FUNCTION_RETURN = 408
        return 408                  # Connection Timeout

    # 연결에 성공해 데이터가 받아와지는 경우
    if response.status_code == 200:

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            invalidTester = str(soup)

            # 유효한 소환사 이름이 아니라서 검색 결과가 없는 경우
            if "검색 결과가 없습니다" in invalidTester:
                printCommandLog(fromWho, "show gameStat --LOL --username {}(Function)".format(username), "FAILED", "NON_EXIST_USERNAME")
                OVERALL_FUNCTION_RETURN = 404
                return 404

            # 유요한 소환사 이름인 경우
            else:

                # 유저 래더 랭킹 현황
                try:
                    USER_LADDER_RANK = soup.select_one('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.summoner-header > div.summoner-header__info > div.summoner-header__profile > span.ranking')
                    _divided = str(USER_LADDER_RANK).split()
                    USER_LADDER_RANK = _divided[4] + " " + _divided[5] + _divided[6]
                except:
                    USER_LADDER_RANK = "NaN위(No Data)"

                # 유저(소환사) 이름
                USERNAME = soup.select_one('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.summoner-header > div.summoner-header__info > div.summoner-header__profile > div > h3').get_text()

                # 유저(소환사) 사진
                USER_PROFILE_PICTURE = soup.select_one('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.summoner-header > div.summoner-header__info > div.summoner-header__portrait > img')['src']
                USER_PROFILE_PICTURE = "https:" + USER_PROFILE_PICTURE

                # 유저(소환사 레벨)
                USERLEVEL = soup.select_one('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.summoner-header > div.summoner-header__info > div.summoner-header__portrait > div').get_text().strip()

                COMMON_USER_INFO = [USER_LADDER_RANK, USERNAME, USER_PROFILE_PICTURE, USERLEVEL]
                # print(COMMON_USER_INFO)

                ##################################################### 솔로 랭크 정보 ####################################################
                # 티어 이미지
                USERSOLORANK_TIER_IMG_URL = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div.col-12.col-md-6.col-lg-12.mb-lg-2 > div > div.summoner-tier__img > img')[0]['src']
                
                # 티어 이름과 Leauge Point(같이 나옴)
                USERSOLORANK_TIER_LP_MIX = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div.col-12.col-md-6.col-lg-12.mb-lg-2 > div > div:nth-child(2) > div.summoner-tier__description')[0].get_text().split()

                # 티어 이름
                USERSOLORANK_TIER_NAME = USERSOLORANK_TIER_LP_MIX[0:-2]
                USERSOLORANK_TIER_NAME = " ".join(USERSOLORANK_TIER_NAME)

                # LP 점수
                USERSOLORANK_TIER_LP = USERSOLORANK_TIER_LP_MIX[-2:]
                USERSOLORANK_TIER_LP = " ".join(USERSOLORANK_TIER_LP)

                # 승률
                try:
                    USERSOLORANK_WINNING_RATE = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div.col-12.col-md-6.col-lg-12.mb-lg-2 > div > div:nth-child(2) > div.summoner-tier__rate > div.win-rate')[0].get_text().strip()
                except:
                    USERSOLORANK_WINNING_RATE = "승률 0%(No Data)"

                # 이긴 게임과 진 게임의 횟수
                try:
                    USERSOLORANK_WIN_LOSE_TIME = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div.col-12.col-md-6.col-lg-12.mb-lg-2 > div > div:nth-child(2) > div.summoner-tier__rate > div:nth-child(2)')[0].get_text().strip().replace(' ','')
                    _divided = USERSOLORANK_WIN_LOSE_TIME.split('\n')       # 승과 패 횟수를 적절하게 띄우기 위함
                    USERSOLORANK_WIN_LOSE_TIME = " ".join(_divided)
                except:
                    USERSOLORANK_WIN_LOSE_TIME = "(0승 0패 / No Data)"

                USERSOLORANK_INFO = [USERSOLORANK_TIER_IMG_URL, USERSOLORANK_TIER_NAME, USERSOLORANK_TIER_LP, USERSOLORANK_WINNING_RATE, USERSOLORANK_WIN_LOSE_TIME]
                # print(USERSOLORANK_INFO)
                ##################################################################################################################################


                ##################################################### 자유 랭크 정보 ####################################################
                # 티어 이미지
                USERFREERANK_TIER_IMG_URL = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div:nth-child(2) > div > div.summoner-tier__img > img')[0]['src']

                # 티어 이름과 Leauge Point(같이 나옴)
                USERFREERANK_TIER_LP_MIX = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div:nth-child(2) > div > div:nth-child(2) > div.summoner-tier__description')[0].get_text().split()

                # 티어 이름
                USERFREERANK_TIER_NAME = USERFREERANK_TIER_LP_MIX[0:-2]
                USERFREERANK_TIER_NAME = " ".join(USERFREERANK_TIER_NAME)

                # LP 점수
                USERFREERANK_TIER_LP = USERFREERANK_TIER_LP_MIX[-2:]
                USERFREERANK_TIER_LP = " ".join(USERFREERANK_TIER_LP)

                # 승률
                try:
                    USERFREERANK_WINNING_RATE = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div:nth-child(2) > div > div:nth-child(2) > div.summoner-tier__rate > div.win-rate')[0].get_text().strip()
                except:
                    USERFREERANK_WINNING_RATE = "승률 0%(No Data)"
                
                # 이긴 게임과 진 게임의 횟수
                try:
                    USERFREERANK_WIN_LOSE_TIME = soup.select('#wrapper > div > div > div > div.container.mt-3.mt-md-4.p-0 > div.mt-3 > div.summoner-tab-content.active > div.row.row-small > div.col-12.col-lg-4.order-1 > div > div:nth-child(2) > div > div:nth-child(2) > div.summoner-tier__rate > div:nth-child(2)')[0].get_text().strip().replace(' ','')
                    _divided = USERFREERANK_WIN_LOSE_TIME.split('\n')       # 승과 패 횟수를 적절하게 띄우기 위함
                    USERFREERANK_WIN_LOSE_TIME = " ".join(_divided)
                except:
                    USERFREERANK_WIN_LOSE_TIME = "(0승 0패 / No Data)"

                USERFREERANK_INFO = [USERFREERANK_TIER_IMG_URL, USERFREERANK_TIER_NAME, USERFREERANK_TIER_LP, USERFREERANK_WINNING_RATE, USERFREERANK_WIN_LOSE_TIME]
                # print(USERFREERANK_INFO)
                ##################################################################################################################################


    ##################################################### 최근 게임플레이 정보 요약 ####################################################
    # 추가적인 정보 가져오기
    
    username = username.replace(' ','')
    url = "https://poro.gg/summoner/kr/" + username + "/matches?queueType=all&offset=0"
    # print(url)

    response = requests.get(url, timeout = 0.9)

    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # GAMEPLAY_INFO_MIX = str(soup)
        GAMEPLAY_INFO_MIX = json.loads(str(soup))
        GAMEPLAY_INFO_MIX = GAMEPLAY_INFO_MIX['summoner_matches']

        # 최근 게임 플레이 자료를 가능한 되는대로 수집해 통계 산출하기
        sequence = 0            # 통계 번호

        # 통계 산출
        GAMEPLAY_TOTAL = 0
        GAMEPLAY_WIN = 0
        GAMEPLAY_LOSE = 0
        GAMEPLAY_KILLS = 0
        GAMEPLAY_DEATH = 0
        GAMEPLAY_ASSISTS = 0
        GAMEPLAY_KDA = 0
        GAMEPLAY_KDA_PERFECT = 0
        GAMEPLAY_MULTI_KILLS = 0
        GAMEPLAY_KILL_PARTICIPATION = 0
        GAMEPLAY_WARDS_PLACED = 0
        GAMEPLAY_KILLED = 0
        GAMEPLAY_CS = 0

        while True:
            try:
                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['is_win'])                # 승리 여부
                if 'True' == str(GAMEPLAY_INFO_MIX[sequence]['participant']['is_win']):    # 문자열 대 문자열로 비교
                    GAMEPLAY_TOTAL += 1
                    GAMEPLAY_WIN += 1
                else:
                    GAMEPLAY_TOTAL += 1
                    GAMEPLAY_LOSE += 1

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['kills'])                 # KILL 횟수
                GAMEPLAY_KILLS += int(GAMEPLAY_INFO_MIX[sequence]['participant']['kills'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['deaths'])                # 죽음 횟수
                GAMEPLAY_DEATH += int(GAMEPLAY_INFO_MIX[sequence]['participant']['deaths'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['assists'])               # 킬 보조
                GAMEPLAY_ASSISTS += int(GAMEPLAY_INFO_MIX[sequence]['participant']['assists'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['kda'])                   # K/DA
                                # K/DA값 산출 : (Kill 횟수 + Assist 횟수) / (Death 횟수)
                                # K/DA값에서 Death 횟수가 0인경우 일반 계산이 불가능하므로 직접 계산한다.
                GAMEPLAY_KDA += (((int(GAMEPLAY_INFO_MIX[sequence]['participant']['kills'])) + int(GAMEPLAY_INFO_MIX[sequence]['participant']['deaths'])) 
                                    / int(GAMEPLAY_INFO_MIX[sequence]['participant']['assists']))
                                # 만약 Death 전적이 없는 경우는 Perfect 평점으로 추가 기록
                if "Perfect" == str(GAMEPLAY_INFO_MIX[sequence]['participant']['kda']):
                    GAMEPLAY_KDA_PERFECT += 1

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['multi_kills'])           # 멀티킬
                GAMEPLAY_MULTI_KILLS += int(GAMEPLAY_INFO_MIX[sequence]['participant']['multi_kills'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['kill_participation'])    # 킬 관여
                                # 백분율로 환산하기 (ex. 0.123 -> 12.3%)
                GAMEPLAY_KILL_PARTICIPATION += float(GAMEPLAY_INFO_MIX[sequence]['participant']['kill_participation']) * 100

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['wards_placed'])          # 와드 설치수
                GAMEPLAY_WARDS_PLACED += int(GAMEPLAY_INFO_MIX[sequence]['participant']['wards_placed'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['wards_killed'])          # 와드 파괴수
                GAMEPLAY_KILLED += int(GAMEPLAY_INFO_MIX[sequence]['participant']['wards_killed'])

                # print(GAMEPLAY_INFO_MIX[sequence]['participant']['cs'])                    # CS(미니언 킬)
                GAMEPLAY_CS += int(GAMEPLAY_INFO_MIX[sequence]['participant']['cs'])

                sequence += 1
            except:
                break
        
        # 정보 종합해서 리스트로 묶기
        GAMEPLAY_STATUS = [GAMEPLAY_TOTAL, GAMEPLAY_WIN, GAMEPLAY_LOSE, GAMEPLAY_KILLS, GAMEPLAY_DEATH, GAMEPLAY_ASSISTS,
                    GAMEPLAY_KDA, GAMEPLAY_KDA_PERFECT, GAMEPLAY_MULTI_KILLS, GAMEPLAY_KILL_PARTICIPATION,
                    GAMEPLAY_WARDS_PLACED, GAMEPLAY_KILLED, GAMEPLAY_CS]

        # print(GAMEPLAY_STATUS[0])
        # 플레이 횟수(전체 판수/이긴 판수/진 판수), KDA_PERFECT를 제외하고는 평균값을 산출한다.
        for _i in range(3, len(GAMEPLAY_STATUS)):
            if _i == 7:     # KDA_PERFECT는 제외
                continue
            GAMEPLAY_STATUS[_i] = round((GAMEPLAY_STATUS[_i] / GAMEPLAY_STATUS[0]), 3)

        # 단위 붙이기, 후가공
        GAMEPLAY_STATUS[0] = "{} 플레이".format(GAMEPLAY_STATUS[0])
        GAMEPLAY_STATUS[1] = "{} 플레이".format(GAMEPLAY_STATUS[1])
        GAMEPLAY_STATUS[2] = "{} 플레이".format(GAMEPLAY_STATUS[2])
        GAMEPLAY_STATUS[3] = "{} 회".format(GAMEPLAY_STATUS[3])
        GAMEPLAY_STATUS[4] = "{} 회".format(GAMEPLAY_STATUS[4])
        GAMEPLAY_STATUS[5] = "{} 회".format(GAMEPLAY_STATUS[5])
        GAMEPLAY_STATUS[8] = "{} 회".format(GAMEPLAY_STATUS[8])
        GAMEPLAY_STATUS[9] = "{} %".format(GAMEPLAY_STATUS[9])
        GAMEPLAY_STATUS[10] = "{} 개".format(GAMEPLAY_STATUS[10])
        GAMEPLAY_STATUS[11] = "{} 개".format(GAMEPLAY_STATUS[11])
        GAMEPLAY_STATUS[12] = "{} 점".format(GAMEPLAY_STATUS[12])

        OVERALL_FUNCTION_RETURN = 200

        # print(GAMEPLAY_STATUS)

    ##################################################################################################################################
    
    _END_TIME = time.time()
    running_time = round((_END_TIME - _START_TIME), 4)
    printCommandLog(fromWho, "show gameStat --LOL --username {}(Function)".format(username), "RUNNING", "running time : " + str(running_time) + " sec/pass")

    return OVERALL_FUNCTION_RETURN, COMMON_USER_INFO, USERSOLORANK_INFO, USERFREERANK_INFO, GAMEPLAY_STATUS, running_time
                


# print(getLOLUserStatistics("EXAMPLE", "미친개 정강지"))
# print(getLOLUserStatistics("EXAMPLE", "라키주작"))
# print(getLOLUserStatistics("EXAMPLE", "사거리 계산"))
