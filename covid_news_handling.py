import requests
from uk_covid19 import Cov19API
import sched
import time
import json
from flask import Flask, request
import global_vars


f = open("config.json")
config = json.load(f)


APIKEY = config["APIKEY"]
BASEURL = "https://newsapi.org/v2/everything?"


sched_news_updates = []
s = sched.scheduler(time.time, time.sleep)



def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    """
    returning articles data from the news API
    returns in a json format
    then uses news_json_to_dict function to convert to dictionary format
    """
    covid_terms = covid_terms.split()
    key_words = ""
    for i in range(len(covid_terms)):
        key_words += ("q=" + covid_terms[i] + "&")
    key_words = key_words[:-1]
    complete_url = BASEURL + key_words + "&soryBy=popularity&apiKey=" + APIKEY
    #put article into a list of dictionaries
    #used this format as that is what the index.html handles
    return (requests.get(complete_url).json())["articles"]


def set_covid_news():
    global_vars.news = news_API_request()



def update_news(update_interval, update_name, repeat):
    """
    update the news using news_API_request
    putting updates into a list of dictionaries so they can be deleted
    """
    sched_updates_dict = {}
    event = s.enter(update_interval, 1, set_covid_news)
    sched_updates_dict["name"] = update_name
    sched_updates_dict["event"] = event
    sched_news_updates.append(sched_updates_dict)
    
    if repeat == True:
        sched_updates_dict = {}
        event_repeat = s.enter(86400, 3, update_news,
                kwargs={"update_interval":update_interval, "update_name":update_name,
                        "repeat":repeat})
        sched_updates_dict["name"] = update_name
        sched_updates_dict["event"] = event_repeat
        sched_news_updates.append(sched_updates_dict)
    s.run()



def delete_news_update(update_name):
    """
    function to delete update from scheduler
    """
    for element in sched_news_updates:
        if element["name"] == update_name:
            s.cancel(element["event"])
            sched_news_updates.remove(element)
            delete_news_update(update_name)
    s.run()



