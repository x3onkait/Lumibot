def calculator(userInput):

    
    calcInput = list(userInput)
    # print(calcInput)

    # 필터링 리스트 
    allowList = ['+', '-', '*', '/', '**', '%', '&', '|', '^', '(', ')', '.']

    # 입력값 검증!
    try:
        for sequence in range(0, len(calcInput) - 1):
            if calcInput[sequence] in allowList or isNumber(calcInput[sequence]) == True:
                pass
            else:
                return "FILTERED"
            
        calcInput = ' '.join(calcInput)
        return eval(calcInput)
    except:
        return "WRONG EXPRESSION"

def isNumber(trial):            # 숫자(정수, 실수인지 판단하기)
    try:
        float(trial)
        return True             # num을 float으로 변환할 수 있는 경우
    except ValueError:          # num을 float으로 변환할 수 없는 경우
        return False

# userInput = input("insert the expression > ")
# print(calculator(('2.1', '+', '3')))