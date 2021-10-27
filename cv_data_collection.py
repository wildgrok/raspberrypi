#!/usr/bin/python3.7
#cv_data_collection.py
#inital version from web_get_page3.py, simplify process
#version in dell desktop

#last update
#10/26/2021 good test bringing file and adding it to dbfile if not exists



import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io
import csv

# import matplotlib.pyplot as plt

#-----------------globals--------------------------------------------

webfolder = ''
workfolder = ''
picsfolder = 'state_deaths/'
csvfolder = 'C:/coronavirus/csv/'
dbfile = 'C:/coronavirus/backup/data_usa.csv'
today = datetime.date.today()
vaccine_data_us_csv_url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/hourly/vaccine_data_us.csv'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
#-----------------------globals end----------------------------------------------------------------------



#-----------------------functions start-------------------------------------------------------------
        
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
    print(url)
    print('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    if os.path.exists(csvfolder + csvfile):
        os.remove(csvfolder + csvfile)
    with open((csvfolder + csvfile), 'wb') as f:
        f.write(r.content)
    print(str(r.status_code))
    print(r.headers['content-type'])
    print(r.encoding)
    print(csvfile)

def get_data():    
    print(sys.version)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print('Today:' + str(today))
    print('Latest file - yesterday:' + str(yesterday))
    yesterdayfile = get_csv_filename(yesterday)
    print(yesterdayfile)
    get_data_to_csv(yesterdayfile, urlbase)
    # next to add the data to the database file, see load_csv_file
    # end of get_data----------------------------------------

def find_date_in_file(file):
    with open((file), 'r') as f:
        r = f.readline()
        r = f.readline()
        p = r.split(',')
    return p[2][0:10] # 2021-10-19



#if date of file exists in file database dbfile, do no insert
# format dbfile Minnesota,US,2021-10-19 04:31:25,8560
# format incoming file
# Alabama,US,2021-10-19 04:31:25,32.3182,-86.9023,814363,15179,,,1.0,16608.857303976903,5929861.0,,1.8639108112721232,84000001.0,USA,120938.96110385393,
def check_existing(file):
    d = find_date_in_file( file)
    #find d on dbfile

    with open(dbfile, 'r') as f:
        if d in f.read():
            # print('found')
            return True
        else:
            print('not found')
            return False
    
    


#exports to text file database contents of current csv file
#this file was downloaded in program web_get_page3.py
#used by load_all_csv_files
def load_csv_file(csvfile):
    filecsv = open(csvfile)   
    csv_data = csv.reader(filecsv, delimiter=',', quotechar='"')
    cnt = 0
    for row in csv_data:
        if str(row[0]) + str(row[1]) == '':
            Province_State = str(row[2])
            Country_Region = str(row[3])
            Last_Update    = str(row[4])
            Deaths         = str(row[8])
        else:
            Province_State = str(row[0])
            Country_Region = str(row[1])
            Last_Update    = str(row[2])
            Deaths         = str(row[6])

        if Country_Region == 'US':
            s = Province_State + ',' + Country_Region + ',' + Last_Update + ',' + Deaths          
            if (Last_Update[:10]) == str(today):
                with open(dbfile, 'a') as f:
                    f.write(s +'\n')
                print('Added ' + s)
                cnt = cnt + 1
    print("Processed " + str(cnt) + ' records from ' + csvfile)

def load_all_csv_files(csvfolder):
    #list of all files in csv files
    files = os.listdir(csvfolder)
    for x in files:
        if len(x) == 14:
            #10/19/2021 adding check of file already processes
            csvfile = csvfolder + x
            if check_existing(csvfile) == False:
                load_csv_file(csvfile)    

#10/26/2021
#used by vaccine_doses
def get_data_to_csv_vac(url):
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

#10/26/2021
def vaccine_doses():
    #8/10/2021rf_model_on_full_data
    vaccine_data_us_csv_url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/hourly/vaccine_data_us.csv'
    get_data_to_csv_vac(vaccine_data_us_csv_url)
    # Sample data
    # FIPS  ,   Province_State    ,    Country_Region    ,    Date          ,       Lat        ,     Long_     ,     Vaccine_Type   , Doses_alloc    ,    Doses_shipped   ,   Doses_admin    ,   Stage_One_Doses    ,   Stage_Two_Doses   ,   Combined_Key
    # 1     ,   Alabama           ,        US            ,    2021-08-10    ,       32.3182     ,    -86.9023  ,     Pfizer         ,                ,    2608740         ,   1898892        ,                      ,   832153            ,   "Alabama, US"
    # 1,Alabama,US,2021-08-10,32.3182,-86.9023,Moderna,,2439960,1689328,,751583,"Alabama, US"
    # 1,Alabama,US,2021-08-10,32.3182,-86.9023,All,,5330000,3712533,2217468,1583987,"Alabama, US"
   
    # cols_chosen = 'Province_State,Vaccine_Type, Doses_admin'
    file = csvfolder + 'vaccine_data_us.csv'
    df_vac = pd.read_csv(file, encoding='latin1',thousands=',', low_memory=False, usecols = ['Province_State','Vaccine_Type','Doses_admin'])
    df_vac = df_vac.set_index('Province_State')
    df_vac = df_vac.drop_duplicates()
    # df_vac2 = df_vac
    # 9/28/2021 sample data
    # Province_State,Vaccine_Type,Doses_admin
    # Alabama,Pfizer,2367864.0
    # Alabama,Moderna,1988601.0
    # Alabama,All,4494228.0
    # Alabama,Unassigned,0.0
    # Alabama,Janssen,137708.0
    # Alabama,Unknown,55.0
    # Alaska,Janssen,33899.0
    #df_vac2.to_csv( csvfolder + 'vaccine_data_us2.csv', index=True, encoding='utf-8')
    mask = (df_vac['Vaccine_Type'] == 'All') 
    df_vac = df_vac.loc[mask]
    df_vac.to_csv( csvfolder + 'vaccine_data_us2.csv', index=True, encoding='utf-8')


    #8/15/2021
    #commented 10/26/2021
    # mask = (df_vac['Vaccine_Type'] == 'Pfizer') |  (df_vac['Vaccine_Type'] == 'Moderna') 
    # df_vac = df_vac.loc[mask]
    # df_vac['Total_Doses'] = df_vac.groupby(['Province_State']).sum('Doses_admin')
    # df_vac = df_vac.drop(['Vaccine_Type', 'Doses_admin'], axis=1)
    # df_vac = df_vac.drop_duplicates()
    # # df_vac = df_vac.sort_values(by=['Total_Doses'])

    # columns = df_vac.columns
    # print('Columns chosen:')
    # for x in columns:
    #     print(x)
    # print(df_vac.head())
    # print(df_vac.describe())

    # #export to csv
    # # df_vac.to_csv( csvfolder + 'df_vac.csv', index=False, encoding='utf-8')
    # df_vac.to_csv( csvfolder + 'df_vac.csv', index=True, encoding='utf-8')

    # end of vaccine_doses-------------------------------------------------------------------
    

#-----end of functions---------------------------------------------------------------





#9/3/2021


# Run program 
if __name__ == '__main__':
    get_data()
    load_all_csv_files(csvfolder)
    vaccine_doses()
    # r = find_date_in_file('c:/coronavirus/csv/10-18-2021.csv')
    # print(r)
    # check_existing('c:/coronavirus/csv/10-18-2021.csv')
    