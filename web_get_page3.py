#!/usr/bin/python3.7
#web_get_page3.py
#version in dell desktop
#from web_get_page2.py
#last modified
#10/4/2021 more on vacs
#9/29/2021 started to add page for state vaccination
#9/3/2021 added describe data
#8/29/2021 added percentage of all deaths for usa population
#8/17/2021 imported function vaccine_doses from vaers.py
#8/8/2021 started adding population from file population_usa_2019.csv
#7/21/2021 changed web page to index_coronavirus.html
#6/21/2021 testing in dell laptop
#12/29/2020 read_csv uses usecols
#12/2/2020 completed fixes for images
#11/24/2020 working adding display of jpg, not ready yet
#11/11/2020 fixing error see file errors_11_11_2020.txt
#KeyError: "['People_Tested' 'Mortality_Rate'] not found in axis" in line 131


import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io
import matplotlib.pyplot as plt

#-----------------globals--------------------------------------------
# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = ''
workfolder = ''
# picsfolder = 'C:/Users/python/PycharmProjects/coronavirus//'
# picsfolder = 'C:\\Users\\python\\PycharmProjects\\coronavirus\\state_deaths\\'
picsfolder = 'state_deaths/'
#FOR TESTING LOCALLY, LEAVE IT COMMENTED
#picsfolder = 'coronavirus/state_deaths/'
# csvfolder = 'C:/Users/admin/Documents/coronavirus/csv/'
csvfolder = 'C:/coronavirus/csv/'
urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
#-----------------------globals end----------------------------------------------------------------------

#-----------------------functions start-------------------------------------------------------------
def path_to_image_html(path):
    return '<img src="'+ path + '" width="200" >'

def writelog(data):
    with open((workfolder + 'web_get_page2.out'), 'a+') as f:
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

def make_html_TEMP(table, total):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + '</b><br>'
    s = s + 'Site under maintenance'
    s = s + '</body>'
    s = s + '</html>'
    webpage = webfolder + 'index_coronavirus.html'
    with open(webpage, 'wt') as f:
        f.write(s)

def make_html(webpage,table, total, death_percent_today):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + ' - Total new deaths for today: ' + str(total) + '</b><br>'
    #8/29/2021
    s = s + '<br><b>Estimated percentage of deaths if the year has this number of deaths every day: ' + str(death_percent_today) + '</b><br>'


    if webpage == webfolder + 'index_coronavirus.html':
        s = s + 'Sorted by New_Deaths<br>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s + 'Sorted by Deaths_As_%_of Population_2019<br>'
    
    s = s + table
    s = s + '<p>'

    if webpage == webfolder + 'index_coronavirus.html':
        s = s  + '<a href="index2_coronavirus.html">Sorted by Deaths_As_%_of Population_2019</a><p>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s  + '<a href="index_coronavirus.html">Sorted by New_Deaths</a><p>'

    s = s + '</body>'
    s = s + '</html>'
    with open(webpage, 'wt') as f:
        f.write(s)

def get_data_to_csv(csvfile, urlbase):
    url = urlbase + csvfile
    writelog(url)
    writelog('Beginning file download with requests: ' + csvfile)
    r = requests.get(url)
    if os.path.exists(csvfolder + csvfile):
        os.remove(csvfolder + csvfile)
    with open((csvfolder + csvfile), 'wb') as f:
        f.write(r.content)
    writelog(str(r.status_code))
    writelog(r.headers['content-type'])
    writelog(r.encoding)
    writelog(csvfile)

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
    # print(csvfile)

