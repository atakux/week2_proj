# week 2

import requests
# import sqlalchemy as db
# import pandas as pd
# from pandas import DataFrame
from pprint import pprint

# receive user input for the city they would like weather for
cityName = input("input a city to get weather: ").capitalize()
radius = int(input("how many metres radius? "))

# get weather api info using the cityName
weather_url = 'https://community-open-weather-map.p.rapidapi.com/climate/month'
weather_query = {"q": cityName}
weather_headers = {
 'X-RapidAPI-Key': 'dfa2158044msh6359d946b81ab6ap188d9ejsn419a4d091251',
 'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com'
}

weather_response = requests.get(weather_url, headers=weather_headers, 
                                params=weather_query)

# empty list to store longitude, latitude in that order
lon_lat = []
# get long and lat from weather api
for key, val in weather_response.json().items():
    if key != 'city':
        continue
    else:
        for k, v in val.items():
            if k == 'coord':
                for v2 in v.values():
                    lon_lat.append(v2)
longitude = lon_lat[0]
latitude = lon_lat[1]

# get places api info using the long and lat from weather api
places_url = "https://nearby-places.p.rapidapi.com/v2/nearby"
# we will change lng and lat to the lng and lat of the cityName according to the
# data from the weather api. this is j example for now
places_query = {"lat": latitude, "lng": longitude, "radius": radius}
places_headers = {
 "X-RapidAPI-Key": "dfa2158044msh6359d946b81ab6ap188d9ejsn419a4d091251",
 "X-RapidAPI-Host": "nearby-places.p.rapidapi.com"
}

places_response = requests.get(places_url, headers=places_headers,
                               params=places_query)


pprint(weather_response.json())
pprint(places_response.json())

'''
we should also put it in a database and or smth


# another way to display:
for key, val in response.json().items():
  pprint(f"{key} : {val} ")

'''
