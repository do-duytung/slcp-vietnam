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
PATH = '/home/ubuntu/projects/slcp-vietnam/data/'
# Load station id from csv
stations = pd.read_csv(PATH + 'stations_list.csv')
output = PATH + 'aqicn_data.csv'

# Request data for all OK stations in the list
for i in range(len(stations)):
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
