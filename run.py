import asyncio, discord
import time
import datetime
from discord.ext import commands

import os #, sys

############################# 직접 만든 모듈 ##################################

import COMMAND_SHOW_EX_.getCryptocurrencyInfo           # 암호화폐 정보
import COMMAND_SHOW_EX_.getStockInfo                    # 주식 정보
import COMMAND_SHOW_EX_.getCurrentTime                  # 현재 시간 정보
import COMMAND_SHOW_EX_.getWorldPopulation              # 인구 정보
import COMMAND_SHOW_EX_.getGame_LOL_Statistics          # 리그 오브 레전드 전적 정보
import COMMAND_SHOW_EX_.getGame_LOLtft_Statistics       # 리그 오브 레전드 전략적 팀 전투(롤토체스) 전적 정보

import COMMAND_RANDOM_.randomToolBox        # 난수 관련
import COMMAND_CALCULATE_.calculator        # 계산기 역할을 하는 다양한 모듈들

from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog  # 각종 시스템 로그 출력하기

###############################################################################

bot = commands.Bot(command_prefix="$")

_DISCORD_BOT_TOKEN = input("enter your token > ")

@bot.event
async def on_ready():
    print("We have loggedd in as {0.user}".format(bot))
    # embed = discord.Embed(title = "Turned To Online :white_check_mark:", description = "Lumibot이 온라인 상태가 되었습니다.", color = 0xffd9ea)
    # embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
    # await ctx.send(embed = embed)
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="enter [$show help] to get info"))
    printCommandLog(bot.user.name, "START THE BOT", "OK")

# 재미를 위한 이스터 에그 :)
@bot.command()
async def overdrive(ctx):
    easterEgg = "**힘이... 어둠이... 넘쳐흐른다! 아↗하하하하하!!!!**"
    await ctx.channel.send(easterEgg)
    printCommandLog(ctx.author.name, "overdrive", "OK", "Easter Egg")


