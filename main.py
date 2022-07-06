# week 2

import requests
import sqlalchemy as db
import pandas as pd
from requests.structures import CaseInsensitiveDict
from pprint import pprint


def miles_to_metres(miles):
    return miles*1609.344


def weather_api(city):
    # get weather api info using the cityName
    weather_url = 'https://api.weatherapi.com/v1/current.json'
    weather_query = {"q": city}
    weather_headers = {
        'key': '0afe61da1abe4a7691b205109220507'
    }

    weather_response = requests.get(weather_url, headers=weather_headers,
                                    params=weather_query)
    return weather_response


def get_location_name():
    weather_response = weather_api('auto:ip')

    the_city = ''

    for key, val in weather_response.json().items():
        if key == 'location':
            for k, v in val.items():
                if k != 'name':
                    continue
                else:
                    the_city = v
    return the_city


def get_weather(city):
    weather_response = weather_api(city)

    if city == 'auto:ip':
        city = get_location_name()

    temp = ''
    sky = ''
    feels_temp = ''
    winds = ''

    for key, val in weather_response.json().items():
        if key == 'location':
            for k, v in val.items():
                if k != 'name':
                    continue
                else:
                    the_city = v
        elif key == 'current':
            for k, v in val.items():
                if k == 'temp_f':
                    temp = v
                elif k == 'condition':
                    for kk, vv in v.items():
                        if kk == 'text':
                            sky = vv
                elif k == 'wind_mph':
                    winds = v
                elif k == 'feelslike_f':
                    feels_temp = v
                else:
                    continue

    return f"The temperature in {city} is {temp} degrees F and the condition is {sky.lower()}. \n\tThe wind speeds " \
           f"are at {winds} mph and it feels like {feels_temp} degrees. "


def coordinates(city):

    weather_response = weather_api(city)

    # empty list to store longitude, latitude in that order
    long_lat = []
    # get long and lat from weather api
    for key, val in weather_response.json().items():
        if key != 'location':
            continue
        else:
            for k, v in val.items():
                if k == 'lat':
                    long_lat.append(v)
                elif k == 'lon':
                    long_lat.append(v)
                else:
                    continue
    return long_lat


def categories():
    category_list = ['accommodation', 'activity', 'beach', 'commercial', 'catering', 'entertainment', 'leisure']
    option = input("if you would like to see a list of categories\nhit enter, otherwise input a category: ").lower()

    if type(option) != str:
        print("invalid input")
    elif option == '':
        print("here is a list of categories to choose from: ")
        for i in category_list:
            print(i, end='\n')
        choice = input("input your category: ")
        if choice not in category_list:
            print("invalid category")
        else:
            return choice
    else:
        if option not in category_list and option != 'm':
            print("invalid category")
        else:
            return option


def places_api(city, rad):
    radius = miles_to_metres(rad)
    how_many = int(input("how many places would you like listed? "))
    # set a maximum number of places
    if how_many > 20:
        print("note: the number of places is limited to 20.")
        how_many = 20

    category = categories()

    lon_lat = coordinates(city)

    longitude = lon_lat[1]
    latitude = lon_lat[0]

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
    city_name = input("input a city to get weather, [leave blank if you want your IP to be inputted for you]: ")
    if city_name == '':
        print(f"...retrieving your IP... location = {get_location_name()}")
        city_name = 'auto:ip'

    miles_radius = int(input("how many miles radius? "))

    if miles_radius > 30:
        miles_radius = int(input("\nmax radius is 30 miles. \nplease input something lower."))
    elif miles_radius < 0:
        miles_radius = int(input("\ncant have negative radius. \nplease input something higher."))

    try:
        places_response = places_api(city_name, miles_radius)
        if city_name == 'auto:ip':
            city_name = get_location_name()

        current_weather = get_weather(city_name)
        print(f"The weather in {city_name}: \n\t{current_weather}")

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
    except:
        print("\nan error occurred.\nplease run the program again and be sure your input is correct.")


db_print()