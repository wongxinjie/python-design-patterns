# coding: utf-8
import os
import urllib
import threading
from urlparse import urlparse, urljoin

import httplib2
from BeautifulSoup import BeautifulSoup as BS


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class ImageDownloadWorker(threading.Thread):

    def __init__(self, thread_id, name, counter):
        super(ImageDownloadWorker, self).__init__()
        self.name = name
        self.thread_id = thread_id
        self.counter = counter

    def run(self):
        print "Starting thread ", self.name
        download_images(self.name)
        print "Finished thread ", self.name


def clean_url(parser, PARSED_ROOT):
    url = '{scheme}://{netloc}{path}'.format(
        scheme=PARSED_ROOT.scheme or parser.scheme,
        netloc=PARSED_ROOT.netloc or parser.netloc,
        path=parser.path or ''
        )
    return url


def _request(url):
    http = httplib2.Http()
    try:
        header, response = http.request(url)
    except:
        return None, None
    return header, response


def traverse_site(url, max_links=10):
    PARSED_ROOT = urlparse(url)
    link_parser = Singleton()

    while link_parser.queue_to_parse:
        if len(link_parser.to_visit) == max_links:
            return

        url = link_parser.queue_to_parse.pop()
        header, response = _request(url)
        if response is None:
            continue

        # Skip if not a web page
        if header.get('content-type') != 'text/html':
            continue

        link_parser.to_visit.add(url)
        print "Add {} to queue".format(url)

        bs = BS(response)
        for link in BS.findAll(bs, 'a'):
            link_url = link.get('href')

            if not link_url:
                continue

            parsed = urlparse(link_url)
            # Skip external webpage
            if parsed.netloc and parsed.netloc != PARSED_ROOT.netloc:
                continue

            link_url = clean_url(parsed, PARSED_ROOT)
            if link_url in link_parser.to_visit:
                continue

            link_parser.queue_to_parse.append(link_url)


def download_images(thread_name):
    singleton = Singleton()
    while singleton.to_visit:
        url = singleton.to_visit.pop()

        print "{} starting download images form {}".format(thread_name, url)
        header, response = _request(url)
        if not response:
            continue

        bs = BS(response)
        images = BS.findAll(bs, 'img')
        for image in images:
            src = image.get('src')
            src = urljoin(url, src)

            basename = os.path.basename(src)
            if basename and src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print 'Downloading ', src
                urllib.urlretrieve(src, os.path.join('images', basename))
        print "{} Finished Downloading images from {}".format(thread_name, url)


def main(url):

    singleton = Singleton()
    singleton.queue_to_parse = [url]
    singleton.to_visit = set()
    singleton.downloaded = set()

    traverse_site(url)

    if not os.path.exists('images'):
        os.makedirs('images')

    worker1 = ImageDownloadWorker(1, "worker-1", 1)
    worker2 = ImageDownloadWorker(2, "worker-2", 2)

    worker1.start()
    worker2.start()


if __name__ == "__main__":
    url = 'http://clothing.lady8844.com'
    main(url)
