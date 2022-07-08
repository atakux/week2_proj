# ACTIVITIES FINDER


##  Description

ACTIVITIES FINDER is a program that suggests places based on the user's location and the weather. It uses the following libraries:
* json
* requests
* [Weather Api](https://www.weatherapi.com/docs/)
* [GeoApify Place API](https://apidocs.geoapify.com/docs/places/#about)

## Run the file
Firstly make sure to install the libraries libraries by running the following command:
* pip install SQLAlchemy
* pip install pandas
* pip install requests

Once all the libraries have been successfully installed, run the file main.py

## Program guide
When starting the program, you will be prompted to enter different criteria to find the best activity for you:
* Your location (city/ zip code/ auto ip)
* Research radius
* Maximum number of results to display
* Category of place you will like to be proposed
* Condition to filter the research (optional)
Once you have respond to all the prompts, the program will display the weather and all the results matching your research criteria. You will then be suggested a few places based on the weather. Your result will then be stored and you will be able to view all your researches result at the end of the program.
