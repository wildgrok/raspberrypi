# from
# https://stackoverflow.com/questions/53468558/adding-image-to-pandas-dataframe
# https://towardsdatascience.com/rendering-images-inside-a-pandas-dataframe-3631a4883f60

import pandas as pd
# from IPython.core.display import display,HTML

df = pd.DataFrame([['A231', 'Book', 5, 3, 150], 
                   ['M441', 'Magic Staff', 10, 7, 200]],
                   columns = ['Code', 'Name', 'Price', 'Net', 'Sales'])

# your images
images1 = ['https://vignette.wikia.nocookie.net/2007scape/images/7/7a/Mage%27s_book_detail.png/revision/latest?cb=20180310083825',
          'https://i.pinimg.com/originals/d9/5c/9b/d95c9ba809aa9dd4cb519a225af40f2b.png'] 


images2 = ['https://static3.srcdn.com/wordpress/wp-content/uploads/2020/07/Quidditch.jpg?q=50&fit=crop&w=960&h=500&dpr=1.5',
           'https://specials-images.forbesimg.com/imageserve/5e160edc9318b800069388e8/960x0.jpg?fit=scale']

df['imageUrls'] = images1
df['otherImageUrls'] = images2


# convert your links to html tags 
def path_to_image_html(path=None):
    return '<img src="'+ path + '" width="60" >'

pd.set_option('display.max_colwidth', None)

image_cols = ['imageUrls', 'otherImageUrls']  #<- define which columns will be used to convert to html

# Create the dictionariy to be passed as formatters
format_dict = {}
for image_col in image_cols:
    format_dict[image_col] = path_to_image_html


# display(HTML(df.to_html(escape=False ,formatters=format_dict)))

df.to_html('c:/coronavirus/test_html.html', escape=False, formatters=format_dict)