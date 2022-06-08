#sourced from example from canvas: tweepy-streaming-example.py
import os
import logging

# sentiment analysis
from couchdb import PreconditionFailed
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


from tweepy import StreamingClient, StreamRule, Tweet

class TweetListener(StreamingClient):
    """
    StreamingClient allows filtering and sampling of realtime Tweets using Twitter API v2.
    https://docs.tweepy.org/en/latest/streamingclient.html#tweepy.StreamingClient
    """

    def on_tweet(self, tweet: Tweet):
        #save tweet whenever search a tweet and add attitude
        info=dict(tweet)
        info['sentiment']=main(info['text'])
        db.save(info)
        print('tweet ',info['id'],' is saved')

    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        self.disconnect()


if __name__ == "__main__":

    #get authentication of twitter API and connect
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    client = TweetListener(bearer_token)

    # https://docs.tweepy.org/en/latest/streamingclient.html#streamrule
    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule
    
    #set parameters
    rules = [
        StreamRule(value='(booster OR pfizer OR moderna OR dose OR vaccine OR vaccinate OR vax) covid lang:en')
    ]

    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream-rules
    resp = client.get_rules()

    #collect geo information
    try:
        client.filter(tweet_fields='geo')
    except KeyboardInterrupt:
        client.disconnect()
