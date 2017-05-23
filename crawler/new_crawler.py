# todo: add text indexing
# todo: consider checking if a url already exists in the queue.

import os
from collections import Counter
from multiprocessing import Queue, Pool
import loggers
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import argparse
import time
from bs4 import BeautifulSoup as Soup

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = loggers.Loggers('sysLogger', 'urlLogger')
urlLogger = logger.get_urllogger()
sysLogger = logger.get_syslogger()


def get_proxy(prx):
    if prx and prx.startswith('http://'):
        return {'http': args.proxy}
    elif prx and prx.startswith('https://'):
        return {'https': args.proxy}
    else:
        return False


def url_get(content, q):
    html = Soup(content, 'html.parser')
    temp_dict = {}
    for i in Counter(html.findAll(text=True)):
        temp_dict.update({i: Counter(html.findAll(text=True)).get(i)})
    print temp_dict
    for tag in html.find_all('a'):
        if tag.get('href') is None:
            continue
        if tag.get('href') and tag.get('href').startswith('http'):
            # logging.info('Found {0}'.format(tag.get('href')))
            q.put(tag.get('href'))
            urlLogger.info(tag.get('href'))


def open_url(scan_url, prx):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/58.0.3029.110 Safari/537.36'}
        if prx:
            r = requests.get(url=scan_url, verify=False, proxies=prx, headers=headers)
        else:
            r = requests.get(url=scan_url, verify=False, headers=headers)

        if r.status_code / 100 == 2:
            return r.text.encode('utf-8')

    except Exception, e:
        sysLogger.exception('Exception for url: {0}'.format(scan_url))
        print e.message
    return None


def process_args():
    parser = argparse.ArgumentParser(description='This is a simple crawler')
    parser.add_argument('--url_start', nargs='+', required=True)
    parser.add_argument('--url_log', required=True)
    parser.add_argument('--max_crawlers', required=True, type=int)
    parser.add_argument('--proxy')
    return parser.parse_args()


def process_url(q, prx):
    sysLogger.info('Worker {0} is started.'.format(os.getpid()))
    while True:
        my_url = q.get(True)
        # Read the URL content
        text = open_url(my_url, prx)
        if text:
            url_get(text, q)


if __name__ == '__main__':
    sysLogger.info('Starting father spider')

    # define vars
    args = process_args()
    proxy = get_proxy(args.proxy)
    queue = Queue()
    sysLogger.debug('Starting process pool')
    pool = Pool(args.max_crawlers, process_url, (queue, proxy))
    sysLogger.debug('Creating queue')
    for url in args.url_start:
        queue.put(url)

    time.sleep(11)
    while queue.qsize() != 0:
        time.sleep(3)
