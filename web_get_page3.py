#!/usr/bin/python3.7
#desktop version
#web_get_page2.py
#version in desktop
#from web_get_page.py as of 8/13/2020
#last modified
#11/24/2020 workimg adding display of jpg, not ready yet
#11/11/2020 fixing error see file errors_11_11_2020.txt
#KeyError: "['People_Tested' 'Mortality_Rate'] not found in axis" in line 131


import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io
import matplotlib.pyplot as plt
from IPython.core.display import HTML

# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = ''
workfolder = ''
# picsfolder = 'C:/Users/python/PycharmProjects/coronavirus//'
# picsfolder = 'C:\\Users\\python\\PycharmProjects\\coronavirus\\state_deaths\\'
picsfolder = 'coronavirus/state_deaths/'

csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv2/'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
#11/24/2020
def path_to_image_html(path):
    return '<img src="'+ path + '" width="200" >'

def writelog(data):
    with open((workfolder + 'web_get_page2.out'), 'a+') as f:
        f.write(data + '\n')
        
def get_csv_filename(datestr):
    month = str(datestr.month)
    day = str(datestr.day)
    year = str(datestr.year)
    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day
    file = month + '-' + day + '-' + year + '.csv'
    return file

def make_html_TEMP(table, total):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + '</b><br>'
    s = s + 'Site under maintenance'
    # s = s + table
    # s = s + '<b> Total new deaths for today: ' + str(total) + '</b>'
    # s = s + '<p>'
    # s = s  + '<a href="references2.html">Misc links</a><p>'
    # s = s  + '<a href="index_old.html">Link to original site</a><p>'
    s = s + '</body>'
    s = s + '</html>'
    webpage = webfolder + 'index.html'
    with open(webpage, 'wt') as f:
        f.write(s)

def make_html(table, total):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + '</b><br>'
    s = s + table
    s = s + '<b> Total new deaths for today: ' + str(total) + '</b>'
    s = s + '<p>'
    s = s  + '<a href="references2.html">Misc links</a><p>'
    s = s  + '<a href="index_old.html">Link to original site</a><p>'
    s = s + '</body>'
    s = s + '</html>'
    webpage = webfolder + 'index3.html'
    with open(webpage, 'wt') as f:
        f.write(s)

