#web_get_page3.py
#version in rpi4gb
#from web_get_page2.py
#last modified
#10/5/2021 added vac functions from desktop
#8/29/2021 added total percentage
#8/9/2021 changed for population 2019
#8/3/2021 pics display only 7 and 30 days moving average, fixed negative deaths display
#8/2/2021 changed web page for moving averages
#7/22/2021 changed for VAERS pages

import sys
import os
import requests
import pandas as pd
import numpy as np
import datetime
import io
import matplotlib.pyplot as plt
# from IPython.core.display import HTML

# workfolder = 'C:\Users\python\PycharmProjects\'
webfolder = '/var/www/html/coronavirus/'
workfolder = '/home/pi/Documents/'
picsfolder = 'state_deaths/'
# csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv2/'
csvfolder = '/home/pi/Documents/'

urlbase = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
#11/24/2020
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
    #to get missing date
    #file = '07' + '-' + '06' + '-' + '2021' + '.csv'
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
    webpage = webfolder + 'index.html'
    with open(webpage, 'wt') as f:
        f.write(s)

def make_html(webpage,table, total, death_percent_today):
    today = str(datetime.date.today())
    s = '<html>'
    s = s + '<body>'
    s = '<h1>Coronavirus USA Data - updated daily</h1>'
    s = s + '<br><b>Date run: ' + today + ' - Total new deaths for today: ' + str(total) + '</b><p>'
    #8/29/2021
    s = s + '<br><b>Estimated yearly percentage of deaths if the year has this number of deaths every day: ' + str(death_percent_today) + '</b><p>'    
    s = s + '<b>Blue: 7 days moving average  -  Orange: 30 days moving average</b><p>'
    
    if webpage == webfolder + 'index_coronavirus.html':
        s = s  + '<a href="index2_coronavirus.html">Sorted by Deaths_As_%_of Population_2019</a><p>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s  + '<a href="index_coronavirus.html">Sorted by New_Deaths</a><p>'

    s = s + table
    s = s + '<p>'

    if webpage == webfolder + 'index_coronavirus.html':
        s = s  + '<a href="index2_coronavirus.html">Sorted by Deaths_As_%_of Population_2019</a><p>'
    if webpage == webfolder + 'index2_coronavirus.html':
        s = s  + '<a href="index_coronavirus.html">Sorted by New_Deaths</a><p>'

    s = s + '</body>'
    s = s + '</html>'
    # webpage = webfolder + 'index.html'
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
    #end of get_data_to_csv--------------------------
    
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
    #end of get_data_to_csv_vac---------------------
    
    
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
    get_data_to_csv(yesterdayfile, urlbase)

    #8/9/2021
    df_population = pd.read_csv((workfolder + 'population_usa_2019.csv'), encoding = 'UTF-8', thousands=',')
    df_population['State'] = df_population['State'].str.strip()
    df_population = df_population.rename(columns={"State": "Province_State", "Population estimate, July 1, 2019": "Population_2019"})
    df_population = df_population.set_index('Province_State')
    df_population = df_population[['Population_2019']].apply(pd.to_numeric)
    writelog('these are the columns - population_usa_2019.csv')
    for col in df_population.columns:
        writelog(col)
        print(col)

    country = ['US']
    
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

    #8/9/2021
    df_previous_day['Population_2019'] = df_population['Population_2019']
    df_previous_day['Deaths_As_%_of Population_2019'] = df_previous_day['Deaths'].divide(df_previous_day['Population_2019']) * 100

    df_previous_day['New_Deaths'] = np.where(df_previous_day['Deaths'] >= df['Deaths'], 0, df['Deaths'] - df_previous_day['Deaths']) #create new column in df1 for deaths diff
    df_previous_day = df_previous_day.sort_values(by=['New_Deaths', 'Province_State'])
    for col in df_previous_day.columns:
        writelog(col)
    total = df_previous_day['New_Deaths'].sum()
    writelog(str(total))
    
    #8/29/2021
    total_population_20219_usa = df_previous_day['Population_2019'].sum()
    print('total population usa 2019', total_population_20219_usa)
    usa_death_percentage_today = (total / total_population_20219_usa) * 100
    print('Today Death percentage as % of US population', usa_death_percentage_today)
    print('Assuming today deaths are the same for one year this is the USA death perpecentage estimate')
    usa_death_percentage_year_estimate = ((total * 365) / (total_population_20219_usa))  * 100
    print('usa_death_percentage_year_estimate', usa_death_percentage_year_estimate)
    
    

    # Create a list named states to store all the image paths
    states = picsfolder + df_previous_day.index + '.jpg'
    df_previous_day['Chart_New_Deaths'] = states
    writelog('state pics:')
    for x in states:
        writelog(x)

    # DO NOT ENABLE THIS, we miss states like New York
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.
    #df_previous_day = df_previous_day[np.abs(df_previous_day.Deaths-df_previous_day.Deaths.mean()) <= (3*df_previous_day.Deaths.std())]
    # Saving the dataframe as a webpage na_rep to prevent Nan in page for no values or null
    # df_previous_day.to_html(webpage,escape=False, formatters=dict(Chart=path_to_image_html))
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))

    webpage = webfolder + 'index_coronavirus.html'
    make_html(webpage, html, total, usa_death_percentage_year_estimate)

    #sorted by Deaths_As_%_of Population_2019
    #8/9/2021
    df_previous_day = df_previous_day.sort_values(by=['Deaths_As_%_of Population_2019', 'Province_State'])
    html = df_previous_day.to_html(na_rep='', escape=False,  formatters=dict(Chart_New_Deaths=path_to_image_html))
    webpage = webfolder + 'index2_coronavirus.html'
    make_html(webpage, html, total, usa_death_percentage_year_estimate)
    
    #10/5/2021
    #Started to create new page with vaccination counts per state
    df_vac = vaccine_doses()
    df_vac = df_vac.drop(['Vaccine_Type'], axis=1)
    df_vac['Population_2019'] = df_previous_day['Population_2019']
    df_vac['Vac/Population'] = df_vac['Doses_admin'] / df_vac['Population_2019']
    df_vac['Deaths_As_%_of Population_2019'] = df_previous_day['Deaths_As_%_of Population_2019']

    print('Making webpage for vaccines by state')
    print('Saving plain html page only states_vaccines.html sorted by state (default)')
    table = df_vac.to_html(na_rep='', escape=False)
    wp = webfolder + 'states_vaccines.html'
    with open(wp, "w", encoding="utf-8") as f:
        f.write(table)
    print('Making webpage for vaccines by Doses_admin')
    print('Saving plain html page only states_vaccines_by_Doses_admin.html sorted by Doses_admin')
    df_vac = df_vac.sort_values(by=['Doses_admin'])
    table = df_vac.to_html(na_rep='', escape=False)
    wp = webfolder + 'states_vaccines_by_Doses_admin.html'
    with open(wp, "w", encoding="utf-8") as f:
        f.write(table)
    print('Making webpage for vaccines by Vac/Population')
    print('Saving plain html page only states_vaccines_by_vac_population.html sorted by Vac/Population')
    df_vac = df_vac.sort_values(by=['Vac/Population'])
    table = df_vac.to_html(na_rep='', escape=False)
    wp = webfolder + 'states_vaccines_by_vac_population.html'
    with open(wp, "w", encoding="utf-8") as f:
        f.write(table)
    print('Making webpage for vaccines by Deaths_As_%_of Population_2019')
    print('Saving plain html page only states_vaccines_by_Deaths_As_%_of Population_2019.html sorted by Deaths_As_%_of Population_2019')
    df_vac = df_vac.sort_values(by=['Deaths_As_%_of Population_2019'])
    table = df_vac.to_html(na_rep='', escape=False)
    wp = webfolder + 'states_vaccines_by_Deaths_As_percent_of_Population_2019.html'
    with open(wp, "w", encoding="utf-8") as f:
        f.write(table)      
    
    #end of get_data----------------------------------

#imported from desktop 10/5/2021
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
    df_vac2.to_csv( csvfolder + 'vaccine_data_us2.csv', index=True, encoding='utf-8')
    mask = (df_vac2['Vaccine_Type'] == 'All') 
    df_vac2 = df_vac2.loc[mask]
    df_vac2.to_csv( csvfolder + 'vaccine_data_us3.csv', index=True, encoding='utf-8')
    return df_vac2
    # end of vaccine_doses--------------------------------------------


# Run program 
if __name__ == '__main__':
    get_data()