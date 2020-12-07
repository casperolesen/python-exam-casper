import pandas as pd
import numpy as np

from classes.Villa import Villa
from tools.Crawler import Crawler
from tools.Writer import Writer

### SETUP ###
writer = Writer('./data/house_data.csv')
crawler = Crawler(writer)

### GET LINKS NEW ###
links_df = pd.read_csv('./data/links.csv', encoding='iso8859_10')
#print(links_df.head())
links = links_df.iloc[:,0]
#links_50 = links[:50].tolist()

### GET LINKS OLD ###
#header_list = ['url', 'bbr_url', 'energy', 'type', 'price'] 
#links_df = pd.read_csv('./data/links.csv', encoding='iso8859_10', names=header_list)
# analyze links
#print(links_df.dtypes)
#print(links_df.head())
# dropping rows with no bbr url
#links_df.drop(links_df[links_df['bbr_url'].str.contains('unavailable')].index, inplace=True)
#print(links_df.head())
#links = links_df['url'].to_numpy()


### CRAWL LINKS AND WRITE DATE TO FILE ###
#print(crawler.run(links))


### VIEW HOUSE DATA ###

#house_data = pd.read_csv('./data/house_data.csv', encoding='UTF-8')
#print(house_data.head())
#print(house_data[:100])


