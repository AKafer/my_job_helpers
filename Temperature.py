import requests
from bs4 import BeautifulSoup
import pandas as pd
GOROD = {'Амурская область' : '4848', 'Приморский край' : '4877', 'Хабаровский край' : '4862', 'Якутия' : '4039',
        'Магаданская область' : '4063', 'Чукотский АО' : '4054', 'Сахалинская область' : '4894', 'Камчатка' : '4907'}
Year = '2021'
Month = '11'
dict_temp = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
headers = {'user-agent': 'my-app/0.0.1'}
y = 1
for key, value in GOROD.items():
    url = 'https://www.gismeteo.ru/diary/{}/{}/{}/'.format(value, Year , Month)
    r = requests.get(url, headers = headers, verify = False)
    soup = BeautifulSoup(r.text, 'lxml')
    print(y, soup.find_all('title')[0].text)
    print()
    y = y + 1
    temp = soup.find_all('td', {'class' : 'first_in_group'})
    i = 0
    L = []
    for t in temp :
        if i%2 == 0 :
            L.append((t.text))
        i = i + 1
    dlina = 31 - len(L)    
    for n in range(dlina):
        L.append('300') 
    dict_temp[key] = L
DataTemp = pd.DataFrame(dict_temp, index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
DataTemp1 = DataTemp.T
DataTemp1.to_excel('База-{}.{}.xls'.format(Month, Year))
DataTemp1