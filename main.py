import pandas as pd
import numpy as np

from classes.Villa import Villa
from tools.Crawler import Crawler
from tools.Writer import Writer

### SETUP ###
writer = Writer('./data/house_data.csv')
crawler = Crawler(writer)


### GET LINKS ###
header_list = ['url', 'bbr_url', 'energy', 'type', 'price'] 
links_df = pd.read_csv('./data/links.csv', encoding='iso8859_10', names=header_list)

# analyze links
print(links_df.dtypes)
print(links_df.head())

# dropping rows with no bbr url
links_df.drop(links_df[links_df['bbr_url'].str.contains('unavailable')].index, inplace=True)
print(links_df.head())

links = links_df['url'].to_numpy()

### CRAWL LINKS ###
crawler.run(links)

### TEST DATA ###
villa1 = Villa({'Boligstørrelse': '105', 'Grund': '700', 'Bygge': '1966', 'Energimærke': 'E', 'Ejerudgift': '1.525', 'Kælderstørrelse': '0'})
villa2 = Villa({'Boligstørrelse': '105', 'Grund': '700', 'Bygge': '1966', 'Energimærke': 'E', 'Ejerudgift': '1.525', 'Kælderstørrelse': '0'})
villa3 = Villa({'Boligstørrelse': '105', 'Grund': '700', 'Bygge': '1966', 'Energimærke': 'E', 'Ejerudgift': '1.525', 'Kælderstørrelse': '0'})

data = [villa1, villa2, villa3]


### WRITE TEST DATA TO FILE ###
writer.write(data)

