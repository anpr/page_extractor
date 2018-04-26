#!/usr/bin/env python
import csv
import pickle
from toolz import concat

from pprint import pprint


def get_raw():
    # raw = list(PressSource.objects.values_list('article_title', 'source_url').all())

    with open('./data/prod_titles.p', 'rb') as f:
        raw = pickle.load(f)
    return raw


def to_lines(raw):
    return [[item[1], item[0]] for item in raw if item[1]]


def csv_writer(lines, path):
    """
    Write data to a CSV file path
    """
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        writer.writerow(['URL', 'title'])
        for line in lines:
            writer.writerow(line)


raw = get_raw()
lines = to_lines(raw)

pprint(lines)
csv_writer(lines, './data/prod_titles.csv')
