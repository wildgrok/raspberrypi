# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# created from plots.py 11/14/2020
# last update:
#version in rpi
#8/2/2021 added moing averages
#7/11/2021
#7/10/2021
#7/9/2021 version with no mysql


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pandas._libs import indexing
from pandas.core.indexes.base import Index

#globals-------------------------------------------------
statedeathsfolder = '//var/www/html/coronavirus/state_deaths'
database = '/home/pi/Documents/data_usa.csv'

# functions -------------------------
#For each state create the death pics and csv and json exports
def get_state_data(state):   
    st = df1['Province_State'] == state
    df = df1[st]
    df = df.drop(['Deaths','Province_State', 'Country_Region'], axis=1)
    df = df.rename(columns={"diffs": "Deaths"})
    df = df.set_index('Last_Update')
    #to prevent negative deaths in the charts
    df['Deaths'] = np.where(df['Deaths'] <0, None, df['Deaths'])
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.
    # df = df[np.abs(df.Deaths-df.Deaths.mean()) <= (3*df.Deaths.std())]

    #saving csv for the state----------
    print('getting csv for ' + state)
    statecsvfile = statedeathsfolder + '/' + state + '.csv'
    df.to_csv(statecsvfile)
    #----------------------------------

    # json section---------------------
    print('getting json file for ' + state)
    statejsonfile = statedeathsfolder + '/' + state + '.json'
    df.to_json(statejsonfile, orient='index')
    #----------------------------------

    # images section--------------------
    print('getting pic for ' + state)
    #8/3/2021
    df['SMA_7'] = df.iloc[:,0].rolling(window=7).mean()
    df['SMA_30'] = df.iloc[:,0].rolling(window=30).mean()
    # dropping Deaths for clear pic
    df = df.drop(['Deaths'], axis=1)
    plt.figure(figsize=[10,5])
    plt.grid(False)
    # plt.plot(df['Deaths'],label='deaths')
    plt.plot(df['SMA_7'],label='SMA 7 days')
    plt.plot(df['SMA_30'],label='SMA 30 days')
    plt.legend(loc=2)
    # plt.xlim([25, 50])
    statejpgfile = statedeathsfolder + '/' + state + '.jpg'
    ax = df.plot.area(stacked=False)
    ax.set_axis_off()
    plt.savefig(statejpgfile)
    #---------------------------------

# end of functions------------------------------------

#create dataframe from dbfile
pd.set_option('display.max_rows', 20)
country = ['US']
df1 = pd.read_csv(database, encoding = 'latin1', thousands=',')
df1 = df1.drop_duplicates()
#df1.columns=df1.columns.str.strip()

#entries=entries.sort(['i','j','ColumnA','ColumnB'])

df1=df1.sort_values(by=['Province_State', 'Last_Update'])
#df1=df1.sort_values(['Province_State', 'Last_Update'])

list_columns = df1.columns
lst_states = df1['Province_State'].unique()

# only take diffs where next row is of the same group
df1['diffs'] = np.where(df1.Province_State == df1.Province_State.shift(1), df1.Deaths.diff(), 0)
df1.to_csv('/home/pi/Documents/dataframe.csv', index=False)
#--------------------------------------------------------


#================================================================


for state in lst_states:
#     state = x.rstrip('\n')
     get_state_data(state)

#-----------------------------------------------------------------------




