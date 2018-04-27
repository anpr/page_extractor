from pprint import pprint

import Algorithmia
from toolz import dissoc, merge

client = Algorithmia.client('simxQ3PHFsh2hvuINmujcBBza9V1')


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
