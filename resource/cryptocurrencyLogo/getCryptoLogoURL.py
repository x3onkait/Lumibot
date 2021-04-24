file = open('./resource/cryptocurrencyLogo/cryptologocclogo_html.txt', 'r')     # 따로 copy한 파일
myFile = open('./resource/cryptocurrencyLogo/cryptoLogoURL.txt', 'w')

while True:
    line = file.readline()
    if ".PNG transparent file download" in line:

        url = line.split()[2].strip('href=').strip('\'').strip('\'>')       # 다운로드 받을 URL 추출
        filename = url.strip('https://cryptologos.cc/logos/').strip('.png?v=002').split('-')[-2].upper()
        
        result = "{}   {}\n".format(url, filename)
        myFile.write(result)

    if not line:
        break

myFile.close()