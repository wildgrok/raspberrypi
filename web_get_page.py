#!/usr/bin/python3.7
import sys
import os
#sys.path.append('/home/pi/.local/lib/python3.7/site-packages/pandas')
#sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import requests
import pandas as pd
import numpy as np
import datetime

workfolder = '/home/pi/Desktop/'

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

def get_data_to_csv(csvfile):
    urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
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
      
    get_data_to_csv(yesterdayfile)
    

    df = pd.read_csv((workfolder + yesterdayfile), encoding = 'latin1')
    df_previous = pd.read_csv((workfolder + weekagofile), encoding = 'latin1')
    #Finally, to drop by column number instead of by column label, try this to delete, e.g. the 1st, 2nd and 4th columns:
    #   0               1               2       3   4           5           6       7           8     9         10            11                12                      13      14   15         16                17
    #Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
    #df = df.drop(df.columns[[0, 1, 3]], axis=1)  # df.columns is zero-based pd.Index
    df = df.drop(df.columns[[                   1,                   3,   4,         5,                   7,          8,   9,          10,           11,             12,                              14,  15,        16,               17]], axis=1)
    df = df[df.Province_State != 'Recovered']
    writelog('these are the columns - current')
    for col in df.columns:
        writelog(col)
    html = df.to_html()
    webpage = '/var/www/html/yesterday.html'
    #with open(webpage, 'wt') as f:
    with open(webpage, 'wt') as f:        
        f.write(html)
        
    #To be fixed using function
    df_previous = df_previous.drop(df_previous.columns[[                   1,                   3,   4,         5,                   7,          8,   9,          10,           11,             12,                              14,  15,        16,               17]], axis=1)
    df_previous = df_previous[df_previous.Province_State != 'Recovered']
    writelog('these are the columns - previous')
    for col in df_previous.columns:
        writelog(col)
    html = df_previous.to_html()
    webpage = '/var/www/html/previous.html'
    #with open(webpage, 'wt') as f:
    with open(webpage, 'wt') as f:        
        f.write(html)        
    
    #added 5/9/2020
    df_previous['Mortality_Rate After'] = df['Mortality_Rate'] #add the Price2 column from df2 to df1
    df_previous['MD Diff'] = np.where(df_previous['Mortality_Rate'] == df['Mortality_Rate'], 0, df['Mortality_Rate'] - df_previous['Mortality_Rate']) #create new column in df1 for price diff
    df_previous = df_previous.sort_values(by=['MD Diff'])
    writelog('these are the columns - added Mortality Rate After and MD Diff')
    for col in df_previous.columns:
        writelog(col)
    html = df_previous.to_html()
    webpage = '/var/www/html/difference.html'
    with open(webpage, 'wt') as f:
        f.write(html)
    #making backup of differences
    webpage = '/var/www/html/' + str(today) + '-difference.html'
    with open(webpage, 'wt') as f:
        f.write(html)
    
    

# Run program 
if __name__ == '__main__':
    get_data()
