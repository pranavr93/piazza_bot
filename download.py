from piazza_api import Piazza
import json
import sys
import config

p = Piazza()
p.user_login(config.creds['email'], config.creds['password'])

course = p.network(config.class_code)

mapSave = {}

posts = course.iter_all_posts(limit=100000000000)
for post in posts:
    content = post["history"][0]["content"]
    id = post["nr"]
    print(id)
    mapSave[id] = content

with open("posts_test.json", "wb") as f:
    f.write(json.dumps(mapSave))