# make a rex parker pan

from urllib2 import urlopen
from pandas import date_range
from bs4 import BeautifulSoup as bs
from textblob import TextBlob
from random import shuffle, randint
from re import split


dates = [d.strftime('%Y-%m-%d') for d in date_range('20140101','20140131')]
urls = ["http://rexwordpuzzle.blogspot.com/search?updated-max=" \
                + d + "T15:00:00-05:00&max-results=1" for d in dates]

reviews = []
for url in urls:

    review = {'date': "", 'constructor': "", 'difficulty': "", \
              'theme': "", 'wotd': "", 'body': ""}

    sock = urlopen(url)
    lines = sock.read()
    sock.close()
    print "check"

    soup = bs(str(lines))
    soup.prettify()

    # date
    html = soup.find("h2", {"class" : "date-header"})
    date = bs(str(html)).get_text()
    review['date'] = date
    
    # constructor / # difficulty
    both = soup.p.get_text()
    divided = both.split('\n')
    review['constructor'] = divided[0]
    review['difficulty'] = divided[2]
    
    # theme
    html = soup.find_all("div", class_="post-body")
    text = bs(str(html)).get_text().split('\n')
    clean = [word for word in text if (word != '')]
    review['theme'] = clean[4]
    
    # word of the day
    for i in xrange(30):
        split_by_colon = clean[i].split(':')
        if 'Word of the Day' in split_by_colon:
            review['wotd'] = clean[i]
            break

    # body
    flag = False
    body_words = []
    for word in clean:
        if unichr(8226) in word:
            flag = True
        if (flag == True):
            word.encode('ascii','ignore')
            body_words.append(word)
    body = ''.join(body_words[1:-4]) 
    review['body'] = body

    reviews.append(review)

# concatenate bodies, only use negative sentences

content = ''.join(r['body'] for r in reviews)
sents = split("[.!?]+", content)
neg_sents = [s for s in sents if (TextBlob(s).sentiment.polarity < -0.2)]
shuffle(neg_sents)

# print pan
 
howmany = len(reviews) - 1
while True:
    n = 0
    somereview = reviews[randint(0,howmany)]['body']
    first = split("[.!?]+", somereview)[0]
    if TextBlob(first).sentiment.polarity < 0.05:
        break
    n += 1
    if n == 10:
        first = "Not going to spend much time on this one, \
            largely because I found it so unpleasant"
        break

date = reviews[randint(0,howmany)]['date']
constructor = reviews[randint(0,howmany)]['constructor']
difficulty = reviews[randint(0,howmany)]['difficulty']
theme = reviews[randint(0,howmany)]['theme']
wotd = reviews[randint(0,howmany)]['wotd']
last = "Signed, Rex Parker, King of CrossWorld"

pan = [(neg_sents[i] + '.') for i in xrange(10)]
body = ''.join(pan)

print date, '\n', constructor, '\n', difficulty, '\n', theme, \
        '\n', wotd, '\n', first, body, last

