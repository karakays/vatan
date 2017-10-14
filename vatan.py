import io
import os
import logging
import argparse
import urllib2
import collections
from datetime import datetime
from decimal import Decimal
from bs4 import BeautifulSoup
from config import product_urls, keyword

logger = logging.getLogger(__name__)

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
ref_amount = None
delta = None


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
    f.write(ser + os.linesep)


class PriceItem(object):
    """Represents a snapshot of the price of self.name at self.datetime
    Attributes:
        name (str): Description of `attr1`.
        amount (Decimal) attr2 (:obj:`int`, optional): Description of `attr2`.
        currency (str)
        datetime (datetime)
    """
    def __init__(self, name, amount, currency, created=None):
        self.name = name
        self.amount = Decimal(amount)
        self.currency = currency
        self.datetime = datetime if created else datetime.now()


class Container(object):
    def __init__(self, name):
        self.name = name
        self.prices = collections.OrderedDict()

    def add_item(self, item):
        self.prices[item.datetime] = item


def read_history():
    def get_file_name():
        return os.environ["HOME"] + '/.item_prices'

    c = Container('abc')

    f = io.open(get_file_name(), 'rt', encoding='UTF-8', newline=None)
    for ln, line in enumerate(f, 1):
        name, amount, currency, date = line.rstrip(os.linesep).split(';')
        logger.debug('line #%s: name=%s, amount=%s, currency=%s, date="%s"',
                     ln, name, amount, currency, date)
        item = PriceItem(name, amount, currency,
                         datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
        c.add_item(item)
    print c.prices

    # TODO close file resource here


def init_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='verbose output',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--delta', type=int, default=10,
                        help='price delta')
    parser.add_argument('reference', type=int,
                        help='reference price')
    return parser


def parse_args():
    global ref_amount, delta
    args = init_arg_parser().parse_args()
    logging.basicConfig(level=args.loglevel)
    ref_amount = Decimal(args.reference)
    delta = Decimal(args.delta)
    return args


def main():
    parse_args()
    # read_prices()
    for url in product_urls:
        item = fetch_price(url)
        if abs(ref_amount - item.amount) >= delta:
            print 'price change event'
        persist(item)


if __name__ == '__main__':
    main()
