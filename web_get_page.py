#!/usr/bin/python3.7
import sys
import os
#sys.path.append('/home/pi/.local/lib/python3.7/site-packages/pandas')
#sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import requests
import pandas as pd
import datetime

workfolder = '/home/pi/Desktop/'

def writelog(data):
    with open((workfolder + 'web_get_page.out'), 'a+') as f:
        f.write(data + '\n')
        
if os.path.exists(workfolder + 'web_get_page.out'):
  os.remove(workfolder + 'web_get_page.out') 


writelog(sys.version) 
writelog('Latest file - yesterday')
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
month = str(yesterday.month)
day = str(yesterday.day)
year = str(yesterday.year)
if len(month) < 2:
    month = '0' + month
if len(day) < 2:
    day = '0' + day
yesterdayfile = month + '-' + day + '-' + year + '.csv'
writelog(yesterdayfile)
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
url = urlbase + yesterdayfile
writelog(url)

writelog('Beginning file download with requests')
r = requests.get(url)
#filename = url[-14:]

if os.path.exists(workfolder + yesterdayfile):
  os.remove(workfolder + yesterdayfile)
  
 
  
#  /usr/bin/python3.7 /home/pi/Desktop/web_get_page.py > /home/pi/Desktop/web_get_page.out

with open((workfolder + yesterdayfile), 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
writelog(str(r.status_code))
writelog(r.headers['content-type'])
writelog(r.encoding)

df = pd.read_csv((workfolder +yesterdayfile), encoding = 'latin1')

#Finally, to drop by column number instead of by column label, try this to delete, e.g. the 1st, 2nd and 4th columns:
#   0               1               2       3   4           5           6       7           8     9         10            11                12                      13      14   15         16                17
#Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
#df = df.drop(df.columns[[0, 1, 3]], axis=1)  # df.columns is zero-based pd.Index
df = df.drop(df.columns[[                   1,                   3,   4,         5,                   7,          8,   9,          10,           11,             12,                              14,  15,        16,               17]], axis=1)
df = df[df.Province_State != 'Recovered']


# print(df)
writelog('these are the columns')
for col in df.columns:
    writelog(col)

html = df.to_html()
#print(html)

webpage = '/var/www/html/yesterday.html'
with open(webpage, 'wt') as f:
    f.write(html)