# show [옵션1]
@bot.command()
async def show(ctx, *option):                   
    if option[0] == "hello":                  # hello | 간단한 인사말 출력
        embed = discord.Embed(title = "hello", description = "만나서 반갑습니다!", timestamp=datetime.datetime.utcnow(), color = 0x3eb489)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "show hello", "OK")

    elif option[0] == "help":                 # help | 도움말 출력
        embed = discord.Embed(title = "command help", description = "봇 정보",  timestamp=datetime.datetime.utcnow(), color = 0x6a5acd)
        embed.add_field(name = "```show``` 계열 명령어", value = 
                '''
                인사 : `show hello`, 도움말 : `show help`, 봇 정보 : `show info` 
                현재 세계 인구 통계 : `show population`, 현재 시간 보기 : `show currentTime`
                이스터에그(폭주!) : `overdrive`

                온라인 게임 전적 조회(유저명 검색)
                게임 옵션) 리그 오브 레전드(`--LOL`), 롤토체스(`--LOLtft`)
                ```show gameStat [게임 옵션] --username [유저명]```
                국내 주식 시세 검색(다음 금융 제공)```show stock --search [국내 주식 종목명(ex. 삼성전자)]```
                암호화폐 시세 검색(빗썸 제공)```show crypto --symbol [암호화폐 기호(ex. BTC)]```
                암호화폐 통계 요약(전세계/코인랭킹 제공)```show crypto --brief```
                ''', inline = False)
        embed.add_field(name = "```echo``` 계열 명령어", value = 
                '''
                입력값 그대로 출력하기(따라하기)```echo [입력값] --count [횟수(1~20)]```
                ''', inline = False)
        embed.add_field(name = "```calculate``` 계열 명령어", value = 
                '''
                간단한 수식 계산(사칙연산/나머지/비트논리연산)```calculate [숫자] [연산자] [숫자] ...```
                지원되는 연산자 `+|-|*|/|**(거듭제곱)|%(나머지)|&(비트and)||(비트or)|^(비트xor)`, 지원되는 숫자 `정수, 실수`
                ''', inline = False)
        embed.add_field(name = "```random``` 계열 명령어", value = 
                '''
                지정한 범위 내에서 랜덤 숫자 출력하기```random --start [시작숫자] --end [끝 숫자]```
                로또 번호 추첨 ```random --drawTheLotto```
                주사위 굴리기(1 ~ 6)```random --rollthedice```
                영숫자 혼합 난수 생성하기```random --getAlphanumeric --length [길이(1~256)]```
                16진수 난수 생성하기```random --getHexadecimal --length [길이(1~256)]```
                ''', inline = False)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "show help", "OK")

    elif option[0] == "info":                 # info | 봇 정보 출력   
        embed = discord.Embed(title = "information", description = "봇 정보",  timestamp=datetime.datetime.utcnow(), color = 0x32cd32)
        embed.add_field(name = "개발 언어", value = "PYTHON", inline = False)
        embed.add_field(name = "개발자", value = "Garam Lee", inline = True)
        embed.set_image(url="https://i.imgur.com/w1pAySc.jpg")
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "show info", "OK")

    elif option[0] == "gameStat" and option[1] == "--LOL" and option[2] == "--username":

        if len(option) == 4:

            OVERALL_FUNCTION_RETURN, COMMON_USER_INFO, USERSOLORANK_INFO, USERFREERANK_INFO, GAMEPLAY_STATUS, running_time = COMMAND_SHOW_EX_.getGame_LOL_Statistics.getLOLUserStatistics(ctx.author.name, str(option[3]))

            if OVERALL_FUNCTION_RETURN == 408:
                embed = discord.Embed(title = "No Response Exception", description = "현재 전적 조회소 poro.gg 에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "FAILED", "NO_RESPONSE_RETURNED")

            elif OVERALL_FUNCTION_RETURN == 404:
                embed = discord.Embed(title = "No Expected Data Received", description = "제대로 된 데이터가 poro.gg에서 오지 않았습니다\n오타가 입력되었을 가능성이 매우 높으니 입력값을 다시 한번 확인해주세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "FAILED", "NO_EXPECTED_DATA_RECEIVED")
            
            printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "RUNNING", "INIT_GET_INFO_PHASE")
            
            embed = discord.Embed(title = "리그 오브 레전드 전적 조회", description = "정보 제공 : poro.gg", timestamp=datetime.datetime.utcnow(), color = 0x307c70)

            embed.set_thumbnail(url = COMMON_USER_INFO[2])

            embed.set_author(name = " : @{}".format(COMMON_USER_INFO[1]), url = USERSOLORANK_INFO[0], icon_url = USERSOLORANK_INFO[0])

            embed.add_field(name = "기본 정보", value = 
            '''
            랭킹 현황 : **{}**
            __유저 이름 : **{}**__
            유저 레벨 : **{}**
            '''.format(COMMON_USER_INFO[0], COMMON_USER_INFO[1], COMMON_USER_INFO[3]), inline = False)

            embed.add_field(name = "솔로 랭크 통계", value = 
            '''
            __랭크 : **{}**__
            리그 포인트 : **{}**
            승률 : **{}** {}
            '''.format(USERSOLORANK_INFO[1], USERSOLORANK_INFO[2], USERSOLORANK_INFO[3], USERSOLORANK_INFO[4]), inline = True)

            embed.add_field(name = "자유 랭크 통계", value = 
            '''
            랭크 : **{}**
            리그 포인트 : **{}**
            승률 : **{}** {}
            '''.format(USERFREERANK_INFO[1], USERFREERANK_INFO[2], USERFREERANK_INFO[3], USERFREERANK_INFO[4]), inline = True)

            embed.add_field(name = "최근 게임 플레이 분석", value = 
            '''
            최근 플레이한 게임 : **{}**
            이긴 게임 / 진 게임 : **{}** / **{}**
            게임당 평균 KILL : **{}**
            게임당 평균 DEATH : **{}**
            게임당 평균 ASSIST : **{}**
            __게임당 평균 KDA : **{}**__
            게임당 평균 멀티킬 : **{}**
            게임당 평균 킬관여 : **{}**
            게임당 평균 와드 설치수 : **{}**
            게임당 평균 와드 파괴수 : **{}**
            게임당 평균 플레이 시간 : **{}**
            __분당 평균 CS : **{}**__
            '''.format(GAMEPLAY_STATUS[0], GAMEPLAY_STATUS[1], GAMEPLAY_STATUS[2], GAMEPLAY_STATUS[3], GAMEPLAY_STATUS[4],
                        GAMEPLAY_STATUS[5], GAMEPLAY_STATUS[6], GAMEPLAY_STATUS[7], GAMEPLAY_STATUS[8], GAMEPLAY_STATUS[9],
                        GAMEPLAY_STATUS[10], GAMEPLAY_STATUS[11], GAMEPLAY_STATUS[12]), inline = False)
            # embed.set_image(url = "https://i.imgur.com/GClp1fh.png")

            embed.set_footer(text="Lumibot | From {}({}) | Run Time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)

            printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "OK")
        
        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show gameStat --LOL --username {}".format(str(option[3])), "FAILED", "ILLEGAL_ARGUMENT_DETECTED")   

    elif option[0] == "gameStat" and option[1] == "--LOLtft" and option[2] == "--username":

        if len(option) == 4:

            OVERALL_FUNCTION_RETURN, COMMON_USER_INFO, USER_GAMEPLAY_OVERALL_STAT, USER_GAMEPLAY_DETAILED_STATUS, running_time = COMMAND_SHOW_EX_.getGame_LOLtft_Statistics.getLOLtftUserStatistics(ctx.author.name, str(option[3]))

            if OVERALL_FUNCTION_RETURN == -1:
                embed = discord.Embed(title = "No Statistics Exists", description = "데이터 수집 중 NoneType을 포함할 수 있는 예외가 발견되었습니다.\n등록된 플레이 기록이 검색되지 않았습니다.\n혹시 게임을 하지 않으셨나요?", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "FAILED", "NO_STATISTICS_EXISTS")

            if OVERALL_FUNCTION_RETURN == 408:
                embed = discord.Embed(title = "No Response Exception", description = "현재 전적 조회소 poro.gg 에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "FAILED", "NO_RESPONSE_RETURNED")

            elif OVERALL_FUNCTION_RETURN == 404:
                embed = discord.Embed(title = "No Expected Data Received", description = "제대로 된 데이터가 poro.gg에서 오지 않았습니다\n오타가 입력되었을 가능성이 매우 높으니 입력값을 다시 한번 확인해주세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "FAILED", "NO_EXPECTED_DATA_RECEIVED")

            printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "RUNNING", "INIT_GET_INFO_PHASE")

            embed = discord.Embed(title = "리그 오브 레전드 전적 조회", description = "정보 제공 : poro.gg", timestamp=datetime.datetime.utcnow(), color = 0x8e6b92)

            embed.set_thumbnail(url = COMMON_USER_INFO[2])

            embed.add_field(name = "기본 정보", value = 
            '''
            __유저 이름 : **{}**__
            유저 레벨 : **{}**
            __랭크 : **{} ( {} )**__
            전체 유저 순위 : **{}**
            리그 포인트 : **{}**
            '''.format(COMMON_USER_INFO[0], COMMON_USER_INFO[1], USER_GAMEPLAY_OVERALL_STAT[0], USER_GAMEPLAY_OVERALL_STAT[2],
            USER_GAMEPLAY_OVERALL_STAT[3], USER_GAMEPLAY_OVERALL_STAT[1]), inline = False)

            embed.add_field(name = "게임플레이 세부 통계", value = 
            '''
            승리 : **{}** ( 상위 {} )
            승률 : **{}** ( 상위 {} )
            게임 플레이 수 : **{}** ( 상위 {} )
            평균 게임 등수 : **{}**
            '''.format(USER_GAMEPLAY_DETAILED_STATUS[0], USER_GAMEPLAY_DETAILED_STATUS[1], USER_GAMEPLAY_DETAILED_STATUS[2], USER_GAMEPLAY_DETAILED_STATUS[3],
                    USER_GAMEPLAY_DETAILED_STATUS[4], USER_GAMEPLAY_DETAILED_STATUS[5], USER_GAMEPLAY_DETAILED_STATUS[6]), inline = False)
            
            embed.set_footer(text="Lumibot | From {}({}) | Run Time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)

            printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "OK")

        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show gameStat --LOLtft --username {}".format(str(option[3])), "FAILED", "ILLEGAL_ARGUMENT_DETECTED")  


    elif option[0] == "crypto" and option[1] == "--symbol":

        if len(option) == 3:
            # print(option)
            if COMMAND_SHOW_EX_.getCryptocurrencyInfo.getNameFromCryptoSymbol(str(option[2])) == 404:
                embed = discord.Embed(title = "No Listed Cryptocurrency", description = "현재 데이터베이스에 제대로 등록되지 않았거나,\n 입력값이 잘못된 것 같습니다(Bithumb 거래소 기준).\n 입력값을 한번 더 확인해주세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "FAILED", "NO_LISTED_CRYPTO_TRIAL")

            #(cryptocurrency_KRname, cryptocurrency_to_KRW, cryptocurrency_change_KRW, cryptocurrency_change_PERCENT, cryptocurrency_transaction_KRW, cryptocurrency_transaction_CRYPTO, running_time) = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyInfo(str(option[2]))
            CRYPTO_KR_NAME, CURRENT_CRYPTO_VALUE_KRW, CURRENT_CRYPTO_VALUE_OPENING_00h, CURRENT_CRYPTO_VALUE_MIN_00h, CURRENT_CRYPTO_VALUE_MAX_00h, CURRENT_CRYPTO_UNIT_TRADE_24h, CURRENT_CRYPTO_KRW_TRADE_24h, CURRENT_CRYPTO_KRW_CHANGE_24h, CURRENT_CRYPTO_PERCENT_CHANGE_24h, CURRENT_UPDATE_TIME, _RUNNING_TIME, CURRENT_CRYPTO_CHANGE_EMOJI, CRYPTO_PICTURE_URL = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyInfo(ctx.author.name, str(option[2]))
            if CRYPTO_KR_NAME == 404:
                embed = discord.Embed(title = "No Response Exception", description = "현재 거래소에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "FAILED", "NO_RESPONSE_RETURNED")

            # 진짜 암호화폐 정보
            embed = discord.Embed(title = option[2] + " 암호화폐 정보", description = "정보 제공 : 빗썸(bithumb.com)", timestamp=datetime.datetime.utcnow(), color = 0xeaf27c)
            printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "RUNNING", "INIT_GET_INFO_PHASE")

            # 텍스트 중심의 정보 출력
            if CRYPTO_PICTURE_URL != "404":     # getCryptocurrencyInfo()에서 URL을 string형태로 반환함
                embed.set_thumbnail(url = CRYPTO_PICTURE_URL)
            
            embed.add_field(name = "암호화폐 이름", value = CRYPTO_KR_NAME, inline = True)
            embed.add_field(name = "현재 가격", value = CURRENT_CRYPTO_VALUE_KRW, inline = True)
            embed.add_field(name = "00시 기준 종가/저가/고가", value = CURRENT_CRYPTO_VALUE_OPENING_00h + " / " + CURRENT_CRYPTO_VALUE_MIN_00h + " / " + CURRENT_CRYPTO_VALUE_MAX_00h, inline = False)
            embed.add_field(name = "가격 변동량(24hr)", value = CURRENT_CRYPTO_KRW_CHANGE_24h + "( " + CURRENT_CRYPTO_PERCENT_CHANGE_24h + " " + CURRENT_CRYPTO_CHANGE_EMOJI + " )", inline = True)
            embed.add_field(name = "거래량(24hr)", value = CURRENT_CRYPTO_UNIT_TRADE_24h + "\n" + CURRENT_CRYPTO_KRW_TRADE_24h, inline = True)
            embed.add_field(name = "업데이트 시각", value = CURRENT_UPDATE_TIME, inline = "False")

            embed.set_footer(text="Lumibot | From {}({}) | Run Time : {} sec".format(ctx.message.author.name, ctx.author.display_name, _RUNNING_TIME), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "OK")    

        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show crypto --symbol {}".format(str(option[2])), "FAILED", "ILLEGAL_ARGUMENT_DETECTED")        

    elif option[0] == "crypto" and option[1] == "--brief":      # 암호화폐 시장 요약
        
        if len(option) == 2:
            allMarketCap, dayCryptoVolume, allCryptoQuantity, allCryptoExchanges, running_time = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyBrief(ctx.message.author.name)

            if allMarketCap == 404:     # 정보 받아오기 실패
                embed = discord.Embed(title = "No Response Exception", description = "현재 Coinranking 측에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show crypto --brief", "FAILED", "NO_RESPONSE_RETURNED")

            embed = discord.Embed(title = "전세계 암호화폐 시장 정보", description = "정보 제공 : 코인랭킹(coinranking.com)", timestamp=datetime.datetime.utcnow(), color = 0x126BFF)
            printCommandLog(ctx.author.name, "show crypto --brief", "RUNNING", "INIT_GET_INFO_PHASE") 

            embed.add_field(name = "전세계 암호화폐 시가총액", value = allMarketCap, inline = False)
            embed.add_field(name = "전세계 최근 1일간 거래량", value = dayCryptoVolume, inline = False)
            embed.add_field(name = "등록된 암호화폐 종류(개수)", value = allCryptoQuantity, inline = True)
            embed.add_field(name = "등록된 암호화폐 거래소", value = allCryptoExchanges, inline = True)
            embed.set_footer(text="Lumibot | From {}({}) | Run Time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)

            printCommandLog(ctx.author.name, "show crypto --brief", "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog(ctx.author.name, "show crypto --brief", "OK")

    elif option[0] == "stock" and option[1] == "--search":

        if len(option) == 3:
            # print(option)
            if COMMAND_SHOW_EX_.getStockInfo.getStockCode(str(option[2])) == 404:
                embed = discord.Embed(title = "No Listed Company", description = "현재 데이터베이스에 제대로 등록되지 않았거나,\n공식적으로 상장한 기업이 아닙니다. 입력값을 한번 더 확인해주세요.", timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "FAILED", "NO_LISTED_COMPANY_TRIAL")

            embed = discord.Embed(title = option[2] + " 주식 정보", description = "금융 정보 제공 : 다음 금융",  timestamp=datetime.datetime.utcnow(), color = 0xeaf27c)
            (symbolCode, companyName, tradePrice, changePrice, changeRate, marketCap, running_time) = COMMAND_SHOW_EX_.getStockInfo.getStockInfo(ctx.author.name, str(option[2]))

            if symbolCode == 404:
                embed = discord.Embed(title = "No Response Exception", description = "현재 금융 페이지에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "FAILED", "NO_RESPONSE_RETURNED")

            printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "RUNNING", "INIT_GET_INFO_PHASE")
            embed.add_field(name = "종목 코드", value = symbolCode + "(" + companyName + ")", inline = False)
            embed.add_field(name = "현재 주식 가격", value = tradePrice, inline = False)
            embed.add_field(name = "가격 변동(24hr)", value = changePrice + "(" + changeRate + ")", inline = False)
            embed.add_field(name = "시가 총액", value = marketCap, inline = False)
            embed.set_footer(text="Lumibot | From {}({}) | Run time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "RUNNING", "PASS_GET_INFO_PHASE")
            printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "OK")

        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show stock --search {}".format(str(option[2])), "FAILED", "ILLEGAL_ARGUMENT_DETECTED")
    
    elif option[0] == "currentTime":
            embed = discord.Embed(title = "Current Time", description = "", timestamp=datetime.datetime.utcnow(), color = 0x00e5a3)
            embed.add_field(name = "현재 시간은...", value = COMMAND_SHOW_EX_.getCurrentTime.getCurrentTime() + " 입니다.", inline = False)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "show currentTime", "OK")

    elif option[0] == "population":
        embed = discord.Embed(title = "현재 세계 인구", description = "countermeters 제공",  timestamp=datetime.datetime.utcnow(), color = 0xf0dbb7)
        printCommandLog(ctx.author.name, "show population", "RUNNING", "INIT_GET_INFO_PHASE")
        embed.add_field(name = "현재 세계 인구는...", value = COMMAND_SHOW_EX_.getWorldPopulation.getLiveWorldPopulation() + " 명 입니다.", inline = False)
        printCommandLog(ctx.author.name, "show population", "RUNNING", "PASS_GET_INFO_PHASE")
        embed.set_footer(text = "Lumibot / 업데이트 지연이 있을 수 있습니다.")
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "show population", "OK")

    else:
        embed = discord.Embed(title = "Option Not Found", description = "지원되지 않는 출력 요청입니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "show", "FAILED", "UNEXPECTED_INVALID_REQUEST")

# echo
@bot.command()
async def echo(ctx, *option):       # option이란 tuple 자료형이 메시지와 반복 횟수 모두 제공
    #print(option)
    #print(len(option))
  
    if len(option) == 1:
        # print(option[0])
        await ctx.send(option[0])
        printCommandLog(ctx.author.name, "echo {}".format(str(option[0])), "OK", "Echo Message : " + option[0])

    elif len(option) == 3 and option[1] == '--count':       # 동일 메시지를 여러번 출력할 수 있게 수정
        try:
            message = str(option[0])      # 메시지 내용
            #print(type(message))
            
            Repeat = int(option[2])       # 메시지를 반복해서 출력할 횟수
            #print(type(Repeat))

            if 1 <= Repeat <= 20:  # 20회 이상 동시 요청시 스팸으로 간주하고 요청 거부
                count = 1                    # 반복 변수 초기화
                while(count <= Repeat):
                    progress = "repeat : {} / count : {} of {}".format(message, count, Repeat)
                    printCommandLog(ctx.author.name, "echo {} --count {}".format(message, Repeat), "RUNNING", progress)
                    await ctx.send(message)
                    time.sleep(0.45)
                    count += 1
                printCommandLog(ctx.author.name, "echo {} --count {}".format(message, Repeat), "OK")
            else:                           # 정상적인 횟수 요청이 들어오지 않은 경우
                 embed = discord.Embed(title = "Request Overflow", description = "스패밍 방지를 위해, 반복 횟수는 20회 이하의 자연수로 설정해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                 embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                 await ctx.send(embed = embed)
                 printCommandLog(ctx.author.name, "echo {} --count {}".format(message, Repeat), "FAILED", "REQUEST_OVER_OR_UNDER_FLOW")

        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "echo {}".format(option), "FAILED", "EXCEPTION_OCCURED")
            
    else:
        embed = discord.Embed(title = "Argument Count Overflow", description = "인자가 너무 많습니다 | 형식 : $echo [메시지] [반복횟수(1~10)] ",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "echo {}".format(option), "FAILED", "TOO_MUCH_ARGUMENT")

# calculate # 계산기
@bot.command()
async def calculate(ctx, *option):
    embed = discord.Embed(title = "Calculate the expression", description = "계산 수행",  timestamp=datetime.datetime.utcnow(), color = 0xffcbd2)
    if len(option) > 1 and len(option) % 2 == 1:
        calcResult = COMMAND_CALCULATE_.calculator.calculator(option)
        # 에러 처리
        if calcResult in ['FILTERED', 'WRONG EXPRESSION']:
            embed = discord.Embed(title = "Argument Exception", description = '''
            입력값 형식이 올바르지 않습니다\n
            [입력값] [연산자] [입력값] ... 형식의 일반적인 형식을 지원하고 있습니다\n
            지원되는 연산자는 +, -, *, /, **, %, &, |, ^ 입니다.
            상세 에러 코드 : {}
            '''.format(calcResult),  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "calculate {}".format(option), "FAILED", "ERROR_OR_EXCEPTION_OCCURED... {}".format(calcResult))
        # 리스트의 형식이 아닌 실제 문자열의 형식으로 유저 input을 구체화
        actualUserInput = str(option).replace('\'','').replace(',','').replace(')','').replace('(','')
        embed.add_field(name = "calculate {}".format(actualUserInput), value = calcResult, inline = False)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "calculate {} = {}".format(actualUserInput, calcResult), "OK")
    else:
        embed = discord.Embed(title = "Argument Exception", description = '''
        입력값 형식이 올바르지 않습니다\n
        [입력값] [연산자] [입력값] 처럼 2n - 1 개의 입력값이 들어거야 합니다.
        ''',  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "calculate {}".format(option), "FAILED", "TO_LESS_ARGUMENT")

@bot.command()
async def random(ctx, *option):
    embed = discord.Embed(title = "Randomization", description = "무작위 추출",  timestamp=datetime.datetime.utcnow(), color = 0xf0dbb7)

    if option[0] == "--start" and option[2] == "--end":     # 주어진 범위 내 숫자 추출
        result = COMMAND_RANDOM_.randomToolBox.getRandomNumber(int(option[1]), int(option[3]))
                                             # 숫자 자료이므로 문자열로 변경해주기 - 안하면 출력안될수있음
        embed.add_field(name = "범위 내 난수 생성", value = "결과 : " + str(result), inline = False)
        printCommandLog(ctx.author.name, "random --start {} --end {}".format(str(option[1]), str(option[3])), "OK", str(result))

    elif option[0] == "--drawTheLotto":
        result = COMMAND_RANDOM_.randomToolBox.getLottoNumberPick()

        embed.add_field(name = "로또 번호 추첨", value = result, inline = False)
        printCommandLog(ctx.author.name, "random --drawTheLotto", "OK", str(result))

    elif option[0] == "--rollthedice":
        result = COMMAND_RANDOM_.randomToolBox.diceroll()
        embed.add_field(name = "주사위를 굴립니다... :game_die:", value = str(result) + " 이(가) 나왔습니다.", inline = False)
        printCommandLog(ctx.author.name, "random --rollthedice", "OK", str(result))

    elif option[0] == "--getAlphanumeric" and option[1] == "--length":
        try:
            if 1 <= int(option[2]) <= 256:
                result = COMMAND_RANDOM_.randomToolBox.getAlphanumeric(int(option[2]))
                embed.add_field(name = "Alphanumeric 타입의 난수를 생성합니다. ", value = "결과 : " + str(result), inline = False)
                printCommandLog(ctx.author.name, "random --getAlphanumeric32 --length {}".format(str(option[2])), "OK", result)
            else:
                embed = discord.Embed(title = "length overflow", description = "1이상 256이하의 자연수를 사용해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "random --getAlphanumeric --length {}".format(str(option[2])), "FAILED", "LENGTH_OVER_OR_UNDERFLOW")
        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "random --getAlphanumeric --length {}".format(str(option[2])), "FAILED", "EXCEPTION_OCCURED")

    elif option[0] == "--getHexadecimal" and option[1] == "--length":
        try:
            if 1 <= int(option[2]) <= 256:
                result = COMMAND_RANDOM_.randomToolBox.getHexadecimal(int(option[2]))
                printCommandLog(ctx.author.name, "random --getHexadecimal32 --length {}".format(str(option[1])), "OK", result)
                embed.add_field(name = "Hexadecimal 타입의 난수를 생성합니다. ", value = "결과 : " + str(result), inline = False)
            else:
                embed = discord.Embed(title = "length overflow", description = "1이상 256이하의 자연수를 사용해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog(ctx.author.name, "random --getHexadecimal --length {}".format(str(option[1])), "FAILED", "LENGTH_OVER_OR_UNDERFLOW")
        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog(ctx.author.name, "random --getHexadecimal --length {}".format(str(option[1])), "FAILED", "EXCEPTION_OCCURED")
   
    else:
        embed.add_field(name = "Illegal Argument", value = "제대로 지원되는 입력 형식이 아닙니다.", inline = False)
        printCommandLog(ctx.author.name, "random {}".format(option), "FAILED", "ILLEGAL_ARGUMENT")

    embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Command Not Found", description = "지원되지 않는 명령어입니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog(ctx.author.name, "{}".format(str(error).split()[1]), "FAILED", "NON_EXIST_COMMAND_INPUT... refer {}".format(error))
    	#await ctx.send("명령어를 찾지 못했습니다")
        
# ENTER_MY_OWN_DISCORD_BOT_TOKEN
bot.run(_DISCORD_BOT_TOKEN) #토큰
