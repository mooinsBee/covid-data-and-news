import csv
from uk_covid19 import Cov19API
import json
import sched
import time
import global_vars

f = open("config.json")
config = json.load(f)


sched_covid_updates = []
s = sched.scheduler(time.time, time.sleep)



def parse_csv_data(csv_filename):
    """
    putting data from a csv file into a 2d list
    """
    data = []
    file = open(csv_filename, 'r')
    csv_reader = csv.reader(file)
    for row in csv_reader: 
        data.append(row) #putting each row as a list into the data list
        
    return data



def process_covid_csv_data(covid_csv_data):
    """
    getting the new cases in the last 7 days,
    the current number of hospital cases and
    the total number of deaths
    from the list that would be returned from putting the given csv file into the parse_csv_data function
    """
    newcases_7days = 0
    for i in range(2,9): #not including most recent day
        newcases_7days += int(covid_csv_data[i][6])
    current_hospital_cases = int(covid_csv_data[1][5])
    index = 1
    while True:
        if covid_csv_data[index][4] != '':
            total_deaths = int(covid_csv_data[index][4])
            break
        else:
            index += 1
            
    return newcases_7days, current_hospital_cases, total_deaths



def covid_API_request(location = config["city"], location_type = "ltla"):
    """
    returning data from the covid19 api in a dictionary
    """
    location = ["areaName="+location, "areaType="+location_type]
    layout = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "cumDeathsByPublishDate": "cumDeathsByPublishDate",
        "newDeathsByPublishDate": "newDeathsByPublishDate",
        "hospitalCases": "hospitalCases",
        "newCasesByPublishDateChange": "newCasesByPublishDateChange"
        }
    api = Cov19API(
        filters = location,
        structure = layout,
        )
    #puts data in a list of dictionaries, each entry a new dictionary
    data = (api.get_json())["data"]
    return data



def set_local_data():
    """
    function to set local data
    """
    global_vars.local_data = covid_API_request()



def set_national_data():
    """
    function to set national data
    """
    global_vars.national_data = covid_API_request(config["nation"], "nation")



def schedule_covid_updates(update_interval, update_name, repeat):
    """
    using sched module to schedule updates to covid data
    putting updates in a list of dictionaries, so they can be deleted
    """
    sched_updates_dict = {}
    event_local = s.enter(update_interval, 1, set_local_data)
    sched_updates_dict["name"] = update_name
    sched_updates_dict["event"] = event_local
    sched_covid_updates.append(sched_updates_dict)

    sched_updates_dict = {}
    event_national = s.enter(update_interval, 1, set_national_data)
    sched_updates_dict["name"] = update_name
    sched_updates_dict["event"] = event_national
    sched_covid_updates.append(sched_updates_dict)
    
    if repeat == True:
        sched_updates_dict = {}
        event_repeat = s.enter(86400, 3, schedule_covid_updates,
                kwargs={"update_interval":update_interval, "update_name":update_name,
                        "repeat":repeat})
        sched_updates_dict["name"] = update_name
        sched_updates_dict["event"] = event_repeat
        sched_covid_updates.append(sched_updates_dict)
    s.run()



def delete_covid_update(update_name):
    """
    function to delete update from scheduler
    """
    for element in sched_covid_updates:
        if element["name"] == update_name:
            s.cancel(element["event"])
            sched_covid_updates.remove(element)
            delete_covid_update(update_name)
    s.run()




 





