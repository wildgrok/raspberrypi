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

#globals-------------------------------------------------
statedeathsfolder = r'C:\coronavirus\state_deaths'
# statedeathsfolder = r'C:\Users\admin\Documents\coronavirus\state_deaths'
database = r'C:\coronavirus\data_usa.csv'


#create dataframe from dbfile
pd.set_option('display.max_rows', 20)



country = ['US']
# df1 = pd.read_csv(database, encoding = 'latin1', thousands=',', usecols = ['Province_State','Country_Region','Last_Update','Deaths'])
df1 = pd.read_csv(database, encoding = 'latin1', thousands=',')
# df1 = df1.drop_duplicates
# print(df1)

df1=df1.sort_values(by=['Province_State', 'Last_Update'])
# print(df1)
list_columns = df1.columns
# print('List of columns')
# # print (list_columns)
# for x in list_columns:
    #  print(x)

# df1 = df1.astype({'Deaths': 'int32','Last_Update':'datetime64[ns]'}).dtypes
# df1 = df1.set_index('Province_State')
# df1 = df1['Country_Region'].isin(country)
#list = df1['Province_State']
# lst_states = df1.keys().unique().sort_values()
lst_states = df1['Province_State'].unique()
# print(lst_states)
# print(lst_states[0])
# print(lst_states[-1])
# cls
# print(df1)
# df1 = df1.diff
# print(df1)



# Make sure your data is sorted properly
# df = df.sort_values(by=['group_var', 'value'])

# only take diffs where next row is of the same group
df1['diffs'] = np.where(df1.Province_State == df1.Province_State.shift(1), df1.Deaths.diff(), 0)
print(df1)
# df1 = df1.sort_values(['Province_State', 'Last_Update'], inplace=True)
# df1.sort_values(by  = ['Province_State', 'Last_Update'])cls

# df1['diffs'] = df1.groupby('Province_State')['Deaths'].diff()
# In order to return to the original order, you can the use

# df.sort_index(inplace=True)

#--------------------------------------------------------

def get_state_chart(state):
    statecsvfile = statedeathsfolder + '\\' + state + '.csv'
    df = pd.read_csv(statecsvfile, encoding = 'latin1', thousands=',')
    df = df.set_index('Last_Update')
    df = df[np.abs(df.Deaths-df.Deaths.mean()) <= (3*df.Deaths.std())]
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.
    ax = df.plot.area()

    #12/3/2020
    ax.set_axis_off()
    # ax.plot()
    # df.plot()

    statejpgfile = statedeathsfolder + '\\' + state + '.jpg'
    plt.savefig(statejpgfile)
#================================================================
#df1 = df1.astype({'Deaths': 'int32'}).dtypes

# using apply method
#df1['Deaths']= df1['Deaths'].apply(pd.to_numeric)

# print(df1.drop_duplicates)
# print(df1.columns.values)   


#print(df1.diff())

#list of csv files
#csvfolder = r'C:\Users\python\PycharmProjects\coronavirus\csv2'



#DONE, states list done in line lst_states = df1.keys().unique().sort_values()
#get distinct list of states--------------------------------------------
# states = 'select distinct Province_State from coronavirus.data_usa2;'
# # sql = "SELECT * FROM coronavirus.data_usa2 where Province_State = 'Florida' order by 3 desc,1,2;"
# # cmd = '"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql" -udatareader -pdatareader -e "' + states
# # cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + states
# cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -uroot -pDinosaur1? -e "' + states
# lst_states = os.popen(cmd).readlines()

#------------------------------------------------------------------------
# print(lst)



#get txt--------------------------------------------------------------------
# for x in lst_states:
#     state = x.rstrip('\n')
#     print(state)

#     s = " SELECT a.Last_Update ,b.Deaths - a.Deaths as Deaths "
#     s = s + "  FROM coronavirus.data_usa2 a "
#     s = s + " join coronavirus.data_usa2 b on "
#     s = s + " date(b.Last_Update) > date(a.Last_Update) and "
#     s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
#     s = s + " b.Province_State = a.Province_State "
#     s = s + " where a.Province_State = '" + state + "'"
#     s = s + " and b.Deaths - a.Deaths >= 0 "
#     s = s + " order by 1"

#     # sql = "SELECT Last_Update,Deaths FROM coronavirus.data_usa2 where Province_State = '" + state + "' order by Last_Update;"
#     # print(sql)
#     cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -uroot -pDinosaur1? -e "' + s
#     lst2 = os.popen(cmd).readlines()
#     # print(lst2[0:10])
#     statefile = statedeathsfolder + '\\' + state + '.txt'
#     with open(statefile, 'w') as f:
#         f.writelines(lst2)
#-------------------------------------------------------------------------
#         f.writelines('\n')
#         # f.write(x+ '\n')



#11/21/2020 - json output----------------------------------------------------
# for x in lst_states:
#     state = x.rstrip('\n')
#     # print(state)
#     # sql = "select json_object('Last_Update', Last_Update, 'Deaths',Deaths) from coronavirus.data_usa2 where Province_State = '" + state + "' order by Province_State;"
#     s = " select json_object('Last_Update', a.Last_Update, 'Deaths',(b.Deaths - a.Deaths)) "
#     s = s + " FROM coronavirus.data_usa2 a "
#     s = s + " join coronavirus.data_usa2 b on "
#     s = s + " date(b.Last_Update) > date(a.Last_Update) and "
#     s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
#     s = s + " b.Province_State = a.Province_State "
#     s = s + " where a.Province_State = '" + state + "'"
#     s = s + " and b.Deaths - a.Deaths >= 0 "
#     s = s + " order by a.Last_Update "

#     #sql = "SELECT Last_Update,Deaths FROM coronavirus.data_usa2 where Province_State = '" + state + "' order by Last_Update;"
#     # print(sql)
#     cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -uroot -pDinosaur1? -e "' + s
#     lst2 = os.popen(cmd).readlines()
#     # print(lst2[0:10])
#     statefile = statedeathsfolder + '\\' + state + '.json'
#     with open(statefile, 'w') as f:
#         f.writelines(lst2)
#-------------------------------------------------------------------------



# #csv output----------------------------------------------------------------
# for x in lst_states:
#     state = x.rstrip('\n')

#     s = " SELECT CONCAT_WS(',' ,a.Last_Update ,(b.Deaths - a.Deaths)) "
#     s = s + "  FROM coronavirus.data_usa2 a "
#     s = s + " join coronavirus.data_usa2 b on "
#     s = s + " date(b.Last_Update) > date(a.Last_Update) and "
#     s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
#     s = s + " b.Province_State = a.Province_State "
#     s = s + " where a.Province_State = '" + state + "'"
#     s = s + " and b.Deaths - a.Deaths >= 0 "
#     s = s + " order by 1"


#     print(s)
#     cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -uroot -pDinosaur1?  -e "' + s
#     lst3 = os.popen(cmd).readlines()
#     # print(lst2[0:10])
#     statefile = statedeathsfolder + '\\' + state + '.csv'
#     with open(statefile, 'w') as f:
#         f.writelines('Last_Update,Deaths\n')
#         f.writelines(lst3[1:])
# #------------------------------------------------------------------------

# #11/23/2020 jpg files---------------------------------------------------
# for x in lst_states[1:]: #skipping Province_State line
#     state = x.rstrip('\n')
#     print('getting pic for ' + state)
#     get_state_chart(state)

#-----------------------------------------------------------------------




