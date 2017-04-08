class Post:
	def __init__(self, json):
		try:
			self.folders = json['folders']
			self.body = json['history'][0]['content']
			self.subject = json['history'][0]['subject']
			self.id = json['nr']
			self.views = json['unique_views']
			self.good_question = json['is_tag_good']
			self.is_anon = json['default_anonymity']
			self.created = json['created']
			self.upvotes = len(json['upvote_ids'])
			self.no_answer = json['no_answer']
		except:
			print('could not convert post id {0} to object'.format(self.id))


# bookmarked          : 2
# bucket_name         : 'today'
# created             : creation date of the post
# default_anonymity:  : public/private post
# folders             : labels for the post
# history             : history[0] gives the latest post
# id                  : unique identifier for the post
# is_tag_good         : tells if 'good note' for the post by instructor
# my_favorite         : did the bot mark this post as a favorite for some reason
# no_answer           : 0
# nr                  : post id (number)
# num_favorites       : how many students marked this post as their favorites
# tag_good            : list of dicts, each dict is an instructor and info
# unique_views        : number of unique views in the post
# upvote_ids          : ids of all the students who upvoted(?)