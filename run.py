import asyncio, discord
import time
import datetime
from discord.ext import commands

import os #, sys

############################# 직접 만든 모듈 ##################################

import COMMAND_SHOW_EX_.getCryptocurrencyInfo       # 암호화폐 정보
import COMMAND_SHOW_EX_.getStockInfo                # 주식 정보
import COMMAND_SHOW_EX_.getCurrentTime              # 현재 시간 정보
import COMMAND_SHOW_EX_.getWorldPopulation          # 인구 정보

import COMMAND_RANDOM_.randomToolBox        # 난수 관련
import COMMAND_CALCULATE_.calculator        # 계산기 역할을 하는 다양한 모듈들

from resource.sub_function_used_globally.printCommandLog import printCommandLog as printCommandLog  # 각종 시스템 로그 출력하기

###############################################################################

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("We have loggedd in as {0.user}".format(bot))
    # embed = discord.Embed(title = "Turned To Online :white_check_mark:", description = "Lumibot이 온라인 상태가 되었습니다.", color = 0xffd9ea)
    # embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
    # await ctx.send(embed = embed)
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="enter [$show help] to get info"))
    printCommandLog("START THE BOT", "OK")

# show [옵션1]
@bot.command()
async def show(ctx, *option):                   
    if option[0] == "hello":                  # hello | 간단한 인사말 출력
        embed = discord.Embed(title = "hello", description = "만나서 반갑습니다!", timestamp=datetime.datetime.utcnow(), color = 0x3eb489)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("show hello", "OK")

    elif option[0] == "help":                 # help | 도움말 출력
        embed = discord.Embed(title = "command help", description = "봇 정보",  timestamp=datetime.datetime.utcnow(), color = 0x6a5acd)
        embed.add_field(name = "```show``` 계열 명령어", value = 
                '''
                인사```show hello```
                도움말```show help```
                봇 정보```show info``` 
                현재 세계 인구 통계```show population```
                현재 시간 보기```show currentTime```
                국내 주식 시세 검색(다음 금융 제공)```show stock --search [국내 주식 종목명(이름)]```
                암호화폐 시세 검색(빗썸 제공)```show crypto --symbol [암호화폐 기호(ex. BTC)]```
                암호화폐 통계 요약(전세계/코인랭킹 제공)```show crypto --brief```
                ''', inline = False)
        embed.add_field(name = "```echo``` 계열 명령어", value = 
                '''
                입력값 그대로 출력하기(따라하기)```echo [입력값] --count [횟수(1~20)]```
                ''', inline = False)
        embed.add_field(name = "```calculate``` 계열 명령어", value = 
                '''
                간단한 수식 계산(사칙연산/나머지/비트논리연산)```calculate [숫자] [+|-|*|/|**(거듭제곱)|%(나머지)|&,AND,and||,OR,or|^,XOR,xor] [숫자]```
                ''', inline = False)
        embed.add_field(name = "```random``` 계열 명령어", value = 
                '''
                지정한 범위 내에서 랜덤 숫자 출력하기```random --start [시작숫자] --end [끝 숫자]```
                주사위 굴리기(1 ~ 6)```random --rollthedice```
                영숫자 혼합 난수 생성하기```random --getAlphanumeric --length [길이(1~256)]```
                16진수 난수 생성하기```random --getHexadecimal --length [길이(1~256)]```
                ''', inline = False)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("show help", "OK")

    elif option[0] == "info":                 # info | 봇 정보 출력   
        embed = discord.Embed(title = "information", description = "봇 정보",  timestamp=datetime.datetime.utcnow(), color = 0x32cd32)
        embed.add_field(name = "개발 언어", value = "PYTHON", inline = False)
        embed.add_field(name = "개발자", value = "Garam Lee", inline = True)
        embed.set_image(url="https://i.imgur.com/w1pAySc.jpg")
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("show info", "OK")

    elif option[0] == "crypto" and option[1] == "--symbol":

        if len(option) == 3:
            # print(option)
            if COMMAND_SHOW_EX_.getCryptocurrencyInfo.getNameFromCryptoSymbol(str(option[2])) == 404:
                embed = discord.Embed(title = "No Listed Cryptocurrency", description = "현재 데이터베이스에 제대로 등록되지 않았거나,\n 입력값이 잘못된 것 같습니다(Bithumb 거래소 기준).\n 입력값을 한번 더 확인해주세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("show crypto --symbol", "FAILED", "NO_LISTED_CRYPTO_TRIAL")

            #(cryptocurrency_KRname, cryptocurrency_to_KRW, cryptocurrency_change_KRW, cryptocurrency_change_PERCENT, cryptocurrency_transaction_KRW, cryptocurrency_transaction_CRYPTO, running_time) = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyInfo(str(option[2]))
            CRYPTO_KR_NAME, CURRENT_CRYPTO_VALUE_KRW, CURRENT_CRYPTO_VALUE_OPENING_00h, CURRENT_CRYPTO_VALUE_MIN_00h, CURRENT_CRYPTO_VALUE_MAX_00h, CURRENT_CRYPTO_UNIT_TRADE_24h, CURRENT_CRYPTO_KRW_TRADE_24h, CURRENT_CRYPTO_KRW_CHANGE_24h, CURRENT_CRYPTO_PERCENT_CHANGE_24h, CURRENT_UPDATE_TIME, _RUNNING_TIME, CURRENT_CRYPTO_CHANGE_EMOJI, CRYPTO_PICTURE_URL = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyInfo(str(option[2]))
            if CRYPTO_KR_NAME == 404:
                embed = discord.Embed(title = "No Response Exception", description = "현재 거래소에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("show crypto --symbol", "FAILED", "NO_RESPONSE_RETURNED")

            # 진짜 암호화폐 정보
            embed = discord.Embed(title = option[2] + " 암호화폐 정보", description = "정보 제공 : 빗썸(bithumb.com)", timestamp=datetime.datetime.utcnow(), color = 0xeaf27c)
            printCommandLog("show crypto --symbol", "RUNNING", "INIT_GET_INFO_PHASE")

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
            printCommandLog("show crypto --symbol", "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog("show crypto --symbol", "OK")    

        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("show crypto --symbol", "FAILED", "ILLEGAL_ARGUMENT_DETECTED")        

    elif option[0] == "crypto" and option[1] == "--brief":      # 암호화폐 시장 요약
        
        if len(option) == 2:
            allMarketCap, dayCryptoVolume, allCryptoQuantity, allCryptoExchanges, running_time = COMMAND_SHOW_EX_.getCryptocurrencyInfo.getCryptocurrencyBrief()

            if allMarketCap == 404:     # 정보 받아오기 실패
                embed = discord.Embed(title = "No Response Exception", description = "현재 Coinranking 측에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("show crypto --brief", "FAILED", "NO_RESPONSE_RETURNED")

            embed = discord.Embed(title = "전세계 암호화폐 시장 정보", description = "정보 제공 : 코인랭킹(coinranking.com)", timestamp=datetime.datetime.utcnow(), color = 0x126BFF)
            printCommandLog("show crypto --brief", "RUNNING", "INIT_GET_INFO_PHASE") 

            embed.add_field(name = "전세계 암호화폐 시가총액", value = allMarketCap, inline = False)
            embed.add_field(name = "전세계 최근 1일간 거래량", value = dayCryptoVolume, inline = False)
            embed.add_field(name = "등록된 암호화폐 종류(개수)", value = allCryptoQuantity, inline = True)
            embed.add_field(name = "등록된 암호화폐 거래소", value = allCryptoExchanges, inline = True)
            embed.set_footer(text="Lumibot | From {}({}) | Run Time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)

            printCommandLog("show crypto --brief", "RUNNING", "FIN_GET_INFO_PHASE")   
            printCommandLog("show crypto --brief", "OK")

    
    elif option[0] == "stock" and option[1] == "--search":

        if len(option) == 3:
            # print(option)
            if COMMAND_SHOW_EX_.getStockInfo.getStockCode(str(option[2])) == 404:
                embed = discord.Embed(title = "No Listed Company", description = "현재 데이터베이스에 제대로 등록되지 않았거나,\n공식적으로 상장한 기업이 아닙니다. 입력값을 한번 더 확인해주세요.", timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("show stock --search", "FAILED", "NO_LISTED_COMPANY_TRIAL")
            embed = discord.Embed(title = option[2] + " 주식 정보", description = "금융 정보 제공 : 다음 금융",  timestamp=datetime.datetime.utcnow(), color = 0xeaf27c)
            (symbolCode, companyName, tradePrice, changePrice, changeRate, marketCap, running_time) = COMMAND_SHOW_EX_.getStockInfo.getStockInfo(str(option[2]))
            if symbolCode == 404:
                embed = discord.Embed(title = "No Response Exception", description = "현재 금융 페이지에서 응답이 Timeout 내에 돌아오지 않고 있습니다.\n요청을 단기간에 과도하게 보내지 마시고, 잠시 후 다시 시도하세요.", color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("show stock --search", "FAILED", "NO_RESPONSE_RETURNED")

            printCommandLog("show stock", "RUNNING", "INIT_GET_INFO_PHASE")
            embed.add_field(name = "종목 코드", value = symbolCode + "(" + companyName + ")", inline = False)
            embed.add_field(name = "현재 주식 가격", value = tradePrice, inline = False)
            embed.add_field(name = "가격 변동(24hr)", value = changePrice + "(" + changeRate + ")", inline = False)
            embed.add_field(name = "시가 총액", value = marketCap, inline = False)
            embed.set_footer(text="Lumibot | From {}({}) | Run time : {} sec".format(ctx.message.author.name, ctx.author.display_name, running_time), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("show stock --search", "RUNNING", "PASS_GET_INFO_PHASE")
            printCommandLog("show stock --search", "OK")

        else:
            embed = discord.Embed(title = "Illegal Argument", description = "제대로 지원되는 입력 형식이 아닙니다.",  timestamp=datetime.datetime.utcnow(),  color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("stock --search", "FAILED", "ILLEGAL_ARGUMENT_DETECTED")
    
    elif option[0] == "currentTime":
            embed = discord.Embed(title = "Current Time", description = "", timestamp=datetime.datetime.utcnow(), color = 0x00e5a3)
            embed.add_field(name = "현재 시간은...", value = COMMAND_SHOW_EX_.getCurrentTime.getCurrentTime() + " 입니다.", inline = False)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("show currentTime", "OK")

    elif option[0] == "population":
        embed = discord.Embed(title = "현재 세계 인구", description = "countermeters 제공",  timestamp=datetime.datetime.utcnow(), color = 0xf0dbb7)
        printCommandLog("show population", "RUNNING", "INIT_GET_INFO_PHASE")
        embed.add_field(name = "현재 세계 인구는...", value = COMMAND_SHOW_EX_.getWorldPopulation.getLiveWorldPopulation() + " 명 입니다.", inline = False)
        printCommandLog("show population", "RUNNING", "PASS_GET_INFO_PHASE")
        embed.set_footer(text = "Lumibot / 업데이트 지연이 있을 수 있습니다.")
        await ctx.send(embed = embed)
        printCommandLog("show population", "OK")

    else:
        embed = discord.Embed(title = "Option Not Found", description = "지원되지 않는 출력 요청입니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("show", "FAILED", "UNEXPECTED_INVALID_REQUEST")

# echo
@bot.command()
async def echo(ctx, *option):       # option이란 tuple 자료형이 메시지와 반복 횟수 모두 제공
    #print(option)
    #print(len(option))
  
    if len(option) == 1:
        # print(option[0])
        await ctx.send(option[0])
        printCommandLog("echo (single)", "OK", "Echo Message : " + option[0])

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
                    printCommandLog("echo (multiple)", "RUNNING", progress)
                    await ctx.send(message)
                    time.sleep(0.45)
                    count += 1
                printCommandLog("echo (multiple)", "OK")
            else:                           # 정상적인 횟수 요청이 들어오지 않은 경우
                 embed = discord.Embed(title = "Request Overflow", description = "스패밍 방지를 위해, 반복 횟수는 20회 이하의 자연수로 설정해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                 embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                 await ctx.send(embed = embed)
                 printCommandLog("echo", "FAILED", "REQUEST_OVER_OR_UNDER_FLOW")

        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("echo", "FAILED", "EXCEPTION_OCCURED")
            
    else:
        embed = discord.Embed(title = "Argument Count Overflow", description = "인자가 너무 많습니다 | 형식 : $echo [메시지] [반복횟수(1~10)] ",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("echo", "FAILED", "TOO_MUCH_ARGUMENT")

# calculate # 계산기
@bot.command()
async def calculate(ctx, *option):
    embed = discord.Embed(title = "Calculate the expression", description = "계산 수행",  timestamp=datetime.datetime.utcnow(), color = 0xffcbd2)
    if len(option) == 3:
        if option[1] == "+":
            calcResult = COMMAND_CALCULATE_.calculator.addition(int(option[0]), int(option[2]))
        elif option[1] == "-":
            calcResult = COMMAND_CALCULATE_.calculator.subtraction(int(option[0]), int(option[2]))
        elif option[1] == "*":
            calcResult = COMMAND_CALCULATE_.calculator.multiplication(int(option[0]), int(option[2]))
        elif option[1] == "/":
            calcResult = COMMAND_CALCULATE_.calculator.division(int(option[0]), int(option[2]))
        elif option[1] == "**":
            calcResult = COMMAND_CALCULATE_.calculator.power(int(option[0]), int(option[2]))
        elif option[1] == "%":
            calcResult = COMMAND_CALCULATE_.calculator.modular(int(option[0]), int(option[2]))
        elif option[1] == "&" or option[1] == "AND" or option[1] == "and":
            calcResult = COMMAND_CALCULATE_.calculator.bitAND(int(option[0]), int(option[2]))
        elif option[1] == "|" or option[1] == "OR" or option[1] == "or":
            calcResult = COMMAND_CALCULATE_.calculator.bitOR(int(option[0]), int(option[2]))
        elif option[1] == "^" or option[1] == "XOR" or option[1] == "xor":
            calcResult = COMMAND_CALCULATE_.calculator.bitXOR(int(option[0]), int(option[2]))
        else:
            embed.add_field(name = "Exception Occured", value = "값을 점검해주세요.", inline = False)
            printCommandLog("calculate", "FAILED", "EXCEPTION_OCCURED")
        embed.add_field(name = option[0] + " " + option[1] + " " + option[2] + " " + "= ", value = calcResult, inline = False)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("calculate", "OK")
    else:
        embed = discord.Embed(title = "Argument Overflow", description = "입력값이 너무 많거나 적습니다. | 형식 : [숫자1] [연산자] [숫자2]",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("calculate", "FAILED", "TOO_MUCH_LESS_ARGUMENT")

@bot.command()
async def random(ctx, *option):
    embed = discord.Embed(title = "Randomization", description = "무작위 추출",  timestamp=datetime.datetime.utcnow(), color = 0xf0dbb7)

    if option[0] == "--start" and option[2] == "--end":     # 주어진 범위 내 숫자 추출
        result = COMMAND_RANDOM_.randomToolBox.getRandomNumber(int(option[1]), int(option[3]))
                                             # 숫자 자료이므로 문자열로 변경해주기 - 안하면 출력안될수있음
        embed.add_field(name = "범위 내 난수 생성", value = "결과 : " + str(result), inline = False)
        printCommandLog("random (--getRandomNumber)", "OK", str(result))

    elif option[0] == "--rollthedice":
        result = COMMAND_RANDOM_.randomToolBox.diceroll()
        embed.add_field(name = "주사위를 굴립니다... :game_die:", value = str(result) + " 이(가) 나왔습니다.", inline = False)
        printCommandLog("random --rollthedice", "OK", str(result))

    elif option[0] == "--getAlphanumeric" and option[1] == "--length":
        try:
            if 1 <= int(option[2]) <= 256:
                result = COMMAND_RANDOM_.randomToolBox.getAlphanumeric(int(option[2]))
                embed.add_field(name = "Alphanumeric 타입의 난수를 생성합니다. ", value = "결과 : " + str(result), inline = False)
                printCommandLog("random --getAlphanumeric32", "OK", result)
            else:
                embed = discord.Embed(title = "length overflow", description = "1이상 256이하의 자연수를 사용해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("random --getAlphanumeric", "FAILED", "LENGTH_OVER_OR_UNDERFLOW")
        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("random --getAlphanumeric", "FAILED", "EXCEPTION_OCCURED")

    elif option[0] == "--getHexadecimal" and option[1] == "--length":
        try:
            if 1 <= int(option[2]) <= 256:
                result = COMMAND_RANDOM_.randomToolBox.getHexadecimal(int(option[2]))
                printCommandLog("random --getHexadecimal32", "OK", result)
                embed.add_field(name = "Hexadecimal 타입의 난수를 생성합니다. ", value = "결과 : " + str(result), inline = False)
            else:
                embed = discord.Embed(title = "length overflow", description = "1이상 256이하의 자연수를 사용해주세요.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
                embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
                printCommandLog("random --getHexadecimal", "FAILED", "LENGTH_OVER_OR_UNDERFLOW")
        except:
            embed = discord.Embed(title = "Exception Occured", description = "예외가 발생했습니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
            embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            printCommandLog("random --getHexadecimal", "FAILED", "EXCEPTION_OCCURED")
   
    else:
        embed.add_field(name = "Illegal Argument", value = "제대로 지원되는 입력 형식이 아닙니다.", inline = False)
        printCommandLog("random", "FAILED", "ILLEGAL_ARGUMENT")

    embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Command Not Found", description = "지원되지 않는 명령어입니다.",  timestamp=datetime.datetime.utcnow(), color = 0xff0000)
        embed.set_footer(text="Lumibot | From {}({})".format(ctx.message.author.name, ctx.author.display_name), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        printCommandLog("NaN", "FAILED", "NON_EXIST_COMMAND_INPUT")
    	#await ctx.send("명령어를 찾지 못했습니다")
        
# ENTER_MY_OWN_DISCORD_BOT_TOKEN
bot.run('# ENTER_MY_OWN_DISCORD_BOT_TOKEN') #토큰
