#!/usr/bin/env python
import Algorithmia
from write_csv import get_raw, to_lines

lines = to_lines(get_raw())
urls = [line[0] for line in lines]
input = urls

client = Algorithmia.client('simxQ3PHFsh2hvuINmujcBBza9V1')
algo = client.algo('web/AnalyzeURL/0.2.17')

for line in lines[10:]:
    url = line[0]
    exp_title = line[1]

    try:
        response = algo.pipe([url])
    except Exception as error:
        # Algorithm error if, for example, the input is not correctly formatted
        print(error)
        continue

    title = response.result['title']
    print(f"\n{url:40s}\n\ntitle tag: {title}\nexp title: {exp_title}\n---")
