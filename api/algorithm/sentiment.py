from typing import Tuple

from textblob import TextBlob
from toolz import merge


def get_sentiment(blob: TextBlob) -> Tuple[float, str]:
    polarity = blob.sentiment.polarity

    if polarity < -0.2:
        sentiment = 'Negative'
    elif polarity > 0.2:
        sentiment = 'Positive'
    else:
        sentiment = 'Neutral'

    return polarity, sentiment


def get_language(blob: str) -> str:
    return blob.detect_language()


def with_sentiment(res_dict: dict) -> dict:
    assert 'text' in res_dict
    blob = TextBlob(res_dict['text'])

    polarity, sentiment = get_sentiment(blob)
    return merge(res_dict,
                 {'polarity': polarity,
                  'sentiment': sentiment,
                  'language': get_language(blob)})