def get_data_to_csv(csvfile, urlbase):
    url = urlbase + csvfile
    writelog(url)
    writelog('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    if os.path.exists(csvfolder + csvfile):
        os.remove(csvfolder + csvfile)
    with open((csvfolder + csvfile), 'wb') as f:
        f.write(r.content)
    writelog(str(r.status_code))
    writelog(r.headers['content-type'])
    writelog(r.encoding)
    writelog(csvfile)

def get_data():    
    if os.path.exists(workfolder + 'web_get_page2.out'):
        os.remove(workfolder + 'web_get_page2.out')
    writelog(sys.version)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    writelog('Today:' + str(today))
    writelog('Latest file - yesterday:' + str(yesterday))
    yesterdayfile = get_csv_filename(yesterday)
    writelog(yesterdayfile)
    get_data_to_csv(yesterdayfile, urlbase)


    #----------------------------------adding car deaths 2018, needed for population 2018------------------------------
    carsdf = pd.read_csv((workfolder + 'car_accident_deaths_usa_2018.csv'), encoding = 'latin1', thousands=',')
    #8/13/2020 only need population and car deaths
    carsdf = carsdf.set_index('Province_State')
    carsdf = carsdf.drop(['Vehicle miles traveled (millions)','Fatal crashes', "Deaths per 100,000 population", 'Deaths per 100 million vehicle miles traveled'], axis=1)
    carsdf = carsdf[['Population_2018']].apply(pd.to_numeric)
    writelog('these are the columns for car deaths 2018')

    for col in carsdf.columns:
        writelog(col)
    html_cars = carsdf.to_html()
    webpage = webfolder + 'car_accident_deaths_usa_2018_2.html'
    with open(webpage, 'wt') as f:
        f.write(html_cars)
    #----------------------------------end of adding car deaths 2018--------------------------



    #--------------------------------adding all deaths 2018-----------------------------------
    # Province_State,Births,Fertility_Rate,Deaths,Death_Rate
    # file: deaths_usa_2018.csv
    deaths2018df = pd.read_csv((workfolder + 'deaths_usa_2018.csv'), encoding = 'latin1', thousands=',')
    deaths2018df = deaths2018df.set_index('Province_State')
    deaths2018df = deaths2018df.drop(['Births','Fertility_Rate','Death_Rate'], axis=1)
    #Adding population 2018
    deaths2018df['Population_2018'] = carsdf['Population_2018']
    deaths2018df = deaths2018df.rename(columns={"Deaths": "Deaths_All_Causes"})
    #Deaths,Population_2018
    writelog('these are the columns - all deaths 2018')
    for col in deaths2018df.columns:
        writelog(col)
    #---------------------------------end of adding all deaths 2018---------------------------


    country = ['US']
    df1 = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1')
    df = df1[df1['Country_Region'].isin(country)]
    df = df.set_index('Province_State')
    writelog('these are the columns - current day')
    for col in df.columns:
        writelog(col)
    dayago = today - datetime.timedelta(days=2)
    dayagofile = get_csv_filename(dayago)
    df_previous_day = pd.read_csv((csvfolder + dayagofile), encoding = 'latin1',thousands=',')
    df_previous_day = df_previous_day.set_index('Province_State')

    #11/11/2020
    # df_previous_day = df_previous_day.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3', 'Testing_Rate', 'Hospitalization_Rate', 'Mortality_Rate'], axis=1)
    df_previous_day = df_previous_day.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',                        'People_Hospitalized',  'UID', 'ISO3', 'Testing_Rate', 'Hospitalization_Rate'                  ], axis=1)
    df_previous_day = df_previous_day.drop(['Total_Test_Results',	'Case_Fatality_Ratio'], axis=1)


    df_previous_day['Population_2018'] = carsdf['Population_2018']
    df_previous_day['Deaths_As_%_of Population_2018'] = df_previous_day['Deaths'].divide(df_previous_day['Population_2018']) * 100
    df_previous_day['New_Deaths'] = np.where(df_previous_day['Deaths'] == df['Deaths'], 0, df['Deaths'] - df_previous_day['Deaths']) #create new column in df1 for price diff
    df_previous_day = df_previous_day.sort_values(by=['New_Deaths'])
    for col in df_previous_day.columns:
        writelog(col)
    total = df_previous_day['New_Deaths'].sum()
    print(total)
    # states = sorted(picsfolder + df_previous_day.index + '.jpg')
    states = picsfolder + df_previous_day.index + '.jpg'
    # print(states)
    # Create a list named country to store all the image paths
    # country = ['https://www.countries-ofthe-world.com/flags-normal/flag-of-United-States-of-America.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Brazil.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Russia.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-India.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Peru.png']
    # # Assigning the new list as a new column of the dataframe
    # df['Country'] = country
    df_previous_day['States'] = states



    # df_previous_day.to_html('webpage.html',escape=False, formatters=dict(States=path_to_image_html))


    # Rendering the dataframe as HTML table
    df_previous_day.to_html(escape=False, formatters=dict(States=path_to_image_html))
    # Rendering the images in the dataframe using the HTML method.
    # HTML(df_previous_day.to_html(escape=False,formatters=dict(States=path_to_image_html)))

    webpage = webfolder + 'index3.html'

    # Saving the dataframe as a webpage
    df_previous_day.to_html(webpage,escape=False, formatters=dict(States=path_to_image_html))












    # html = df_previous_day.to_html(na_rep='')
    # make_html(html, total)

    #11/24/2020 working on this
    #img src="'+ path + '" width="60" >
    #df_previous_day['Chart'] = '<img src=C:\\Users\\python\\PycharmProjects\\coronavirus\\state_deaths\\' + df_previous_day.index + '.jpg width 60>'
    # df_previous_day['pics'] = picsfolder +  df_previous_day.index + '.jpg'
    # country = df_previous_day['Chart']
    # print(country)
    # df.to_html(escape=False, formatters=dict(Country=path_to_image_html))
    #html = df_previous_day.to_html(escape=False, formatters=dict(Country=path_to_image_html))
    # html = HTML(df_previous_day.to_html(escape=False,formatters=dict(Country=path_to_image_html)))
    # print(html)
    #
    # html = df_previous_day.to_html(webpage,escape=False, formatters=dict(pics=path_to_image_html))
    # webpage = webfolder + 'index3.html'
    # with open(webpage, 'wt') as f:
    #      f.write(f)
    # Saving the dataframe as a webpage
    # df_previous_day.to_html(webpage,escape=False, formatters=dict(Country=path_to_image_html))

# Run program 
if __name__ == '__main__':
    get_data()
