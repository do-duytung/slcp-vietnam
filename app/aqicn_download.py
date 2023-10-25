import pytz
import datetime
import os
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup as soup
import urllib.request as ul
from csv import writer

token = 'b1cede462ae6739ef0536814b6440f0e1ae05b73'
link = 'https://api.waqi.info/feed/'
# station = 'A231934'
PATH = '/home/ec2-user/'
# Load station id from csv
stations = pd.read_csv(PATH + 'stations_list.csv')
output = 'aqicn_data.csv'

# Request data for all OK stations in the list
for i in range(len(stations)-4):
    station = stations.iloc[i,0]
    id = stations.iloc[i,1]
    url = link + id +'/?token=' + token
    response = requests.get(url)
    data = json.loads(response.text)
    # Load data from json file
    
    tstamp = data['data']['time']['s']
    List = [tstamp,station,id]
    iaqi = ['pm25', 'o3', 'no2', 'so2', 'co', 't', 'p', 'h', 'w']
    for i in iaqi:
        if i in data['data']['iaqi']:
            i = data['data']['iaqi'][i]['v']
        else:
            i = 'NA'
        List.append(i)
    
    with open(output, 'a') as f:
        filewriter = writer(f)
        filewriter.writerow(List)
    f.close()

# Scrape data of the last 4 stations
def scraping():
    pagesoup = soup(htmldata, "html.parser")
    HAN = pytz.timezone('Asia/Saigon')
    tstamp = datetime.datetime.now(HAN)
    #itemlocator = pagesoup.findAll('div uk-grid', {"class":"uk-grid"})
    pm25 = getattr(pagesoup.find('td', {"id":"cur_pm25"}), 'text', 'NA')
    o3 = getattr(pagesoup.find('td', {"id":"cur_o3"}), 'text', 'NA')
    no2 = getattr(pagesoup.find('td', {"id":"cur_no2"}), 'text', 'NA')
    so2 = getattr(pagesoup.find('td', {"id":"cur_so2"}), 'text', 'NA')
    co = getattr(pagesoup.find('td', {"id":"cur_co"}), 'text', 'NA')
    t = getattr(pagesoup.find('td', {"id":"cur_t"}), 'text', 'NA')
    p = getattr(pagesoup.find('td', {"id":"cur_p"}), 'text', 'NA')
    h = getattr(pagesoup.find('td', {"id":"cur_h"}), 'text', 'NA')
    w = getattr(pagesoup.find('td', {"id":"cur_w"}), 'text', 'NA')
    
    List = [tstamp,station,id,pm25,o3,no2,so2,co,t,p,h,w]
       
    headers = "Tstamp, Station, PM25, Ozone, NO2, SO2, CO, Temp, Pressure, Humidity, Windspeed\n"
    if not os.path.isfile(output):
        with open(output, "w", encoding="utf-8") as f:
            f.write(headers)
    
    with open(output, "a", newline='', encoding="utf-8") as f:    
        writer_obj = writer(f)
        writer_obj.writerow(List)   
    return List

for i in range(len(stations)-4,len(stations)):
    station = stations.iloc[i,0]
    link = stations.iloc[i,2]
    id = stations.iloc[i,1]
    req = ul.Request(link, headers={'User-Agent':'Mozilla/5.0'})
    client = ul.urlopen(req)
    htmldata = client.read()
    client.close()
    scraping()
