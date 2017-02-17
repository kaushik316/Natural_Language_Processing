import pandas as pd
import requests
import codecs
import numpy as np
import gensim
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.word2vec import Word2Vec
from gensim.models.ldamodel import LdaModel
from gensim.matutils import Sparse2Corpus
import nltk
import praw

# Select subreddits to mine comments from
sub_reddits = ['all', 'worldnews', 'news', 'politics', 'uncensorednews','open_news']
user_agent = "My comment scraping topic gatherer program by u/dataswannabe"
r = praw.Reddit(user_agent=user_agent)

docs = []

def comment_gatherer(arr):
	for subreddit in arr:
		subreddit_comments = r.get_comments(subreddit)
		for comment in subreddit_comments:
			docs.append(str(comment))


comment_gatherer(sub_reddits)

# Create a series to pass into the Vectorizer
comment_series = pd.Series(docs)

# CountVectorizer turns each word into a feature
cv = CountVectorizer(binary=False,
	stop_words='english',
	min_df=3)

vectorized = cv.fit_transform(comment_series)
id2word = dict(enumerate(cv.get_feature_names()))

# First we convert our word-matrix into gensim's format
corpus = Sparse2Corpus(vectorized, documents_columns = False)

# Then we fit an LDA model
lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=10)
num_topics = 10 
words_per_topic = 5

# Shows us the different topics as well as the strength of their correlation
for ti, topic in enumerate(lda_model.show_topics(num_topics= num_topics, num_words= words_per_topic)):
    print("Topic: %d" % (ti))
    print (topic)
    print()

