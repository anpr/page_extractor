#!/usr/bin/env python
import csv
import pickle

from pprint import pprint


def pickle_load(path):
    # title_raw = list(PressSource.objects.values_list('article_title', 'source_url').all())

    with open(path, 'rb') as f:
        raw = pickle.load(f)
    return raw


def to_title_lines(title_raw):
    return [[item[1], item[0]] for item in title_raw if item[1]]


def csv_writer(path, header, lines):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='#')
        writer.writerow(header)
        for line in lines:
            writer.writerow(line)


title_raw = pickle_load('../data/prod_titles.p')
title_lines = to_title_lines(title_raw)

csv_writer('../data/prod_titles.csv', ['URL', 'title'], title_lines)

prod = pickle_load('../data/prod.p')
pprint(prod)
csv_writer('../data/prod.csv', ['URL', 'title', 'pubdate', 'sentiment', 'artist'], prod)
