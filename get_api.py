"""A module used to get all the information from the API's"""
import json
import requests 
from uk_covid19 import Cov19API
def get_weather() -> dict:
    """Gets the weather from the API"""
    with open('config.json', 'r') as f:
        x = json.load(f)
        y = x["keys"]
        z = x["location"]
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = y["weather"]
        city_name = z["area"]
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        return x
def get_news_alarm() -> str:
    """Gets the news from the API for alarms"""
    with open('config.json', 'r') as f:
        x = json.load(f)
        y = x["keys"]
        z = x["location"]
        base_url = "https://newsapi.org/v2/top-headlines?"
        api_key = y["news"]
        country = z["country"]
        complete_url = base_url + "country=" + country + "&apiKey=" + api_key
        response = requests.get(complete_url)
        return corona_news_alarm(response.json())
def get_news_notification() -> list:
    """Gets the news from the API for notifications"""
    with open('config.json', 'r') as f:
        x = json.load(f)  
        y = x["keys"]
        z = x["location"]
        base_url = "https://newsapi.org/v2/top-headlines?"
        api_key = y["news"]
        country = z["country"]
        complete_url = base_url + "country=" + country + "&apiKey=" + api_key
        response = requests.get(complete_url)
        return corona_news_notification(response.json())
def corona_news_alarm(L: dict) -> str:
    """Formats the news for alarms
    L -- dictionary from the json file of news"""
    with open('config.json', 'r') as f:
        x = json.load(f)  
        y = x["news_words"]
        new_dict = L
        articles = new_dict["articles"]
        news = ""
        for article in articles:
            for i in y:
                if i.lower() in article['title'].lower():
                    temp = article['title'].split("-")
                    news = news + "From " + article['source']['name'] + ". " + temp[0] + ". "
        news = news + get_covid19_alarm()
        return news
def corona_news_notification(L: dict) -> list:
    """Formats the news for notifications
    L -- dictionary from the json file of news"""
    with open('config.json', 'r') as f:
        x = json.load(f)  
        y = x["news_words"]
        new_dict = L
        news = []
        articles = new_dict["articles"]
        for article in articles:
            for i in y:
                if i.lower() in article['title'].lower():
                    temp = article['title'].split("-")
                    redundant = temp.pop()
                    temp = " ".join(temp)
                    news.append({'name': article['source']['name'], 'content': temp})
        data = get_covid19_notifications()
        news.append({'name': "Decalired cases on the " + str(data["data"][0]["date"]), 'content': str(data["data"][0]["newCasesByPublishDate"])})
        news.append({'name': "Total cases as of the " + str(data["data"][0]["date"]), 'content': str(data["data"][0]["cumCasesByPublishDate"])})
        return news
def get_covid19_alarm() -> str:
    """Gets the covid19 information for alarms"""
    england_only = ['areaType=nation', 'areaName=England']
    cases_and_deaths = {"date":"date","areaName":"areaName","areaCode":"areaCode","newCasesByPublishDate":"cumCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate"}
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()
    return "On the " + str(data["data"][0]["date"]) + " there were " + str(data["data"][0]["newCasesByPublishDate"]) + " new cases bringing the total cases in england too " + str(data["data"][0]["cumCasesByPublishDate"])
def get_covid19_notifications() -> dict:
    """gets the covid19 information for notifications"""
    england_only = ['areaType=nation', 'areaName=England']
    cases_and_deaths = {"date":"date","areaName":"areaName","areaCode":"areaCode","newCasesByPublishDate":"cumCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate"}
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()
    return data
