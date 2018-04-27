from pprint import pprint

from textblob import TextBlob
from toolz import dissoc, merge


def get_sentiment(text):
    blob = TextBlob(text)
    
    polarity = blob.sentiment.polarity

    print("***")
    print(polarity)
    if polarity < -0.2:
        return 'Negative'
    elif polarity > 0.2:
        return 'Positive'
    return 'Neutral'


def with_sentiment(res_dict):
    assert 'text' in res_dict

    return merge(res_dict, {'sentiment': get_sentiment(res_dict['text'])})
