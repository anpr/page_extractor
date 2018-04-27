#!/usr/bin/env python
from pprint import pprint

import Algorithmia

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
    return dict_slice(response.result, {'title', 'thumbnail', 'date', 'summary', 'text'})

