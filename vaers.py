#vaers.py
#version in dell laptop imported from rpi 6205
#last modified
#8/16/2021 created graph vaers_vaccine_doses.jpg
#8/15/2021 automating data from all data from zip file
#8/10/2021 started to work on vaccines file to be continued
#https://github.com/govex/COVID-19/blob/master/data_tables/vaccine_data/us_data/hourly/vaccine_data_us.csv
#7/31/2021 added moving averages
#7/25/2021 fixed daterange
#7/24/2021 imported from rpi 6205
#7/22/2021 imported from dell laptop
#7/21/2021 changed web pages creation


import csv
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
today = datetime.date.today()

#webfolder = '/var/www/html/coronavirus/'
csvfolder = 'C:/coronavirus/'
workfolder = csvfolder
webfolder = csvfolder
# workfolder = '/home/pi/Documents/'
#8/15/2021

#------------------------functions------------------------------------------
# Updates VAERSDATA.csv from latest downloaded zip contents in 
# C:\Users\admin\Downloads\AllVAERSDataCSVS
def get_csvfile_combined(foldercsv):
    os.chdir(foldercsv)
    # os.chdir("/mydir")
    #C:/Users/admin/Downloads/AllVAERSDataCSVS
    extension = 'csv'
    all_filenames = [i for i in glob.glob('????VAERSDATA.{}'.format(extension))]
    print(all_filenames)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    # combined_csv.to_csv( "VAERSDATA.csv", index=False, encoding='utf-8-sig')
    combined_csv.to_csv( "VAERSDATA.csv", index=False, encoding='utf-8')

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

def get_data_to_csv(url):
    # url = urlbase + csvfile
    print(url)
    print('Beginning file download with requests: vaccine_data_us.csv')
    r = requests.get(url)
    if os.path.exists(csvfolder + 'vaccine_data_us.csv'):
        os.remove(csvfolder + 'vaccine_data_us.csv')
    with open((csvfolder + 'vaccine_data_us.csv'), 'wb') as f:
        f.write(r.content)
    print(str(r.status_code))
    print(r.headers['content-type'])
    print(r.encoding)
    # print(csvfile)

#------------------------end of functions------------------------------------------------------

folder_csv = 'C:/Users/admin/Downloads/AllVAERSDataCSVS'
print('All csv files:')
get_csvfile_combined(folder_csv)
os.chdir(workfolder)



dbfile = folder_csv + '/' + 'VAERSDATA.csv'
#/home/pi/Documents/VAERSDATA.csv
webpage = webfolder + 'vaers.html'
webpage2 = webfolder + 'vaers2.html'
# vaccine_data_us_csv = 'https://github.com/govex/COVID-19/blob/master/data_tables/vaccine_data/us_data/hourly/vaccine_data_us.csv'
vaccine_data_us_csv = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/hourly/vaccine_data_us.csv'

pd.set_option('display.max_rows', 5)

#8/10/2021rf_model_on_full_data
get_data_to_csv(vaccine_data_us_csv)
# Sample data
# FIPS  ,   Province_State    ,    Country_Region    ,    Date          ,       Lat        ,     Long_     ,     Vaccine_Type   , Doses_alloc    ,    Doses_shipped   ,   Doses_admin    ,   Stage_One_Doses    ,   Stage_Two_Doses   ,   Combined_Key
# 1     ,   Alabama           ,        US            ,    2021-08-10    ,       32.3182     ,    -86.9023  ,     Pfizer         ,                ,    2608740         ,   1898892        ,                      ,   832153            ,   "Alabama, US"
# 1,Alabama,US,2021-08-10,32.3182,-86.9023,Moderna,,2439960,1689328,,751583,"Alabama, US"
# 1,Alabama,US,2021-08-10,32.3182,-86.9023,All,,5330000,3712533,2217468,1583987,"Alabama, US"
# 1,Alabama,US,2021-08-10,32.3182,-86.9023,Unassigned,,0,0,2090441,251,"Alabama, US"
# 1,Alabama,US,2021-08-10,32.3182,-86.9023,Janssen,,281300,124309,127027,,"Alabama, US"
# 1,Alabama,US,2021-08-10,32.3182,-86.9023,Unknown,,0,4,,,"Alabama, US"

