import pickle,BeautifulSoup,urllib2,re
import numpy as np
import pylab as P

RAW_FILE='bookdata_raw'
PICKLE_FILE='bookdata_pickle'
COLOR_FILE='color_pickle'
TAB='	'

def get_books():
    try:
        with file(PICKLE_FILE,'rb') as f:
            books=pickle.load(f)
    except:
        books=[]
        with open(RAW_FILE,'r') as f:
            for line in f.readlines():
                book={}
                book['color'],book['name'],book['animal']=line.split(TAB)
                book['color']=' '.join(book['color'].split()) # fix: remove the last space in color name 'PMS 301C '
                books.append(book)

        with file(PICKLE_FILE,'wb') as f:
            pickle.dump(books,f)
    return books

def get_rgb():
    pms2rgb={}
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen('http://oreilly.com/animals.html').read())
    table=soup.findAll('table')[1]
    for row in table.findAll('tr')[1:]:
        cell=row.findAll('td')[0]
        rgb,pms=cell['bgcolor'].upper(),' '.join(cell.text.split())
        if pms not in pms2rgb.keys():
            pms2rgb[pms]=rgb
    return pms2rgb

def color_set(books):
    try:
        with file(COLOR_FILE,'rb') as f:
            colors=pickle.load(f)
    except:
        colors={}
        for book in books:
            if book['color'] in colors.keys():
                colors[book['color']].append(book['name'])
            else:
                colors[book['color']]=[book['name']]
        with file(COLOR_FILE,'wb') as f:
            pickle.dump(colors,f)
    return colors

def book_num_by_colors_img(colors):
    x=[key for key in colors.keys()]
    y=[len(colors[key]) for key in colors.keys()]
    # the histogram of the data
    pms2rgb=get_rgb()
    for xitem,yitem in zip(xrange(len(x)),y):
        P.bar(xitem,yitem,color=pms2rgb[x[xitem]],align="center")
    P.xticks(xrange(len(x)),x)
    P.show()

def book_keywords(books):
    wordset={}
    for book in books:
        words=re.split(r'\s+',book.lower())
        for word in words:
            if word in wordset:
                wordset[word]=wordset[word]+1
            else:
                wordset[word]=1
    
    for word in wordset:
        print word,wordset[word]

def word_cloud(words):
    pass
    
books=get_books()
colors=color_set(books)
book_num_by_colors_img(colors)
#print colors['PMS Reflex Blue']
#book_keywords(colors['PMS Reflex Blue'])
