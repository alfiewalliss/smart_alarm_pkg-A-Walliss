"""This module is involved in taking the arguments from the URL and then manipulating them to set alarms and notifcations with information taken from external API's"""
from flask import Flask
from flask import request
import pyttsx3
from subprocess import call
from datetime import datetime as dt
import datetime
from flask import render_template
from time_conversions import hhmm_to_seconds
from time_conversions import hhmmss_to_seconds
from time_conversions import current_time_hhmm
from get_api import get_weather
from get_api import get_news_alarm
from get_api import get_news_notification
from get_api import get_weather
from get_api import get_news_alarm
import tests1
import logging
import time
import sched
import json

s = sched.scheduler(time.time, time.sleep)
logging.basicConfig(level=logging.DEBUG, filename='sys.log')
app = Flask(__name__)
engine = pyttsx3.init()
notifications = []
alarms = []
future_alarms = []
cancel_alarms = []
times = []
global time_to_midnight
time_to_midnight = 0
with open('config.json', 'r') as f:
        x = json.load(f) 
        picture = x["picture"]
        
@app.route('/')
def go_to_page():
    """This function initialises lots of the variables and sets the time to midnight used to refresh the notifications at midnight."""
    global setup
    global time_to_midnight
    s.run(blocking=False)
    current_time = dt.now()
    current_time = str(current_time.strftime("%H:%M:%S"))
    time_to_midnight = 86400 - int(hhmmss_to_seconds(current_time))
    s.enter(time_to_midnight, 1, alarm_intermediate)
    notification_alert(True)
    logging.info('Progam correctly initialised')
    return render_template('template.html', title='Daily update', image=picture, notifications=notifications)

@app.route('/index')
def schedule_event():
    """This function adds the alarms set to the UI and also schedules alarms. It also is invloved in changing the UI when an alarm is canceled """
    s.run(blocking=False)
    alarm_time = request.args.get("alarm")
    name = request.args.get("two")
    alarm_item = request.args.get("alarm_item")
    notif = request.args.get("notif")
    weather = request.args.get("weather")
    news = request.args.get("news")
    if alarm_time:
        year = str(alarm_time)[0: 4]
        month = str(alarm_time)[5: 7]
        day = str(alarm_time)[8:10]
        alarm = datetime.datetime(int(year), int(month), int(day))
        date_today = dt.today()
        year = str(date_today)[0: 4]
        month = str(date_today)[5: 7]
        day = str(date_today)[8:10]
        today = datetime.datetime(int(year), int(month), int(day))
        remember_name = name
        if weather and news: 
            name = name.replace(name[0], name[0].upper(), 1) + " (Weather and News Alarm)"
        elif weather:
            name = name.replace(name[0], name[0].upper(), 1) + " (Weather Alarm)"
        elif news:
            name = name.replace(name[0], name[0].upper(), 1) + " (News Alarm)"
        else:
            name = name.replace(name[0], name[0].upper(), 1)
        alarms.append({ 'title': name, 'content': str(alarm_time).replace("T", " ")})
        alarm_hm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
        if alarm > today:
                alarm_to_list(name, alarm_time)
        else:
            delay = hhmm_to_seconds(alarm_hm) - hhmm_to_seconds(current_time_hhmm())
            priorety = 1
            if str(alarm_time).replace("T", " ") in times:
                priorety = times.index(str(alarm_time).replace("T", " ")) + 2
            times.append(str(alarm_time).replace("T", " "))
            cancel_alarms.append({"name": name, "countdown": s.enter(int(delay), priorety, announcment_alarm, [remember_name, weather, news,])})
            logging.info('Alarm set at ' + alarm_hm)
    if alarm_item:
        check = "{'title': '" + alarm_item
        for i in alarms:
            if check in str(i):
                number = i
                alarms.remove(i)
                logging.info('Alarm schedule canceled: ' + alarm_item)
        for i in cancel_alarms:
            if i.get("name") == alarm_item:
                position = cancel_alarms.index(i)
                s.cancel(i.get("countdown"))
                redundant = cancel_alarms.pop(position)
                logging.info('Alarm removed from UI: ' + alarm_item)
    if notif:
        check = "{'title': '" + notif
        for i in notifications:
            if check in str(i):
                number = i
                notifications.remove(i)
                logging.info('Notification removed from UI: ' + notif)
    return render_template('template.html', title='Daily update', alarms=alarms,  image=picture, notifications=notifications) 

