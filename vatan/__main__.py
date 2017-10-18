import sys
import vatan
import argparse
import logging


def parse_args():
    """
    Usage:
    vatan.py pull
    vatan.py reg <url>
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', help='verbose output',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)

    subparsers = parser.add_subparsers(dest='command')

    pull_parser = subparsers.add_parser('pull')

    reg_parser = subparsers.add_parser('reg')
    reg_parser.add_argument('url', type=vatan.valid_url)
    reg_parser.add_argument('--delta', type=int, default=10,
                            help='price delta')

    return parser.parse_args()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parse_args()

    if args.command == 'reg':
        vatan.register(args.url)
    elif args.command == 'pull':
        for i in vatan.read_items():
            snapshot = vatan.fetch_price(i.uri)
            vatan.persist(vatan.make_item_path(i.uri), snapshot)
            if snapshot.amount != i.amount:
                pass
                # notify.send_mail(i, snapshot)
    elif args.command == 'read':
        pass
    else:
        pass


if __name__ == '__main__':
    main()
