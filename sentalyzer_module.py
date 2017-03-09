from __future__ import division
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import pandas as pd
import codecs
import numpy as np
import gensim
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.word2vec import Word2Vec
from gensim.models.ldamodel import LdaModel
from gensim.matutils import Sparse2Corpus
from collections import Counter


class TopClassifier(ClassifierI):

	def __init__(self, *classifiers):
		self._classifiers = classifiers


	def pickler(self, *clf_names):
		cl_dict = dict(zip(clf_names, self._classifiers))
		for name in cl_dict.keys():
			filename = "pickled_algos/{}.pickle".format(name)
			print filename
			pickle_file = open(filename, "wb")
			pickle.dump(cl_dict[name], pickle_file)
			pickle_file.close()


	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features) # vote will be positive or negative
			votes.append(v)
			return mode(votes)


	def confidence(self, features):
		votes = []
		for c in self._classifiers:
		    v = c.classify(features)
		    votes.append(v)

		choice_votes = votes.count(mode(votes))
		conf = choice_votes / len(votes)
		return conf


# documents_f = open("pickled_docs/documents.pickle", "rb")
# documents = pickle.load(documents_f)
# documents_f.close()

word_features_f = open("pickled_docs/word_features.pickle", "rb")
word_features = pickle.load(word_features_f)
word_features_f.close()

# featuresets_f = open("pickled_docs/featuresets.pickle", "rb")
# featuresets = pickle.load(featuresets_f)
# featuresets_f.close()

# random.shuffle(featuresets)

# testing_set = featuresets[10000:]
# training_set = featuresets[:10000]


def find_features(document):
	words = word_tokenize(document.decode('utf-8'))
	featureset = {}
	for word in word_features:
		featureset[word] = (word in words) # returns a boolean
	return featureset


open_file = open("pickled_algos/NLTK.pickle", "rb")
nltk_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/MNB_classifier.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/BernoulliNB.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/LogisticRegression.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/SGDClassifier.pickle", "rb")
SGD_classifier = pickle.load(open_file)
open_file.close()


top_classifier =  TopClassifier(nltk_classifier, MNB_classifier, BernoulliNB_classifier, LogisticRegression_classifier, SGD_classifier)


def sentiment(text):
    feats = find_features(text)
    return top_classifier.classify(feats),top_classifier.confidence(feats)


def clean_list(wordlist):
	for i in range(0, len(wordlist)):
		wordlist[i] = re.sub(r'#','',wordlist[i])
		wordlist[i] = re.sub(r"RT|'|http\S+|@\S+","",wordlist[i])
	return wordlist


def pct_positive(_list):
	pos_list = []
	neg_list = []
	for item in _list:
		_sentiment = sentiment(item.encode('utf-8', 'ignore'))
		if _sentiment[0] == 'neg':
			neg_list.append(item)
			neg_pct = "negative {0:.1f}%".format((len(neg_list)/len(_list))*100)
		else:
			pos_list.append(item)
			pos_pct = "positive {0:.1f}%".format((len(pos_list)/len(_list))*100)
	
	neg_pct = "negative {0:.1f}%".format((len(neg_list)/len(_list))*100)
	pos_pct = "positive {0:.1f}%".format((len(pos_list)/len(_list))*100)
	print pos_pct + " " + neg_pct


def related_topics(docs):
	comment_series = pd.Series(docs)
	# CountVectorizer turns each word into a feature
	cv = CountVectorizer(binary=False,
		stop_words='english',
		min_df=3)

	vectorized = cv.fit_transform(comment_series)
	id2word = dict(enumerate(cv.get_feature_names()))
	corpus = Sparse2Corpus(vectorized, documents_columns = False) # First we convert our word-matrix into gensim's format

	lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=10) # Then we fit an LDA model
	num_topics = 10 
	words_per_topic = 5

	for ti, topic in enumerate(lda_model.show_topics(num_topics= num_topics, num_words= words_per_topic, formatted=True)):
	    print("Topic: %d" % (ti)) # Shows us the different topics as well as the strength of their correlation
	    print (topic)


def popular_words(iterable, pos):
	pos_dict = {"noun": ["NN", "NNP", "NNPS", "NNS"], "verb": ["VB", "VBP"], "adjective": ["JJ", "JJR", "JJS"], "adverb": ["RB", "RBR", "RBS"]}
	iter_2_str = ' '.join(iterable)
	tokenized_str = nltk.word_tokenize(iter_2_str)
	pos_list = [nltk.pos_tag(tokenized_str)]

	for key in pos_dict.keys():
		if pos == key:
			subset = [tup[0] for tup in pos_list[0] if tup[1] in pos_dict[key]]
			most_common = Counter(subset).most_common(5)

	print most_common

