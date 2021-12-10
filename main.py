from flask import Flask, request, make_response, redirect, render_template, flash
import time
import sched
import logging
import json

import global_vars
import config
import covid_data_handler
from covid_news_handling import news_API_request, update_news


#loading the config file
f = open("config.json")
config = json.load(f)


#setting up a log file
logging.basicConfig(filename="sys.log", level=logging.DEBUG)



#setting up a scheduler
s = sched.scheduler(time.time, time.sleep)



def create_app():
    """
    initialising a flask application
    """
    app = Flask(__name__)

    return app


#initialising the app
app = create_app()


"""
the entire interface
"""
@app.route("/index", methods=["GET", "POST"])
def home():

    """
    populating the global variables
    """
    global_vars.news = news_API_request()
    if len(global_vars.local_data) == 0:
        global_vars.local_data = covid_data_handler.covid_API_request()
    if len(global_vars.national_data) == 0:
        global_vars.national_data = covid_data_handler.covid_API_request(config["nation"], "nation")
    """
    checking if someone has does something, then responding
    """
    if request.method == "GET":
        #getting the info from the NEWS COLUMN form
        update_time = request.args.get("update")
        update_name = request.args.get("two")
        #getting info from checkboxes on form (returns name label)
        repeat_update_box = request.args.get("repeat")
        update_data_box = request.args.get("covid-data")
        update_news_box = request.args.get("news")
        
        #if the form was submitted
        if update_name != None:
            """
            adding the update info to the updates list of dictionaries
            """
            #creating the update content (string of most recent data)
            new_data = covid_data_handler.covid_API_request()
            update_dict = {}
            update_dict["title"] = update_name
            update_dict["time"] = update_time
            update_content = ""
            if repeat_update_box == "repeat":
                update_dict["repeat"] = True
            else:
                update_dict["repeat"] = False
            if update_data_box == "covid-data":
                update_dict["data"] = True
                update_content = ("Update: Date, Area Name, New Cases, Cumulative Cases, "
                              +"Local 7 Day Infection Rate, National 7 Day Infection Rate, "
                              +"Hospital Cases, Total Deaths\n"
                              +"At: "+update_time)
            else:
                update_dict["data"] = False
            if update_news_box == "news":
                update_dict["news"] = True
                update_content = "Update: News\n At: "+update_time
            else:
                update_dict["news"] = False
            update_dict["content"] = update_content
            global_vars.updates.append(update_dict)
            
            """
            scheduling the updates
            """
            #calculating the update interval using the current time (line98-111)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            #converting current time to secs since midnight
            current_time_from_midnight_secs = (int(current_time[0]+current_time[1]) *(60^2) +
                                               int(current_time[3]+current_time[4]) *60 +
                                               int(current_time[6]+current_time[7]))
            #converting the update time to secs since midnight
            update_time_from_midnight_secs = (int(update_time[0]+update_time[1]) *(60^2) +
                                              int(update_time[3]+update_time[4]) *60)
            #calculating the time form the current time till the update time in secs
            if update_time_from_midnight_secs > current_time_from_midnight_secs:
                update_interval = update_time_from_midnight_secs - current_time_from_midnight_secs
            else:
                update_interval = 86400 - current_time_from_midnight_secs + update_time_from_midnight_secs
            #running the update functions for updating data and news
            if update_dict["data"] == True:
                covid_data_handler.schedule_covid_updates(update_interval, update_name, update_dict["repeat"])
            if update_dict["news"] == True:
                covid_news_handling.update_news(update_interval, update_name, update_dict["repeat"])
                  
    """
    to delete closed updates using list of deleted articles
    """
    updates = global_vars.updates
    if request.args.get("update_item") != None:
        update_to_delete = request.args.get("update_item")
        for i in range(len(updates)):
            if updates[i]["title"] == update_to_delete:
                #to delete the updates from their schedulars
                if updates[i]["data"] == True:
                    covid_data_handler.delete_covid_update(updates[i]["title"])
                if updates[i]["news"] == True:
                    covid_news_handling.delete_news_update(updates[i]["title"])
                #to delete widget
                updates.pop(i)
                i = len(updates)
    global_vars.updates = updates
    
    """
    appending closed articles to a list for all deleted articles
    """
    if request.args.get("notif") != None:
        article_to_delete = request.args.get("notif")
        global_vars.deleted_articles.append(article_to_delete)
        

    """
    removing all the articles in the list of deleted articles from the news_articles
    so they will not be re-displayed
    """
    if global_vars.deleted_articles != []:
        for delete_article in global_vars.deleted_articles:
            for check_article in global_vars.news:
                if check_article["title"] == delete_article:
                    global_vars.news.remove(check_article)

    """
    using function in covid_data_handler to get the local and national 7 day infection rates
    I assumed this meant the cumulative infections for the last 7 days?
    """
    local_7day_infections = 0
    for n in range(7):
        local_7day_infections += global_vars.local_data[n]["newCasesByPublishDateChange"]
    national_7day_infections = 0
    for m in range(7):
        national_7day_infections += global_vars.national_data[m]["newCasesByPublishDateChange"]

    #getting the current hospital cases from the national data
    hospital_cases = global_vars.national_data[0]["hospitalCases"]
    #getting the death total
    deaths_total = global_vars.national_data[0]["cumDeathsByPublishDate"]

    #putting everything in the template and rendering
    return render_template("index.html",
                           title="Your Covid Update",
                           location="Exeter",
                           local_7day_infections=local_7day_infections,
                           nation_location="England",
                           national_7day_infections=national_7day_infections,
                           hospital_cases=hospital_cases,
                           deaths_total=deaths_total,
                           news_articles=global_vars.news,
                           updates=updates)



#to run the app
if __name__ == "__main__":
    app.run()

