import bot
import json
import os.path

def has_at(post):
    if (post.has_i_answer and '#64;' in post.i_answer):
        return True
    return False

if __name__ == "__main__":
    bot = bot.Bot()
    posts = bot.get_all_posts_json()
    print(len(posts))
    ps = [p for p in posts if has_at(p)]
    for p in ps:
        if p.has_i_answer:
            print("QUESTION: ", p.body)
            print("POST: ", p.i_answer)
