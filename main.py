# week 2
# The pair programming assignment is messed up


'''
lets make a plan and decide what idea we are going to use ?

I am fine with both

sounds good


which of our ideas from google docs sounds the most fun/interesting ?

The recipe, the activity and the youtube looks fun


sounds good

hmmm,,, i kinda like the activity one a lot bc its kinda unique
I like it too, we can go for it


i sent a link for a potential api we could use on slack

'''



# an example maybe: ?

import requests
# import sqlalchemy as db
# import pandas as pd
# from pandas import DataFrame
from pprint import pprint

cityName = input("input a city to get weather: ").capitalize()


weather_url = 'https://community-open-weather-map.p.rapidapi.com/climate/month'
places_url = "https://nearby-places.p.rapidapi.com/nearby"

weather_query = {"q": cityName}

# we will change lng and lat to the lng and lat of the cityName according to the 
# data from the weather api. this is j example for now
places_query = {"lat":"49.283030","lng":"-123.118990","type":"cafe","radius":"200"}

weather_headers = {
	'X-RapidAPI-Key': 'dfa2158044msh6359d946b81ab6ap188d9ejsn419a4d091251',
	'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com'
}

places_headers = {
	"X-RapidAPI-Key": "dfa2158044msh6359d946b81ab6ap188d9ejsn419a4d091251",
	"X-RapidAPI-Host": "nearby-places.p.rapidapi.com"
}


weather_response = requests.get(weather_url, headers = weather_headers, params = weather_query)
places_response = requests.get(places_url, headers=places_headers, params=places_query)


pprint(weather_response.json())
pprint(places_response.json())



'''
we should also put it in a database and or smth


# another way to display:
for key, val in response.json().items():
  pprint(f"{key} : {val} ")

'''


