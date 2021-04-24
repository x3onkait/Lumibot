import random
import string

def getRandomNumber(starter, ender):
    print(starter)
    print(ender)
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

# a = "10"
# b = "80"

# print(getRandomNumber(int(a), int(b)))