#web_get_page3.py
#version in rpi4gb
#from web_get_page2.py
#last modified
#8/9/2021 changed for population 2019
#8/3/2021 pics display only 7 and 30 days moving average, fixed negative deaths display
#8/2/2021 changed web page for moving averages
#7/22/2021 changed for VAERS pages

import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io
import matplotlib.pyplot as plt
# from IPython.core.display import HTML

# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = '/var/www/html/coronavirus/'
workfolder = '/home/pi/Documents/'
picsfolder = 'state_deaths/'
# csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv2/'
csvfolder = '/home/pi/Documents/'

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
    #to get missing date
    #file = '07' + '-' + '06' + '-' + '2021' + '.csv'
    return file

def make_html_TEMP(table, total):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + '</b><br>'
    s = s + 'Site under maintenance'
    s = s + '</body>'
    s = s + '</html>'
    webpage = webfolder + 'index.html'
    with open(webpage, 'wt') as f:
        f.write(s)

def make_html(webpage,table, total):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + ' - Total new deaths for today: ' + str(total) + '</b><br>'
    s = s + '<b>Blue: 7 days moving average  -  Orange: 30 days moving average</b><br>'
    
    if webpage == webfolder + 'index_coronavirus.html':
        s = s  + '<a href="index2_coronavirus.html">Sorted by Deaths_As_%_of Population_2019</a><p>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s  + '<a href="index_coronavirus.html">Sorted by New_Deaths</a><p>'

    s = s + table
    s = s + '<p>'

    if webpage == webfolder + 'index_coronavirus.html':
        s = s  + '<a href="index2_coronavirus.html">Sorted by Deaths_As_%_of Population_2019</a><p>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s  + '<a href="index_coronavirus.html">Sorted by New_Deaths</a><p>'

    s = s + '</body>'
    s = s + '</html>'
    # webpage = webfolder + 'index.html'
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

    #8/9/2021
    df_population = pd.read_csv((workfolder + 'population_usa_2019.csv'), encoding = 'UTF-8', thousands=',')
    df_population['State'] = df_population['State'].str.strip()
    df_population = df_population.rename(columns={"State": "Province_State", "Population estimate, July 1, 2019": "Population_2019"})
    df_population = df_population.set_index('Province_State')
    df_population = df_population[['Population_2019']].apply(pd.to_numeric)
    writelog('these are the columns - population_usa_2019.csv')
    for col in df_population.columns:
        writelog(col)
        print(col)

    country = ['US']
    
    df1 = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1', thousands=',', usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
    df = df1[df1['Country_Region'].isin(country)]
    df = df.set_index('Province_State')
    writelog('these are the columns - current day')
    for col in df.columns:
        writelog(col)
    dayago = today - datetime.timedelta(days=2)
    dayagofile = get_csv_filename(dayago)

    #1/22/2020 need to add check for missing previous day
    if os.path.exists(csvfolder + dayagofile):
        df_previous_day = pd.read_csv((csvfolder + dayagofile), encoding = 'latin1',thousands=',' ,usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
    else:
        df_previous_day = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1',thousands=',' ,usecols = ['Province_State','Country_Region','Last_Update','Deaths'])

    df_previous_day = df_previous_day.set_index('Province_State')
    df_previous_day = df_previous_day.drop(['Country_Region'], axis=1)

    #8/9/2021
    df_previous_day['Population_2019'] = df_population['Population_2019']
    df_previous_day['Deaths_As_%_of Population_2019'] = df_previous_day['Deaths'].divide(df_previous_day['Population_2019']) * 100

    df_previous_day['New_Deaths'] = np.where(df_previous_day['Deaths'] >= df['Deaths'], 0, df['Deaths'] - df_previous_day['Deaths']) #create new column in df1 for deaths diff
    df_previous_day = df_previous_day.sort_values(by=['New_Deaths', 'Province_State'])
    for col in df_previous_day.columns:
        writelog(col)
    total = df_previous_day['New_Deaths'].sum()
    writelog(str(total))

    # Create a list named states to store all the image paths
    states = picsfolder + df_previous_day.index + '.jpg'
    df_previous_day['Chart_New_Deaths'] = states
    writelog('state pics:')
    for x in states:
        writelog(x)

    # DO NOT ENABLE THIS, we miss states like New York
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.
    #df_previous_day = df_previous_day[np.abs(df_previous_day.Deaths-df_previous_day.Deaths.mean()) <= (3*df_previous_day.Deaths.std())]
    # Saving the dataframe as a webpage na_rep to prevent Nan in page for no values or null
    # df_previous_day.to_html(webpage,escape=False, formatters=dict(Chart=path_to_image_html))
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))

    webpage = webfolder + 'index_coronavirus.html'
    make_html(webpage, html, total)

    #sorted by Deaths_As_%_of Population_2019
    #8/9/2021
    df_previous_day = df_previous_day.sort_values(by=['Deaths_As_%_of Population_2019', 'Province_State'])
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))
    webpage = webfolder + 'index2_coronavirus.html'
    make_html(webpage, html, total)


# Run program 
if __name__ == '__main__':
    get_data()