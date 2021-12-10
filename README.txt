This is a file outlining the implementation and use of this project.
This project uses python, which should be already downloaded onto your computer as a default.
If you do not already have python downloaded, visit https://www.python.org/downloads/ and download the latest version of python


DOWNLOADING MODULES
The modules you will need:
    * flask
    * time
    * sched
    * logging
    * json
    * uk-covid19
    * requests
    * pytest
To download a module:
    * Open command prompt
    * Use the command "pip install ...", replacing ... with the module to download
    * If this does not work, try command: "python -m pip install ..."
      again replacing ... with the module to download


DOWNLOADING THE PROJECT
To download simply download all the given files into the same directory.
Then put the index.html file into a folder called templates in that directory.


GETTING AN API KEY
To be able to run this project, you will need an API key for the news API.
This will allow you to access data about news articles.
To get an API key:
    * Go to https://newsapi.org/ and click the button to get an API key.
    * Follow the instructions on the website, you do not need to pay money.
    * Then open the config.json file in the project.
    * Copy your API key in the speach marks next to "APIKEY": in the config.json file


THE CONFIG FILE
Aswell as putting your API key in the config.json file, you will also need to enter you country and city.
    * Open the config.json file.
    * In the speach marks next to "nation": type in your country, starting with a capital letter.
      E.g. "England"
    * In the speach marks next to "city": type in your city, starting with a capital letter. E.g. "London"


TESTING
You can quickly type pytest into your command prompt, to ensure there was no errors in downloading.
Though this is not necessary.


RUNNING THE PROJECT
To start using the covid project, you will have needed to get your API key, and put it in the config file,
and have downloaded all the needed modules.
Then:
    * Run the main.py file.
    * Open the sys.log file.
    * The first line in this file should start with "INFO:".
    * In this line it says "Running on " and then an url.
    * Put this url into the web browser, with the word "index" on the end.
    * You can look at news articles and set updates!


USING THE WEBPAGE
To get rid of a news article:
    * Simply cross it off and it will disapear.
To set an update:
    * Fill in the time of your desired update.
    * Then select the tick boxes for whether to update the news, data and whether to repeat the update.
    * Then press submit.
    * You will need to refresh the page after you submit if you wish to submit a new update,
      this will not remove your existing update.
    * To remove the update from the shown updates, cross it off. This will not stop the update from running.

