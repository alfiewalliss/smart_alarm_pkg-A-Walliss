"""Use this page to test all the functions in the program"""
from time_conversions import minutes_to_seconds
from time_conversions import hours_to_minutes
from time_conversions import hhmmss_to_seconds
from time_conversions import hhmm_to_seconds
from time_conversions import current_time_hhmm
from get_api import get_weather
from get_api import get_news_alarm
from get_api import get_news_notification
from get_api import get_covid19_alarm
import pyttsx3
import logging


import time
def test_hhmmss_to_seconds():
    """Tests a time conversion"""
    try:
        assert hhmmss_to_seconds("09:30:28") == 34228
    except AssertionError:
        logging.error("hhmmss_to_seconds error. Program will continue to run but maintinence required")
            
def test_hhmm_to_seconds():
    """Tests a time conversion""" 
    try:
        assert hhmm_to_seconds("09:30") == 34200
    except AssertionError:
        logging.error("hhmm_to_seconds error. Program will continue to run but maintinence required")
    
def test_current_time_hhmm():
    """Tests wheather the current time variable is correct"""
    try:
        assert current_time_hhmm() == str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
    except AssertionError:
        logging.error("current_time_hhmm error. Program will continue to run but maintinence required")
          
def test_minutes_to_seconds():
    """Tests a time conversion""" 
    try:
        assert minutes_to_seconds(20) == 20*60
    except AssertionError:
        logging.error("minutes_to_seconds error. Program will continue to run but maintinence required")

def test_hours_to_minutes():
    """Tests a time conversion"""  
    try:
        assert hours_to_minutes(4) == 4*60
    except AssertionError:
        logging.error("hours_to_minutes error. Program will continue to run but maintinence required")

def test_get_weather():
    """Tests the data type of what the get_weather() function returns"""
    try:
        assert type(get_weather()) == dict
    except AssertionError:
        logging.error("get_weather error. Check weather API status")
    
def test_get_news_alarms():
    """Tests the data type of what the get_news_alarms() function returns"""
    try:
        assert type(get_news_alarm()) == str
    except AssertionError:
        logging.error("get_news_alarms error. Check news API status")

def test_get_news_notifications():
    """Tests the data type of what the get_news_notifications() function returns"""
    try:
        assert type(get_news_notification()) == list
    except AssertionError:
        logging.error("get_news_notification error. Check news and covid19 API status")
            
def test_get_covid19_alarm():
    """Tests the data type of what the get_covid_alarm() function returns"""
    try:
        assert type(get_covid19_alarm()) == str
    except AssertionError:
        logging.error("get_covid19_alarm error. Check covid19 API status")

def test_notification_alert(notifications: list, function):
    """Checks that notifications are appended to the notification list and also checks the data structure notifications"""
    try:
        check = str(notifications)
        function
        new = str(notifications)
        assert check != new
        assert type(notifications) == list
    except AssertionError:
        logging.error("notification_alert error. Check all API's status")
            
def test_go_to_page(time_to_midnight: int):
    """Tests the data type of what the variable time_to_midnight, a global variable used in go_to_page()
    time_to_midnight -- time until midnight"""
    try:
        assert type(time_to_midnight) == int
    except AssertionError:
        logging.error("go_to_page error. Program will continue to run but maintinence required")

def test_schedule_event(alarms: list):
    """Tests the data structure type of the list alarms, a global list used in schedule_event()
    alarms -- list of alarms"""
    try:
        assert type(alarms) == list
    except AssertionError:
        logging.error("schedule_event error. Program will continue to run but maintinence required")
        
def test_alarm_announcement(engine):
    """Tests that pyttsx3 has been correctly initialized which provides the main functionallity of alarm_announcement()"""
    try:
        assert engine == pyttsx3.init()
    except AssertionError:
        logging.error("alarm_announcement error. Program will continue to run but maintinence required")
        
def test_alarm_to_list(future_alarms: list):
    """Tests the data structure type of the list future_alarms, a global list used in alarm_to_list()
    future_alarms -- a list of alarms not happening on the current day"""
    try:
        assert type(future_alarms) == list
    except AssertionError:
        logging.error("alarm_to_list error. Program will continue to run but maintinence required")
    
def test_alarm_intermediate(function, function1):
    """Tests that the check_alarms() function is correctly returned
    function -- the first function used in the comparison
    function1 -- the second function used in the comparison"""
    try:
        assert function == function1
    except AssertionError:
        logging.error("go_to_page error. Program will continue to run but maintinence required")

