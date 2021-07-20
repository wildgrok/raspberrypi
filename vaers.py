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
pd.set_option('display.max_rows', 2)
df1 = pd.read_csv(dbfile, encoding = 'latin1', thousands=',', low_memory=False, usecols = ['VAERS_ID','RECVDATE','SYMPTOM_TEXT','STATE','AGE_YRS','DIED'])
columns = df1.columns
# print('columns')
# print(columns)
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
# df1 = df1.loc[df1['DIED'] == 'Y']
# df1 = df1.loc[df1['SYMPTOM_TEXT'] > '']
# new_df = old_df[((old_df['C1'] > 0) & (old_df['C1'] < 20)) & ((old_df['C2'] > 0) & (old_df['C2'] < 20)) & ((old_df['C3'] > 0) & (old_df['C3'] < 20))]
print('df1 no limitations count')
print(df1.VAERS_ID.count())


l = ['covid','Covid','COVID']
df1 = df1[ (df1['DIED'] == 'Y') & ( df1['SYMPTOM_TEXT'] > '' )]
print("df1 DIED and SYMPTOM_TEXT > '' count")
print(df1.VAERS_ID.count())
l = ['covid','Covid','COVID']
df1 = df1[df1['SYMPTOM_TEXT'].str.contains('covid', case = False)]
print('df1 after string covid count')
print(df1.VAERS_ID.count())

print('getting pic')
df = df1.drop(['VAERS_ID','STATE','AGE_YRS','SYMPTOM_TEXT'], axis=1)

df["RECVDATE"] = pd.to_datetime(df["RECVDATE"])

df.set_index('RECVDATE')

df = df.groupby('RECVDATE').count()


total_deaths = df.DIED.sum()
print('Total deaths after df.DIED.sum()')
print(total_deaths)


columns = df.columns

ax = df.plot.area(stacked=False)
# ax.set_axis_off()
statejpgfile = 'c:/coronavirus/vaers.jpg'
plt.savefig(statejpgfile)