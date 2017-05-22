import logging # For debugging purposes only
import psutil
import subprocess
import requests
import argparse
import time
from bs4 import BeautifulSoup as Soup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s\t|\t%(levelname)s\t|%(message)s')


def save_url(url_found):
    with open(args.url_log, 'r') as g:
        urls = g.readlines()

    if url_found not in urls and url_found.startswith('http://'):
        with open(args.url_log, 'a') as g:
            g.write('{0}\n'.format(url_found))


def processes_get():
    process_counter = 0
    for p in psutil.process_iter():
        if 'python.exe' == p.name():
            process_counter += 1
    return process_counter


def url_get(content):
    # for line in content.split('\n'):
    #     if 'http' in line:
    #         URL_LIST.append('' + line.split('http')[0])
    html = Soup(content, 'html.parser')
    # print([a['href'] for a in html.find_all('a')])
    for link in html.find_all('a'):
        if link.get('href') is None:
            continue
        if link.get('href').startswith('http'):
            #todo:    if link.get('href').startswith('http'):
            #todo:      AttributeError: 'NoneType' object has no attribute 'startswith'
            url_list.append(link.get('href'))


def open_url(url):
    r = requests.get(url=url)
    if r.status_code/100 == 2:
        return r.text
    return None


def url_check_exists(url, url_log_path):
    with open(url_log_path, 'r') as f:
        file_content = f.readlines()
    if url in file_content:
        return True
    return False


def process_args():
    parser = argparse.ArgumentParser(description='This is a simple crawler')
    parser.add_argument('--url_start')
    parser.add_argument('--url_log')
    parser.add_argument('--max_crawlers')
    return parser.parse_args()


def crawler_check_number(current=0):
    # Make sure crawlers don't spawn out of hand
    if int(args.max_crawlers) - (processes_get() + current) <= 0:
        # time.sleep(2)
        exit()

if __name__ == '__main__':
    # define vars
    spawn_time = time.time()

    url_list = []
    crawler_counter = 0
    logging.info("Starting crawler")
    args = process_args()
    crawler_check_number(1)

    # Check if it's a new URL
    logging.info('Checking number of processes')
    if url_check_exists(args.url_start, args.url_log):
        exit()
    logging.info('Opening link')
    # Get the website's response
    web_content = open_url(args.url_start)
    if not web_content:
        exit()
    logging.info("Parsing web content")
    url_get(web_content)
    # todo: Index text should go here
    # Spawn other crawlers for found URLs
    for url in url_list:
        save_url(url)

        crawler_check_number(1)
        subprocess.Popen(['python', 'new_crawler.py', '--url_start', url, '--url_log', args.url_log,
                          '--max_crawlers', args.max_crawlers])

    print('Finished after: {0}'.format(time.time() - spawn_time))