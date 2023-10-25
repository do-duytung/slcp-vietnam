from bs4 import BeautifulSoup as soup
import urllib.request as ul
from csv import writer
import pandas as pd
import os

PATH = '/home/ec2-user/'
df = pd.read_csv(PATH + 'metstations_list.csv')
for i in range(len(df)):
    station = df.iloc[i,0]
    link = df.iloc[i,1]
    req = ul.Request(link, headers={'User-Agent':'Mozilla/5.0'})
    client = ul.urlopen(req)
    htmldata = client.read()
    
    pagesoup = soup(htmldata, "html.parser")
    tstamp = pagesoup.find('div', {"class":"time-update"}).text
    items = pagesoup.find('ul', {"class":"list-info-wt"})
    List = [tstamp, station]
    for ii in items.find_all('div', {"class":"uk-width-3-4"}):
        value = ii.text.strip(' :')
        List.append(value)

    filename = "KTTV.csv"
    headers = "Tstamp, Station, Temp, Weather, Humidity, Wind\n"
    if not os.path.isfile(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(headers)    
    with open(filename, "a", newline='', encoding="utf-8") as f:    
        writer_obj = writer(f)
        writer_obj.writerow(List)

    client.close()
