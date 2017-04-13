from bot import Bot
from index import Index
from dateutil import parser
from datetime import timedelta
from post import Post
from topNdoc import find_top_N_similar_docs

def clean_string(input):
    return input.replace('<p>','').replace('</p>','').replace('\n','').encode('utf-8')

class Jarvis:
    def __init__(self):
        self.bot = Bot()
        self.index = Index()

    # public method
    def add_top_10_questions(self):
        end_date = parser.parse('2016-12-19T21:25:13Z')
        start_date = end_date + timedelta(days=-7)
        results = self.index.search_date('date', start_date, end_date, 1000)
        newlist = sorted(results, key=lambda x: x.good_question_tally, reverse=True)
        newlist2 = [item for item in newlist if len(item.body) < 200 and item.is_question and item.has_i_answer]
        top10 = newlist2[:5]

        body = '<br>'
        for item in top10:
            question = '{0} - {1}'.format(clean_string(item.subject), clean_string(item.body))
            answer = clean_string(item.i_answer)
            #body += '<b>Question:</b>\n{0}\n<b>Answer:</b>{1}\n\n\n'.format(question, answer)
            body += '\n<b>{0}</b>\n- {1}\n\n\n'.format(question, answer)

        body += '<br>#pin'
        subject = 'FAQ for the Week'
        try:
            self.bot.create_post(subject, body)
        except:
            print('FAQ for this week already made')
        #print(body)

    # given a list of ids, it returns html equivalent for @first_item, @second_item..
    def get_at_response(self, id_list):
        response = ''
        for item in id_list:
            response += '&#64;{0} '.format(item)
        return response

    # private method that searches through piazza
    def get_search_results(self, query):
        # assume id_list has the list of ids of all the search results
        id_list = [6,7]
        response = get_at_response(id_list)
        return '<p>Here are some posts matching your queries {0}</p>'.format(response)

    # provide an additional way to search on piazza (custom search)
    # public method
    def answer_search_queries(self):
        search_posts = self.index.search_folder('search')
        for post in search_posts:
            if post.has_i_answer: # ignore posts with TA answer
                continue
            search_query = post.subject
            response = self.get_search_results(search_query)
            self.bot.create_answer(post.guid, response)

    def get_duplicates(self, post):
        # given post, find duplicates of this post
        # get all the posts with the same folder
        candidates = []
        for folder in post.folders.split(' '):
            # all posts in the same folder with answers are candidates
            all_posts = self.index.search_folder(folder)
            candidates.extend([pst for pst in all_posts if pst.has_answer])

        res, scores = find_top_N_similar_docs(post, candidates, 1)
        if len(res) == 0:
            print('no sufficiently similar post found')
            return ''
        else:
            if scores[0] > 0.3:
                print('found {0} potential matches'.format(len(res)))
                return self.get_at_response(res)

    # find duplicate questions and link them to similar old ones
    # public method
    def answer_unanswered_questions(self):

        unanswered_posts = self.index.search_other_unanswered()
        # the below code looks into same index and finds unanswered questions
        # unanswered_posts = self.index.search_unanswered()
        for u_post in unanswered_posts:
            if u_post.is_question and 'search' not in u_post.folders:
                response = self.get_duplicates(u_post)
                # if some response was obtained
                if response != '':
                    self.bot.create_answer(u_post.guid, response)

def main():
    jarvis = Jarvis()
    jarvis.add_top_10_questions()
    jarvis.answer_unanswered_questions()

if __name__ == "__main__":
    main()

    