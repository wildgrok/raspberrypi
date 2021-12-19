#!/usr/bin/python3.7
#version in rpi 6205 from dell laptop 12/19/2021
#last modified
#12/19/2021 testing on rpi 6205
#12/11/2021 reconfiguring for all countries
#created 6/12/2020


import sys
import os
from numpy import longlong
import requests
import pandas as pd
#import numpy as np
import datetime

# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = '/var/www/html/coronavirus/'
workfolder = '/home/pi/Documents/'
csvfolder = '/home/pi/Documents/csv_world/'
#webfolder = 'c:/coronavirus/'
#workfolder = 'c:/coronavirus/'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
world_population = 'world_population_2020.csv'
world_deaths = 'world_deaths.csv'

def writelog(data):
    with open((workfolder + 'web_get_page_world.out'), 'a+') as f:
        f.write(data + '\n')

def make_webpage(df, webpage):
    # df = df.to_html(float_format='{:20,.2f}'.format)
    html = df.to_html(na_rep='', float_format='{:20}'.format)
    webpage = webfolder + webpage
    with open(webpage, 'wt') as f:
        f.write(html)
        
        
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
# csvfile is in form 12-15-2021.csv
def get_data_to_csv(csvfile, urlbase):
    url = urlbase + csvfile
    writelog(url)
    writelog('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    #if os.path.exists(workfolder + csvfile):
    if os.path.exists(csvfolder + csvfile):
        os.remove(csvfolder + csvfile)
    with open((csvfolder + csvfile), 'wb') as f:
        f.write(r.content)
    #making backup
    # with open((workfolder + ('full_' + csvfile)), 'wb') as f:
    #     f.write(r.content)
    # Retrieve HTTP meta-data    
    #writelog(str(r.status_code))
    #writelog(r.headers['content-type'])
    #writelog(r.encoding)
    #writelog(csvfile)

def get_data():    
    if os.path.exists(workfolder + 'web_get_page_world.out'):
        os.remove(workfolder + 'web_get_page_world.out') 
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterdayfile = get_csv_filename(yesterday)
    get_data_to_csv(yesterdayfile, urlbase)
    df1 = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1')
    df = df1.set_index('Country_Region')
    # these are all the columns
    #Country_Region,Last_Update Lat Long_ Confirmed Deaths
    # Recovered Active FIPS Incident_Rate
    # People_Tested People_Hospitalized Mortality_Rate UID
    #ISO3 Testing_Rate Hospitalization_Rate
    # 
    df = df.drop(['Province_State', 'Lat', 'Long_', 'FIPS', 'Admin2', 'Confirmed', 'Recovered', 'Active','Combined_Key',	'Incident_Rate',	'Case_Fatality_Ratio'], axis=1)
    df = df.groupby(['Country_Region'])['Deaths'].sum().reset_index()
    df.rename(columns = {'Country_Region':'Province_State'}, inplace = True)
    make_webpage(df, 'daily_report_world.html')

    return df

# new 12/14/2021
def get_world_population():
    file = workfolder + world_population
    columns = [r"Country Name", r"2020"]
    df1 = pd.read_csv(file, encoding='latin1',thousands=',', low_memory=False, usecols = columns)
    #rename
    df1.rename(columns = {'Country Name':'Province_State','2020':'Population'}, inplace = True)
    # df = df1.set_index('Province_State')
    df1.to_csv( workfolder + 'world_population_2020_dataframe.csv', index=True, encoding='utf-8')
    for col in df1.columns:
        print(col)
    #12/18/2021
    #make fixes
    # df1.at['US', 'Province_State'] = 'United States'
    df1.loc[df1.Province_State =='United States' ,'Province_State'] = 'US'
    df1.loc[df1.Province_State =='Russian Federation' ,'Province_State'] = 'Russia'
    df1.loc[df1.Province_State =='Slovak Republic' ,'Province_State'] = 'Slovakia'
    df1.loc[df1.Province_State =='Syrian Arab Republic' ,'Province_State'] = 'Syria'
    df1.loc[df1.Province_State =='Egypt, Arab Rep.' ,'Province_State'] = 'Egypt'
    df1.loc[df1.Province_State =='Yemen, Rep.' ,'Province_State'] = 'Yemen'
    df1.loc[df1.Province_State =='Venezuela, RB' ,'Province_State'] = 'Venezuela'
    df1.loc[df1.Province_State =='Lao PDR' ,'Province_State'] = 'Laos'
    df1.loc[df1.Province_State =='Kyrgyz Republic' ,'Province_State'] = 'Kyrgyzstan'
    df1.loc[df1.Province_State =='Bahamas, The' ,'Province_State'] = 'Bahamas'
    df1.loc[df1.Province_State =='Czech Republic' ,'Province_State'] = 'Czechia'
    df1.loc[df1.Province_State =='Iran, Islamic Rep.' ,'Province_State'] = 'Iran'
    df1.loc[df1.Province_State =='Gambia, The' ,'Province_State'] = 'Gambia'
    # Slovak Republic
    # Syrian Arab Republic
    # Egypt, Arab Rep.
    # Yemen, Rep.
    # Venezuela, RB
    # Lao PDR
    # Kyrgyz Republic
    # 	Bahamas, The
    # Czech Republic
    # Iran, Islamic Rep.
    # 	Gambia, The
    make_webpage(df1, 'world_population_2020.html')
    return df1

def get_data_world():
    # get countries deaths
    df = get_data()
    # get_world_population()
    df2 = get_world_population()
    # add population
    df = df.join(df2.set_index('Province_State'), on='Province_State')
    # add deaths as % of population
    df['Deaths_As_%_of Population'] = df['Deaths'].divide(df['Population']) * 100
    # make web page
    make_webpage(df, 'world_deaths_and_population.html')
    # sorted by deaths as % of population
    df = df.sort_values(by=['Deaths_As_%_of Population'], ascending=[False])
    make_webpage(df, 'world_deaths_and_population2.html')

# Run program 
if __name__ == '__main__':
    get_data_world()