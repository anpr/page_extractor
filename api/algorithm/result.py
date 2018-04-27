from toolz import thread_first

from .algorithmia import analyze_url, with_publication_date
from .title import with_title
from .sentiment import with_sentiment


def get_result(url: str) -> dict:
    return thread_first(url,
                        analyze_url,
                        with_title,
                        with_publication_date,
                        with_sentiment)
