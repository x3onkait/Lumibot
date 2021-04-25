# 로그 메시지가 입력되면 정해진 시간 포맷과 함께 메시지가 같이 정렬되어 출력된다.
# 로그를 보다 보기 좋게 하기 위함

from datetime import datetime

                    # command : 실행한 명령어
                    # status : 실행한 명령어의 결과(상태)
                    # message : 메시지
                    # fromWho : (미구현) 누가 명령을 실행했는지에 대한 정보
def printCommandLog(command, status, *message):
    CURRENT_TIME = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    COMMAND = "%-30s" % command         # 정렬
    STATUS = "%-25s" % status           # 정렬
    LOG_MESSAGE = "[ " + CURRENT_TIME + " ] > " + " COMMAND = " + COMMAND + "\tSTATUS = " + STATUS
    print(LOG_MESSAGE)

    if message:
        MESSAGE = " ┖ " + str(message[0])
        print(MESSAGE)
    
    print()

    # return LOG_MESSAGE

# printCommandLog("show hello", "OK", "test123")
# printCommandLog("show hello", "OK")
