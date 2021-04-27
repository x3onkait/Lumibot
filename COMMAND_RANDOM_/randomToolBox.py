import random
import string

def getRandomNumber(starter, ender):
    #print(starter)
    #print(ender)
    return random.randrange(starter, ender)

def diceroll():
    selection = ['1', '2', '3', '4', '5', '6']
    return random.choice(selection)

def getAlphanumeric(length):
    string_pool = string.ascii_letters + string.digits

    result=""
    for _i in range(length):
        result += random.choice(string_pool)
    return result

def getHexadecimal(length):
    string_pool = '1234567890ABCDEF'

    result=""
    for _i in range(length):
        result += random.choice(string_pool)
    return result

def getLottoNumberPick():
    result_pool = random.sample(range(1, 45 + 1), 7)
    result_string = ""

    for i in range(0, 6 + 1):
        if i == 6:
            result_string += " + "
        result_string += ("**" + str(result_pool[i]) + "**")            # for highlight(bold style) in Discord
        if i < 5:
            result_string += " | "

    return result_string

# a = "10"
# b = "80"

# print(getRandomNumber(int(a), int(b)))
# print(getLottoNumberPick())