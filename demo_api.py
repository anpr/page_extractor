import sys
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class PageExtractor(Resource):
    def post(self):
        url = request.form['url']
        return {'url': url}


api.add_resource(PageExtractor, '/extract')

if __name__ == '__main__':
    debug = True if len(sys.argv) > 1 else False
    print(f"\n ==== Starting page extractor demo API. Debug={debug} ====\n")
    app.run(debug=True)
