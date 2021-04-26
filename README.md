# Lumibot@Python

평범한 학생이 **Python**을 사용해 간단하게 만들어본 다목적 디스코드 채팅봇입니다.

처음 시작할 때는 별다른 목적 없이 그저 즐거움, 재미 정도의 목적으로만 활용했으나,

하나하나 구현해고픈 기능이 있어서 차곡차곡 기능을 _심심할 때만_  구현하고 있습니다.

개인 블로그 : [https://blog.naver.com/agerio100](blog)

<hr/> 

###### 제공하는 기능들 > 명령어

- show : 인사하기 / 도움말 /봇 정보
- show population : 실시간 세계인구 통계
- show currentTime : 현재 시간을 년/월/일/시(24hr)/분/초 단위로 보기
- show stock --search [종목] : 국내 주식 종목 확인(다음 금융)
- show crypto --brief : 전세계 암호화폐 시장 현환 요약 정리(시가총액이나 24h volume)
- show crypto --search [암호화폐 심볼(ex. BTC/ETH)] : 암호화폐 시세 검색(빗썸)
- calculate [피연산자1] [연산자] [피연산자2] : 연산자를 중심으로 한 간단한 연산 수행. 사칙연산, 나머지, 거듭제곱, bit단위 논리 연산을 포함합니다.
- random --start [시작 숫자] --end [끝 숫자] : 시작 숫자 ~ 끝 숫자 사이에서 랜덤 수 하나 출력
- random --rollthedice : 주사위 굴리기(1 ~ 6 면을 반환함)
- random --getAlphanumeric --length [길이(1 ~ 256)] : 정해진 길이만큼의 영숫자 혼합 난수 생성
- random --getHexadecimal --length [길이(1 ~ 256)] : 정해진 길이만큼의 16진수 난수 생성



<hr/>

###### 로그

> 언제 어떤 명령이 실행되는지를 터미널 창에 간략하게 보여줍니다. 아래는 예시입니다.

```
We have loggedd in as Lumibot#1512
[ 2021-04-26 02:11:29.171 ] >  COMMAND = START THE BOT                  STATUS = OK

[ 2021-04-26 02:17:18.860 ] >  COMMAND = show crypto --brief(Function)  STATUS = RUNNING
 ┖ Getting Brief Information

[ 2021-04-26 02:17:18.912 ] >  COMMAND = show crypto --brief(Function)  STATUS = RUNNING
 ┖ running time : 1.412 sec/pass

[ 2021-04-26 02:17:18.913 ] >  COMMAND = show crypto --brief            STATUS = RUNNING
 ┖ INIT_GET_INFO_PHASE

[ 2021-04-26 02:17:19.182 ] >  COMMAND = show crypto --brief            STATUS = RUNNING
 ┖ FIN_GET_INFO_PHASE

[ 2021-04-26 02:17:19.182 ] >  COMMAND = show crypto --brief            STATUS = OK
```

<hr/>

