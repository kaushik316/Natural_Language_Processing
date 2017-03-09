import requests
import praw
import sentalyzer_module as sm 
from auth import r

# Select subreddits to mine comments from
sub_reddits = ['all', 'worldnews', 'news', 'politics', 'uncensorednews','open_news']
user_agent = "My comment scraping topic gatherer program by u/dataswannabe"

docs = []

def comment_gatherer(arr):
	for subreddit in arr:
		subreddit_comments = r.get_comments(subreddit)
		for comment in subreddit_comments:
			docs.append(str(comment))


comment_gatherer(sub_reddits)

sm.related_topics(docs)




