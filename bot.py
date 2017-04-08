from piazza_api import Piazza
import json
import sys
import config

def get_all_posts():
	POST_LIMIT = 100000000

	p = Piazza()
	p.user_login(config.creds['email'], config.creds['password'])

	course = p.network(config.class_code)

	documents = []
	posts = course.iter_all_posts(limit= POST_LIMIT)
	for post in posts:
	    documents.append(post)

	return documents
