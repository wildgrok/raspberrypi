#!/usr/bin/env python
import requests
import pandas as pd
import datetime

workfolder = '/home/pi/Desktop/'

print('Latest file - yesterday')
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
print(yesterdayfile)
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
url = urlbase + yesterdayfile
print(url)

print('Beginning file download with requests')
r = requests.get(url)
#filename = url[-14:]

with open((workfolder + yesterdayfile), 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)

df = pd.read_csv((workfolder +yesterdayfile), encoding = 'latin1')

#Finally, to drop by column number instead of by column label, try this to delete, e.g. the 1st, 2nd and 4th columns:
#   0               1               2       3   4           5           6       7           8     9         10            11                12                      13      14   15         16                17
#Province_State Country_Region  Last_Update Lat Long_   Confirmed   Deaths  Recovered   Active  FIPS    Incident_Rate   People_Tested   People_Hospitalized Mortality_Rate  UID ISO3    Testing_Rate    Hospitalization_Rate
#df = df.drop(df.columns[[0, 1, 3]], axis=1)  # df.columns is zero-based pd.Index
# df = df.drop(df.columns[[                   1,             2,      3,   4,         5,                   7,          8,   9,          10,           11,             12,                              14,  15,        16,               17]], axis=1)
# df = df[df.Province_State != 'Recovered']


# print(df)
print ('these are the columns')
for col in df.columns:
    print(col)

html = df.to_html()
#print(html)

webpage = '/var/www/html/yesterday.html'
with open(webpage, 'wt') as f:
    f.write(html)

