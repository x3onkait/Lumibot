import requests
from bs4 import BeautifulSoup

import sys, os

######################################################################################
# 이 getStockInfo.py를 기준으로 1단계 상위 디렉토리 레벨선상에 있는 resource파일을 가져오기 위해
# import sys, os를 사용하고, sys.path.append(...)로 이를 가능하게 한다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로깅 처리 함수 불러오기
from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog
######################################################################################

import time

def getLOLUserStatistics(username):

    _START_TIME = time.time()       # 함수 퍼포먼스(작동 시간) 측정

    url = "https://www.op.gg/summoner/userName=" + username
    

    try:
        response = requests.get(url, timeout = 0.9)
        printCommandLog("show gameStat --LOL(Function)", "RUNNING", "Getting LOL Statistics.. username : " + username)
    except:
        USERNAME = 404              # username을 통해 함수 실행 실패를 알려줌(응답이 제 시간 내 돌아오지 않는 경우)
        return 404

    try:

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')


            # 유저 이름
            USERNAME = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Profile > div.Information > span').get_text()
            # print(USERNAME)

            USERLEVEL = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Face > div > span').get_text()
            USERLEVEL = "Lv. " + USERLEVEL
            # print(USERLEVEL)
            
            # 유저 프로필 사진 
            USER_PROFILE_PICTURE = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Face > div > img')
            USER_PROFILE_PICTURE = str(USER_PROFILE_PICTURE).split()[2].replace('src="','').replace("\"/>",'')
            USER_PROFILE_PICTURE = "https:" + USER_PROFILE_PICTURE
            print(USER_PROFILE_PICTURE)

            # 유저 랭킹 / 보다 가독성 좋게 잘라서 다시 알려주기
            try:
                USERRANK_MIX = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Profile > div.Information > div > div > a').get_text().strip()
                # op.gg에서는 "Ladder Rank 2,345,555(xx% of top)이라고 표현해 줄 때가 
                # 있고 그냥 "랭킹 1위"이런식으로 표현해 줄 때강 있다.
                if len(USERRANK_MIX.split()) == 6:                      # 일반 유저
                    digitRank = USERRANK_MIX.split()[2]
                    percentageRank = USERRANK_MIX.split()[3].replace('(','')
                    USERRANK = "랭킹 " + digitRank + " 위" + " / ( 상위 " + percentageRank + " )"
                    # print(USERRANK)

                elif len(USERRANK_MIX.split()) == 2:                    # 랭커
                    digitRank = USERRANK_MIX.split()[1]
                    USERRANK = "랭킹 " + digitRank + " 위"
                    # print(USERRANK)
            except:
                # print("랭킹 순위 정보 없음")
                USERRANK = "No Data"

            TIER_SYMBOL_PIC_URL = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box')
            TIER_SYMBOL_PIC_URL = str(TIER_SYMBOL_PIC_URL.select('.Image')).split()[2].replace('src="','').replace("\"/>]",'')
            TIER_SYMBOL_PIC_URL = "https:" + TIER_SYMBOL_PIC_URL
            # print(TIER_SYMBOL_PIC_URL)

            # 솔로 랭킹 티어 종합 정보
            TIER_SOLO_RANK_INFO = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo')
            # 순서대로 랭킹 현황(ex. 브론즈, 골드..) / LP(리그 포인트) / 이긴 게임 / 진 게임 / 승률
            try:
                TIER_SOLO_RANK_STEP = str(TIER_SOLO_RANK_INFO.select('.TierRank')).replace('[','').replace(']','').replace('<div class="TierRank">','').replace('</div>','')
                TIER_SOLO_LEAGUE_POINT = str(TIER_SOLO_RANK_INFO.select('.LeaguePoints')).split()[2] + " LP"
                TIER_SOLO_GAME_PLAY_WIN = str(TIER_SOLO_RANK_INFO.select('.wins')).replace('[<span class="wins">','').replace('W</span>]','') + " 게임"
                TIER_SOLO_GAME_PLAY_LOSE = str(TIER_SOLO_RANK_INFO.select('.losses')).replace('[<span class="losses">','').replace('L</span>]','') + " 게임"
                TIER_SOLO_GAME_WINNING_RATIO = str(TIER_SOLO_RANK_INFO.select('.winratio')).split()[3].replace('\'','').replace('%</span>]','') + " %"
                # print(TIER_SOLO_RANK_STEP)
                # print(TIER_SOLO_LEAGUE_POINT)
                # print(TIER_SOLO_GAME_PLAY_WIN)
                # print(TIER_SOLO_GAME_PLAY_LOSE)
                # print(TIER_SOLO_GAME_WINNING_RATIO)
            except:
                # print("솔로 랭킹 티어 종합 정보 없음")
                TIER_SOLO_RANK_STEP = "Unranked"
                TIER_SOLO_LEAGUE_POINT = "No Data"
                TIER_SOLO_GAME_PLAY_WIN = "No Data"
                TIER_SOLO_GAME_PLAY_LOSE = "No Data"
                TIER_SOLO_GAME_WINNING_RATIO = "No Data"

            

        ##################################################################################
        _END_TIME = time.time()
        running_time = round((_END_TIME - _START_TIME), 4)
        printCommandLog("show gameStat --LOL(Function)", "RUNNING", "running time : " + str(running_time) + " sec/pass")

        return str(USERNAME), str(USERLEVEL), str(USER_PROFILE_PICTURE), str(USERRANK), str(TIER_SYMBOL_PIC_URL), str(TIER_SOLO_RANK_STEP), str(TIER_SOLO_LEAGUE_POINT), str(TIER_SOLO_GAME_PLAY_WIN), str(TIER_SOLO_GAME_PLAY_LOSE), str(TIER_SOLO_GAME_WINNING_RATIO), str(running_time)

    except:
        printCommandLog("show gameStat --LOL(Function)", "FAILED", "UNEXPECTED_DATA_RECEIVED")
        return 403, 403, 403, 403, 403, 403, 403, 403, 403, 403


# print(getLOLUserStatistics("오리 빵빵댕이"))
# print(getLOLUserStatistics("DRX Decky"))
# print(getLOLUserStatistics("해리포비"))
# print(getLOLUserStatistics("INVALID_TEST_123asdf!@#!@@"))