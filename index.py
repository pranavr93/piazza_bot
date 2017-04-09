from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os.path
import config
from whoosh.qparser import QueryParser
import sys
from bot import Bot
import shutil

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
        return Schema(post=TEXT, subject=TEXT, json=STORED)

    def post_to_document(self, document):
        return  { 
                    'post': document['history'][0]['content'],
                    'subject': document['history'][0]['subject'],
                    'json': document
                } 

    # create index from scratch
    def create_index(self):
        writer = self.ix.writer()
        for document in self.bot.get_all_posts():
            dict = self.post_to_document(document)
            writer.add_document(**dict)
        writer.commit()
        print('\n-----------index created-----------\n\n')

    # incremental update to index
    def update_index(self):
        pass

    # search for query terms in the description
    def search(self, query):
        print('searching \'{0}\'...'.format(query))
        all_results = []
        with self.ix.searcher() as searcher:
            for word in query.split(' '):
                query = QueryParser('post', self.ix.schema).parse(word)
                results = searcher.search(query)
                all_results.extend(results)

            if len(results) > 0:
                print('here are the matches:\n')
                for result in all_results:
                    print(result)
            else:
                print('no matches found\n')

def main():
    if len(sys.argv) == 1:
        print('no query terms provided')
        return
    query_terms = sys.argv[1:]
    id = Index()
    id.search(' '.join(query_terms))

if __name__ == "__main__":
    main()
