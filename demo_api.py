import sys
from flask import Flask, request
from flask_restful import Resource, Api
from toolz import merge

from api.algorithm.result import get_result

app = Flask(__name__)
api = Api(app)


class PageExtractor(Resource):
    def get(self):
        return {'Hello', 'Page Extractor'}

    def post(self):
        url = request.form['url']
        result = get_result(url)
        return merge(result,
                     {'url': url})


api.add_resource(PageExtractor, '/extract')

if __name__ == '__main__':
    debug = True if len(sys.argv) > 1 else False
    print(f"\n ==== Starting page extractor demo API. Debug={debug} ====\n")
    app.run(debug=True)
