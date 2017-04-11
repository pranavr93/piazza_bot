from bot import Bot
from index import Index
from dateutil import parser
from datetime import timedelta
from post import Post

def clean_string(input):
    return input.replace('<p>','').replace('</p>','').replace('\n','').encode('utf-8')

class Jarvis:
    def __init__(self):
        self.bot = Bot()
        self.index = Index()

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
        self.bot.create_post(subject, body)
        print(body)

    def get_search_results(self, query):
        # assume id_list has the list of ids of all the search results
        id_list = [6,7]
        response = ''
        for item in id_list:
            response += '&#64;{0} '.format(item)
        return '<p>Here are some posts matching your queries {0}</p>'.format(response)

    def answer_search_queries(self):
        search_posts = self.index.search_folder('search')
        for post in search_posts:
            if post.has_i_answer: # ignore posts with TA answer
                print('how')
                continue
            search_query = post.subject
            response = self.get_search_results(search_query)
            self.bot.create_answer(post.guid, response)

    def answer_unanswered_questions(self):
        pass        

def main():
    jarvis = Jarvis()
    #jarvis.add_top_10_questions()
    jarvis.answer_search_queries()

if __name__ == "__main__":
    main()

    