# cols_chosen = 'Province_State,Vaccine_Type, Doses_admin'
file = csvfolder + 'vaccine_data_us.csv'
df_vac = pd.read_csv(file, encoding='latin1',thousands=',', low_memory=False, usecols = ['Province_State','Vaccine_Type','Doses_admin'])
df_vac = df_vac.set_index('Province_State')
df_vac = df_vac.drop_duplicates()
#8/15/2021
mask = (df_vac['Vaccine_Type'] == 'Pfizer') |  (df_vac['Vaccine_Type'] == 'Moderna') 
df_vac = df_vac.loc[mask]
df_vac['Total_Doses'] = df_vac.groupby(['Province_State']).sum('Doses_admin')
df_vac = df_vac.drop(['Vaccine_Type', 'Doses_admin'], axis=1)
df_vac = df_vac.drop_duplicates()
# df_vac = df_vac.sort_values(by=['Total_Doses'])
# print('df_vac.head()')
# print(df_vac.head())

columns = df_vac.columns
print('Columns chosen:')
for x in columns:
    print(x)
print(df_vac.head())
print(df_vac.describe())

#8/16/2021
# df['SMA_7'] = df.iloc[:,0].rolling(window=7).mean()
# df['SMA_30'] = df.iloc[:,0].rolling(window=30).mean()
plt.figure(figsize=[15,10])
plt.grid(True)
plt.plot(df_vac['Total_Doses'],label='Total Doses')
# plt.plot(df_vac['SMA_7'],label='SMA 7 days')
# plt.plot(df_vac['SMA_30'],label='SMA 30 days')
# plt.plot(df['SMA_4'],label='SMA 4 Months')
plt.legend(loc=2)
statejpgfile = webfolder + 'vaers_vaccine_doses.jpg'
#delete if exists
if os.path.exists(statejpgfile):
    os.remove(statejpgfile)
plt.savefig(statejpgfile)




#create dataframe from dbfile
print('dbfile: ', dbfile)
# df1 = pd.read_csv(dbfile, encoding='latin1',thousands=',', low_memory=False, usecols = ['VAERS_ID','RECVDATE','SYMPTOM_TEXT','STATE','AGE_YRS','DIED'])
df1 = pd.read_csv(dbfile, encoding='latin1',thousands=',', low_memory=True, usecols = ['VAERS_ID','RECVDATE','SYMPTOM_TEXT','STATE','AGE_YRS','DIED'])

# df1 = df1.drop_duplicates()
columns = df1.columns
print('Columns chosen:')
for x in columns:
    print(x)
df1["RECVDATE"] = pd.to_datetime(df1["RECVDATE"])

#8/15/2021
mask = (df1['RECVDATE'] > '2019-12-31')
# Select the sub-DataFrame:
# df.loc[mask]
# or re-assign to df
df1 = df1.loc[mask]


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
print('Saving file with selected columns, no limitations')
df1.to_csv(workfolder + 'VAERS_ID-RECVDATE-SYMPTOM_TEXT-STATE-AGE_YRS-DIED.csv', index=False)


df0= df1[(df1['DIED'] == 'Y')] #]) &  (df1['SYMPTOM_TEXT'].str.contains('covid', case = False) | df1['SYMPTOM_TEXT'].str.contains('coronavirus', case = False) )]
print('df0 dead count')
print(df0.VAERS_ID.count())
print('Saving deaths file all columns')
df0.to_csv(workfolder + 'vaers_covid_deaths0.csv', index=False)


df1 = df0[ (df0['SYMPTOM_TEXT'].str.contains('covid', case = False) | df0['SYMPTOM_TEXT'].str.contains('coronavirus', case = False) )]
df1 = df1.sort_values(by='RECVDATE', ascending = False)
deathscount = len(df1[df1['DIED'] == 'Y'])
print(deathscount)
print('Saving file all columns')
df1.to_csv(workfolder + 'vaers_covid_deaths.csv', index=False)


print('Creating main webpage vaers.html')
df3 = df1.drop(['DIED'], axis=1)
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


#7/31/2021
print('df.head')
print(df.head())
df['SMA_7'] = df.iloc[:,0].rolling(window=7).mean()
df['SMA_30'] = df.iloc[:,0].rolling(window=30).mean()
plt.figure(figsize=[15,10])
plt.grid(True)
plt.plot(df['DIED'],label='deaths')
plt.plot(df['SMA_7'],label='SMA 7 days')
plt.plot(df['SMA_30'],label='SMA 30 days')
# plt.plot(df['SMA_4'],label='SMA 4 Months')
plt.legend(loc=2)
statejpgfile = webfolder + 'vaers_moving_average.jpg'
#delete if exists
if os.path.exists(statejpgfile):
    os.remove(statejpgfile)
plt.savefig(statejpgfile)
