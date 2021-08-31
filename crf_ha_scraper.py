from selenium import webdriver # pip install selenium
import time
#from datetime import datetime  # pip install datetime
#from bs4 import BeautifulSoup
#import os
#import csv
#import mysql.connector
#import pandas as pd
#from sqlalchemy import create_engine

PATH = "C:/Program Files (x86)/chromedriver"  # Change path to driver location

username = "cuberootfarms"
password = "cuberootfarms1@"

driver = webdriver.Chrome(PATH)

driver.get("http://192.168.100.242:8123/")
time.sleep(15)

driver.execute_script(
    "return document.querySelector('ha-authorize').shadowRoot.querySelector('ha-auth-flow').shadowRoot.querySelector("
    "'ha-form').shadowRoot.querySelector('ha-form').shadowRoot.querySelector("
    "'ha-form-string').shadowRoot.querySelector('paper-input').shadowRoot.querySelector('input')").send_keys(
    username)

driver.execute_script(
    "return document.querySelector('ha-authorize').shadowRoot.querySelector('ha-auth-flow').shadowRoot.querySelector("
    "'ha-form').shadowRoot.querySelectorAll('ha-form')[1].shadowRoot.querySelector("
    "'ha-form-string').shadowRoot.querySelector('paper-input').shadowRoot.querySelector('input')").send_keys(
    password)

driver.execute_script(
    "return document.querySelector('ha-authorize').shadowRoot.querySelector('ha-auth-flow').shadowRoot.querySelector("
    "'mwc-button')").click()

time.sleep(15)

driver.execute_script(
    "return document.querySelector('home-assistant').shadowRoot.querySelector("
    "'ha-store-auth-card').shadowRoot.querySelectorAll('mwc-button')[1]").click()

Temperature = driver.execute_script(
    "return document.querySelector('home-assistant').shadowRoot.querySelector("
    "'home-assistant-main').shadowRoot.querySelector('ha-panel-lovelace').shadowRoot.querySelector("
    "'hui-root').shadowRoot.querySelector('hui-masonry-view').shadowRoot.querySelectorAll('hui-state-label-badge')["
    "3].shadowRoot.querySelector('ha-state-label-badge').shadowRoot.querySelector("
    "'ha-label-badge').shadowRoot.querySelector('span')").text

Humidity = driver.execute_script(
    "return document.querySelector('home-assistant').shadowRoot.querySelector("
    "'home-assistant-main').shadowRoot.querySelector('ha-panel-lovelace').shadowRoot.querySelector("
    "'hui-root').shadowRoot.querySelector('hui-masonry-view').shadowRoot.querySelectorAll('hui-state-label-badge')["
    "5].shadowRoot.querySelector('ha-state-label-badge').shadowRoot.querySelector("
    "'ha-label-badge').shadowRoot.querySelector('span')").text

#print(Temperature)

#print(Humidity)

driver.quit()



date = str(datetime.date(datetime.now()))  # Gives current date

t = time.localtime()
time = time.strftime("%H:%M:%S", t)  # Gives current time

Temperature_str = str(Temperature)
Humidity_str = str(Humidity)

>>>csv information

# stored_information forms a commas separated line in the format relative to the website
stored_information = date + " " + time + "," + Temperature + "," + Humidity
# header is the column headers for the csv file
header = "insert column header here" + "\n"
# create crf.csv file
file = open(os.path.expanduser("crf.csv"), "wb")
# write headers to csv file
file.write(bytes(header, encoding="ascii", errors='ignore'))
# write the formatted information to csv file
file.write(bytes(stored_information, encoding="ascii", errors='ignore'))
file.close()





>>>sql code

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="TeamValor2007",
    database="covid_19"
)

mycursor = mydb.cursor()

# most recent data which was exported from the database as a CSV via SQL query
db_query = pd.read_sql(
    "SELECT * FROM countries c1 WHERE c1.date = (SELECT MAX(c2.date) FROM countries c2 WHERE c2.country = c1.country) GROUP BY country ORDER BY country;",
    mydb)

# saves most recent country data query as a csv
db_query.to_csv('covid_19.csv')

# reads in database data from csv so that it can be used in operations
db_data = pd.read_csv('covid_19.csv')

# test data which will be scraped from COVID website (only one line of data per scraped csv file)
new_data = pd.read_csv("Bahamas.csv")

# stores scraped data information as variables for comparison

new_country = new_data.at[0, "country"]
new_positive_samples = new_data.at[0, "positive_samples"]
new_active_cases = new_data.at[0, "active_cases"]
new_recovered = new_data.at[0, "recovered"]
new_deaths = new_data.at[0, "deaths"]

# each country's row is checked to see if its country name matches with the new data's country name
for row in range(0, 4):
    db_country = db_data.at[row, "country"]

    if new_country == db_country:
        db_positive_samples = db_data.at[row, "positive_samples"]
        db_active_cases = db_data.at[row, "active_cases"]
        db_deaths = db_data.at[row, "deaths"]
        db_recovered = db_data.at[row, "recovered"]

        # if the new data's date is more recent or its data is different than the current, the new data is inserted
        if new_positive_samples > db_positive_samples or new_active_cases != db_active_cases or new_recovered > db_recovered or new_deaths > db_deaths:
            engine = create_engine(
                'mysql+mysqlconnector://root:TeamValor2007@localhost/covid_19')  # creates connection to mysql database
            new_data.to_sql('countries', con=engine, index=False,
                            if_exists='append')  # inserts the new data into the mysql database

exec(open('5. CSV to JSON Converter.py').read())
