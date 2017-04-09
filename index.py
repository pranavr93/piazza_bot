from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.query import *
import os.path
import config

import sys
from bot import Bot
import shutil
from dateutil import parser
class Index:
    def __init__(self):
        # define schema for the index
        schema = self.get_schema()
        self.bot = Bot()
        try:
            self.ix = open_dir(config.index_directory)
            self.update_index()
        except:
            # if issues loading index, create index from scratch
            if os.path.exists(config.index_directory):
                shutil.rmtree(config.index_directory)
            os.mkdir(config.index_directory)
            self.ix = create_in(config.index_directory, schema)
            self.create_index()
            
    # tentative schema, can add more indices to this
    def get_schema(self):
        # build index on post and subject; not storing them
        # store raw json in 'json' field
        return Schema(subject=TEXT, body=TEXT, date=DATETIME, json=STORED, views=NUMERIC)

    def post_to_document(self, document):
        return  { 
                    'body': document['history'][0]['content'],
                    'subject': document['history'][0]['subject'],
                    'date': parser.parse(document['created']),
                    'json': document,
                    'views': int(document['unique_views'])
                } 

    # create index from scratch
    def create_index(self):
        writer = self.ix.writer()
        for document in self.bot.get_all_posts():
            dict = self.post_to_document(document)
            writer.add_document(**dict)
        writer.commit()
        print('\nindex created!\n\n')

    # incremental update to index
    def update_index(self):
        pass

    # search for query terms in the description
    def search(self, query):
        print(query)
        ret_list = []
        ret_list = []
        with self.ix.searcher() as searcher:
            results = searcher.search(query)
            for result in results:
                ret_list.append(dict(result))
        return ret_list

    # get all posts with field having query terms
    def search_terms(self, field, query_terms):
        print('searching \'{0}\'...'.format(query_terms))
        all_results = []
        for word in query_terms.split():
            query = Term(field, word)
            all_results.extend(self.search(query))
        return all_results

    # get all posts with field between low and high
    def search_numeric(self, field, low, high):
        query = NumericRange(field, low, up)
        return self.search(query)

    # get all posts between dates start_date and end_date
    def search_date(self, field, start_date, end_date):
        query = DateRange(field, start_date, end_date)
        return self.search(query)


def main():
    if len(sys.argv) == 1:
        print('no query terms provided')
        return
    query_terms = sys.argv[1:]
    id = Index()
    results = id.search_terms('body',' '.join(query_terms))
    print(len(results))
    print(results[0])
    for result in results:
        print(result)
        print('\n')
    if len(results) == 0:
        print('no search results for the given term')

if __name__ == "__main__":
    main()
