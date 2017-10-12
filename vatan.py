import io
import os
import logging
import argparse
import urllib2
from datetime import datetime
from decimal import Decimal
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

url1 = 'http://www.vatanbilgisayar.com/dell-xps-\
13-9360-core-i7-7500u-2-7ghz-8gb-ram-256-ssd-int-13-3-w10.html'

url2 = 'http://www.vatanbilgisayar.com/lenovo-thinkpad-x1-carbon-\
core-i7-7600u-2-8ghz-16gb-ram-256gb-ssd-int-14-w10.html'

url3 = 'http://www.vatanbilgisayar.com/dell-xps\
-13-core-i7-7500u-2-7ghz-16gb-ram-512-ssd-int-13-3-w10.html'

urls = (url1, url2, url3)

keyword = 'taksit_pesin taksitTutar1'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

headers = {'User-Agent': user_agent}


def fetch_price(url):
    request = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), 'html.parser')

    price_elem = soup.find('td', class_=keyword).contents[0]
    amount, currency = price_elem.split()
    amount = amount.replace(',', '')
    desc = unicode(soup.h1.contents[0])

    logger.debug('amount=%s, currency=%s, desc=%s', amount, currency, desc)
    item = PriceItem(desc, amount, currency)
    return item

# print soup.find('span', class_='urunDetay_satisFiyat').contents[0]
# print soup.find('span', class_='urunDetay_satisFiyat')
# \.contents[1].contents[0]


def persist(item):
    def get_file_name():
        return os.environ["HOME"] + '/.item_prices'

    f = io.open(get_file_name(), 'at', encoding='UTF-8', newline=None)
    ser = ':'.join((item.name,
                    str(item.amount).encode('UTF-8'),
                    item.currency,
                    str(item.datetime)))
    f.write(ser + '\n')


class PriceItem(object):
    """Represents a snapshot of the price of self.name at self.datetime
    Attributes:
        name (str): Description of `attr1`.
        amount (Decimal) attr2 (:obj:`int`, optional): Description of `attr2`.
        currency (str)
        datetime (datetime)
    """
    def __init__(self, name, amount, currency, datetime=None):
        self.name = name
        self.amount = Decimal(amount)
        self.currency = currency
        self.datetime = datetime if datetime else datetime.now()


class Container(object):
    def __init__(self, name):
        self.name = name
        self.prices = {}

    def add_item(self, item):
        self.prices[item.datetime] = item


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='go with debug level',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    return parser.parse_args()


def read_prices():
    def get_file_name():
        return os.environ["HOME"] + '/.item_prices'

    c = Container('abc')

    f = io.open(get_file_name(), 'rt', encoding='UTF-8', newline=None)
    logger.debug('reading from file with encoding %s', f.encoding)
    i = 1
    for line in f:
        name, amount, currency, date = line.rstrip(os.linesep).split(';')
        logger.debug('line #%s: name=%s, amount=%s, currency=%s, date="%s"',
                     i, name, amount, currency, date)
        i = i + 1
        item = PriceItem(name, amount, currency,
                         datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
        c.add_item(item)
    print c.prices


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)
    read_prices()
    # for url in urls:
    #    item = fetch_price(url)
    #    persist(item)


if __name__ == '__main__':
    main()
