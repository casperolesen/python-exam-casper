from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import csv
import threading

links = ['link-1', 'link-2', 'link-3', 'link-4', 'link-5', 'link-6', 'link-7', 'link-8', 'link-9', 'link-10']
csv_writer_lock = threading.Lock()

def multithreading(func, args, workers=None):
        #print(args)
        with ThreadPoolExecutor(workers) as ex:
            res = list(tqdm(ex.map(func, args), total=len(args)))

        return list(res)

def getData(url):
    time.sleep(2)
    return url

def safeData(data):
    with open('./data/test.csv', 'a', newline='', encoding='utf-8') as file:
        with csv_writer_lock:
            writer = csv.writer(file)
            writer.writerow(data)

def helper(link):
    data = getData(link)
    safeData(data)

def run(links):
    res = multithreading(helper, links)

    return res

run(links)