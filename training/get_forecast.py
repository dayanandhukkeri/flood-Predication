import csv
import datetime
import pickle
import requests

def get_data(lat, lon):
    
    
    k = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations=" + str(lat) + "%2C%20" + str(lon) + "&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType=json&key=DK3R39R6VYS25DZXNXWZGCHTY"
    x = requests.get(k).json()['locations']
    for i in x:
        y = x[i]['values']

    final = [0, 0, 0, 0, 0, 0]

    for j in y:
        final[0] += j['temp']
        if j['maxt'] > final[1]:
            final[1] = j['maxt']
        final[2] += j['wspd']
        final[3] += j['cloudcover']
        final[4] += j['precip']
        final[5] += j['humidity']
    final[0] /= 15
    final[2] /= 15
    final[3] /= 15
    final[5] /= 15

    return final

def testConnection():
    return "yo"


import sys
sys.stdout.reconfigure(encoding='utf-8')

f = open('D:\\daya\\flood\\FloodML-master\\FloodML-master\\training\\cities.csv', 'r', encoding='UTF-8')
ff = open('D:\\daya\\flood\\FloodML-master\\FloodML-master\\training\plotting.csv', mode='w', newline = '')
writer = csv.writer(ff, delimiter=',')

r = csv.reader(f)

for row in r:
    print(row)
    writer.writerow(get_data(row[1], row[2]))