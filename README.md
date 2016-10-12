# Natural_Language_Processing
Topic gathering and parts of speech classification


## Bad English Teacher
The bad english teacher file contains code that can be used to parse Twitter conversations to identify parts of speech using the spaCy natural language processing library. However, you'll see that Twitter is like the wild west with the number of characters that need to be stripped out of a typical sentence and misspelled words often causing difficulties for natural language processing libraries. Which is why I don't recommend usage of this code to teach yourself English, if you are a non native speaker or a toddler.

To obtain the list of tweets (our corpus), we make use of the Tweepy python package. This package simplifies twitter authentication, especially helpful since at the time of this writing Twitter requires authentication for all GET requests to its API.

You'll notice that I've used a switch and that the value of this switch determines the source from which the tweets are pulled. If the switch is set to 0, a list of 300 tweets are pulled based on a keyword that you enter when prompted. If the switch is set to 1, the tweets are pulled from my Twitterbot's profile, which retweets tweets about Data Science. 

Then, the tweets are cleaned and stripped of hashtags and '@' symbols before being parsed by the various helper functions written. For example, if we want to retrieve all the nouns associated used in the obtained list of tweets all we would have to do is call the get_nouns function.


## Reddit Topics
The Reddit Topics scripts makes use of the Reddit API and a powerful model known as the Latent Dirichlet Allocation model. The LDA model posits that each document in our corpus is a collection of topics. In order to determine what words make up a certain topic, the LDA model looks at how words in a particular document are used in relation to one another rather than looking at a certain words standalone meaning.

I used the PRAW python package here, retreiving a list of comments from 6 different news subreddits before running the series through a count vectorizer. The cv turns each word into a feature, with the entries under each column corresponding to the number of times a word appears in a given article so that the strength of the relationship between certain words can be calculated. 

The one potential drawback of using this model is that you might need a working knowledge of your corpus beforehand since you must specify the number of topics you are looking for. In this case I chose to create 10 topic pools with 5 words in each topic. 
