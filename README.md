# Natural_Language_Processing
Topic gathering and parts of speech classification

## Bad English Teacher
The bad english teacher file contains code that can be used to parse Twitter conversations to identify parts of speech using the spaCy library. However, you'll see that Twitter is like the wild west with the number of characters that need to be stripped out of a typical sentence and misspelled words often causing difficulties for natural language processing libraries. Which is why I don't recommend usage of this code to teach yourself English, if you are a non native speaker or a toddler.

To obtain the list of tweets, we make use of the Tweepy python package. This package simplifies twitter authentication, especially helpful since at the time of this writing Twitter requires authentication for all GET requests to its API.

You'll notice that I've used a switch and that the value of this switch determines the source from which the tweets are pulled. If the switch is set to 0, a list of 300 tweets are pulled based on a keyword that you enter when prompted. If the switch is set to one, the tweets are pulled from my Twitterbot's profile, which retweets tweets about Data Science. 

Then, the tweets are cleaned and stripped of hashtags and '@' symbols before being parsed by the various helper functions written. For example, if we want to retrieve all the nouns associated used in the obtained list of tweets all we would have to do is call the get_nouns function.
