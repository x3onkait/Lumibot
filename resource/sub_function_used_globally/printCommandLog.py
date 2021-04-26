# 로그 메시지가 입력되면 정해진 시간 포맷과 함께 메시지가 같이 정렬되어 출력된다.
# 로그를 보다 보기 좋게 하기 위함

from datetime import datetime

                    # fromWho : (미구현) 누가 명령을 실행했는지에 대한 정보
                    # command : 실행한 명령어
                    # status : 실행한 명령어의 결과(상태)
                    # message : 메시지
def printCommandLog(fromWho, command, status, *message):
    CURRENT_TIME = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    FROMWHO = str(fromWho)
    COMMAND = "%s" % command         # 정렬
    STATUS = "%s" % status           # 정렬
    LOG_MESSAGE = "[ " + CURRENT_TIME + " ] : " + "@" + FROMWHO + " --> " + " COMMAND = " + COMMAND + " | STATUS = " + STATUS
    print(LOG_MESSAGE)

    if message:
        MESSAGE = " ┖ " + str(message[0])
        print(MESSAGE)
    
    print()

    # return LOG_MESSAGE

# printCommandLog("TEST#1234", "short command", "OK", "test123")
# printCommandLog("TEST#1234", "longlonglonglonglonglonglonglong command", "OK", "test123")
# printCommandLog("ASDF#0000", "show hello", "OK")
