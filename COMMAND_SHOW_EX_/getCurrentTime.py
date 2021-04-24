from datetime import datetime

def getCurrentTime():
    now = datetime.now()
    result = "%04d년 %02d월 %02d일 %02d시 %02d분 %02d초" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    return result