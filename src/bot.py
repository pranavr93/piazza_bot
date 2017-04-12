# bot that deals with interactions with piazza
# sits in between Jarvis and Piazza
from piazza_api import Piazza
import json
import sys
import config
import os.path
from post import Post

from piazza_api.rpc import PiazzaRPC



class Bot:
    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(config.creds['email'], config.creds['password'])
        self.course = self.piazza.network(config.class_code)

        self.post_limit = 100000

        self.piazza_rpc = PiazzaRPC(config.class_code)
        self.piazza_rpc.user_login(config.creds['email'], config.creds['password'])

    def get_all_posts(self):
        documents = []
        posts = self.course.iter_all_posts(limit=self.post_limit)
        for post in posts:
            print('downloading post {0}'.format(post['nr']))
            documents.append(Post(post))
        return documents

    def get_all_posts_json(self):
        documents = []
        posts = []
        file_name = '{0}.txt'.format(config.class_code)
        if not os.path.isfile(file_name):
            data = self.course.iter_all_posts(limit=self.post_limit)
            for post in data:
                print('downloading post {0}'.format(post['nr']))
                documents.append(post)
                posts.append(Post(post))
            obj = open(file_name, 'wb')
            json.dump(documents, obj)
        else:
            obj = open(file_name, 'r')
            data = json.load(obj)
            for post in data:
                posts.append(Post(post))
        return posts

    def create_post(self, subject, body, folder=['hw1']):
        params = {'type':'note','subject':subject, 'content':body, 'folders':folder}
        self.piazza_rpc.content_create(params)
