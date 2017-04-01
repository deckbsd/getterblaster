import csv


def file_to_headers(headers_file, char):
    headers = {}
    with open(headers_file, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=char)

        for row in reader:
            headers[row[0]] = row[1]

        return headers
