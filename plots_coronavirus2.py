# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# created from plots.py 11/14/2020
# last update:
#7/10/2021
#7/9/2021 version with no mysql
#6/22/2021: version in dell laptop
#12/3/2020 fix to remove axis to image
#11/21/2020: created json files
#11/21/2020: created state deaths files


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pandas._libs import indexing
from pandas.core.indexes.base import Index

#globals-------------------------------------------------
statedeathsfolder = 'C:/coronavirus/state_deaths2'
# statedeathsfolder = r'C:\Users\admin\Documents\coronavirus\state_deaths'
database = 'C:/coronavirus/data_usa.csv'

#create dataframe from dbfile
pd.set_option('display.max_rows', 20)
country = ['US']
df1 = pd.read_csv(database, encoding = 'latin1', thousands=',')

df1=df1.sort_values(by=['Province_State', 'Last_Update'])
list_columns = df1.columns
lst_states = df1['Province_State'].unique()

# only take diffs where next row is of the same group
df1['diffs'] = np.where(df1.Province_State == df1.Province_State.shift(1), df1.Deaths.diff(), 0)
df1.to_csv('c:/coronavirus/dataframe.csv', index=False)
#--------------------------------------------------------

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
    # ax = df.plot.area()
    ax = df.plot.area(stacked=False)
    ax.set_axis_off()
    # ax.plot()
    # df.plot()
    statejpgfile = statedeathsfolder + '/' + state + '.jpg'
    plt.savefig(statejpgfile)
    #---------------------------------
#================================================================





for state in lst_states:
#     state = x.rstrip('\n')
     get_state_data(state)

#-----------------------------------------------------------------------





