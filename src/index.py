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
INF = 100000

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
                    id=NUMERIC(sortable=True),
                    subject=TEXT,
                    body=TEXT,
                    date=DATETIME,
                    json=STORED,
                    views=NUMERIC,
                    folders=TEXT
                    )

    def post_to_document(self, document):
        return  { 
                    'id': document.id,
                    'subject': document.subject,
                    'body': document.body,
                    'date': document.date,
                    'json': document.json,
                    'views': document.views,
                    'folders':document.folders
                } 

    # add all documents to the index
    def add_to_index(self, documents):
        writer = self.ix.writer()
        for document in documents:
            dict = self.post_to_document(document)
            writer.add_document(**dict)
        writer.commit()

    # create index from scratch
    def create_index(self):
        documents = self.bot.get_all_posts()
        self.add_to_index(documents)
        print('\nindex created!\n\n')

    # incremental update to index
    def update_index(self):
        # get the last indexed post
        last_post = self.search_numeric('id', 0, INF, 1)
        documents = self.bot.get_all_posts(last_post[0].id)
        self.add_to_index(documents)
        print('\nindex updated!\n\n')

    # search for query terms in the description
    def search(self, query, limit, sort_by_field=None):
        print(query)
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
    def search_terms(self, field, query_terms, limit = INF):
        print('searching \'{0}\'...'.format(query_terms))
        all_results = []
        for word in query_terms.split():
            query = Term(field, word)
            all_results.extend(self.search(query, limit))
        return all_results

    # get all posts with field between low and high
    def search_numeric(self, field, low=0, high=INF, limit=INF):
        query = NumericRange(field, low, high)
        return self.search(query, limit, field)

    # get all posts between dates start_date and end_date
    def search_date(self, field, start_date, end_date, limit=INF):
        query = DateRange(field, start_date, end_date)
        return self.search(query, limit)

    def search_folder(self, query_term, limit=INF):
        query = Term('folders', query_term)
        all_results = self.search(query, limit)
        return all_results

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
