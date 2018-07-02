#!/usr/bin/python

import zlib
import argparse
from header import *
from http_request import *

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 'Accept-Encoding': "gzip, deflate", 'DNT': "1",
           'Upgrade-Insecure-Requests': "1"}


def print_row(output, data):
    print(" %30s %-50s " % (output, data))


def response_to_file(file, response_data, body_data):
    response_file = open(file, 'a')
    response_file.writelines("Status : " + str(response_data['status']) + "\n")
    response_file.writelines("Message : " + str(response_data['message']) + "\n")
    [response_file.writelines(header + " : " + response_headers[header] + "\n") for header in response_headers]

    if body_data is not None:
        response_file.write(body_data)

    response_file.close()


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
        parser.add_argument('--headers', dest='headers_file', default=None,
                            help='initialise request headers with file')
        parser.add_argument('--delimiter', '-d', dest='headers_delimiter', default=':',
                            help='set the delimiter to use when reading headers file (specified by --header or -h) '
                                 "default ':'")
        parser.add_argument('--output', '-o', dest='output_file', default=None,
                            help='save the response into file')
        parser.add_argument('--method', '-m', dest='method', default='get',
                            help='http method (get or post)')
        parser.add_argument('--data', '-a', dest='data', default=None,
                            help='body of the request')
                        


        args = parser.parse_args()
        if args.headers_file is not None:
            headers = file_to_headers(args.headers_file, args.headers_delimiter)

        response = http_request(args.site_address, method=args.method, body=args.data, protocol=args.protocol, path=args.path, headers=headers)
        response_headers = response['headers']
        encoding = None
        if 'Content-Encoding' in response_headers:
            encoding = response_headers['Content-Encoding']

        print('RESPONSE :')
        print_row("Status :", str(response['status']))
        print_row("Message :", str(response['message']))
        [print_row(header + " :", response_headers[header]) for header in response_headers]
        body = None
        if args.print_body:
            if encoding is None:
                body = response['body'].decode('utf-8')
                print(body)
            else:
                body = str(zlib.decompress(response['body'], 16 + zlib.MAX_WBITS))
                print(body)

        if args.output_file is not None:
            response_to_file(args.output_file, response, body)

    except ValueError as e:
        print(e)
    except Exception as ex:
        print(ex)
