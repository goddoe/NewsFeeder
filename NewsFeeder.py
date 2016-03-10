from flask import Flask, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from datetime import datetime
from random import shuffle
from simplexml import dumps 

def output_xml(data, code, headers=None):
    resp = make_response(dumps(data), code)
    resp.headers.extend(headers or {})

    return resp


class home(Resource):
	
    def __init__(self):
        client			= MongoClient("mongodb://ec2-52-69-42-132.ap-northeast-1.compute.amazonaws.com:27017")
        self.db			= client["rss"]


    def get(self):
        result                  = self.generateFeed();
        return result


    def generateFeed(self):
        coll_etnews             = (self.db['etnews'],   '전자신문')
        coll_khan               = (self.db['khan'],     '국민일보')
        coll_mk                 = (self.db['mk'],       '매일경제')
        coll_hankyung           = (self.db['hankyung'], '한국경제')
        coll_yonhapnews         = (self.db['yonhapnews'],'연합뉴스')
        coll_edaily             = (self.db['edaily'],   '이데일리')
        coll_mt                 = (self.db['mt'],       '머니투데이')
        
        collections_news        = [coll_etnews
                                    , coll_khan
                                    , coll_mk       # this makes error
                                    , coll_hankyung
                                    , coll_yonhapnews
                                    , coll_edaily
                                    , coll_mt]
        
        result                  = {}
        result['rss']           = {}
        result['rss']['channel']= {}

        items                   = result['rss']['channel']
        items['item']           = []

        for coll, publisher in collections_news:
            for news in coll.find()[:10]:

                insert_data                 = {}
                insert_data['url']          = news['_id']
                insert_data['title']        = news['title']
                insert_data['description']  = news['description']
                insert_data['pubdate']      = news['pubdate'].ctime()
                insert_data['publisher']    = publisher
                insert_data['category']     = news['category']

                items['item'].append(insert_data)
        
        shuffle(items['item'])

        return result


def main():
    app = Flask(__name__)
    api = Api(app, default_mediatype='application/xml')
    api.representations['application/xml'] = output_xml
    api.representations['application/json'] = output_xml
    api.add_resource(home, '/')

    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
