class Crawler():
    def __init__(self, writer):
        self.encoding = 'iso8859_10'
        self.writer = writer

    def run(self, links):
        print('running crawler')
        for link in links:
            print(link)

    def crawl_villa(self, link):
        pass

    def crawl_apartment(self, link):
        pass

