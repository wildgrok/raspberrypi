#essays.py
#created 11/24/2021
#last modified
#11/25/2021
import os
import random
import re

#----------------globals--------------

# BOOKFOLDER = 'C:/Users/admin/Documents/books'
BOOKFOLDER = 'C:/coronavirus/test'
print(BOOKFOLDER)
booklist = os.listdir(BOOKFOLDER)
print(booklist)
OUTFILE = 'c:/coronavirus/essay.txt'

#----------------end of globals--------

#----------------functions-------------
#clean one sentence
def clean_sentence(s):
    pass

#extracts list of sentences from book
def get_sentences1(book):
    with open((BOOKFOLDER + '/' + book), encoding="utf-8") as f:
    # with open((BOOKFOLDER + '/' + book)) as f:
        txt = f.read()
        # a = txt.split('.')
        b = str(txt.split('\n\n'))
        a = b.split('.')
    return a[0:5]
    # pass

def get_book_text(book):    
    with open((BOOKFOLDER + '/' + book), encoding="utf-8") as f:
        txt = f.read()
    # a = txt.split('.')
    b = txt.replace('\n', ' ')
    d = b.replace(r"  ", ' ')
    c = d.replace(r"\r", '')
    a = c.replace(r"\\", '')
    # b = str(txt.split('\n\n'))
    # a = b.split('.')
    return a


def get_all_books():
    lst = []
    s = ''
    
    for x in booklist:
        # get text of book, append to string
        m = get_book_text(x)
        s = s + '.' + m

        # Splitting characters in String 
        #res = re.split(', |_|-|!', data)
        # lst = re.split('.', s)
        #lst = s.split('.')

    # lst.append(lst2)
    lst = s.split('.')
    random.shuffle(lst)
    # lst = re.split('.', s)

    return lst


def save_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)  
#----------------end of functions------


#----------------program start---------
lst = get_all_books()
random.shuffle(lst)
# dd:dd 
line = ''
# line = re.sub(r"</?\[\d+>", "", line)
# line = re.sub(r"\d+:\d+", "", line)

s = ''
for x in lst:
    # remove line in all caps
    if x.isupper(): x = ''
    # remove 1:22
    x = re.sub(r"\d+[:]\d+", "", x)
    s = s + '. ' + x

save_file(OUTFILE, s)


#----------------program end-----------

