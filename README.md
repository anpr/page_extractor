## Getting Started

1. Install Python and pip
1. `pip install pipenv`
1. `pipenv install`
1. `python -m textblob.download_corpora`  # <--- Important!
## Start API

Start the API with

`python demo_api.py`

Test it with:

`curl "localhost:5000/extract?url=http://www.backspin.de/rae-sremmurd-wissen-solltest/"`

`curl -X POST localhost:5000/extract -d "url=http://minutenmusik.de/wochenrueckblick/die-fantastischen-vier-mani-orrason-shaw-mendes-snow-patrol-the-cool-quest-wochenrueckblick-kw-12-2018"`

## Frontend

### frontend2 based on RESTool (https://github.com/dsternlicht/RESTool)
```
cd frontend2
npm install
 npm install -g @angular/cli
 npm install typescript@'>=2.1.0 <2.4.0'
ng serve
```

```
http://localhost:4200/
```
