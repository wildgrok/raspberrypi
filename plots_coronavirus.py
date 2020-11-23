# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# created from plots.py 11/14/2020
# last update:
#11/21/2020: created json files
#11/21/2020: created state deaths files

import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
#pd.options.plotting.backend
import os

# df = pd.DataFrame({
#     'sales': [3, 2, 3, 9, 10, 6],
#     'signups': [5, 5, 6, 12, 14, 13],
#     'visits': [20, 42, 28, 62, 81, 50],
# }, index=pd.date_range(start='2018/01/01', end='2018/07/01',
#                        freq='M'))
# ax = df.plot.area()
# ax.plot()
# df.plot()
# # plt.show()
# plt.savefig("c://DOWNLOADS/plot.jpg")
# # print(ax)
# # matplotlib.validate_backend


#list of csv files
#csvfolder = r'C:\Users\python\PycharmProjects\coronavirus\csv2'
statedeathsfolder = r'C:\Users\python\PycharmProjects\coronavirus\state_deaths'



#get distinct list of states--------------------------------------------
states = 'select distinct Province_State from coronavirus.data_usa2;'
# sql = "SELECT * FROM coronavirus.data_usa2 where Province_State = 'Florida' order by 3 desc,1,2;"
# cmd = '"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql" -udatareader -pdatareader -e "' + states
cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + states
lst_states = os.popen(cmd).readlines()
#------------------------------------------------------------------------
# print(lst)

#get txt--------------------------------------------------------------------
for x in lst_states:
    state = x.rstrip('\n')
    print(state)

    s = " SELECT a.Last_Update ,b.Deaths - a.Deaths as Deaths "
    s = s + "  FROM coronavirus.data_usa2 a "
    s = s + " join coronavirus.data_usa2 b on "
    s = s + " date(b.Last_Update) > date(a.Last_Update) and "
    s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
    s = s + " b.Province_State = a.Province_State "
    s = s + " where a.Province_State = '" + state + "'"
    s = s + " and b.Deaths - a.Deaths >= 0 "
    s = s + " order by 1"

    # sql = "SELECT Last_Update,Deaths FROM coronavirus.data_usa2 where Province_State = '" + state + "' order by Last_Update;"
    # print(sql)
    cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + s
    lst2 = os.popen(cmd).readlines()
    # print(lst2[0:10])
    statefile = statedeathsfolder + '\\' + state + '.txt'
    with open(statefile, 'w') as f:
        f.writelines(lst2)
#-------------------------------------------------------------------------
#         f.writelines('\n')
#         # f.write(x+ '\n')



#11/21/2020 - json output----------------------------------------------------
for x in lst_states:
    state = x.rstrip('\n')
    # print(state)
    # sql = "select json_object('Last_Update', Last_Update, 'Deaths',Deaths) from coronavirus.data_usa2 where Province_State = '" + state + "' order by Province_State;"
    s = " select json_object('Last_Update', a.Last_Update, 'Deaths',(b.Deaths - a.Deaths)) "
    s = s + " FROM coronavirus.data_usa2 a "
    s = s + " join coronavirus.data_usa2 b on "
    s = s + " date(b.Last_Update) > date(a.Last_Update) and "
    s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
    s = s + " b.Province_State = a.Province_State "
    s = s + " where a.Province_State = '" + state + "'"
    s = s + " and b.Deaths - a.Deaths >= 0 "
    s = s + " order by a.Last_Update "

    #sql = "SELECT Last_Update,Deaths FROM coronavirus.data_usa2 where Province_State = '" + state + "' order by Last_Update;"
    # print(sql)
    cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader -e "' + s
    lst2 = os.popen(cmd).readlines()
    # print(lst2[0:10])
    statefile = statedeathsfolder + '\\' + state + '.json'
    with open(statefile, 'w') as f:
        f.writelines(lst2)
#-------------------------------------------------------------------------



#csv output----------------------------------------------------------------
for x in lst_states:
    state = x.rstrip('\n')

    s = " SELECT CONCAT_WS(',' ,a.Last_Update ,(b.Deaths - a.Deaths)) "
    s = s + "  FROM coronavirus.data_usa2 a "
    s = s + " join coronavirus.data_usa2 b on "
    s = s + " date(b.Last_Update) > date(a.Last_Update) and "
    s = s + " date(b.Last_Update) <= date(a.Last_Update) + 1 and "
    s = s + " b.Province_State = a.Province_State "
    s = s + " where a.Province_State = '" + state + "'"
    s = s + " and b.Deaths - a.Deaths >= 0 "
    s = s + " order by 1"


    print(s)
    cmd = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -udatareader -pdatareader  -e "' + s
    lst3 = os.popen(cmd).readlines()
    # print(lst2[0:10])
    statefile = statedeathsfolder + '\\' + state + '.csv'
    with open(statefile, 'w') as f:
        f.writelines('Last_Update,Deaths\n')
        f.writelines(lst3[1:])
#------------------------------------------------------------------------