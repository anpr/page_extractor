#!/usr/bin/env python
from pprint import pprint

import Algorithmia

client = Algorithmia.client('simxQ3PHFsh2hvuINmujcBBza9V1')
algo = client.algo('web/AnalyzeURL/0.2.17')


def get_title(url):
    try:
        response = algo.pipe([url])
    except Exception as error:
        # Algorithm error if, for example, the input is not correctly formatted
        print(error)
        return

    # pprint(response.result)
    return response.result['title']