def announcment_alarm(text: str, weather: str, news: str) -> None:
    """Called by the scheduler and concatinates the data spoken by the alarm
    text -- the data written by the user
    weather -- whether the user selected the weather radio button or not
    news -- whether the user selected the news radio button or not"""
    global done
    s.run(blocking=False)
    origional = text
    if weather:
        forcast = get_weather()
        x = forcast["weather"]
        y = forcast["main"]
        forcast = ". It is currently " + x[0]["description"] + " in Exeter. The temperature is " + str(round(y["temp"] - 273.15)) + "degrees celcius."
        text = text + ". Weather report. " + forcast
    if news:
        reports = get_news_alarm()
        text = text + ". News report. " + reports
    try:
        engine.endLoop()
    except:
        logging.error("pyttsx3 endloop error. No action taken Program should continue to run")
    engine.say(text)
    engine.runAndWait()
    logging.info('Alarmed: ' + origional)
    origional = origional.replace(origional[0], origional[0].upper(), 1)
    check = "{'title': " + "'" + origional
    for i in alarms:
        if check in str(i):
            number = i
            alarms.remove(i)

    
def alarm_to_list(header: str, content: str) -> None:
    """Appends all alarms to the list
    header -- The head data of the alarm
    content -- The content of the alarm"""
    future_alarms.append({content: header})

def alarm_intermediate() -> None:
    """Schedules the check_alarms function to be called in 24 hours before pointing to it"""
    s.enter(86400, 1, check_alarms())
    logging.info('Scheduled check_alarm for 24 hours')
    check_alarms()
    
def check_alarms() -> None:
    """Checks if an alarm within the list is to go off within the next 24-hr and then schedules it if true"""
    s.run(blocking=False)
    date_today = dt.today()
    date_today = str(date_today)[0:10]
    for i in future_alarms:
        for key in i:
            if date_today in key[0:10]:
                alarm_hm = key[11:16]
                delay = hhmm_to_seconds(alarm_hm) - hhmm_to_seconds(current_time_hhmm())
                s.enter(int(delay), 1, announcment_alarm, [i.get(key),])
    logging.info('Alarms scheduled for current day')

def notification_alert(first: bool) -> None:
    """Updates the notifications on the right hand side of the UI and then schedules itself to happen again in 24 hours. It also schedues all testing to happen every night at midnight"""
    global time_to_midnight
    s.run(blocking=False)
    forcast = get_weather()
    news = get_news_notification()
    x = forcast["weather"]
    y = forcast["main"]
    notifications.append({ 'title': "Current Weather", 'content': "It is currently " + x[0]["description"] + " and the temperature is " + str(round(y["temp"] - 273.15)) + "°C"})
    logging.info('Notifications successfully appened to UI')
    for i in news:
        notifications.append({'title': i['name'], 'content': i['content']})
    if first == True:
        s.enter(time_to_midnight, 1, notification_alert, [False,])
    else:
        s.enter(86400, 1, notification_alert, [False,])
        s.enter(86400, 1, test_functionality,)
    logging.info('Notifications scheduled for midnight')

def test_functionality():
    """Calls all test functions and logs any errors"""
    tests1.test_hhmmss_to_seconds()
    tests1.test_hhmm_to_seconds()
    tests1.test_current_time_hhmm()
    tests1.test_minutes_to_seconds()
    tests1.test_hours_to_minutes() 
    tests1.test_get_weather()
    tests1.test_get_news_alarms()
    tests1.test_get_news_notifications()
    tests1.test_go_to_page(time_to_midnight)
    tests1.test_get_covid19_alarm()    
    tests1.test_schedule_event(alarms)
    tests1.test_alarm_announcement(engine)
    tests1.test_alarm_to_list(future_alarms)
    tests1.test_alarm_intermediate(alarm_intermediate(), check_alarms())
    tests1.test_notification_alert(notifications, notification_alert(False)) 


if __name__ == '__main__':
    logging.info("Application starting...")
    app.run()
