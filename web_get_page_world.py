#!/usr/bin/python3.7
#desktop version, Spain
#last modified
#created 6/12/2020


import sys
import os
import requests
import pandas as pd
#import numpy as np
import datetime

# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = '/var/www/html/'
workfolder = '/home/pi/Desktop/'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def writelog(data):
    with open((workfolder + 'web_get_page_spain.out'), 'a+') as f:
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
    #making backup
    with open((workfolder + ('full_' + csvfile)), 'wb') as f:
        f.write(r.content)
    # Retrieve HTTP meta-data    
    writelog(str(r.status_code))
    writelog(r.headers['content-type'])
    writelog(r.encoding)
    writelog(csvfile)

def get_data():    
    if os.path.exists(workfolder + 'web_get_page_spain.out'):
        os.remove(workfolder + 'web_get_page_spain.out') 
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

    #6/12/2020
    # country = ['Spain', 'France','Sweden']
    country = ['Spain']
    df1 = pd.read_csv((workfolder + yesterdayfile), encoding = 'latin1')
    # df = df1[df1.Country_Region='US']
    df = df1[df1['Country_Region'].isin(country)]
    df = df.set_index('Province_State')
    #6/12/2020
    # writelog('these are the columns - current day')
    # for col in df.columns:
    #     writelog(col)

    # for later: check for no file FileNotFoundError: [Errno 2] No such file or directory: '05-02-2020.csv'
    # if os.path.exists(workfolder + weekagofile) == False:
    #     weekagofile = yesterdayfile

    # df_previous = pd.read_csv((workfolder + weekagofile), encoding = 'latin1')
    # df_previous = df_previous.set_index('Province_State')

    #New 6/7/2020, saving full report with all the original columns
    #writelog('these are all the columns - current full')
    #Country_Region,Last_Update Lat Long_ Confirmed Deaths
    # Recovered Active FIPS Incident_Rate
    # People_Tested People_Hospitalized Mortality_Rate UID
    #ISO3 Testing_Rate Hospitalization_Rate
    df = df.drop(['Lat', 'Long_', 'FIPS', 'Admin2'], axis=1)
    for col in df.columns:
        writelog(col)
    html = df.to_html()
    webpage = webfolder + 'daily_report_spain.html'
    with open(webpage, 'wt') as f:
        f.write(html)
    # FIPS  Admin2  Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  Combined_Key    Incidence_Rate  Case-Fatality_Ratio
    #Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
    #df = df.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3',    'Testing_Rate',    'Hospitalization_Rate'], axis=1)
    # df = df.drop(['Country_Region','Lat', 'Long_', 'FIPS', 'Admin2'], axis=1)


        
    # df_previous = df_previous.drop(['Country_Region','Lat', 'Long_','Confirmed','Recovered',   'Active',  'FIPS',    'Incident_Rate',   'People_Tested',   'People_Hospitalized',  'UID', 'ISO3',    'Testing_Rate',    'Hospitalization_Rate'], axis=1)
    # writelog('these are the columns - previous')
    # for col in df_previous.columns:
    #     writelog(col)
    # html = df_previous.to_html()
    # webpage = webfolder + 'previous.html'
    # with open(webpage, 'wt') as f:
    #     f.write(html)


    #links to current week
    # df_previous['Deaths_After'] = df['Deaths']                 #add the Price2 column from df2 to df1
    # df_previous['Mortality_Rate_After'] = df['Mortality_Rate'] #add the Price2 column from df2 to df1
    # df_previous['Deaths_Diff_After'] = np.where(df_previous['Deaths'] == df['Deaths'], 0, df['Deaths'] - df_previous['Deaths']) #create new column in df1 for price diff
    # df_previous['Mortality_Rate_Diff'] = np.where(df_previous['Mortality_Rate'] == df['Mortality_Rate'], 0, df['Mortality_Rate'] - df_previous['Mortality_Rate']) #create new column in df1 for price diff
    #
    # # exporting to csv before sorting by Deaths diff
    #
    # df_previous.to_csv(workfolder + 'Differences_Report.csv')


    #df_previous = df_previous.sort_values(by=['Deaths Diff'])
    # df_previous = df_previous.sort_values(by=['Mortality_Rate_Diff'])
    #
    # writelog('these are the columns - added Mortality Rate After, Deaths After, MD Diff, Deaths Diff, Deaths_2018, Death_Rate_2018')
    # for col in df_previous.columns:
    #     writelog(col)
    # html = df_previous.to_html()
    # webpage = webfolder + 'difference.html'
    # with open(webpage, 'wt') as f:
    #     f.write(html)
    #
    # #making backup of differences
    # webpage = webfolder + str(today) + '-difference.html'
    # with open(webpage, 'wt') as f:
    #     f.write(html)


# Run program 
if __name__ == '__main__':
    get_data()
