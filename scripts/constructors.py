# get list of crossword constructors for the current week
# from reviews at Fiend

import urllib
import re

# get the data in html
sock = urllib.urlopen("http://www.crosswordfiend.com/blog/")
lines = sock.readlines()
sock.close()

l = len(lines)
text = []
for i in range(l):
    if "daily-puzzles" in lines[i] and "View" not in lines[i]:
        text.append(lines[i])
string = str(text)

# now we have all lines with constructors
hyphenated = re.findall(r'\w+(?:-\w+)+',string)		
sh = str(hyphenated)

# remove tagging
tags = re.findall(r"\'tag-+\w+-+\w+",sh)
tags_middle_names = re.findall(r"\'tag-+\w+-+\w+-+\w+",sh)
alltags = tags + tags_middle_names

# remove punctuation
authors = str(alltags)
authors = re.sub("\'tag-","",authors)
authors = re.sub("\w+-.\", ","", authors)
authors = re.sub("-"," ", authors)
authors = authors.translate(None, '[]"')

# listify and sort
authlist = authors.split(', ')
authlist = sorted(list(set(authlist)))

# final nuisances
if "brendan emmett" in authlist:
    authlist.remove("brendan emmett")
if "martin ashwood" in authlist:
    authlist.remove("martin ashwood")

print authlist