def get_data():    
    if os.path.exists(workfolder + 'web_get_page2.out'):
        os.remove(workfolder + 'web_get_page2.out')
    writelog(sys.version)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    writelog('Today:' + str(today))
    writelog('Latest file - yesterday:' + str(yesterday))
    yesterdayfile = get_csv_filename(yesterday)
    writelog(yesterdayfile)
    # populates daily file of the form MM-DD-YYYY.csv from web data frm urlbase
    get_data_to_csv(yesterdayfile, urlbase)


    #8/8/2021
    df_population = pd.read_csv((workfolder + 'population_usa_2019.csv'), encoding = 'UTF-8', thousands=',')
    df_population['State'] = df_population['State'].str.strip()
    df_population = df_population.rename(columns={"State": "Province_State", "Population estimate, July 1, 2019": "Population_2019"})
    df_population = df_population.set_index('Province_State')
    df_population = df_population[['Population_2019']].apply(pd.to_numeric)
    writelog('these are the columns - population_usa_2019.csv')
    for col in df_population.columns:
        writelog(col)

    country = ['US']
    # added usecols 12/29/2020
    #Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,Total_Test_Results,People_Hospitalized,Case_Fatality_Ratio,UID,ISO3,Testing_Rate,Hospitalization_Rate
    #Province_State,Country_Region,Last_Update,Deaths

    df1 = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1', thousands=',', usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
    df = df1[df1['Country_Region'].isin(country)]
    df = df.set_index('Province_State')
    writelog('these are the columns - current day')
    for col in df.columns:
        writelog(col)
    dayago = today - datetime.timedelta(days=2)
    dayagofile = get_csv_filename(dayago)

    #1/22/2020 need to add check for missing previous day
    if os.path.exists(csvfolder + dayagofile):
        df_previous_day = pd.read_csv((csvfolder + dayagofile), encoding = 'latin1',thousands=',' ,usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
    else:
        df_previous_day = pd.read_csv((csvfolder + yesterdayfile), encoding = 'latin1',thousands=',' ,usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
    df_previous_day = df_previous_day.set_index('Province_State')
    df_previous_day = df_previous_day.drop(['Country_Region'], axis=1)

    #8/8/2021------
    df_previous_day['Population_2019'] = df_population['Population_2019']
    df_previous_day['Deaths_As_%_of Population_2019'] = df_previous_day['Deaths'].divide(df_previous_day['Population_2019']) * 100

    df_previous_day['New_Deaths'] = np.where(df_previous_day['Deaths'] >= df['Deaths'], 0, df['Deaths'] - df_previous_day['Deaths']) 
    # df_previous_day['New_Deaths'] = np.where(df_previous_day['Deaths'] > df['Deaths'], False, df['Deaths'] - df_previous_day['Deaths']) 
    #df_previous_day = df_previous_day['New_Deaths' ]
    df_previous_day = df_previous_day.sort_values(by=['New_Deaths', 'Province_State'])
    for col in df_previous_day.columns:
        writelog(col)
    total = df_previous_day['New_Deaths'].sum()

    #8/29/2021
    total_population_20219_usa = df_previous_day['Population_2019'].sum()
    print('total population usa 2019', total_population_20219_usa)
    usa_death_percentage_today = (total / total_population_20219_usa) * 100
    print('Today Death percentage as % of US population', usa_death_percentage_today)
    print('Assuming today deaths are the same for one year this is the USA death perpecentage estimate')
    usa_death_percentage_year_estimate = ((total * 365) / (total_population_20219_usa))  * 100
    print('usa_death_percentage_year_estimate', usa_death_percentage_year_estimate)


    writelog(str(total))
    writelog('Create a list named states to store all the image paths')
    states = picsfolder + df_previous_day.index + '.jpg'
    df_previous_day['Chart_New_Deaths'] = states
    writelog('state pics:')
    for x in states:
        writelog(x)
    # print(states)

    # DO NOT ENABLE THIS, we miss states like New York
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.
    #df_previous_day = df_previous_day[np.abs(df_previous_day.Deaths-df_previous_day.Deaths.mean()) <= (3*df_previous_day.Deaths.std())]
    # Saving the dataframe as a webpage na_rep to prevent Nan in page for no values or null
    # df_previous_day.to_html(webpage,escape=False, formatters=dict(Chart=path_to_image_html))
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))
    # 7/21/2021
    webpage = webfolder + 'index_coronavirus.html'

    #8/29/2021
    # make_html(webpage, html, total)
    make_html(webpage, html, total, usa_death_percentage_year_estimate)

    #sorted by Deaths_As_%_of Population_2019
    #8/8/2021
    df_previous_day = df_previous_day.sort_values(by=['Deaths_As_%_of Population_2019','Province_State'])
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))
    # 7/21/2021
    webpage = webfolder + 'index2_coronavirus.html'
    #8/29/2021
    # make_html(webpage, html, total)
    make_html(webpage, html, total, usa_death_percentage_year_estimate)

    # 9/3/2021
    print('describe df_previous_day[New_Deaths]')
    print(df_previous_day['New_Deaths'].describe())
    describe = df_previous_day['New_Deaths'].describe()
    print(describe)


    #9/29/2021
    #10/4/2021
    #Started to create new page with vaccination counts per state
    df_vac = vaccine_doses()
    df_vac = df_vac.drop(['Vaccine_Type'], axis=1)
    df_vac['Population_2019'] = df_previous_day['Population_2019']
    df_vac['Vac/Population'] = df_vac['Doses_admin'] / df_vac['Population_2019']
    df_vac['Deaths_As_%_of Population_2019'] = df_previous_day['Deaths_As_%_of Population_2019']
    print('Making webpage for vaccines by state')
    table = df_vac.to_html(na_rep='', escape=False)
    print('Saving plain html page only states_vaccines.html')
    wp = webfolder + 'states_vaccines.html'
    with open(wp, "w", encoding="utf-8") as f:
        f.write(table)

    # end of get_data----------------------------------------

#8/17/2021 imported from vaers.py, not used yet
#last updated 9/29/2021
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
    df_vac2 = df_vac
    # 9/28/2021 sample data
    # Province_State,Vaccine_Type,Doses_admin
    # Alabama,Pfizer,2367864.0
    # Alabama,Moderna,1988601.0
    # Alabama,All,4494228.0
    # Alabama,Unassigned,0.0
    # Alabama,Janssen,137708.0
    # Alabama,Unknown,55.0
    # Alaska,Janssen,33899.0
    df_vac2.to_csv( csvfolder + 'vaccine_data_us2.csv', index=True, encoding='utf-8')
    mask = (df_vac2['Vaccine_Type'] == 'All') 
    df_vac2 = df_vac2.loc[mask]
    df_vac2.to_csv( csvfolder + 'vaccine_data_us3.csv', index=True, encoding='utf-8')
    return df_vac2

    #8/15/2021
    mask = (df_vac['Vaccine_Type'] == 'Pfizer') |  (df_vac['Vaccine_Type'] == 'Moderna') 
    df_vac = df_vac.loc[mask]
    df_vac['Total_Doses'] = df_vac.groupby(['Province_State']).sum('Doses_admin')
    df_vac = df_vac.drop(['Vaccine_Type', 'Doses_admin'], axis=1)
    df_vac = df_vac.drop_duplicates()
    # df_vac = df_vac.sort_values(by=['Total_Doses'])

    columns = df_vac.columns
    print('Columns chosen:')
    for x in columns:
        print(x)
    print(df_vac.head())
    print(df_vac.describe())

    #export to csv
    # df_vac.to_csv( csvfolder + 'df_vac.csv', index=False, encoding='utf-8')
    df_vac.to_csv( csvfolder + 'df_vac.csv', index=True, encoding='utf-8')

    # end of vaccine_doses--------------------------------------------

#9/3/2021


# Run program 
if __name__ == '__main__':
    get_data()