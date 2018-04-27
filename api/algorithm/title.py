import bs4
from bs4 import BeautifulSoup
import urllib
import ssl

from toolz import merge


def get_soup(url):
    r = urllib.request.urlopen(url, context=ssl._create_unverified_context()).read()
    return BeautifulSoup(r, 'html.parser')


substitutes = [
    ("// Track", ""),
    ("feat.", "ft"),
    ("–", "-"),
    ("inkl. Video",""),
    ("|  WR.de  | Kultur",""),
    (" // Live", ""),
]
translation = "".maketrans("»«",'""')


def fetch_title(soup: BeautifulSoup) -> str:
    h1 = None
    # 1 rule
    try:
        for h in soup.find_all("h1",limit=3):

            if 'site-title' not in h['class']:
                h1 = h
                break
    except KeyError:
        h1 = h

    title = h1 and (h1.string or list(h1.strings)[-2])

    depth = 0
    if h1:
        for i in h1.previous_elements:
            depth += 1
            if depth > 6:
                break
            if type(i) == bs4.element.Tag and i.name == 'h2':
                title = f'{i.string}: {title}'
                break

    if not title or len(title) < 3:
        title = soup.h2 and soup.h2.string


    # 2nd rule
    if not title or len(title) < 3:
        title = soup.title.string


    # clean up
    if title:
        for f, t in substitutes:
            title = title.replace(f, t)
        title = title.translate(translation).strip()

    return title


def with_title(res_dict: dict) -> dict:
    assert 'url' in res_dict

    title = fetch_title(get_soup(res_dict['url']))

    return merge(res_dict,
                 {'title': title})
