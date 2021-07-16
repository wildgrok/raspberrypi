#vaers.py
#created 7/12/2021
#version in dell laptop

import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
today = datetime.date.today()

csvfolder = 'C:/coronavirus/csv/'
dbfile = 'C:/Users/admin/Downloads/2021VAERSData/2021VAERSData.csv'





#create dataframe from dbfile
pd.set_option('display.max_rows', 20)
df1 = pd.read_csv(dbfile, encoding = 'latin1', thousands=',', low_memory=False, usecols = ['VAERS_ID','RECVDATE','SYMPTOM_TEXT','STATE','AGE_YRS','DIED'])
columns = df1.columns
print(columns)
# Index(['VAERS_ID', 'RECVDATE', 'STATE', 'AGE_YRS', 'CAGE_YR', 'CAGE_MO', 'SEX',
#        'RPT_DATE', 'SYMPTOM_TEXT', 'DIED', 'DATEDIED', 'L_THREAT', 'ER_VISIT',
#        'HOSPITAL', 'HOSPDAYS', 'X_STAY', 'DISABLE', 'RECOVD', 'VAX_DATE',
#        'ONSET_DATE', 'NUMDAYS', 'LAB_DATA', 'V_ADMINBY', 'V_FUNDBY',
#        'OTHER_MEDS', 'CUR_ILL', 'HISTORY', 'PRIOR_VAX', 'SPLTTYPE',
#        'FORM_VERS', 'TODAYS_DATE', 'BIRTH_DEFECT', 'OFC_VISIT', 'ER_ED_VISIT',
#        'ALLERGIES'],

#print(df1)
# df.loc[df['column_name'] == some_value]
# only bring died with covid mentioned in SYMPTOM_TEXT
df1 = df1.loc[df1['SYMPTOM_TEXT'] > '']
df1 = df1[df1['SYMPTOM_TEXT'].str.contains('covid')]
df1 = df1.loc[df1['DIED'] == 'Y']
print(df1)


print('getting pic')
# ax = df.plot.area()
df = df1.drop(['VAERS_ID','STATE','AGE_YRS','SYMPTOM_TEXT'], axis=1)

# Grouping By Day, Week and Month with Pandas DataFrames
# This maybe useful to someone besides me. I had a dataframe in the following format:

# 0,2013-07-15 17:15:19,1,8872,291840,92
# 1,2011-07-19 23:26:24,2,18890,760336,0
# 2,2011-07-26 22:58:35,2,2902,76746,0
# 3,2011-07-28 22:27:12,2,103222,954442,0
# 4,2011-07-29 21:26:27,2,107134,885380,0
# 5,2011-07-31 04:11:38,2,44228,813568,0
# 6,2011-08-02 23:17:39,2,109242,1157330,0
# 7,2011-08-03 22:14:08,2,51736,870914,0
# 8,2011-08-04 21:41:33,2,18390,652704,0

# And I wanted to sum the third column by day, wee and month. There are multiple reasons why you can just read in this code with a simple

# df = pd.read_csv(file)



# And go to town. First we need to change the second column (_id) from a string to a python datetime object to run the analysis:

df["RECVDATE"] = pd.to_datetime(df["RECVDATE"])


# OK, now the _id column is a datetime column, but how to we sum the count column by day,week, and/or month? 
# First, we need to change the pandas default index on the dataframe (int64). You can find out what type of index 
# your dataframe is using by using the following command

print(df.index)

# To perform this type of operation, we need a pandas.DateTimeIndex and then we can use pandas.resample, 
# but first lets strip modify the _id column because I do not care about the time, just the dates.

# df['date_minus_time'] = df["RECVDATE"].apply( lambda df : datetime.datetime(year=df.year, month=df.month, day=df.day))	
# df.set_index(df["date_minus_time"],inplace=True)
df.set_index('RECVDATE')

# Finally, if you want to group by day, week, month respectively:

# df['count'].resample('D', how='sum')
# df['count'].resample('W', how='sum')
# df['count'].resample('M', how='sum')

# df.groupby('a').resample('3T').sum()
# df['DIED'].resample('D').count
# df['DIED'].resample('W').count
# df['DIED'].resample('M').count

# df.groupby('RECVDATE').resample('M').count()
df = df.groupby('RECVDATE').count('COUNT')

print(df)

total_deaths = df.DIED.sum()
# start_date = df['RECVDATE'].min()
# last_date =  df['RECVDATE'].max()
# print('Total deaths from ', start_date, ' to ', last_date )
print(total_deaths)

columns = df.columns
print(columns)





# df.index = pd.to_datetime(df['RECVDATE'])
# df.index = pd.to_datetime(df['RECVDATE'],format='%m/%d/%y')
# df.index = pd.to_datetime(df['RECVDATE'],format='%m/%d/%y %I:%M%p')
# df.groupby(by=[df.index.month, df.index.year])
# df = df.groupby(['RECVDATE'])



# df['Deaths'] = df.groupby(['RECVDATE']).count()
# df = df.drop(['DIED'], axis=1)
# df.groupby(['RECVDATE']).sum()
ax = df.plot.area(stacked=False)
# ax.set_axis_off()
# ax.plot()
# df.plot()
statejpgfile = 'c:/coronavirus/vaers.jpg'
plt.savefig(statejpgfile)