import csv
import datetime
import pickle
import requests

def get_data(lat, lon):
    print("Dayanand")

    # k="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/belagavi?unitGroup=us&key=DK3R39R6VYS25DZXNXWZGCHTY&contentType=json"
    k = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations=" + str(lat) + "%2C%20" + str(lon) + "&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType=json&key=DK3R39R6VYS25DZXNXWZGCHTY"
    # base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    # location_url = f"{lat},{lon}"

    # api_key = "DK3R39R6VYS25DZXNXWZGCHTY"  # Replace with your actual API key
    # unit_group = "us"
    # content_type = "json"

    # k = f"{base_url}{location_url}?unitGroup={unit_group}&key={api_key}&contentType={content_type}"
    f=requests.get(k)
    print(f.json())

    x = requests.get(k).json()['locations']
    print(x)

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