import bs4
import requests

# go to MAIN page
r = requests.get('https://www.boliga.dk/bolig/1728082/boegildsvej_12_9440_aabybro')
r.raise_for_status()
soup = bs4.BeautifulSoup(r.text, 'html.parser')

#div = soup.select_one('.app-inner-details > div:nth-child(3) > div:nth-child(1) > div:nth-child(1)')
#size = div.select_one('div.mb-md-4:nth-child(1) > app-property-detail:nth-child(1) > app-tooltip:nth-child(1) > div:nth-child(2) > span:nth-child(4)')
#print(div)

app_inner = soup.select_one('app-inner-details')
app_details = app_inner.select('app-property-detail')
spans = app_inner.select('app-property-detail  span')

data = {}
for span in spans:
    #print(span.text)
    if (':' in span.text):
        #print(span.text)
        splits = span.text.split(':')
        names = ['bolig', 'grund', 'bygge', 'energi', 'ejer', 'basement']
        data[splits[0]] = splits[1]
print(data)


# # find info on MAIN page
# price = soup.select_one('span.h4').text
# energy = soup.select_one('div.col-6:nth-child(8) > app-property-detail:nth-child(1) > app-tooltip:nth-child(1) > div:nth-child(1) > span:nth-child(4)').text
# print('Price:', price)
# print('Energy:', energy)

# go to BBR page
bbr_link = soup.select_one('div.pl-3:nth-child(2) > a:nth-child(1)').get('href')
print('BBR link:', bbr_link)
r = requests.get('https://www.boliga.dk/bbrinfo/e76ae057-3107-45b3-af17-c97924489e63')
r.raise_for_status()
soup = bs4.BeautifulSoup(r.text, 'html.parser')

# find info on BBR page
#roof = soup.select_one('app-generic-property-info-content:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > span:nth-child(2)').text
#print("Roof:", roof)

headers = soup.select('app-generic-property-info-content h4')
spans = soup.select('app-generic-property-info-content span')
cards = soup.select('app-generic-property-info-content .card-body')
blocks = soup.select('app-generic-property-info-content .block')
blocks_2 = soup.select('app-generic-property-info-content app-property-information-block')
#blocks = generics('block')
#headers = blocks.select('h4')
#spans = generics.selct('span')

#print(blocks)

for block in blocks:
    header = block.select_one('h4').text
    span = block.select_one('span').text
    print(header + ': ' + span)

# for block in blocks_2:
#     header = block.select_one('h4').text
#     span = block.select_one('span').text
#     print(header + ': ' + span)

# for card in cards:
#     span = card.select('span')
#     print(span.text)
# for idx header in headers:
#     print(header.text)

# for span in spans:
#     print(span.text)



