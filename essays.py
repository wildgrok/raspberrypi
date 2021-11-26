#essays.py
#created 11/24/2021
#last modified
#11/25/2021
import os
import random

#----------------globals--------------

BOOKFOLDER = 'C:/Users/admin/Documents/books'
BOOKFOLDER = 'C:/coronavirus/test'
print(BOOKFOLDER)
booklist = os.listdir(BOOKFOLDER)
print(booklist)

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

def get_sentences(book):    
    with open((BOOKFOLDER + '/' + book), encoding="utf-8") as f:
        txt = f.read()
    # a = txt.split('.')
    b = txt.replace('\n', ' ')
    a = b.replace(r"\\", '')
    # b = str(txt.split('\n\n'))
    # a = b.split('.')
    return a


def get_all_books():
    lst = []
    s = ''
    
    for x in booklist:
        
        m = get_sentences(x)
        s = s + ' ' + m
    lst = s.split('.')

    return lst

#----------------end of functions------


#----------------program start---------
lst = get_all_books()
random.shuffle(lst)
s = ''
for x in lst:
    s = s + '. ' + x
print(s)
# for x in lst:
#     b = str(x)
#     c = b.replace(r'\n',' ')
#     d = c.replace('\\','')
#     print(d)

# c = b.replace(r'\n',' ')
# d = c.replace('\\','')
# print(d)

#----------------program end-----------

