# coding: utf-8

# Can we train a computer to make a crossword? part 1: scraping data

# In[1]:

import urllib
import re
import datetime

from ast import literal_eval
from calendar import month_name


# In[2]:

# get the urls with the finished grids
# TODO switch to crosswordfiend to augment with other outlets
N_weeks = 50
url_start, url_end = "http://rexwordpuzzle.blogspot.com/search?updated-max=", "T00:00:00-00:00&max-results=10"
dates = []
today = datetime.datetime.now()
for i in range(N_weeks):
    diff = datetime.timedelta(days=7 * i)
    earlier = today - diff
    dates.append(earlier.strftime("%Y-%m-%d"))
    
urls = [url_start + date + url_end for date in dates]

# extract just the grid images, usually uploaded as tiffs
tiffs = []
for url in urls:
    sock = urllib.urlopen(url)
    lines = sock.readlines()
    tiffs.extend(re.findall("https://[^ ]*s1600[^ ]*[0-9].tiff", str(lines)))
    sock.close()


# In[3]:

# some more filtering of bad tiffs because my first regex was lazy
# also had to remove a few cases where the day of month was >31 for some reason

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_pattern = "|".join(months)
good_tiffs = [t for t in tiffs if re.findall(month_pattern, t)]
good_tiffs = list(set(good_tiffs)) # about 280 left


# In[4]:

with open("good_tiffs.pkl", "w") as f:
    pickle.dump(ratings_dict, f)


# In[5]:

# download the images to appropriately named files
for t in good_tiffs:
    month = t.split("/")[-1][:3]
    day = t.split("/")[-1][3:-5]
    urllib.urlretrieve(t, "grids/{0}_{1}.tiff".format(month, day))


# In[6]:

# get ratings for the crosswords
ratings_dict = {}

url_start, url_end = "http://crosswordfiend.com/ratings_count_json.php?puzz=", "-ny"
month_names = [month_name[i].lower() for i in range(1, 13)]
month_dict = dict(zip(months, month_names))
get_year = lambda month: '2017' if month in month_names[:3] else '2016'

for t in good_tiffs:
    month = month_dict[t.split("/")[-1][:3]]
    day = t.split("/")[-1][3:-5]
    year = get_year(month)
    day_of_week = datetime.datetime.strptime(month + day + year, '%B%d%Y').strftime('%A').lower()
    url_mid = "-".join([day_of_week, month, day, year])
    url = url_start + url_mid + url_end

    sock = urllib.urlopen(url)
    lines = sock.readlines()
    sock.close()
    rating = literal_eval(lines[0])['round_avg']
    ratings_dict[month + "_" + day] = rating


# In[7]:

with open("ratings_dict.pkl", "w") as f:
    pickle.dump(ratings_dict, f)
