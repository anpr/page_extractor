#!/usr/bin/env python
import datetime
from pprint import pprint

import Algorithmia
from toolz import merge

from api.utils import dict_slice

client = Algorithmia.client('simxQ3PHFsh2hvuINmujcBBza9V1')
algo = client.algo('web/AnalyzeURL/0.2.17')


def analyze_url(url):
    try:
        response = algo.pipe([url])
    except Exception as error:
        # Algorithm error if, for example, the input is not correctly formatted
        print(error)
        return

    # pprint(response.result)
    return dict_slice(response.result, {'url', 'title', 'thumbnail', 'date', 'summary', 'text'})


def publication_date(date_str):
    return date_str[:10]


def with_publication_date(res_dict):
    assert 'date' in res_dict

    return merge(res_dict, {'publication_date':  publication_date(res_dict['date'])})


def get_result(url):
    return with_publication_date(analyze_url(url))
