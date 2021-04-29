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
        printCommandLog(fromWho, "show gameStat --LOLtft --username {}(Function)".format(username), "RUNNING", "Getting LOL Statistics.. username : " + username)

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

        # 유저 기본 정보
        # 유저 이름
        USERNAME = soup.select_one('#profile > div > div.profile__header > div.profile__summoner > span').get_text().split()[0]

        # 유저 레벨
        USERLEVEL = soup.select_one('#profile > div > div.profile__header > div.profile__icon > span').get_text()

        # 유저 사진
        USER_PROFILE_PICTURE = str(soup.select_one('#profile > div > div.profile__header > div.profile__icon > img')).split()[6]
        USER_PROFILE_PICTURE = USER_PROFILE_PICTURE.replace('src="','').replace('"/>','')
        USER_PROFILE_PICTURE = "http:" + USER_PROFILE_PICTURE

        COMMON_USER_INFO = [USERNAME, USERLEVEL, USER_PROFILE_PICTURE]
        print(COMMON_USER_INFO)

        # 유저 게임플레이 관련 정보
        # 순서대로 티어 이름, LP(League Point), 상위 퍼센트, 그리고 전체 등수
        USER_TIER_INFO_MIX = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__info > div.profile__tier__summary').get_text().split()
        USER_RANKING_STEP = soup.select_one('#profile > div > div:nth-child(2) > div.row.row-normal.mt-3 > div.col-lg-4 > div.profile__tier > div.profile__tier__info > div.profile__tier__summary > div.text-dark-gray.font-size-11 > span.rank-region').get_text().strip()

        USER_TIER_NAME = "{} {}".format(USER_TIER_INFO_MIX[1], USER_TIER_INFO_MIX[2])
        USER_LEAGUE_POINT = "{} {}".format(USER_TIER_INFO_MIX[3], USER_TIER_INFO_MIX[4])
        USER_TOP_PERCENT = "{} {}".format(USER_TIER_INFO_MIX[5], USER_TIER_INFO_MIX[6])

        USER_GAMEPLAY_OVERALL_STAT = [USER_TIER_NAME, USER_LEAGUE_POINT, USER_TOP_PERCENT, USER_RANKING_STEP]
        print(USER_GAMEPLAY_OVERALL_STAT)

        


getLOLtftUserStatistics("EXAMPLE123", "6L3gap")