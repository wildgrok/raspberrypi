#!/usr/bin/python3.7
#Last modified 5/12/2020
import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime

workfolder = '/home/pi/Desktop/'
webfolder  = '/var/www/html/'
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
    return file

def get_data_to_csv(csvfile, urlbase):
    url = urlbase + csvfile
    writelog(url)
    writelog('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    if os.path.exists(workfolder + csvfile):
        os.remove(workfolder + csvfile)
    with open((workfolder + csvfile), 'wb') as f:
        f.write(r.content)
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
    writelog('File -week ago:' + str(weekago))  
    yesterdayfile = get_csv_filename(yesterday)
    weekagofile = get_csv_filename(weekago) 
    writelog(yesterdayfile)
    writelog(weekagofile)
      
    get_data_to_csv(yesterdayfile, urlbase)
    
    #----------------------------------adding car deaths 2018------------------------------
    carsdf = pd.read_csv((workfolder + 'car_accident_deaths_usa_2018.csv'), encoding = 'latin1')
    writelog('these are the columns for car deaths 2018')
    carsdf = carsdf.set_index('Province_State')
    for col in carsdf.columns:
        writelog(col)
    html = carsdf.to_html()
    webpage = workfolder + 'car_accident_deaths_usa_2018.html'
    with open(webpage, 'wt') as f:
        f.write(html)
    #----------------------------------end of adding car deaths 2018--------------------------

    df = pd.read_csv((workfolder + yesterdayfile), encoding = 'latin1')
    df = df.set_index('Province_State')   
    if os.path.exists(workfolder + weekagofile):
        df_previous = pd.read_csv((workfolder + weekagofile), encoding = 'latin1')
    else:
        writelog("Missing previous file " + weekagofile)
        #temp fix to continue process 
        df_previous = pd.read_csv((workfolder + yesterdayfile), encoding = 'latin1')
    df_previous = df_previous.set_index('Province_State')


    #Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
    df = df.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3',    'Testing_Rate',    'Hospitalization_Rate'], axis=1)

    writelog('these are the columns - current')
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

    df_previous['Population_2018'] = carsdf['Population_2018']
    df_previous['Deaths_Car_2018'] = carsdf['Deaths_Car_2018']

    df_previous['Mortality_Rate After'] = df['Mortality_Rate'] #add the Price2 column from df2 to df1
    df_previous['Deaths After'] = df['Deaths']                 #add the Price2 column from df2 to df1
    df_previous['Deaths Diff'] = np.where(df_previous['Deaths'] == df['Deaths'], 0, df['Deaths'] - df_previous['Deaths']) #create new column in df1 for price diff
    df_previous['Mortality Death Diff'] = np.where(df_previous['Mortality_Rate'] == df['Mortality_Rate'], 0, df['Mortality_Rate'] - df_previous['Mortality_Rate']) #create new column in df1 for price diff


    #df_previous = df_previous.sort_values(by=['Deaths Diff'])
    df_previous = df_previous.sort_values(by=['Mortality Death Diff'])

    writelog('these are the columns - added Mortality Rate After, Deaths After, MD Diff, Deaths Diff')
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


# Run program 
if __name__ == '__main__':
    get_data()
