#!/usr/bin/python3.7
#desktop version
#last modified
#6/24/2020 started to work on new report (no mortality rate, just deaths and differences
#6/19/2020 fixed bad data from source (imported manually missing csvs)
#5/27/2020 added df['Population_2018'] = carsdf['Population_2018']
#6/7/2020 adding full original report, fixed mortality rate
# (no info, means per million, 100,000 noted
#

import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io


# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = ''
workfolder = ''
csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv/'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'


def writelog(data):
    with open((workfolder + 'web_get_page.out'), 'a+') as f:
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
    #6/19/2020
    #file = year + '-'+ month + '-' + day + '.csv'
    return file

def get_data_to_csv(csvfile, urlbase):
    url = urlbase + csvfile
    writelog(url)
    writelog('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    if os.path.exists(csvfolder + csvfile):
        os.remove(csvfolder + csvfile)
    #6/17/2020
    with open((csvfolder + csvfile), 'wb') as f:
        f.write(r.content)
    #making backup
    # with open((workfolder + ('full_' + csvfile)), 'wb') as f:
    #     f.write(r.content)
    # Retrieve HTTP meta-data    
    writelog(str(r.status_code))
    writelog(r.headers['content-type'])
    writelog(r.encoding)
    writelog(csvfile)

def get_data():    
    if os.path.exists(workfolder + 'web_get_page.out'):
        os.remove(workfolder + 'web_get_page.out') 
    writelog(sys.version)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    writelog('Today:' + str(today))
    writelog('Latest file - yesterday:' + str(yesterday))
    weekago = today - datetime.timedelta(days=7)
    #weekago = today - datetime.timedelta(days=14)
    writelog('File -week ago:' + str(weekago))
    yesterdayfile = get_csv_filename(yesterday)
    weekagofile = get_csv_filename(weekago) 
    writelog(yesterdayfile)
    writelog(weekagofile)
    get_data_to_csv(yesterdayfile, urlbase)


    #----------------------------------adding car deaths 2018------------------------------
    #THIS IS A ONE TIME, DON'T REDO EVERYTIME (for later)
    # Province_State,Population_2018,Vehicle miles traveled (millions),Fatal crashes,Deaths_Car_2018,"Deaths per 100,000 population",Deaths per 100 million vehicle miles traveled
    #6/24/2020 added thousands=','
    carsdf = pd.read_csv((workfolder + 'car_accident_deaths_usa_2018.csv'), encoding = 'latin1', thousands=',')
    #new 6/9/2020 adding column Deaths per 100,000 population * 10
    carsdf['Cars_Mortality_Rate_2018'] = carsdf['Deaths per 100,000 population'] * 10
    writelog('these are the columns for car deaths 2018')
    carsdf = carsdf.set_index('Province_State')
    for col in carsdf.columns:
        writelog(col)
    html = carsdf.to_html()
    webpage = webfolder + 'car_accident_deaths_usa_2018.html'
    with open(webpage, 'wt') as f:
        f.write(html)
    #----------------------------------end of adding car deaths 2018--------------------------

    #--------------------------------adding all deaths 2018-----------------------------------
    # Province_State,Births,Fertility_Rate,Deaths,Death_Rate
    # file: deaths_usa_2018.csv
    deaths2018df = pd.read_csv((workfolder + 'deaths_usa_2018.csv'), encoding = 'latin1')
    deaths2018df = deaths2018df.set_index('Province_State')
    deaths2018df = deaths2018df.drop(['Births','Fertility_Rate'], axis=1)
    deaths2018df['Population_2018'] = carsdf['Population_2018']
    deaths2018df = deaths2018df.rename(columns={"Death_Rate": "Death_Rate_per_1000000"})
    #Deaths,Death_Rate,Population_2018
    writelog('these are the columns - all deaths 2018')
    for col in deaths2018df.columns:
        writelog(col)
    html2 = deaths2018df.to_html()
    webpage2 = webfolder + 'deaths_usa_2018.html'
    with open(webpage2, 'wt') as f:
         f.write(html2)
    #---------------------------------end of adding all deaths 2018---------------------------

    #6/12/2020
    country = ['US']
    #6/17/2020
    df1 = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1')
    # df = df1[df1.Country_Region='US']
    df = df1[df1['Country_Region'].isin(country)]


    df = df.set_index('Province_State')
    #6/12/2020
    writelog('these are the columns - current day')
    for col in df.columns:
        writelog(col)

    # for later: check for no file FileNotFoundError: [Errno 2] No such file or directory: '05-02-2020.csv'
    #6/17/2020
    if os.path.exists(csvfolder + weekagofile) == False:
        weekagofile = yesterdayfile

    #6/17/2020
    df_previous = pd.read_csv((csvfolder + weekagofile), encoding = 'latin1')
    df_previous = df_previous.set_index('Province_State')

    #New 6/7/2020, saving full report with all the original columns
    writelog('these are all the columns - current full')
    #Country_Region,Last_Update Lat Long_ Confirmed Deaths
    # Recovered Active FIPS Incident_Rate
    # People_Tested People_Hospitalized Mortality_Rate UID
    #ISO3 Testing_Rate Hospitalization_Rate
    for col in df.columns:
        writelog(col)
    html = df.to_html()
    webpage = webfolder + 'full_daily_report.html'
    with open(webpage, 'wt') as f:
        f.write(html)

    #Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
    df = df.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3',    'Testing_Rate',    'Hospitalization_Rate'], axis=1)
    #added population 2018
    df['Population_2018'] = carsdf['Population_2018']
    writelog('these are the columns - current after dropping columns')
    #Last_Update Deaths Mortality_Rate Population_2018
    for col in df.columns:
        writelog(col)
    html = df.to_html()
    webpage = webfolder + 'yesterday.html'
    with open(webpage, 'wt') as f:        
        f.write(html)
        
    df_previous = df_previous.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3',    'Testing_Rate',    'Hospitalization_Rate'], axis=1)
    writelog('these are the columns - previous')
    for col in df_previous.columns:
        writelog(col)
    html = df_previous.to_html()
    webpage = webfolder + 'previous.html'
    with open(webpage, 'wt') as f:        
        f.write(html)


    #link to cars dataframe
    df_previous['Population_2018'] = carsdf['Population_2018']
    df_previous['Deaths_Car_2018'] = carsdf['Deaths_Car_2018']
    # df_previous['Cars_2018_Death_Rate_Per_100000'] = carsdf['Deaths per 100,000 population']
    #new 6/9/2020 carsdf['Cars_Mortality_Rate_2018']
    df_previous['Cars_Mortality_Rate_2018'] = carsdf['Cars_Mortality_Rate_2018']

    #link to deaths 2018 dataframe
    df_previous['Deaths_All_2018'] = deaths2018df['Deaths']
    df_previous['Mortality_Rate_All_Causes_2018'] = deaths2018df['Death_Rate_per_1000000']


    #links to current week
    df_previous['Deaths_After'] = df['Deaths']                 #add the Price2 column from df2 to df1
    df_previous['Mortality_Rate_After'] = df['Mortality_Rate'] #add the Price2 column from df2 to df1
    df_previous['Deaths_Diff_After'] = np.where(df_previous['Deaths'] == df['Deaths'], 0, df['Deaths'] - df_previous['Deaths']) #create new column in df1 for price diff
    df_previous['Mortality_Rate_Diff'] = np.where(df_previous['Mortality_Rate'] == df['Mortality_Rate'], 0, df['Mortality_Rate'] - df_previous['Mortality_Rate']) #create new column in df1 for price diff

    # exporting to csv before sorting by Deaths diff

    df_previous.to_csv(workfolder + 'Differences_Report.csv')


    #df_previous = df_previous.sort_values(by=['Deaths Diff'])
    df_previous = df_previous.sort_values(by=['Mortality_Rate_Diff'])

    writelog('these are the columns - added Mortality Rate After, Deaths After, MD Diff, Deaths Diff, Deaths_2018, Death_Rate_2018')
    for col in df_previous.columns:
        writelog(col)
    html = df_previous.to_html()
    webpage = webfolder + 'difference.html'
    with open(webpage, 'wt') as f:
        f.write(html)

    #making backup of differences
    webpage = webfolder + str(today) + '-difference.html'
    with open(webpage, 'wt') as f:
        f.write(html)

    #NEW REPORT 6/24/2020
    df_previous = df_previous.sort_values(by=['Province_State'])
    df_new = df_previous.drop(['Mortality_Rate','Cars_Mortality_Rate_2018', 'Mortality_Rate_All_Causes_2018','Mortality_Rate_After','Mortality_Rate_Diff'], axis=1)
    df_new['Deaths_Diff_%_of Population_2018'] = df_new['Deaths_Diff_After'].divide(df_new['Population_2018']) * 100
    df_new['Deaths_Cars_%_of Population_2018'] = df_new['Deaths_Car_2018'].divide(df_new['Population_2018']) * 100
    df_new = df_new.sort_values(by=['Deaths_Diff_%_of Population_2018'])

    writelog('these are the columns of the new report')
    for col in df_new.columns:
        writelog(col)
    html = df_new.to_html()
    webpage = webfolder + 'differences_new.html'
    with open(webpage, 'wt') as f:
        f.write(html)


# Run program 
if __name__ == '__main__':
    get_data()
