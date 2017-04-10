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
from post import Post
# deals with fetching/storing/searching data in the index
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
        return Schema(
                    subject=TEXT,
                    body=TEXT,
                    date=DATETIME,
                    json=STORED,
                    views=NUMERIC,
                    upvotes=NUMERIC(sortable=True)
                    )

    def post_to_document(self, document):
        return  { 
                    'subject': document.subject,
                    'body': document.body,
                    'date': document.date,
                    'json': document.json,
                    'views': document.views,
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
    def search(self, query, limit, sort_by_field=None):
        print(query)
        ret_list = []
        ret_list = []
        with self.ix.searcher() as searcher:
            if sort_by_field == None:
                results = searcher.search(query, limit=limit)
            else:
                results = searcher.search(query, limit=limit, sortedby=sort_by_field, reverse=True)
            for result in results:
                ret_list.append(Post(result['json']))
        return ret_list

    # get all posts with field having query terms
    def search_terms(self, field, query_terms, limit=1000):
        print('searching \'{0}\'...'.format(query_terms))
        all_results = []
        for word in query_terms.split():
            query = Term(field, word)
            all_results.extend(self.search(query, limit))
        return all_results

    # get all posts with field between low and high
    def search_numeric(self, field, low, high, limit=1000):
        query = NumericRange(field, low, high)
        return self.search(query, limit, field)

    # get all posts between dates start_date and end_date
    def search_date(self, field, start_date, end_date, limit=1000):
        query = DateRange(field, start_date, end_date)
        return self.search(query, limit)


def main():
    if len(sys.argv) == 1:
        id = Index()
    else:
        query_terms = sys.argv[1:]
        id = Index()
        results = id.search_terms('body',' '.join(query_terms))
        #results = id.search_numeric('upvotes',0, 1000, 20)
        print(len(results))
        for result in results:
            print(result)
            print('\n')
        if len(results) == 0:
            print('no search results for the given term')

if __name__ == "__main__":
    main()
