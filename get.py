#!/usr/bin/python

import zlib
import argparse
from http_request import *

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 'Accept-Encoding': "gzip, deflate", 'DNT': "1",
           'Upgrade-Insecure-Requests': "1"}


def print_row(output, data):
    print(" %30s %-50s " % (output, data))

if __name__ == "__main__":
    try:

        parser = argparse.ArgumentParser(description='Execute get request.')
        parser.add_argument('--site', '-s', dest='site_address', required=True,
                            help='the website address (without the path')
        parser.add_argument('--protocol', '-p', dest='protocol', default='http',
                            help='the protocol to use')
        parser.add_argument('--path', dest='path', default='/',
                            help='the path into the website')
        parser.add_argument('--body', '-b', dest='print_body', action='store_const',
                            const=True, default=False,
                            help='print the body (by default : no')

        args = parser.parse_args()
        response = http_request(args.site_address, protocol=args.protocol, path=args.path, headers=headers)
        response_headers = response['headers']

        encoding = None
        if 'Content-Encoding' in response_headers:
            encoding = response_headers['Content-Encoding']

        print('RESPONSE :')
        print_row("Status :", str(response['status']))
        print_row("Message :", str(response['message']))
        [print_row(header + " :", response_headers[header]) for header in response_headers]

        if args.print_body:
            if encoding is None:
                print(response['body'].decode('utf-8'))
            else:
                decompressed_content = zlib.decompress(response['body'], 16+zlib.MAX_WBITS)
                print(decompressed_content)

    except ValueError as e:
        print(e)
    except Exception as ex:
        print(ex)
