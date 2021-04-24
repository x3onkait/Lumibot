import json

with open('./resource/cryptocurrencyBithumbList.txt','rt', encoding='UTF8') as cryptoList:
    result = cryptoList
    select = result["C0125"]
    print(select)

# while True:
#     line = file.readline()
#     if not line:
#         break
#     result = line.split('\t')[0].strip()
#     print(result)

