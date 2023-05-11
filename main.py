import logging
import logging.handlers
import os

import pandas as pd
import requests
import json
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_filer_handler = logging.handlers.RotatingFileHandler(
  "status.log",
  maxBytes=1024*1024,
  backupCount=1,
  encoding="utf8",
)

link = 'https://api.waqi.info/feed/'
# An example station id = 'A230398'
try:
  token = os.environ["MY_AQICN"]
except KeyError:
  token = "Token not available"

ids = ['A230398', 'A230383', 'A230626', 'A230443', 'A231934', 'A364435', 'A358570', 'A06487']
def scraping():
  for i in ids:
    id = i
    url = link + id +'/?token=' + token
    response = requests.get(url)
    data = json.loads(response.text)
    time = data['data']['time']['s']
    aqi = data['data']['aqi']
    List = [time, id, aqi]
    with open('purpleair.csv', 'a') as f:
      writer = csv.writer(f)
      writer.writerow(List)
    print(List)
