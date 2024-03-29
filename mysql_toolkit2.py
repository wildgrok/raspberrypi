__author__ = 'python'
#version in rasberry pi
#last modified
#7/10/2021 fixed csvfolder
#7/8/2021 version with no mysql
#6/22/2021 moved to dell laptop
#12/4/2020 fixed folder to /csv2, was /csv
# 7/6/2020 works with short table data_usa2
# 6/17/2020

import csv
# import MySQLdb
import os
import pandas as pd
import datetime
today = datetime.date.today()


csvfolder = '/home/pi/Documents/'
dbfile = '/home/pi/Documents/data_usa.csv'

#exports to text file database contents of current csv file
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
            csvfile = csvfolder + x
            load_csv_file(csvfile)
            # print('Processed ' + csvfile)

#===========================================================================


load_all_csv_files(csvfolder)