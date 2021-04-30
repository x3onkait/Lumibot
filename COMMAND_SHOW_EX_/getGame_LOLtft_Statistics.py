import requests
from bs4 import BeautifulSoup

import sys, os

import time

######################################################################################
# 이 getStockInfo.py를 기준으로 1단계 상위 디렉토리 레벨선상에 있는 resource파일을 가져오기 위해
# import sys, os를 사용하고, sys.path.append(...)로 이를 가능하게 한다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로깅 처리 함수 불러오기
from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog
######################################################################################

def getLOLtftUserStatistics(fromWho, username):

    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://lolchess.gg/profile/kr/" + username

    try:
        response = requests.get(url, timeout = 0.9)
        printCommandLog(fromWho, "show gameStat --LOLtft --username {}(Function)".format(username), "RUNNING", "Getting LOLtft Statistics.. username : " + username)
    except:
        OVERALL_FUNCTION_RETURN = 408
        return 408, None, None, None, None                  # Connection Timeout

    # 연결에 성공해 데이터가 받아와지는 경우
    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        invalidTester = str(soup)

        # 유효한 소환사 이름이 아니라서 검색 결과가 없는 경우
        if "검색 결과가 없습니다" in invalidTester:
            printCommandLog(fromWho, "show gameStat --LOL --username {}(Function)".format(username), "FAILED", "NON_EXIST_USERNAME")
            OVERALL_FUNCTION_RETURN = 404
            return 404, None, None, None, None

        try:

            # 유저 기본 정보
            # 유저 이름 > 띄어쓰기를 통한 공백이 이름 안에 있는 경우 문제 발생
            # USERNAME = soup.select_one('#profile > div > div.profile__header > div.profile__summoner > span').get_text().split()[0]
            USERNAME = username

            # 유저 레벨
            USERLEVEL = soup.select_one('#profile > div > div.profile__header > div.profile__icon > span').get_text()

            # 유저 사진
            USER_PROFILE_PICTURE = str(soup.select_one('#profile > div > div.profile__header > div.profile__icon > img')).split()[6]
            USER_PROFILE_PICTURE = USER_PROFILE_PICTURE.replace('src="','').replace('"/>','')
            USER_PROFILE_PICTURE = "http:" + USER_PROFILE_PICTURE

            COMMON_USER_INFO = [USERNAME, USERLEVEL, USER_PROFILE_PICTURE]
            # print(COMMON_USER_INFO)

            # 유저 게임플레이 관련 정보
            # 순서대로 티어 이름, LP(League Point), 상위 퍼센트, 그리고 전체 등수
            USER_TIER_INFO_MIX = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__info > div.profile__tier__summary').get_text().split()
            USER_RANKING_STEP = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__info > div.profile__tier__summary > div.text-dark-gray.font-size-11 > span.rank-region').get_text().strip()

            USER_TIER_NAME = "{} {}".format(USER_TIER_INFO_MIX[1], USER_TIER_INFO_MIX[2])
            USER_LEAGUE_POINT = "{} {}".format(USER_TIER_INFO_MIX[3], USER_TIER_INFO_MIX[4])
            USER_TOP_PERCENT = "{} {}".format(USER_TIER_INFO_MIX[5], USER_TIER_INFO_MIX[6])

            USER_GAMEPLAY_OVERALL_STAT = [USER_TIER_NAME, USER_LEAGUE_POINT, USER_TOP_PERCENT, USER_RANKING_STEP]
            # print(USER_GAMEPLAY_OVERALL_STAT)

            # 유저 게임 세부 통계 관련 정보
            # 순서대로 이긴 게임 수와 그에 대한 상위 % 비율 / 평균 승률과 그에 대한 상위 % 비율
            # 게임 플레이 수와 그에 대한 상위 % 비율 / 평균 게임 등수(1 ~ 8등)
            USER_GAMEPLAY_VICTORY = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__wins > div.profile__tier__stat.clearfix > span.profile__tier__stat__value.float-right').get_text().strip()
            USER_GAMEPALY_VICTORY_TOP_PERCENT = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__wins > span').get_text().split()[1]
            USER_GAMEPLAY_WINNING_RATE = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__winrate_10 > div.profile__tier__stat.clearfix > span.profile__tier__stat__value.float-right').get_text().strip()
            USER_GAMEPLAY_VICTORY_TOP_PERCENT = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__winrate_10 > span').get_text().split()[1]
            USER_GAMEPLAY_GAME_COUNT = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__plays > div.profile__tier__stat.clearfix > span.profile__tier__stat__value.float-right').get_text().strip()
            USER_GAMEPLAY_GAME_COUNT_TOP_PERCENT = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__plays > span').get_text().split()[1]
            USER_GAMEPLAY_AVERAGE_GRADE = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__stats > div > div.col-6.profile__tier__avg_rank > div.profile__tier__stat.clearfix > span.profile__tier__stat__value.float-right').get_text().strip()

            USER_GAMEPLAY_DETAILED_STATUS = [USER_GAMEPLAY_VICTORY, USER_GAMEPALY_VICTORY_TOP_PERCENT, USER_GAMEPLAY_WINNING_RATE,
                                            USER_GAMEPLAY_VICTORY_TOP_PERCENT, USER_GAMEPLAY_GAME_COUNT, USER_GAMEPLAY_GAME_COUNT_TOP_PERCENT,
                                            USER_GAMEPLAY_AVERAGE_GRADE]

            # print(USER_GAMEPLAY_DETAILED_STATUS)

            OVERALL_FUNCTION_RETURN = 200

            _END_TIME = time.time()
            running_time = round((_END_TIME - _START_TIME), 4)
            printCommandLog(fromWho, "show gameStat --LOLtft --username {}(Function)".format(username), "RUNNING", "running time : " + str(running_time) + " sec/pass")

            return OVERALL_FUNCTION_RETURN, COMMON_USER_INFO, USER_GAMEPLAY_OVERALL_STAT, USER_GAMEPLAY_DETAILED_STATUS, running_time
        
        # 플레이 기록이 없어 통계가 안 남는 경우
        except:
            OVERALL_FUNCTION_RETURN = -1
            return OVERALL_FUNCTION_RETURN, -1, -1, -1, -1


# print(getLOLtftUserStatistics("EXAMPLE123", "l항아l"))