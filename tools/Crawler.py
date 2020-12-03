import bs4
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm
import re
from operator import itemgetter

class Crawler():
    def __init__(self, writer):
        self.expected = ['Type', 'Energimærke', 'Ejerudgift', 'Boligydelse', 'Anvendelse', 'Boligtype', 'Enhedsareal', 'Beboelsesareal', 'Værelser', 'Antal toiletter', 'Badeforhold', 'Antal badeværelser', 'Køkkenforhold', 'Energikode', 'Toiletforhold', 'Bygningsnummer', 'Ydervæg', 'Anvendelse',
                        'Tag', 'Etager', 'Carport', 'Seneste ombygning', 'Udhus', 'Boligstørrelse (BBR)', 'Objekt status', 'Boligstørrelse, tinglyst:', 'Afvigende etager', 'Boligstørrelse', 'Boligenhed med eget køkken', 'Varmeinstallation', 'Boligenhed uden eget køkken', 'Matrikelnummer', 'Kommunal ejerlav navn', 'Grundstørrelse', 'Lands ejerlav kode', 'Vejareal', 'Lands ejerlav navn', 'Primær matrikel', 'Ejendomsnummer', 'Kommunal ejerlav kode']
        self.expected_with_types = [
            {'Type': 'str'},
            {'Energimærke': 'str'},
            {'Ejerudgift': 'int'},
            {'Boligydelse': 'int'},
            {'Anvendelse': 'str'},
            {'Boligtype': 'str'},
            {'Enhedsareal': 'int'},
            {'Beboelsesareal': 'int'},
            {'Værelser': 'int'},
            {'Antal toiletter': 'int'},
            {'Badeforhold': 'str'},
            {'Antal badeværelser': 'int'},
            {'Køkkenforhold': 'str'},
            {'Energikode': 'str'},
            {'Toiletforhold': 'str'},
            {'Bygningsnummer': 'int'},
            {'Ydervæg': 'str'},
            {'Anvendelse': 'str'},
            {'Tag': 'str'},
            {'Etager': 'int'},
            {'Carport': 'int'},
            {'Seneste ombygning': 'int'},
            {'Udhus': 'int'},
            {'Boligstørrelse (BBR)': 'int'},
            {'Objekt status': 'str'},
            {'Boligstørrelse, tinglyst:': 'int'},
            {'Afvigende etager': 'str'},
            {'Boligstørrelse': 'int'},
            {'Boligenhed med eget køkken': 'int'},
            {'Varmeinstallation': 'str'},
            {'Boligenhed uden eget køkken': 'int'},
            {'Matrikelnummer': 'str'},
            {'Kommunal ejerlav navn': 'str'},
            {'Grundstørrelse': 'int'},
            {'Lands ejerlav kode': 'str'},
            {'Vejareal': 'int'},
            {'Lands ejerlav navn': 'str'},
            {'Primær matrikel': 'str'},
            {'Ejendomsnummer': 'str'},
            {'Kommunal ejerlav kode': 'str'}
        ]

        self.encoding = 'iso8859_10'
        self.writer = writer

    def clean_data(self, key, value):
        cleaned = value
        ##exp_type = next(item for item in self.expected_with_types if key in item)
        exp_type = [item for item in self.expected_with_types if key in item] 
        if exp_type[0][key] == 'int':
            cleaned = re.sub('[^0-9]','', cleaned)
        
        return cleaned

    def run(self, links):
        #print(links)
        results = self.multithreading(self.runCrawler, links)

        return results

    def runCrawler(self, url):
        #print('running crawler')
        #for url in links:
            #print(url)
        
        try:
            data = self.crawlHousePage(url)

        except Exception as e:
            print(e)
        else:
            if data is not None:
                if self.writer.write(data, self.expected):
                    return 'Saved ' + url
                else:
                    return 'Error writing ' + str(data)
            else:
                return "no data @ " + url

    def multithreading(self, func, args, workers=None):
        start = time.time()
        #print(args)
        with ThreadPoolExecutor(workers) as ex:
            res = list(tqdm(ex.map(func, args), total=len(args)))
        
        stop = time.time()

        #return list(res), stop-start
        return 'all done', stop-start

    def crawlHousePage(self, url):
        #print(url)
        data_raw = {}
        data = {}

        # MAIN page
        r = requests.get(url)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        # checking for link to BBR page
        bbr_div = soup.select_one('div.pl-3:nth-child(2) > a:nth-child(1)')
        if bbr_div is None:
            #return "No BBR link found @ " + url
            return None

        bbr_link = bbr_div.get('href')
        if 'skoede' in bbr_link:
            #return "Link to skøde found instead of BBR @ " + url
            return None 

        # data from MAIN page
        
        # type
        type_key = 'Type'
        type_value = soup.select_one('app-property-label.d-none > label:nth-child(1) > span:nth-child(2)').text.strip()
        data_raw[type_key] = type_value
        # energimærke
        energy_span = soup.select_one('div.col-6:nth-child(8) > app-property-detail:nth-child(1) > app-tooltip:nth-child(1) > div:nth-child(1) > span:nth-child(4)').text.strip()
        energy_key = energy_span.split(':')[0]
        energy_value = energy_span.split(':')[1].strip()
        data_raw[energy_key] = energy_value

        # ejerudgift/boligydelse
        udgift_ydelse_span = soup.select_one('div.d-none:nth-child(9) > app-property-detail:nth-child(1) > app-tooltip:nth-child(1) > div:nth-child(2) > span:nth-child(4)').text.strip()
        udgift_ydelse_key = udgift_ydelse_span.split(':')[0]
        udgift_ydelse_value = udgift_ydelse_span.split(':')[1].strip()
        data_raw[udgift_ydelse_key] = udgift_ydelse_value

        # BBR page
        
        r = requests.get('https://www.boliga.dk' + bbr_link)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        # data from BBR page
        contents = soup.select('app-generic-property-info-content')

        temp = [] # for help creating the expected list
        type1 = ['Detaljerede boliginformationer', 'Bygning', 'Matrikler']
        type2 = ['Skatter', 'Ejerskab', 'Grunde']

        
        for content in contents:
            header = content.select_one('.card-header').text.strip()

            if header in type1:
                blocks = content.select('.block')
                for block in blocks:
                    key = block.select_one('h4').text.strip()
                    value = block.select_one('span').text.strip()
                    
                    #print(key + ': ' + value)
                    #temp.append(key.strip())

                    data_raw[key] = value

            if header in type2:
                blocks = content.select('app-property-information-block')
                for block in blocks:
                    header_div = block.select_one('.description')
                    value_div = block.select_one('.value')

                    if header_div is not None:
                        header = header_div.text.strip()

                    if value_div is not None:
                        value = value_div.text.strip()

                    #print(str(header) + ': ' + str(value))
                    #temp.append(key.strip())

                    data_raw[key] = value

        # cross-check crawled data with expected data types for missing data
        for ex_key in self.expected:
            if ex_key in data_raw:
                data[ex_key] = data_raw[ex_key]
                data[ex_key] = self.clean_data(ex_key, data_raw[ex_key])
            else:
                data[ex_key] = None

        #print(temp)
        return data

   


