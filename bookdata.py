import pickle,BeautifulSoup,urllib2,re
import numpy as np
import pylab as P
import nltk
import networkx as nx
import matplotlib.pyplot as plt

RAW_FILE='bookdata_raw'
PICKLE_FILE='bookdata_pickle'
COLOR_FILE='color_pickle'
STOPWORDS_FILE='stopwords'
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
                book['color'],book['name'],book['animal']=line.split(TAB) #lower title
                book['color']=' '.join(book['color'].split()) # fix: remove the last space in color name 'PMS 301C '
                books.append(book)

        with file(PICKLE_FILE,'wb') as f:
            pickle.dump(books,f)
    return books

def get_stopwords():
    with open(STOPWORDS_FILE,'r') as f:
        return f.read().split()

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
    stopwords=get_stopwords()
    for book in books:
        words=re.split(r'\s+',book.lower())
        for word in words:
            if word not in stopwords and word in wordset:
                wordset[word]=wordset[word]+1
            else:
                wordset[word]=1
    return sorted(wordset.items(), key=lambda d: d[1],reverse=True)

def network(books):
    stopwords=get_stopwords()
    G=nx.Graph()
    for book1 in books:
        G.add_node(book1['name'])
        book1_words=book1['name'].lower().split()
        for book2 in books:
            if book1==book2:
                continue
            else:
                for word in book1_words:
                    book2_words=book2['name'].lower().split()
                    if word not in stopwords and word in book2_words:
                        G.add_edge(book1['name'],book2['name'])
    pos=nx.spring_layout(G)
    nx.draw_networkx_edges(G,pos,alpha=0.05)
    nx.draw_networkx_nodes(G,pos,node_size=[G.degree(v)*10+10 for v in G],alpha=0.3)
    #nx.draw_networkx_labels(G,pos,alpha=0.3)
    print G.degree()
    plt.show()

def wordle(words):
    tags = make_tags(fdist.items()[:100], maxsize=50)
    create_tag_image(tags, 'sample_word_cloud.png', size=(900, 600), background=(0, 0, 0))
    
    
books=get_books()
colors=color_set(books)
#book_num_by_colors_img(colors)
#print colors['PMS Reflex Blue']
#print book_keywords(colors['PMS 301C'])
network(books)
