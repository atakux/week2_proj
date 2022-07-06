# week 2

import requests
import sqlalchemy as db
import pandas as pd
from requests.structures import CaseInsensitiveDict
from pprint import pprint


def miles_to_metres(miles):
    """converts miles to metres, returns measurement in metres"""
    return miles*1609.344


def weather_api(city):
    """access the weatherapi and return the response/data"""
    # get weather api info using the cityName
    weather_url = 'https://api.weatherapi.com/v1/current.json'
    weather_query = {"q": city}
    weather_headers = {
        'key': '0afe61da1abe4a7691b205109220507'
    }

    weather_response = requests.get(weather_url, headers=weather_headers,
                                    params=weather_query)
    return weather_response


def get_location_ip():
    """returns user location name based on their ip address"""
    weather_response = weather_api('auto:ip')

    the_city = ''

    # parse through weatherapi response data to retrieve location name
    for key, val in weather_response.json().items():
        if key == 'location':
            for k, v in val.items():
                if k != 'name':
                    continue
                else:
                    the_city = v
    return the_city


def get_location_zip(zip_code):
    """returns user location name based on their zipcode"""
    weather_response = weather_api(zip_code)

    the_city = ''

    # parse through weatherapi response data to retrieve location name
    for key, val in weather_response.json().items():
        if key == 'location':
            for k, v in val.items():
                if k != 'name':
                    continue
                else:
                    the_city = v
    return the_city


def get_weather(city):
    """retrieves temp, condition, feels temp, and winds based on user city
       returns formatted sentence displaying gathered info"""

    weather_response = weather_api(city)

    if city == 'auto:ip':
        city = get_location_ip()

    # empty variables for storage
    temp = ''
    sky = ''
    feels_temp = ''
    winds = ''

    # parse through weatherapi response data to gather info
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

    weather_data = [temp, sky, feels_temp, winds]

    return weather_data


def coordinates(city):
    """returns coordinates based on user location"""
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
    """prompts user for categorical input to send to place api. returns category"""
    category_list = ['accommodation', 'activity', 'beach', 'commercial', 'catering', 'entertainment', 'leisure']
    option = input("if you would like to see a list of categories\nhit enter, otherwise input a category: ").lower()

    # check for invalid input
    if type(option) != str:
        print("invalid input")
    elif option == '':
        # display menu since user hit enter
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


def filter_categories(weather):

    f_categories = []

    # temp = 0, sky = 1
    if int(weather[0]) > 75 and weather[1].lower() == "sunny":
        f_categories = ['commercial.outdoor_and_sport', 'sport.swimming_pool', 'beach', 'catering.ice_cream',
                        'entertainment.miniature_golf', 'leisure.park']
    elif int(weather[0]) > 75 and weather[1].lower != "sunny":
        f_categories = ['commercial.outdoor_and_sport', 'leisure.spa']
    elif int(weather[0]) < 50:
        f_categories = ['commercial.shopping_mall', 'commercial.toy_and_game']
    else:
        f_categories = ['commercial.shopping_mall']

    print(f"Based on your weather we suggest you the following categories: {''.join(f_categories)}")


def places_api(city, rad):
    """access the placesapi and return response/data"""
    radius = miles_to_metres(rad)

    # prompt user for amount of locations, if invalid use default
    how_many = int(input("how many places would you like listed? "))
    # set a maximum number of places
    if how_many > 20:
        print("the number of places is limited to 20. \ndefaulting to 20 places.")
        how_many = 20
    elif how_many < 1:
        print("the number of places must be at least 1. \ndefaulting to 1 place")
        how_many = 1

    # prompt the user to choose a category
    category = categories()

    # retrieve user coordinates
    lon_lat = coordinates(city)

    # store coordinates in separate variables
    longitude = lon_lat[1]
    latitude = lon_lat[0]

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # set up the url based on user input and base links
    main_url = "https://api.geoapify.com/v2/places?"
    category_url = "categories="+category
    coord_url = "&filter=circle:"+str(longitude)+","+str(latitude)+","+str(radius)
    limit_url = "&limit="+str(how_many)
    api_key = "&apiKey=f9d148d7161c4dd591412df7d0bd9801"

    places_url = main_url + category_url + coord_url + limit_url + api_key

    places_response = requests.get(places_url, headers=headers)

    return places_response


def db_print():
    """prompt user for starter info. call other functions to retrieve information. add information into database.
       print information for the user
    """
    # receive user input for the city they would like weather for
    city_name = input("input a city or zipcode to get weather, [leave blank if you want your IP to be inputted "
                      "for you]: ")
    # check if the user wants to use their ip or zipcode instead of city name
    if city_name == '':
        print(f"...retrieving your IP... location = {get_location_ip()}")
        city_name = 'auto:ip'
    elif city_name.isdigit():
        print(f"your location at the zipcode {city_name} is {get_location_zip(city_name)}")

    # prompt user for radius in miles
    miles_radius = int(input("how many miles radius? "))

    # set max and min radius, default values if invalid
    if miles_radius > 30:
        print("\nmax radius is 30 miles. \ndefaulting to 30 miles.")
        miles_radius = 30
    elif miles_radius < 1:
        print("\nmin radius is 1 mile. \ndefaulting to 1 mile.")
        miles_radius = 1

    # checking for invalid city_name input
    try:
        # call places_api to get places
        places_response = places_api(city_name, miles_radius)

        # check if the city_name was a zip code or blank, rather than a city name
        if city_name == 'auto:ip':
            city_name = get_location_ip()
        elif city_name.isdigit():
            city_name = get_location_zip(city_name)

        # display the current weather conditions for the city
        current_weather = get_weather(city_name)
        print(f"The weather in {city_name}: \n\t{current_weather}")

        # storing in database
        engine = db.create_engine('sqlite:///activity_db.db')
        places = places_response.json()["features"]

        # printing
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

        filter_categories(get_weather(city_name))

    # if user inputted invalid city_name display error message
    except:
        print("\nan error occurred.\nplease run the program again and be sure your input is correct.")


db_print()
