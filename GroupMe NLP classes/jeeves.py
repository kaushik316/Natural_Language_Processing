from BukList import *
from textblob import TextBlob
from collections import Counter
import requests
import json
import nltk

# Jeeves is a butler class that uses TextBlob to conduct sentiment analysis and other 
# natural language processing functions.
class Jeeves(object):

	def __init__(self):
		self.message_list = []
		self.token_list = []
		self.searchlist = []
		self.response = 0
		self.lowercase_response = 0
		self.counts = 0
		self.output = ""
		

    # Function to create a list from the Groupme Response
	def message_to_list(self):
		for message in self.response:
			if message['text'] is not None:
				if message['name']!='Jeeves':
					sentence = message['text'] + "."
					self.message_list.append(sentence)
			else:
				pass		
		self.message_list = list(set(self.message_list))


    # GroupMe returns a maximum of 100 messages at a time. Here, I get the id of the last message
    # so that I can submit a get request for the 100 messages before that message and so on.
	def get_many_messsages(self,number):
		for i in range(0,number):
			if i == 0:
				req = requests.get('https://api.groupme.com/v3/groups/'+ group_id +'/messages?token=' + api_key2 + '&limit=100')
				messages_json = json.loads(req.text) 
				self.response = messages_json['response']['messages']
				self.message_to_list()
				oldest_message_id = messages_json['response']['messages'][-1]['id']
			else:
				req = requests.get('https://api.groupme.com/v3/groups/'+ group_id +'/messages?token=' + api_key2 + '&limit=100&before_id=' + self.oldest_message_id)
				messages_json = json.loads(req.text) 
				self.response = messages_json['response']['messages']
				self.message_to_list()
				oldest_message_id = messages_json['response']['messages'][-1]['id']
				

     # SImple function to make a post in a group
	def make_post(self,content):
	    bot = {"bot_id" : bot_id, "text": content}
	    r = requests.post("https://api.groupme.com/v3/bots/post", params = bot)


    # TextBlob works by taking a 'Blob' of text and converting it to a class with various methods
    # This function takes a list as an input and then converts it to a blob
	def blob_maker(self,list_var):
		joined_list = " ".join(x for x in list_var)
		groupme_blob = TextBlob(joined_list)
		return groupme_blob


    # function to count the most popular nouns or verbs in the last 100 messages in a group.
	def count_partsofspeech(self,tag, num):
		self.get_many_messsages(10)
		print len(self.message_list)
		tag_blob = self.blob_maker(self.message_list)
		self.token_list += [word for word, pos in tag_blob.tags if pos == tag ]
		self.counts = Counter(self.token_list).most_common(num)
		self.output = "In the last 1000 messages it appears you all have used \n %s %d times\n %s %d times\n %s %d times\n %s %d times\n %s %d times" % (self.counts[0][0],self.counts[0][1],self.counts[1][0],self.counts[1][1],self.counts[2][0],self.counts[2][1],self.counts[3][0],self.counts[3][1],self.counts[4][0],self.counts[4][1])
		self.make_post(self.output)


    # TextBlob sentiment analysis function. Classifier is default Naive Bayes algorithm.
	def calculate_sentiment(self,searchterm):
		self.get_many_messsages(12)
		self.searchlist += [message for message in self.message_list if searchterm in message.lower()]
		self.searchlist = list(set(self.searchlist))
		print self.searchlist

		if len(self.searchlist) > 0:
			search_blob = self.blob_maker(self.searchlist)
			sentiment_on_search = search_blob.sentiment	# returns a tuple

			if sentiment_on_search[0] > 0:
				if sentiment_on_search[0] > 0.6:
					self.make_post("You all appear to feel very positive about " + searchterm + ", sir.")
				elif sentiment_on_search[0] > 0.3 :
					self.make_post("You all appear to feel somewhat positive about " + searchterm + ", sir.")
				else: 
					self.make_post("You all appear to feel a smidge positive about " + searchterm + ", sir.")
			elif sentiment_on_search[0] < 0 :
				if sentiment_on_search[0] < -0.6:
					self.make_post("You all appear to feel very negative about " + searchterm + ", sir.")
				elif sentiment_on_search[0] < 0.3 :
					self.make_post("You all appear to feel somewhat negative about " + searchterm + ", sir.")
				else: 
					self.make_post("You all appear to feel a smidge negative about " + searchterm + ", sir.")

		else:
			self.make_post("My apologies, you all have not spoken about " + searchterm + " recently sir.")




