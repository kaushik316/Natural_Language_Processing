# Sentalyzer

A natural language processing module built on nltk and scikit-learn. Returns sentiment, related topics and popular parts of speech utilized in a given corpus. 

## Usage


#### *sentalyzer.sentiment()* 

Takes a string as input and returns a tuple with sentiment, polarity.

```python
import sentalyzer_module as sm
print sm.sentiment("This sentence is horrible, very bad")

# outputs "(neg, 0.9)"
```


#### *sentalyzer.pct_positive(list)*

Takes a list as input and returns percentage of strings in the list that are classified as positive and negative

```python
import sentalyzer_module as sm

pizza_list = ["I like pizza a lot", "I love pizza", "Pizza is the best", "I dislike pizza"]
print sm.pct_positive(pizza_list)

# returns "negative: 25%  positive: 75%"
```


#### *sentalyzer.related_topics(list, number of topics, number of words per topic)*

Takes a list as input and returns a specified number of words that fall into a similar topic found in the list.

```python
import sentalyzer_module as sm

news_list = ["Oil prices drop as US shale producers increase production", 
             "OPEC agrees on production cutbacks to avoid price drop",
             "Customers buy less solar powered cars as gasoline becomes cheaper",
             "Driving activity go up as gas prices fall")]

print sm.related_topics(news_list, num_topics=1, w_per_topic=3)

# returns
# Topic 1:
# Oil, production, gas    
```          


#### *sentalyzer.popular_words(list, part of speech)*

Takes a list and a specified part of speech (noun, verb, etc) as input and returns most popular words under that subtype.

```python
import sentalyzer_module as sm

news_list = ["Oil prices drop as US shale producers increase production",
             "OPEC agrees on production cutbacks to avoid price drop",
             "Customers buy less solar powered cars as gasoline becomes cheaper",
             "Driving activity go up as gas prices fall")]
             
print sm.popular_words(news_list, pos="noun")
```


