import bs4
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm
import re
from operator import itemgetter

class Crawler():
    def __init__(self, writer):
        self.expected = ['URL', 'Adresse', 'Year build', 'Pris', 'Type', 'Energimærke', 'Ejerudgift', 'Boligydelse', 'Anvendelse', 'Boligtype', 'Enhedsareal', 'Beboelsesareal', 'Værelser', 'Antal toiletter', 'Badeforhold', 'Antal badeværelser', 'Køkkenforhold', 'Energikode', 'Toiletforhold', 'Bygningsnummer', 'Ydervæg',
                        'Tag', 'Etager', 'Carport', 'Seneste ombygning', 'Udhus', 'Boligstørrelse BBR', 'Objekt status', 'Boligstørrelse tinglyst', 'Afvigende etager', 'Boligstørrelse', 'Boligenhed med eget køkken', 'Varmeinstallation', 'Boligenhed uden eget køkken', 'Matrikelnummer', 'Kommunal ejerlav navn', 'Grundstørrelse', 'Lands ejerlav kode', 'Vejareal', 'Lands ejerlav navn', 'Primær matrikel', 'Ejendomsnummer', 'Kommunal ejerlav kode', 'Ejendomsværdiskat', 'Grundskyld']
        self.expected_with_types = [
            {'URL': 'url'},
            {'Adresse': 'str'},
            {'Year build': 'int'},
            {'Pris': 'int'},
            # {'Kvadratmeter pris': 'int'},
            # {'Gnm kvadratmeter pris i area', 'int'},
            # {'Area Population': 'int'},
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
            {'Tag': 'str'},
            {'Etager': 'int'},
            {'Carport': 'int'},
            {'Seneste ombygning': 'int'},
            {'Udhus': 'int'},
            {'Boligstørrelse BBR': 'int'},
            {'Objekt status': 'str'},
            {'Boligstørrelse tinglyst': 'int'},
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
            {'Kommunal ejerlav kode': 'str'},
            {'Ejendomsværdiskat': 'int'},
            {'Grundskyld': 'int'}
        ]

        self.encoding = 'iso8859_10'
        self.writer = writer

    def clean_header(self, header):
        cleaned = header
        cleaned = re.sub(r'\W+', ' ', cleaned).strip()

        return cleaned

    def clean_data(self, key, value):
        cleaned = value
        ##exp_type = next(item for item in self.expected_with_types if key in item)
        exp_type = [item for item in self.expected_with_types if key in item] 
        if exp_type[0][key] == 'int':
            cleaned = re.sub('[^0-9]','', cleaned)

        if exp_type[0][key] == 'str':
            cleaned = re.sub(r'\W+', ' ', cleaned).strip()
        
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
                        #return 'Saved ' + url
                        return str(data)
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
        
        # url
        url_key = 'URL'
        url_value = url
        data_raw[url_key] = url_value

        # pris
        pris_key = 'Pris'
        pris_value = soup.select_one('span.h4').text.strip()
        data_raw[pris_key] = pris_value
        
        # year build
        year_build_span = soup.select_one('div.col-6:nth-child(7) > app-property-detail:nth-child(1) > app-tooltip:nth-child(1) > div:nth-child(1) > span:nth-child(4)').text.strip()
        year_build_key = 'Year build'
        year_build_value = year_build_span.split(':')[1].strip()
        data_raw[year_build_key] = year_build_value

        # adresse
        addr_key = 'Adresse'
        addr_value = soup.select_one('div.col-md-12:nth-child(1) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)').text.strip()
        data_raw[addr_key] = addr_value

        # # kvadratmeter pris
        # sqmeter_price_key = 'Kvadratmeter pris'
        # sqmeter_price_value = soup.select_one('span.d-block:nth-child(2)').text.strip()
        # data_raw[sqmeter_price_key] = sqmeter_price_value

        # # area avg kvadratmeter pris
        # avg_sqmeter_price_area_key = 'Gnm kvadratmeter pris i area'
        # avg_sqmeter_price_area_value = soup.select_one('div.border-bottom:nth-child(2) > div:nth-child(1) > app-property-information-block:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)').text.strip()
        # data_raw[avg_sqmeter_price_area_key] = avg_sqmeter_price_area_value

        # #area population
        # area_population_key = 'Area Population'
        # area_population_value = soup.select_one('app-property-information-block.col-6:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text.strip()
        # data_raw[area_population_key] = area_population_value


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

        type1 = ['Detaljerede boliginformationer', 'Bygning', 'Matrikler']
        type2 = ['Skatter', 'Ejerskab', 'Grunde']

        
        for content in contents:
            header = content.select_one('.card-header').text.strip()

            if header in type1:
                blocks_type1 = content.select('.block')
                for block_type1 in blocks_type1:
                    key_type1 = block_type1.select_one('h4').text.strip()
                    value_type1 = block_type1.select_one('span').text.strip()

                    #print(key_type1 + ': ' + value_type1)
                    #temp.append(key.strip())

                    #print(self.clean_header(key))

                    data_raw[self.clean_header(key_type1)] = value_type1

            if header in type2:
                blocks_type2 = content.select('app-property-information-block')
                for block_type2 in blocks_type2:
                    header_div_type2 = block_type2.select_one('.description')
                    value_div_type2 = block_type2.select_one('.value')

                    if header_div_type2 is not None and value_div_type2 is not None:
                        header_type2 = header_div_type2.text.strip()
                        value_type2 = value_div_type2.text.strip()
                    
                    #if value_div is not None:
                        #value = value_div.text.strip()

                        #print(header_type2 + ' : ' + value_type2)
                    #temp.append(key.strip())

                    #print(self.clean_header(key))

                        data_raw[self.clean_header(header_type2)] = value_type2
                    

        #print('DATA RAW')
        #print(data_raw)
        # cross-check crawled data with expected data types for missing data
        #print('cross checking: ')
        for ex_key in self.expected:
            if ex_key in data_raw:
                #print(ex_key + ' : ' + data_raw[ex_key])
                #data[ex_key] = data_raw[ex_key]
                data[ex_key] = self.clean_data(ex_key, data_raw[ex_key])
            else:
                #print(ex_key + ' : ' + 'None data')
                data[ex_key] = None

        return data

   


