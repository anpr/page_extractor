from toolz import thread_first

from .algorithmia import analyze_url, with_publication_date
from .sentiment import with_sentiment


def get_result(url):
    return thread_first(url,
                        analyze_url,
                        with_publication_date,
                        with_sentiment)
