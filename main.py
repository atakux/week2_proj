# week 2

import requests
import sqlalchemy as db
import pandas as pd
from requests.structures import CaseInsensitiveDict


def miles_to_metres(miles):
    return miles*1609.344


def weather_api(city):
    # get weather api info using the cityName
    weather_url = 'https://community-open-weather-map.p.rapidapi.com/climate/month'
    weather_query = {"q": city}
    weather_headers = {
        'X-RapidAPI-Key': 'dfa2158044msh6359d946b81ab6ap188d9ejsn419a4d091251',
        'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com'
    }

    weather_response = requests.get(weather_url, headers=weather_headers,
                                    params=weather_query)

    # empty list to store longitude, latitude in that order
    long_lat = []
    # get long and lat from weather api
    for key, val in weather_response.json().items():
        if key != 'city':
            continue
        else:
            for k, v in val.items():
                if k == 'coord':
                    for v2 in v.values():
                        long_lat.append(v2)
    return long_lat


def places_api(city, rad):
    radius = miles_to_metres(rad)
    how_many = int(input("how many places would you like listed? "))
    category = input("what type of places would you like listed? ")

    lon_lat = weather_api(city)

    longitude = lon_lat[0]
    latitude = lon_lat[1]

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # get places api info using the long and lat from weather api
    main_url = "https://api.geoapify.com/v2/places?"
    category_url = "categories="+category
    coord_url = "&filter=circle:"+str(longitude)+","+str(latitude)+","+str(radius)
    limit_url = "&limit="+str(how_many)
    api_key = "&apiKey=f9d148d7161c4dd591412df7d0bd9801"

    places_url = main_url + category_url + coord_url + limit_url + api_key

    places_response = requests.get(places_url, headers=headers)

    return places_response


def db_print():
    # receive user input for the city they would like weather for
    city_name = input("input a city to get weather: ").capitalize()
    miles_radius = int(input("how many miles radius? "))

    places_response = places_api(city_name, miles_radius)

    # Storing in database
    engine = db.create_engine('sqlite:///activity_db.db')
    places = places_response.json()["features"]
        
    print('Place Name \t\t\t\t\t Address')
    print('---------- \t\t\t\t\t -------')
    for place in places:
        detail = place["properties"]
        try:
            name = detail["name"]
            address = detail["address_line1"] + " " + detail["address_line2"]
        
        except:
            name = detail["street"]
            address = detail["address_line1"] + " " + detail["address_line2"]

        
        print(f'{name} \t\t\t\t\t {address} ')
        place_dict = {'address': address, 'name': name}
        df = pd.DataFrame.from_dict([place_dict])
        df.to_sql('Activity', con=engine, if_exists='append', index=False)
    # result = engine.execute('SELECT * FROM Activity;').fetchall()
    # print(pd.DataFrame(result))


db_print()
