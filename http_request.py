#!/usr/bin/python

import http.client


def http_request(host, protocol='http', path='/', method='GET', data=None, headers={}):
    if protocol == 'https':
        connection = http.client.HTTPSConnection(host)
    else:
        connection = http.client.HTTPConnection(host)

    connection.request(method, path, data, headers=headers)
    response = connection.getresponse()
    headers = {}
    pairs = response.getheaders()

    if pairs:
        for pair in pairs:
            headers[pair[0]] = pair[1]
    return {'body': response.read(),
            'status': response.status,
            'headers': headers,
            'message': response.reason}
