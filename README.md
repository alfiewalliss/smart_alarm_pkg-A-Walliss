# smart_alarm_pkg-A-Walliss

## Introduction

This smart alarm program allows users to create alarms with news and weather updates. It also updates a notifications column at the side of the page every 24 hours. You are able to customise the keywords you wish to search for in the news using a config file.


## Prerequisites:
Python version 3.8 was used for development
Any browser other than Firefox (chrome was used for development)
A stable internet connection

## Installation
pip install request
pip install pyttsx3
pip install logging

## Getting started
To use this program you must enter the get an API key for both: 
http://api.openweathermap.org/
https://newsapi.org/
You must then enter your API keys in the config file in the keys dictionary in the corresponding space.
You can then change the area of location used by the API's using the location field within the dictionary.
You can then also change any key words within the news_words list within the config file which will be used to dictate which news articles are pushed to you.
To run the program the command python ca3.main should be run when you are in the code directory.

## Testing
Testing automatically is carried out on startup and then at midnight upon all functions using the tests in tests.py. Any errors will then be outputted to the log file. Logs will also be created when alarms are created and notifications are updated.

## Developed Documentation
### ca3_main.py
This module is involved in taking the arguments from the URL and then manipulating them to set alarms and notifications with information taken from external API's.

#### go_to_page():
This function initialises lots of the variables and sets the time to midnight used to refresh the notifications at midnight.

#### schedule_event():
This function adds the alarms set to the UI and also schedules alarms. It also is invloved in changing the UI when an alarm is canceled.

#### announcment_alarm(text: str, weather: str, news: str) -> None:
   Called by the scheduler and concatinates the data spoken by the alarm
    text -- the data written by the user
    weather -- whether the user selected the weather radio button or not
    news -- whether the user selected the news radio button or not

#### alarm_to_list(header: str, content: str) -> None:
Appends all alarms to the list
header -- The head data of the alarm
content -- The content of the alarm

#### alarm_intermediate() -> None:
Schedules the check_alarms function to be called in 24 hours before pointing to it

#### check_alarms() -> None:
Checks if an alarm within the list is to go off within the next 24-hr and then schedules it if true

#### notification_alert(first: bool) -> None:
Updates the notifications on the right hand side of the UI and then schedules itself to happen again in 24 hours. It also schedules all testing to happen every night at midnight

#### test_functionality():
Calls all test functions and logs any errors

### get_api.py
A module used to get all the information from the API's

#### get_weather() -> dict:
Gets the weather from the API

#### get_news_alarm() -> str:
Gets the news from the API for alarms

#### get_news_notification() -> list:
Gets the news from the API for notifications

#### corona_news_alarm(L: dict) -> str:
Formats the news for alarms
 L -- dictionary from the json file of news
 
#### corona_news_notification(L: dict) -> list:
Formats the news for notifications
L -- dictionary from the json file of news

#### get_covid19_alarm() -> str:
Gets the covid19 information for alarms

#### get_covid19_notifications() -> dict:
Gets the covid19 information for notifications

### time_conversion.py
"""a module containing all of the time operations used within the program"""

#### minutes_to_seconds( minutes: str ) -> int:
Converts minutes to seconds
minutes -- the minutes to be converted to seconds

#### hours_to_minutes( hours: str ) -> int:
Converts hours to minutes
hours -- the hours to be converted to minutes

#### hhmm_to_seconds( hhmm: str ) -> int:
converts hhmm to seconds
hhmm -- the time in the format hh:mm to be converted to seconds

#### hhmmss_to_seconds( hhmmss: str ) -> int:
converts hhmmss to seconds
hhmmss -- The time in hh:mm:ss to be converted into seconds

#### current_time_hhmm() -> str:
returns the current time

### tests1.py
Use this page to test all the functions in the program

#### test_hhmmss_to_seconds():
Tests a time conversion

#### test_hhmm_to_seconds():
Tests a time conversion

#### test_current_time_hhmm():
Tests wheather the current time variable is correct

#### test_minutes_to_seconds():
Tests a time conversion 

#### test_hours_to_minutes():
Tests a time conversion

#### test_get_weather():
Tests the data type of what the get_weather() function returns

#### test_get_news_alarms():
Tests the data type of what the get_news_alarms() function returns

#### test_get_news_notifications():
Tests the data type of what the get_news_notifications() function returns

#### test_get_covid19_alarm():
Tests the data type of what the get_covid_alarm() function returns

#### test_notification_alert(notifications: list, function):
Checks that notifications are appended to the notification list and also checks the data structure notifications
notifications -- notification list
function -- the function that is being checked

#### test_go_to_page(time_to_midnight: int):
Tests the data type of what the variable time_to_midnight, a global variable used in go_to_page()
time_to_midnight -- time until midnight

#### test_schedule_event(alarms: list):
Tests the data structure type of the list alarms, a global list used in schedule_event()
alarms -- list of alarms

#### test_alarm_announcement(engine):
Tests that pyttsx3 has been correctly initialised which provides the main functionality of alarm_announcement()

#### test_alarm_to_list(future_alarms: list):
Tests the data structure type of the list future_alarms, a global list used in alarm_to_list()
future_alarms -- a list of alarms not happening on the current day

####  test_alarm_intermediate(function, function1):
Tests that the check_alarms() function is correctly returned
function -- the first function used in the comparison
function1 -- the second function used in the comparison

## Details
### Author:
Alfie Walliss

### Licence:
 Apache License, Version 2.0
