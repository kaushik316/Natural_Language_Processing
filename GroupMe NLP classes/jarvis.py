from BukList import *
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
import requests
from pytz import timezone

# Jarvis is a butler class that performs non NLP functions, translating 
# provided text, and greeting people based on the current time

class Jarvis(object):

	def __init__(self):
		self.name = "Jarvis"
		self.known_langs = {"hindi":"hi", "german":"de", "italian":"it", "spanish":"es", "french":"fr"}
		self.friend_dict = {"8994029": {
							"city":"Atlanta",
							"timedelta":0,
							"name": "Kash"
							},
							"20428510": {
							"city":"State College",
							"timedelta":0,
							"name":"David"
							},
							"20428423": {
							"city":"Gainesville",
							"timedelta":0,
							"name": "Jacob"
							},
							"8578182": {
							"city":"San Diego",
							"timedelta":3,
							"name":"Tyler"
							},
							"12906814": {
							"city":"Gainesville",
							"timedelta":0,
							"name":"Casey"
							},
							"9899062": {
							"city":"Austin",
							"timedelta":1,
							"name":"Milan"
							},
						    "5128170": {
							"city":"Boston",
							"timedelta":0,
							"name":"Connor"
							},
							"12249871": {
							"city":"Santa Barbara",
							"timedelta":3,
							"name":"Alana"
							},
							"13439387": {
							"city":"Minneapolis",
							"timedelta":1,
							"name":"Josh"
							},
							"8565541": {
							"city":"Gainesville",
							"timedelta":0,
							"name":"Will"
							},

		} 


	def make_post(self,content): # Function to post something in the groupme
	    bot = {"bot_id" : bot_id, "text": content}
	    r = requests.post("https://api.groupme.com/v3/bots/post", params = bot)


	def greet(self, userid): # The userid of the groupmember is passed in to determine timedelta
		eastern_time = datetime.now(timezone('US/Eastern')) # Sets a current timezone
		delta = self.friend_dict[userid]['timedelta'] # Based on the timezone of the groupmember adds a timedelta
		now = eastern_time + timedelta(hours=delta)

		if time(21,00) <= now.time() or now.time() <= time(03,30):  
			print self.friend_dict[userid]['name']
			self.make_post("A good night to you, " + self.friend_dict[userid]['name'])
		elif time(03,30) <= now.time() <= time(12,00):   
			self.make_post("Good morning, " + self.friend_dict[userid]['name'] + "." " How are things in  " + self.friend_dict[userid]['city'] + "?")
		elif time(12,00) <= now.time() <= time(16,30):  
			self.make_post("Good afternoon, " + self.friend_dict[userid]['name'])
		elif time(16,40) <= now.time() <= time(21,00):  
			self.make_post("Good evening, " + self.friend_dict[userid]['name'])
			

	def translate(self, to_translate, target_lang):
		if target_lang in self.known_langs:
		  # Build a service object for interacting with the API.
			language_code = self.known_langs[target_lang]
			service = build('translate', 'v2', developerKey=goog_key) 
			translated = service.translations().list(
			  source='en',
			  target=language_code,
			  q=[to_translate]
			).execute()
			translated_post = translated['translations'][0]['translatedText'] 
			self.make_post(translated_post)
		else:
			self.make_post("I'm sorry sir, wans't able to translate that for you.")






