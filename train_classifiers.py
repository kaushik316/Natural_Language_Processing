import random
import nltk
from nltk.corpus import movie_reviews 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from nltk.classify import ClassifierI
from statistics import mode
import pickle


stop = stopwords.words('english')

pos_file = open("reviews/positive.txt", "r").read()
neg_file = open("reviews/negative.txt", "r").read()

docs = []

for rev in pos_file.splitlines():
	docs.append((rev, "pos"))

for rev in neg_file.splitlines():
	docs.append((rev, "neg"))

with open("pickled_docs/documents.pickle", "wb") as d_file:
	pickle.dump(docs, d_file)
d_file.close()

# create a list of positive and negative words excluding stop words and punctuation
pos_words = [w.lower() for w in word_tokenize(pos_file.decode('utf-8')) if w not in stop and w.isalpha()] 
neg_words = [w.lower() for w in word_tokenize(neg_file.decode('utf-8')) if w not in stop and w.isalpha()]


all_words_list = pos_words + neg_words
all_words = nltk.FreqDist(all_words_list) # creates a dictionary with words and the number of times they appear
word_features = list(all_words.keys())[:5000] # save the 5000 most popular words

with open("pickled_docs/word_features.pickle", "wb") as wf:
	pickle.dump(word_features, wf)
wf.close()


def find_features(document):
	words = word_tokenize(document.decode('utf-8'))
	featureset = {}
	for word in word_features:
		featureset[word] = (word in words) # returns a boolean
	return featureset


featuresets = [(find_features(rev), category) for (rev, category) in docs ]

with open("pickled_docs/featuresets.pickle", "wb") as feat_file:
	pickle.dump(featuresets, feat_file)
feat_file.close()

random.shuffle(featuresets)

training_set = featuresets[:10000]
test_set = featuresets[10000:]



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



def format_input(sentence): # test function for algos
	return dict([(word, True) for word in sentence.split() if word not in stop])


# Initialization of the Naive Bayes classifier
nltk_classifier = nltk.NaiveBayesClassifier.train(training_set)
print "NLTK classifier accuracy : {}".format(nltk.classify.accuracy(nltk_classifier, test_set)*100)
nltk_classifier.show_most_informative_features(15)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print "MNB_classifier accuracy : {}".format(nltk.classify.accuracy(MNB_classifier, test_set) * 100) 

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print "BernoulliNB_classifier accuracy : {}".format(nltk.classify.accuracy(BernoulliNB_classifier, test_set) * 100) 

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print "LogisticRegression_classifier accuracy percent: {}".format(nltk.classify.accuracy(LogisticRegression_classifier, test_set)*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print "SGDClassifier_classifier accuracy percent: {}".format(nltk.classify.accuracy(SGDClassifier_classifier, test_set)*100)

top_clf = TopClassifier(nltk_classifier, MNB_classifier, BernoulliNB_classifier, LogisticRegression_classifier, SGDClassifier_classifier)
top_clf.pickler("NLTK", "MNB_classifier", "BernoulliNB", "LogisticRegression", "SGDClassifier")
print "voted_classifier accuracy percent: {}".format(nltk.classify.accuracy(top_clf, test_set)*100)

print "Classification: {} {}".format(top_clf.classify(test_set[0][0]), top_clf.confidence(test_set[0][0])*100)
print "Classification: {} {}".format(top_clf.classify(test_set[1][0]), top_clf.confidence(test_set[1][0])*100)






