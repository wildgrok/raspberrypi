__author__ = 'python'
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-data-frame
from IPython.core.display import HTML

import pandas as pd
import numpy as np
# import matplotlib
import matplotlib.pyplot as plt

folder = 'C:\\Users\\python\\PycharmProjects\\coronavirus\\state_deaths\\'
folder2 = 'C:\\DOWNLOADS\\'
#pd.options.plotting.backend
def get_state_chart(state):
    df = pd.read_csv((folder + state + '.csv'), encoding = 'latin1', thousands=',')
    df = df.set_index('Last_Update')
    df = df[np.abs(df.Deaths-df.Deaths.mean()) <= (3*df.Deaths.std())]
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Deaths'.

    ax = df.plot.area()

    # ax.plot()
    # df.plot()
    ax.set_axis_off()

    # plt.plot(df['Deaths'].rolling(3).mean(),label= 'MA 3 days')
    plt.savefig(folder2 + 'foo.jpg', dpi=100, bbox_inches='tight', pad_inches=0.0, transparent=True)
    plt.savefig(folder2  + state + '.jpg')


if __name__ == '__main__':
    # C:\Users\python\PycharmProjects\coronavirus\state_deaths
    get_state_chart('Florida')