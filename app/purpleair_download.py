import json
import requests
from csv import writer

token = 'b1cede462ae6739ef0536814b6440f0e1ae05b73'
link = 'https://api.waqi.info/feed/'

# Load station id of PurpleAir
stations = ['A230398', 'A230383', 'A230626', 'A230443', 'A231934', 'A364435', 'A358570', 'A06487']

# Request data for all stations in the list
for s in stations:
    station = s
    url = link + station +'/?token=' + token
    response = requests.get(url)
    data = json.loads(response.text)
    # Load data from json file
    time = data['data']['time']['s']
    pm25 = data['data']['iaqi']['pm25']['v']
    pm10 = data['data']['iaqi']['pm10']['v']
    h = data['data']['iaqi']['h']['v']
    t = data['data']['iaqi']['t']['v']
    List = [time, station, pm25, pm10, h, t]
    with open('purpleair.csv', 'a') as f:
        filewriter = writer(f)
        filewriter.writerow(List)
    f.close()
