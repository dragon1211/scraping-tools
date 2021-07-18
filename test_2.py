import requests
from bs4 import BeautifulSoup as bs
URL = ['https://www.geeksforgeeks.org','https://www.geeksforgeeks.org/page/10/']
  
for url in range(0,2):
    req = requests.get(URL[url])
    soup = bs(req.text, 'html.parser')
  
    titles = soup.find_all('div',attrs={'class','head'})
    for i in range(4, 19):
        if url+1  > 1:
            print(f"{(i - 3) + url * 15}" + titles[i].text)
        else:
            print(f"{i - 3}" + titles[i].text)