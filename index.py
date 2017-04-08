from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os.path
import config
from whoosh.qparser import QueryParser
import sys

class Index:
    def __init__(self):

        # define schema for the index
        schema = Schema(Name=TEXT(stored=True), age=NUMERIC(stored=True), id=ID(stored=True), description=TEXT(stored=True))

        try:
            self.ix = open_dir(config.index_directory)
            self.update_index()
        except:
            # if issues loading index, create index from scratch
            shutil.rmtree(config.index_directory)
            os.mkdir(config.index_directory)
            self.ix = create_in(config.index_directory, schema)
            self.create_index()
            
    # create index from scratch
    def create_index(self):
        
        writer = self.ix.writer()
        writer.add_document(Name=u"Pranav Ramarao", age=u"25", id=u"2011a7ps013h", description=u"he is a computer science student")
        writer.add_document(Name=u"Vishaal Mohan", age=u"23", id=u"2011aaps006h", description=u"he is an electrical student")                        
        writer.commit()

    # incremental update to index
    def update_index(self):
        pass

    # search for query terms in the description
    def search(self, query):
        all_results = []
        with self.ix.searcher() as searcher:
            for word in query.split(' '):
                query = QueryParser("description", self.ix.schema).parse(word)
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
