from __future__ import unicode_literals
import requests
import pandas as pd
import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import re
import spacy
from spacy.en import English
from Tweepy_auth import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
tweetlist = []
switch = 0


# Remove @ - twitter handles, http - links, # - Hashtags and RT - retweets
def clean_tweets(wordlist):
	for i in range(0, len(wordlist)):
		wordlist[i] = re.sub(r'#','',wordlist[i])
		wordlist[i] = re.sub(r"RT|http\S+|@\S+","",wordlist[i])


# Based on the switch setting, uses retweets from my twitterbot or tweets returned based off a keyword search
def get_tweets(wordlist):
	if switch == 0:
		searchword = raw_input('Enter a keyword to find related tweets: ')
		print searchword
		wordlist += [tweet.text for tweet in tweepy.Cursor(api.search, q=searchword).items(300)] #instead of redefining the list here use += 
		clean_tweets(wordlist)	
		return
	elif switch == 1:
		wordlist += [tweet.text for tweet in tweepy.Cursor(api.user_timeline, screen_name = 'Data_Monke', count = 300, include_rts = True).items(300) if 'RT' in tweet.text]
        clean_tweets(wordlist)
        return
	

# Using spaCy to find organizations mentioned in Data Science tweets
nlp_toolkit = English()


# spaCy functions
def mentions_company(parsed):
    for entity in parsed.ents:
        if entity.label_ == 'ORG':
            print entity 

def get_verbs(parsed):
	for token in parsed:
		if token.pos == spacy.parts_of_speech.VERB:
			print token 

def get_nouns(parsed):
    for token in parsed:
        if token.pos == spacy.parts_of_speech.NOUN:
            print token

def parse_list(wordlist, function):
	for tweet in wordlist:
		parsed_tweet = nlp_toolkit(tweet)
		function(parsed_tweet)


# Return some commone nouns associated with the term you searched for.
get_tweets(tweetlist)
parse_list(tweetlist, get_nouns)




