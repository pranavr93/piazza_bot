from piazza_api import Piazza
import json
import sys
import config

class Bot:
    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(config.creds['email'], config.creds['password'])
        self.course = self.piazza.network(config.class_code)

    def get_all_posts(self):
        documents = []
        posts = self.course.iter_all_posts()
        for post in posts:
            print('downloading post {0}'.format(post['nr']))
            documents.append(post)
        return documents