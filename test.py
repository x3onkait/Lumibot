import requests

url = "https://api.upbit.com/v1/ticker"

response = requests.request("GET", url)

print(response.text)