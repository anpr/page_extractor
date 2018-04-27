#!/usr/bin/env python
from pprint import pprint

import Algorithmia
from toolz import merge, thread_first, dissoc

from api.utils import dict_slice

client = Algorithmia.client('simxQ3PHFsh2hvuINmujcBBza9V1')


def analyze_url(url):
    algo = client.algo('web/AnalyzeURL/0.2.17')
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


def get_sentiment(text):
    algo = client.algo('nlp/SocialSentimentAnalysis/0.1.4')

    try:
        response = algo.pipe({'sentence': text})
    except Exception as error:
        # Algorithm error if, for example, the input is not correctly formatted
        print(error)
        return 'Unknown'

    pprint(dissoc(response.result[0], 'sentence'))

    compound = response.result[0]['compound']
    if compound < -0.2:
        return 'Negative'
    elif compound > 0.2:
        return 'Positive'
    return 'Neutral'


def with_sentiment(res_dict):
    assert 'text' in res_dict

    return merge(res_dict, {'sentiment': get_sentiment(res_dict['text'])})


def get_result(url):
    return thread_first(url,
                        analyze_url,
                        with_publication_date,
                        with_sentiment)
