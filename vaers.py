#vaers.py
#version in dell laptop imported from rpi 6205
#last modified
#7/25/2021 fixed daterange
#7/24/2021 imported from rpi 6205
#7/22/2021 imported from dell laptop
#7/21/2021 changed web pages creation


import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
today = datetime.date.today()

#webfolder = '/var/www/html/coronavirus/'
csvfolder = 'C:/coronavirus/'
workfolder = csvfolder
webfolder = csvfolder
# workfolder = '/home/pi/Documents/'
dbfile = 'C:/Users/admin/Downloads/AllVAERSDataCSVS/VAERSDATA.csv'
# dbfile = workfolder + 'VAERSDATA.csv'
#/home/pi/Documents/2021VAERSDATA.csv
webpage = webfolder + 'vaers.html'
webpage2 = webfolder + 'vaers2.html'

#------functions-----------------------------------
# webpage is the file like index.html (full path)
# table is the html content as table, coming from dataframe.to_csv
# total is the count of the table items
def make_html(webpage,table, total, daterange, message=''):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>VAERS USA Data - updated from latest file from vaers.hhs.gov </h1>'
    s = s + '<br><b>Date run: ' + today + ' - Total deaths ' + str(total) + '</b><br>'
    s = s + '<br><b>' + daterange  + '</b><br>'
    s = s + message
    s = s + table
    s = s + '<p>'
    s = s  + '<a href="vaers_notes.html">Notes on data</a><p>'
    s = s + '</body>'
    s = s + '</html>'
    with open(webpage, "w", encoding="utf-8") as f:
        f.write(s)

#------end of functions----------------------------



#create dataframe from dbfile
pd.set_option('display.max_rows', 2)
df1 = pd.read_csv(dbfile, encoding='latin1',thousands=',', low_memory=False, usecols = ['VAERS_ID','RECVDATE','SYMPTOM_TEXT','STATE','AGE_YRS','DIED'])
columns = df1.columns
print('Columns chosen:')
for x in columns:
    print(x)
df1["RECVDATE"] = pd.to_datetime(df1["RECVDATE"])
mindate = df1['RECVDATE'].min()
maxdate = df1['RECVDATE'].max()
print('mindate, maxdate', mindate, maxdate)
datesrange = 'Dates range:' + str(mindate) + ' to ' + str(maxdate)
print(datesrange)
# print(columns)
# Index(['VAERS_ID', 'RECVDATE', 'STATE', 'AGE_YRS', 'CAGE_YR', 'CAGE_MO', 'SEX',
#        'RPT_DATE', 'SYMPTOM_TEXT', 'DIED', 'DATEDIED', 'L_THREAT', 'ER_VISIT',
#        'HOSPITAL', 'HOSPDAYS', 'X_STAY', 'DISABLE', 'RECOVD', 'VAX_DATE',
#        'ONSET_DATE', 'NUMDAYS', 'LAB_DATA', 'V_ADMINBY', 'V_FUNDBY',
#        'OTHER_MEDS', 'CUR_ILL', 'HISTORY', 'PRIOR_VAX', 'SPLTTYPE',
#        'FORM_VERS', 'TODAYS_DATE', 'BIRTH_DEFECT', 'OFC_VISIT', 'ER_ED_VISIT',
#        'ALLERGIES'],

print('df1 no limitations count')
print(df1.VAERS_ID.count())


df1 = df1[ (df1['DIED'] == 'Y') &  (df1['SYMPTOM_TEXT'].str.contains('covid', case = False) | df1['SYMPTOM_TEXT'].str.contains('coronavirus', case = False) )]

deathscount = len(df1[df1['DIED'] == 'Y'])
print(deathscount)
print('Saving file all columns')
df1.to_csv(workfolder + 'vaers_covid_deaths.csv', index=False)

print('Creating main webpage vaers.html')
table = df1.to_html(na_rep='', escape=False)
print('Saving plain html page only vaers_covid_deaths.html')
wp = webfolder + 'vaers_covid_deaths.html'
with open(wp, "w", encoding="utf-8") as f:
     f.write(table)

make_html(webpage,table, deathscount, datesrange)

print('getting pic')
#here we use df1, which contains DIED
df = df1.drop(['VAERS_ID','STATE','AGE_YRS','SYMPTOM_TEXT'], axis=1)
df["RECVDATE"] = pd.to_datetime(df["RECVDATE"])
df.set_index('RECVDATE')
df = df.groupby('RECVDATE').count()
# df now:
# RECVDATE,DIED
# 2021-01-01,1
# ...
# 2021-07-09,12

total_deaths = df.DIED.sum()
print('Total deaths after df.DIED.sum()')
print(total_deaths)
print('Saving file date and deaths only')
df.to_csv(workfolder + 'vaers_covid_deaths2.csv')

print('Making webpage for the grouped death counts by date')
table = df.to_html(na_rep='', escape=False)
print('Saving plain html page only vaers_covid_deaths3.html')
wp = webfolder + 'vaers_covid_deaths3.html'
with open(wp, "w", encoding="utf-8") as f:
     f.write(table)
message = 'Number of deaths for given day'
make_html(webpage2,table, deathscount, datesrange, message)


ax = df.plot.area(stacked=False)
# ax.set_axis_off()
statejpgfile = webfolder + 'vaers.jpg'
plt.savefig(statejpgfile)