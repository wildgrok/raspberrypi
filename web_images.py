# https://towardsdatascience.com/rendering-images-inside-a-pandas-dataframe-3631a4883f60#791d

# Importing the necessary libraries
import pandas as pd
from IPython.core.display import HTML
# Create a dataframe using pandas library
df = pd.DataFrame([[2768571, 130655, 1155027, 34713051, 331002277],
[1448753, 60632, 790040, 3070447, 212558178],[654405, 9536, 422931, 19852167, 145934619],[605216, 17848, 359891, 8826585, 1379974505],[288477, 9860, 178245, 1699369, 32969875]], columns = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Tests', 'Population'])
# Create a list named country to store all the image paths
country = ['https://www.countries-ofthe-world.com/flags-normal/flag-of-United-States-of-America.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Brazil.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Russia.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-India.png','https://www.countries-ofthe-world.com/flags-normal/flag-of-Peru.png']
# Assigning the new list as a new column of the dataframe
df['Country'] = country
# Converting links to html tags
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'
# Rendering the dataframe as HTML table
# df.to_html(escape=False, formatters=dict(Country=path_to_image_html))
# Rendering the images in the dataframe using the HTML method.
# HTML(df.to_html(escape=False,formatters=dict(Country=path_to_image_html)))
# Saving the dataframe as a webpage
df.to_html('webpage.html',escape=False, formatters=dict(Country=path_to_image_html))