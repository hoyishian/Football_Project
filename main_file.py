from bs4 import BeautifulSoup
import requests
import pandas as pd


headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.us/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/plus/1"

pageTree = requests.get(url, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

table1 = pageSoup.find("table", attrs = {"class" : "items"})
table_header = table1.thead.find_all("tr")



headings = []
for th in table_header[0].find_all("th"):
    headings.append(th.text.replace('\n', ' ').strip())

data = []
table_data = table1.tbody.find_all("tr")
for tr in table_data:
    t_row = {}
    for td, th in zip(tr.find_all("td"), headings):
        t_row[th] = td.text.replace('\n', '').strip()
    data.append(t_row)


print(data)


# print(headings)
# PlayerList = []
# ValuesList = []



