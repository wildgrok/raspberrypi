# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# created from plots.py 11/14/2020
# last update:
#12/3/2020 fix to remove axis to image
#11/21/2020: created json files
#11/21/2020: created state deaths files


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess

#globals-------------------------------------------------
#statedeathsfolder = r'C:\Users\python\PycharmProjects\coronavirus\state_deaths'
statedeathsfolder = '/home/pi/Documents/state_deaths'
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





#list of csv files
#csvfolder = r'C:\Users\python\PycharmProjects\coronavirus\csv2'




#get distinct list of states--------------------------------------------
states = 'select distinct Province_State from coronavirus.data_usa2;'
# sql = "SELECT * FROM coronavirus.data_usa2 where Province_State = 'Florida' order by 3 desc,1,2;"
# cmd = '"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql" -udatareader -pdatareader -e "' + states
#cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + states
cmd = 'mysql -udbuser -pdbuserpassword -e ' + "'" + states + "'"
lst_states = os.popen(cmd).readlines()
#print(lst_states)

#------------------------------------------------------------------------
# print(lst)

#get txt--------------------------------------------------------------------
for x in lst_states:
    st = x.rstrip('\n')
    if st == 'Florida':
        
        
        print(st)

        #s = " SELECT a.Last_Update ,b.Deaths - a.Deaths as Deaths "
#         s = " SELECT a.Last_Update ,b.Deaths - a.Deaths "
#         s = s + "  FROM coronavirus.data_usa2 a "
#         s = s + " join coronavirus.data_usa2 b on "
#         s = s + " date(b.Last_Update) > date(a.Last_Update) and "
#         s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
#         s = s + " b.Province_State = a.Province_State "
#         s = s + " where a.Province_State = '" + state + "' "
#         s = s + " and b.Deaths - a.Deaths >= 0;"
#         #s = s + " order by 1"

        s = "SELECT a.Last_Update,a.Deaths FROM data_usa2 a WHERE a.Province_State = '" + st + "' order by a.Last_Update;"
        # print(sql)
        cmd = 'mysql -udbuser -pdbuserpassword coronavirus -e ' + "'" + s + "'" 
        lst2 = os.popen(cmd)
        # print(lst2[0:10])
        statefile = statedeathsfolder + '/' + st + '.txt'
        with open(statefile, 'w') as f:
            f.writelines(lst2)
            #f.write(lst2)
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
# 
#     #sql = "SELECT Last_Update,Deaths FROM coronavirus.data_usa2 where Province_State = '" + state + "' order by Last_Update;"
#     # print(sql)
#     cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + s
#     lst2 = os.popen(cmd).readlines()
#     # print(lst2[0:10])
#     statefile = statedeathsfolder + '\\' + state + '.json'
#     with open(statefile, 'w') as f:
#         f.writelines(lst2)
#-------------------------------------------------------------------------



#csv output----------------------------------------------------------------
# for x in lst_states:
#     state = x.rstrip('\n')
# 
#     s = " SELECT CONCAT_WS(',' ,a.Last_Update ,(b.Deaths - a.Deaths)) "
#     s = s + "  FROM coronavirus.data_usa2 a "
#     s = s + " join coronavirus.data_usa2 b on "
#     s = s + " date(b.Last_Update) > date(a.Last_Update) and "
#     s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
#     s = s + " b.Province_State = a.Province_State "
#     s = s + " where a.Province_State = '" + state + "'"
#     s = s + " and b.Deaths - a.Deaths >= 0 "
#     s = s + " order by 1"
# 
# 
#     print(s)
#     cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader  -e "' + s
#     lst3 = os.popen(cmd).readlines()
#     # print(lst2[0:10])
#     statefile = statedeathsfolder + '\\' + state + '.csv'
#     with open(statefile, 'w') as f:
#         f.writelines('Last_Update,Deaths\n')
#         f.writelines(lst3[1:])
#------------------------------------------------------------------------

#11/23/2020 jpg files---------------------------------------------------
# for x in lst_states[1:]: #skipping Province_State line
#     state = x.rstrip('\n')
#     print('getting pic for ' + state)
#     get_state_chart(state)

#-----------------------------------------------------------------------




