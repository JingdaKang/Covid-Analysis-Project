#sourced from example from canvas: tweepy-search-example.py
from distutils.log import info
import os

from couchdb import PreconditionFailed
from tweepy import Client

#sentiment analysis
from textblob import TextBlob
import re
import emoji


# Remove hashtags, mentions, urls
# These elements mostly does not contain user's emotions, but might distract the sentiment analysis process
def tweet_cleaning(text):
    # remove hashtags
    remove_hashtag = ' '.join(re.sub("(#[A-Za-z0-9]+)", " ", text).split())
    # remove mentions
    remove_mentions = ' '.join(re.sub("(@[A-Za-z0-9_]+)", " ", remove_hashtag).split())
    # remove url start with http: or https:
    remove_url = ' '.join(re.sub("^http:\S+ | ^https:\S+", " ", remove_mentions).split())
    return remove_url


# emojis or emoticons contain emotion information a lot, transfer to text
def emoji_transformation(text):
    # express the emoji/emoji unicode into its actual meaning in text
    emoji_meaning = emoji.demojize(text)
    # a dictionary of commonly used emoticons
    emoticon_dict = {':‑(': 'sad', ':(': 'sad', ':)': 'smile', ':-)': 'smile', 'XD': 'laugh', ':‑D': 'laugh',
                     ':D': 'laugh', ';-)': 'winking smile', ':-/': 'frown', ':-D': 'big smile'}
    emoticon_list = list(emoticon_dict.keys())
    word_list = emoji_meaning.split()
    new_word_list = []
    for word in word_list:
        # if there is a emoticon, convert to its meaning
        if word in emoticon_list:
            new_word_list.append(emoticon_dict[word])
        else:
            new_word_list.append(word)
    emoticon_meaning = ' '.join(new_word_list)
    return emoticon_meaning


def main(text):
    remove_useless = tweet_cleaning(text)
    express_emoji = emoji_transformation(remove_useless)
    tweet_cleand = TextBlob(express_emoji)
    # polarity ranges from -1 to 1
    polarity = tweet_cleand.sentiment.polarity
    # if the polarity is from -1 to -0.1, treat as negative
    if -1 <= polarity < -0.1:
        attitude = 'negative'
    # if the polarity is from -0.1 to 0.1, treat as neutral
    elif  -0.1 <= polarity <= 0.1:
        attitude = 'neutral'
    # if the polarity is from 0.1 to 1, treat as positive
    elif 0.1 < polarity <= 1:
        attitude = 'positive'
    return attitude

#connect to server and specific couchdb file
import couchdb

server = couchdb.Server(url='http://admin:admin@172.26.134.79:5984/')
try:
    db = server.create('covid_vaccine')
except PreconditionFailed as e:
    print(e)
    db = server['covid_vaccine']
else:
    print("Program stopped.")

if __name__ == "__main__":
    """
     - Save it in a secure location
     - Treat it like a password or a set of keys
     - If security has been compromised, regenerate it
     - DO NOT store it in public places or shared docs
    """
    
    #get authentication of twitter API and connect
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    client = Client(bearer_token)

    #set parameters
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    query = "(booster OR pfizer OR moderna OR dose OR vaccine OR vaccinate OR vax) covid lang:en"

    max_results = 100
    limit = 5000
    counter = 0

    #collect tweets
    # https://docs.tweepy.org/en/stable/client.html#search-tweets
    resp = client.search_recent_tweets(query, max_results=max_results,tweet_fields='geo')
    if resp.errors:
        raise RuntimeError(resp.errors)
    if resp.data:
        for tweet in resp.data:
            counter += 1
            info=dict(tweet)
            #collect attitudes 
            info['sentiment']=main(info['text'])
            db.save(info)
            print('tweet ',info['id'],' is saved')

    #since max result is 100 per query, if not reach our collect goal amount, automatically turn to next page and check if no more related tweets and keep collecting
    while resp.meta["next_token"] and counter < limit:
        resp = client.search_recent_tweets(query, max_results=max_results, next_token=resp.meta["next_token"])
        if resp.errors:
            raise RuntimeError(resp.errors)
        if resp.data:
            for tweet in resp.data:
                counter += 1
                info=dict(tweet)
                info['sentiment']=main(info['text'])
                db.save(info)
                print('tweet ',info['id'],' is saved')
    
    
    
