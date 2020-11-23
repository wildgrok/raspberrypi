__author__ = 'python'
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html


import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
#pd.options.plotting.backend

df = pd.read_csv((r'C:\Users\python\PycharmProjects\coronavirus\state_deaths\Florida.csv'), encoding = 'latin1', thousands=',')
#df = pd.read_csv((r'C:\downloads\Florida2.csv'), encoding = 'latin1', thousands=',')

# df = pd.DataFrame({
#     'sales': [3, 2, 3, 9, 10, 6],
#     'signups': [5, 5, 6, 12, 14, 13],
#     'visits': [20, 42, 28, 62, 81, 50],
# }, index=pd.date_range(start='2018/01/01', end='2018/07/01',
#                       freq='M'))
df = df.set_index('Last_Update')


ax = df.plot.area()
ax.plot()
df.plot()
# plt.show()
plt.savefig("c://DOWNLOADS/plot.jpg")
# print(ax)
# matplotlib.validate_backend