#vaers.py
#created 7/12/2021
#version in dell laptop

import csv
import os
import pandas as pd
import datetime
today = datetime.date.today()

csvfolder = 'C:/coronavirus/csv/'
dbfile = 'C:/Users/admin/Downloads/2021VAERSData/2021VAERSData.csv'

#create dataframe from dbfile
pd.set_option('display.max_rows', 20)
df1 = pd.read_csv(dbfile, encoding = 'latin1', thousands=',', low_memory=False, usecols = ['VAERS_ID','RECVDATE','STATE','AGE_YRS','DIED'])
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
df1 = df1.loc[df1['DIED'] == 'Y']
print(df1)