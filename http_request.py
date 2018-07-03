#!/usr/bin/python

import http.client


def http_request(host, protocol='http', path='/', method='GET', data=None, headers={}, proxy=None, port=-1):

    if proxy is not None:
        if protocol == 'https':
            connection = http.client.HTTPSConnection(proxy, port)
        else:
            connection = http.client.HTTPConnection(proxy, port)

        connection.set_tunnel(host)
    else:
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
